import pickle
import math

#get data for preprocessed data
infile = open('wordsData','rb')
words = pickle.load(infile)
wordCount = pickle.load(infile)
unigram = pickle.load(infile)
bigram = pickle.load(infile)
char = pickle.load(infile)
infile.close()

infile = open('matrices','rb')
del_matrix = pickle.load(infile)
add_matrix = pickle.load(infile)
sub_matrix = pickle.load(infile)
trans_matrix = pickle.load(infile)
infile.close()

#input: two words
#output: min-distance table
def edit_distance(str1, str2):
    m = len(str1)+1
    n = len(str2)+1

    table = {}
    #set insert cost for the words
    for i in range(m): table[i,0]=i
    for j in range(n): table[0,j]=j
    
    #set the table based of the min adjacent table values
    for i in range(1, m):
        for j in range(1, n):
            cost = 0 if str1[i-1] == str2[j-1] else 2
            table[i,j] = min(table[i,j-1]+1, 
                         table[i-1,j]+1, 
                         table[i-1,j-1]+cost)

    return table

#input: input words and min-distance table
#output: list of changes from str1 to str2 
def backtrace(str1, str2, table):
    i,j = len(str1), len(str2)
    
    changes = []
    
    while not (i == 0  and j == 0):
        prev_cost = table[i,j]
        back = []
        
        #get neighor cells value
        if(i!=0 and j!=0):
            back.append(table[i-1,j-1])
        if(i!=0):
            back.append(table[i-1,j])
        if(j!=0):
            back.append(table[i,j-1])
        
        #get min path 
        min_cost = min(back)
        
        #save the changes
        if(min_cost == prev_cost):            
            i, j = i-1, j-1
        elif(i!=0 and j!=0 and min_cost == table[i-1,j-1]):
            i, j = i-1, j-1
            changes.append({'type':'sub', 'x':str1[i], 'y':str2[j], 'position':i})
        elif(i!=0 and min_cost == table[i-1,j]):
            i, j = i-1, j
            if j == len(str2):
                changes.append({"type":'delete', 'x':str2[j-1], 'y':str1[i], 'position':i})
            elif j == 0:
                changes.append({"type":'delete', 'x':'#', 'y':str1[i], 'position':i})
            else:
                changes.append({"type":'delete', 'x':str2[j-1], 'y':str1[i], 'position':i})
        elif(j!=0 and min_cost == table[i,j-1]):
            i, j = i, j-1
            if i == len(str1):
                changes.append({"type":'insert', 'x':str1[i-1], 'y':str2[j], 'position':i})
            elif i == 0:
                changes.append({"type":'insert', 'x':'#', 'y':str2[j], 'position':i})
            else:
                changes.append({"type":'insert', 'x':str1[i-1], 'y':str2[j], 'position':i})
     
    return changes
            
#input: word
#output: list of candidate words and backtrace
def get_candidates(str1):
    can_list = []
    can_changes = []
    for word in words:
        table = edit_distance(str1, word)
        distance = table[len(str1),len(word)]        
        if distance <= 2:
            can_list.append(word)
            can_changes.append(backtrace(str1, word, table))
    can_changes = fix_changes(can_list,can_changes)
    return can_list, can_changes

#input: dictionary with type of change
#output: int with conditional probability
#return condidional probability based on changes
def con_probabilities(change):
    if not change:
        return 1
    else:
        type_change = change['type']
        x = change['x']
        y = change ['y']
        #check if the changes are letter besides #
        if (x.isalpha() or x =='#') and y.isalpha():
            prob = 0
            
            #get value from cost matrix and divide by the frequency of char(s)
            if type_change == 'delete':
                if x == '#':
                    y = y.lower()
                    value_from_matrix = del_matrix[26][ord(y)-97]
                    prob = value_from_matrix/char[y]
                else:
                    x = x.lower()
                    y =  y.lower()
                    value_from_matrix = del_matrix[ord(x)-97][ord(y)-97]
                    prob = value_from_matrix/char[x+y]
            
            elif type_change == 'insert':
                if x == '#':
                    y =  y.lower()
                    value_from_matrix = add_matrix[26][ord(y)-97]
                    prob = value_from_matrix/char[y]
                else:
                    x = x.lower()
                    y =  y.lower()
                    value_from_matrix = add_matrix[ord(x)-97][ord(y)-97]
                    prob = value_from_matrix/char[x]
                    
            elif type_change == 'sub':
                x = x.lower()
                y =  y.lower()
                value_from_matrix = sub_matrix[ord(x)-97][ord(y)-97]
                prob = value_from_matrix/char[y]
                
            elif type_change == 'trans':
                x = x.lower()
                y =  y.lower()
                value_from_matrix = trans_matrix[ord(x)-97][ord(y)-97]
                prob = value_from_matrix/char[x+y]
            return prob
        else:
            return 1

#input: list of candidate words and their changes to get to the incorrect word
#output: fix changes if there was a transpose
#loops for changes and identifies transpose changes
def fix_changes(can_list,can_changes):
    new_can_changes = []
    
    # loop for each candidate word
    for i in range(len(can_list)):
        pre_correct_changes = can_changes[i]
        change = []
        skip = False
        # loop though all the changes for one candidate word and skip the next one if it is a transpose
        for j in range(len(pre_correct_changes)):
            if len(pre_correct_changes)-j > 1 and not skip:
                first = pre_correct_changes[j]
                second = pre_correct_changes[j+1]
                if (first['type'] == 'delete' and second['type'] == 'insert') and  (first['position']-1 == second['position']):
                    change.append({"type":'trans', 'x':first['x'], 'y':first['y'], 'position':0})
                    skip = True #skip the next change because it is a part of the transpose
                else:
                    change.append(first)
                    skip = False
            elif not skip:
                first = pre_correct_changes[j]
                change.append(first)
            else:
                skip = False
        new_can_changes.append(change)
    return new_can_changes

#input: list of candidate words, their changes to get to the incorrect word,flag if it is getting probability of real-world error ,the next word, and previous word
#output: a list of tuple with the candidate words and their probability
#gets prob based on spelling changes and bigram prob
def get_probabilities(can_list, can_changes,real_world_spelling,next_word, pre_word):
    total = []

    for i in range(len(can_list)):
        can_word = can_list[i]
        #check if changes in the word exist
        if can_changes:
            changes = can_changes[i]
        else:
            changes = []
        con_pro = 0
        
        #loop through all the changes from candidate word to incorrect word
        for j in range(len(changes)):
            if con_pro == 0:
                con_pro = con_probabilities(changes[j])

            else:
                con_pro *= con_probabilities(changes[j])
        
        #Probability of no error word
        if con_pro == 0:
            con_pro = .90
            lan_pro = 1
            if not can_word in words: 
                total.append((can_word, math.log(lan_pro*con_pro)))
            else:
                if pre_word != "" and pre_word in words:
                    if(pre_word, can_word) in bigram:
                        lan_pro *= bigram[(pre_word,can_word)]
                    else:
                        #use bigram smoothing if the pair is not seen in the bigram
                        lan_pro *= (1/(wordCount[pre_word]+len(words)))
                if next_word != "" and next_word in words:
                    if (can_word, next_word) in bigram:
                        lan_pro *= bigram[(can_word, next_word)]
                    else:
                        #use bigram smoothing if the pair is not seen in the bigram
                        lan_pro *= (1/(wordCount[can_word]+len(words)))
                if pre_word == '' and next_word == '':
                    lan_pro *= unigram[can_word]
                
                total.append((can_word, math.log(con_pro*lan_pro)))
        
        #probability of all other candidate words            
        else:
            lan_pro = 1
            if not can_word in words: 
                total.append((can_word, math.log(lan_pro*con_pro)))
            else:
                if pre_word != "" and pre_word in words:
                    if(pre_word, can_word) in bigram:
                        lan_pro *= bigram[(pre_word,can_word)]
                    else:
                        #use bigram smoothing if the pair is not seen in the bigram                       
                        lan_pro *= (1/(wordCount[pre_word]+len(words)))
                if next_word != "" and next_word in words:
                    if (can_word, next_word) in bigram:
                        lan_pro *= bigram[(can_word, next_word)]
                    else:
                        #use bigram smoothing if the pair is not seen in the bigram
                        lan_pro *= (1/(wordCount[can_word]+len(words)))
                if pre_word == '' and next_word == '':
                    lan_pro *= unigram[can_word]
                if real_world_spelling:
                    con_pro = ((1-.95)/len(can_list))*con_pro
                total.append((can_word, math.log(con_pro*lan_pro)))
    return total

#input: String with the current incorrect word, the next word, the previous word
#output: return the best candidate word to replace the incorrect word
def getCorrectSpelling(current_word,next_word, pre_word):  
    #if incorrect word is a number return number
    if (current_word.isdigit()):
        return current_word   
    #get candidate words for the incorrect word
    can_list, can_changes = get_candidates(current_word)
    
    #if candidate list is not empty return the word with the highest probability
    if can_list: 
        #print(get_probabilities(can_list, can_changes, next_word,pre_word))
        replace_word ,_ = max(get_probabilities(can_list, can_changes, False,next_word,pre_word),key=lambda item:item[1])
        return replace_word
    else:
        return current_word

#input: A list of the words in a sentence
#output: return the best candidate word to replace the incorrect word
def check_real_words(sentence):
    
    candidates_per_word = []        #list of candidates for each word
    candidates_backtrace = []       #changes from each candidate word to the incorrect
    total = []                      #list of tuple with the candidate words and their probability for each word in the sentence
    words_prob = {}                 #Dictionary with candidate words and their probabilities
    all_sentences = []              #list of all possible sentence combinations
    
    #get all candidates words and their changes and all it to two lists
    for i in range(len(sentence)):
        if sentence[i] in words:
            
            #ignores proper nouns with a captial letter that is not at the begnning of the setence
            if i != 0 and sentence[i][0].isupper():
                candidates_per_word.append([sentence[i]])
                candidates_backtrace.append([])
            else:
                candidate_words, candidate_back = get_candidates(sentence[i])
            
                #add the word it self
                if not sentence[i] in candidate_words: 
                    candidate_words.append(sentence[i])
                    candidate_back.append([])
                
                candidates_per_word.append(candidate_words)
                candidates_backtrace.append(candidate_back)
        else:
            candidates_per_word.append([sentence[i]])
            candidates_backtrace.append([])
    
    #Loop though each candidate word and their changes get their probabilities
    for i in range(len(candidates_per_word)):
        if i == 0 and len(candidates_per_word) == 1:
            total.append(get_probabilities(candidates_per_word[i],candidates_backtrace[i],True,'',''))
        elif i == 0:
            total.append(get_probabilities(candidates_per_word[i],candidates_backtrace[i],True,sentence[i+1],''))
        elif i == len(sentence) or i == len(sentence)-1:
            total.append(get_probabilities(candidates_per_word[i],candidates_backtrace[i],True,'',sentence[i-1]))
        else:
            total.append(get_probabilities(candidates_per_word[i],candidates_backtrace[i],True,sentence[i+1],sentence[i-1]))   
    
    #save the probability of each candidate word in a dictionary
    for i in range(len(total)):
        for j in range(len(total[i])):
            w,p = total[i][j]
            words_prob[w] = p
    
    #replace one word of a sentence with a candidate word
    for i in range(len(sentence)):
        for j in range(len(total[i])):
            sent = sentence.copy()      #copy original sentence
            replace, _ = total[i][j]  
            #repalce one word
            sent[i] = replace
            #add new sentence to the list of all sentences
            if sent != sentence:
                all_sentences.append(sent)
    
    #for each word in a the list of new sentences add up there probability
    cost_sentences = []
    for sentence in all_sentences:
        cost = 0 
        for word in sentence:
            cost += words_prob[word]
        cost_sentences.append((sentence,cost))
    
    #get the max from the new sentence combination
    replace_sentence = max(cost_sentences,key=lambda item:item[1])

    return replace_sentence

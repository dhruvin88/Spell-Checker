import pickle
import re

#input: dictionary of words and frequency
#output: dictionary of words and probability
def div_d(my_dict,freq):
    for i in my_dict:
        my_dict[i] = (my_dict[i]/freq)
    return my_dict 

#input: dictionary of word pairs and frequency
#output: dictionary of words pairs and probability
def calculate_bigram(bigram):
    for word1, word2 in bigram:
        #smoothing bigram for unseen pairs
        bigram[(word1,word2)] = (bigram[(word1,word2)]+1)/(unigram[word1]+ len(words))
    return bigram

#input: String from bigram file
#output: clean the string to remove punctuations
def stripCharacters(str1):
    str1 = str1.strip('\n')
    str1 = str1.rstrip('?:!.,;/-')
    
    #remove words with -
    if '-' in str1:
        str1 = ''
    
    #remove all non letter characters
    str1 = re.sub(r'&amp;','',str1)
    str1 = re.sub(r'[^a-zA-Z-]','', str1)
    return str1

# COCA bigram file
bigramFile = open('w2.txt','r')

words = set()           #set of words
wordsCount = {}         #dictionary of all words
total_frequency = 0     #words the total occurences of words
bigram = {}             #dictionary for bigrams
unigram = {}            #dictionary for unig
char = {}               #dictionary of characters frequenciess

for line in bigramFile:
    line = line.split('\t')
    
    word1 = stripCharacters(line[1])
    
    word2 = stripCharacters(line[2])

    if word1 != '' and word2 != '':
        pair_frequency = int(line[0])
        
        #saves total frequency of all known words
        total_frequency += pair_frequency
        
        #adds to the set
        words.add(word1)
        words.add(word2)           
        
        #if the two words are equal save the frequency once
        if word1 == word2:
            if word1 in unigram:
                unigram[word1]+= pair_frequency
            else:
                unigram[word1] = pair_frequency
        else:
            if word1 in unigram:
                unigram[word1]+= pair_frequency
            else:
                unigram[word1] = pair_frequency
            if word2 in unigram:
                unigram[word2] += pair_frequency
            else:
                unigram[word2] = pair_frequency
        
        #add the word pairs to the 
        bigram[(word1, word2)] = pair_frequency

#count the char frequency
for word in unigram:
    for i in range(len(word)):
        if i > 1:
            if word[i]+word[i-1] in char:
                char[word[i]+word[i-1]] += unigram[word]
            else:
                char[word[i]+word[i-1]] = unigram[word]
        if word[i] in char:
            char[word[i]] += unigram[word]
        else:
            char[word[i]] = unigram[word]

#save the count of each word
wordCount = unigram.copy()
bigram = calculate_bigram(bigram)
unigram = div_d(unigram,total_frequency)
            
### pickle data
output = open('wordsData','wb')
pickle.dump(words,output)
pickle.dump(wordCount,output)
pickle.dump(unigram,output)
pickle.dump(bigram,output)
pickle.dump(char,output)
output.close()
            
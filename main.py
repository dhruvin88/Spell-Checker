import pickle
import string
from nltk.tokenize import sent_tokenize
from util import getCorrectSpelling, check_real_words

infile = open('wordsData','rb')
words = pickle.load(infile)
infile.close()

#Input: a string that is a word
#Output: a string without a ending punctuation and the puncuation itself
def remove_punctuation(str1):
    if str1[-1] in string.punctuation:
        return str1[:-1], str1[-1]
    else:
        return str1, ""

#Input: a list with the spelling errors corrected, the original list of words in a sentence,
#       puncuations in the sentence, and the output file
def output_correct(new_sentence, old_sentence, punctuations, fileout):
    punc= []
    position = []
    for pun, pos in punctuations:
        punc.append(pun)
        position.append(pos)
    for i in range(len(new_sentence)):
        fileout.write(old_sentence[i])
        if new_sentence[i] != old_sentence[i]:
            fileout.write(" ("+new_sentence[i]+")")
        if i in position:
            index = position.index(i)
            fileout.write(punc[index]+" ")
        else:
            fileout.write(" ")
        

##############################################################################################
filename_in = input("Enter the input filename:")
file_in = open(filename_in, 'r')
file_out = open('output.txt','w')

for line in file_in:
    #split line into sentences
    sent_tokenize_list = sent_tokenize(line)
    for x in range(len(sent_tokenize_list)):
        # split sentence into words
        list_of_words = sent_tokenize_list[x].split(" ")
        
        #create new list of words in sentence after fixing
        new_list_of_words = []
            
        #save puncation in sentence and position
        punctuation = []
        
        for i in range(len(list_of_words)):
            #if beginning of sentence
            if i == 0:
                current_word, current_word_p = remove_punctuation(list_of_words[i])
                list_of_words[i] = current_word
                next_word, next_word_p = remove_punctuation(list_of_words[i+1])
                
                #find spelling errors at start of a sentence
                if current_word not in words and not current_word == '\n':
                    replace_word = getCorrectSpelling(current_word,next_word, "")
                    new_list_of_words.append(replace_word) 
                else:
                    new_list_of_words.append(current_word)
                if not current_word_p == '':
                    punctuation.append((current_word_p, i))
            
            # if end of a sentence
            elif i == len(list_of_words) or i == len(list_of_words)-1:
                previous_word, previous_word_p = remove_punctuation(list_of_words[i-1])
                current_word, current_word_p = remove_punctuation(list_of_words[i])
                list_of_words[i] = current_word
                
                #find spelling errors at end of a sentence
                if current_word not in words and not current_word == '\n':
                    replace_word = getCorrectSpelling(current_word,'',previous_word)
                    new_list_of_words.append(replace_word)
                else:
                    new_list_of_words.append(current_word)
                if not current_word_p == '':
                    punctuation.append((current_word_p, i))
                
            else:
                previous_word, previous_word_p = remove_punctuation(list_of_words[i-1])
                current_word, current_word_p = remove_punctuation(list_of_words[i])
                next_word, next_word_p = remove_punctuation(list_of_words[i+1])
                list_of_words[i] = current_word
                
                #find spelling errors in the middle of a sentence
                if current_word not in words and not current_word == '\n':
                    replace_word = getCorrectSpelling(current_word,next_word,previous_word)
                    new_list_of_words.append(replace_word)
                else:
                    new_list_of_words.append(current_word)
                if not current_word_p == '':
                    punctuation.append((current_word_p, i))

        #check of real-world spelling errors
        new_list_of_words,_ = check_real_words(new_list_of_words)
            
        #output corrected sentence to output file
        output_correct(new_list_of_words, list_of_words, punctuation, file_out)

file_out.close()
print("Output.txt was created")
file_in.close()
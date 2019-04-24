#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 29 11:34:40 2018

@author: dhruvinpatel
"""

if i == 0:
                current_word, current_word_p = remove_punctuation(list_of_words[i])
                next_word, next_word_p = remove_punctuation(list_of_words[i+1])
                file_out.write(current_word)
                
                if current_word not in words and not current_word == '\n':
                    replace_word = getCorrectSpelling(current_word,next_word, "")
                    if not replace_word == current_word:
                        file_out.write(" ("+replace_word+")")
                        list_of_words[i] = replace_word 
                if not current_word_p == "":
                    file_out.write(current_word_p+' ')
                else:
                    file_out.write(" ")
            
            # if end of a sentence
            elif i == len(list_of_words) or i == len(list_of_words)-1:
                previous_word, previous_word_p = remove_punctuation(list_of_words[i-1])
                current_word, current_word_p = remove_punctuation(list_of_words[i])
                
                file_out.write(current_word)
                if current_word not in words and not current_word == '\n':
                    replace_word = getCorrectSpelling(current_word,next_word,previous_word)
                    if not replace_word == current_word:
                        file_out.write(" ("+replace_word+")")
                        list_of_words[i] = replace_word 
                if not current_word_p == "":
                    file_out.write(current_word_p + ' ')
                else:
                    file_out.write(" ")
                
            else:
                previous_word, previous_word_p = remove_punctuation(list_of_words[i-1])
                current_word, current_word_p = remove_punctuation(list_of_words[i])
                next_word, next_word_p = remove_punctuation(list_of_words[i+1])
                
                file_out.write(current_word)
                if current_word not in words and not current_word == '\n':
                    replace_word = getCorrectSpelling(current_word,next_word,previous_word)
                    if not replace_word == current_word:
                        file_out.write(" ("+replace_word+")")
                        list_of_words[i] = replace_word 
                if not current_word_p == "":
                    file_out.write(current_word_p+ ' ')
                else:
                    file_out.write(" ")
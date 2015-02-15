#sentiment classifier for english using sentiwordnet language database

import re,os
from nltk.stem import *
from nltk.stem.porter import *
class Sentiment:

    training_data_sentiments = os.path.dirname(os.path.realpath("sentiment")) +"\\trainingData\senti.txt"

    #dictionary that contains the words and their corresponding
    #senti scores. Format is "index: [(pos_tag,(pos_score,neg_score))]"
    sentiwordnet = {}
    stemmer = PorterStemmer()
    
    do_not_include = ["is","and","was","are","for","the","were","there","this","that",
                      "who","where","when","whose","why","but","on","in","which",
                      "very","much","so","the","too"]
        
    #pos tags equivalent
    #sentiwordnet uses a different naming for pos tags
    #so we translated it
    tags_name = {
            "a":"adj",
            "s":"adj",
            "r":"adv",
            "n":"n",
            "v":"v",
            '':''
        }
    
    def __init__(self):
        self.train()
        pass

    #train the model using the senti.txt (SentiWordNet 3.0 word database )
    #each line is seperated by \t
    #when the line is splitted, the elements are as follows:
    #[0] - pos tag, [1] - sentiwordnet id, [2] positive score, [3] negative score, [4] words, [5] definition
    def train(self):
        fs = open(self.training_data_sentiments,"r")
        contents = fs.readlines()
        fs.close()

        for line in contents:
            
            entry = line.split("\t")
            pos_tag = entry[0]
            try:
                posi_score,nega_score,obj_score = entry[2],entry[3],`1.0-(float(entry[2])+float(entry[3]))`
            except Exception:
                pass
               # print entry
                
            words = re.sub("#[0-9]+","",entry[4]).split()

            for word in words:
                if word in self.sentiwordnet:
                    if pos_tag in self.sentiwordnet[word].keys(): 
                        self.sentiwordnet[word][self.tags_name[pos_tag]].append( (posi_score,nega_score,obj_score) )
                    else:
                        self.sentiwordnet[word][self.tags_name[pos_tag]] = [(posi_score,nega_score,obj_score)]
                else:
                    self.sentiwordnet[word] = {self.tags_name[pos_tag]: [(posi_score,nega_score,obj_score)]}
                
    
    #predict multiple entries; words are given in a list
    #get the average of the entries, and then return its polarity
    #if an entry is not found, then decrease the total
    def predict_multi(self,iterable,pos_tag=""):
        total_polarity = [0,0,0]
        total = len(iterable)

        for entry in iterable:
            temp_polarity = [0,0,0]
            words = entry.split(" ")
            word_polarity = [0,0,0]
            
            words_total = len(words)
            pos_tag = ""
            if len(words)>=1:
                
                for word in words:
                    if word not in self.do_not_include and len(word)>1:
                        word_polarity = self.predict(word,pos_tag)
                        
                        if word_polarity == [0,0,0] or word_polarity == [0,0,1]:
                            words_total-=1
                            word_polarity[2] = 0

                    else:
                        words_total-=1
                        
                    temp_polarity[0] += word_polarity[0]
                    temp_polarity[1] += word_polarity[1]
                    temp_polarity[2] += word_polarity[2]


                if words_total > 0 :
                    
                    temp_polarity[0] /= float(words_total)
                    temp_polarity[1] /= float(words_total)
                    temp_polarity[2] /= float(words_total)
                
                total_polarity[0] += temp_polarity[0]
                total_polarity[1] += temp_polarity[1]
                total_polarity[2] += temp_polarity[2]
            else:
                total-=1

      

        if total <= 0:
            return [0,0,0]   

        if len(iterable) > 0:
            total_polarity[0] /= float(total)
            total_polarity[1] /= float(total)
            total_polarity[2] /= float(total)

         
        return total_polarity


    #predict the value of a word using the dictionary trained earlier (self.sentiwordnet)
    #2 parameters, word and pos_tag, word is the one being predicted, and pos_tag is the part-of-speech of that word (for word sense disambiguation)
    #if no pos tag is given, get the average of all values
    #if a pos tag is given, get the average of all values with the corresponding pos tag
    #return --- [positive, negative, objective]
    def predict(self,word,pos_tag = ""):
        pos = 0
        neg = 0
        obj = 0
        total = 0
        entry = None
        pos_tag = ""
        if pos_tag == "" or pos_tag == "AMB" or pos_tag == "UNK":
            
            try:
                for pos_tag in self.sentiwordnet[word].keys():
                    for entry in self.sentiwordnet[word][pos_tag]:

                        total +=1
                        pos += float(entry[0]) 
                        neg += float(entry[1])
                        obj += float(entry[2])
                    
                    
            except KeyError:
                word = self.stemmer.stem(word)
                if word in self.sentiwordnet.keys():
                    return self.predict(word)
                else:
                    return [0,0,0]
                """try:
                    return self.predict(word)
                except KeyError:
                    print "#----- Word not found ------- "
                    return [0,0,0] """
                
                
        else:
            try:
                container = self.sentiwordnet[word][pos_tag]
                for entry in container:
                    total+=1
                    pos+= float(entry[0])
                    neg+=  float(entry[1])
                    obj+= float(entry[2])
                    
            except KeyError:
                word = self.stemmer.stem(word)
                if word in self.sentiwordnet.keys():
                    return self.predict(word)
                else:
                    return [0,0,0]
                """try:

                    return self.predict(word)
                except KeyError:
                    print "#----- Word not found ------- "
                    return [0,0,0]"""
                """
                if word not in self.sentiwordnet.keys():
                    print "#----- Word not found ------- "
                    
                elif pos_tag not in self.sentiwordnet[word].keys():
                   
                    print "#------ pos tag not found ------"
                return [0,0,0]"""

        return [pos/total,neg/total,obj/total]



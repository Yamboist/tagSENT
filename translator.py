import re,os
class Translator:

    #text file containing all the tagalog-english translations
    __WORDS_DIR = os.path.dirname(os.path.realpath("translator")) +"\\trainingData\\tag-eng.txt"

    __tagalog_words = {}
    
    def __init__(self):
        self.train()
        pass

    def train(self,tag_eng = __WORDS_DIR):
        freader = open(tag_eng,"r")
        contents = freader.readlines()
        freader.close()
        for line in contents:
            word_def = line.split(" : ")

            #definition is the always in the second index of word_def
            #replace remaining ":" if there is remaining
            defn = word_def[1].replace(":","").strip()
            
            defn = defn.replace(word_def[0],"").strip()

            #remove the line's other transformation, 
            #ex: ... (word1, word2, word3) ...
            defn = re.sub("[(].+?[)]","",defn).strip()

            #seperate different translations; synonyms
            defn = defn.split(";")

            #remove POS tags like n., v., inf., and numberings 1. 2. ...
            for index in range(len(defn)):
                defn[index] = re.sub("[A-Za-z0-9]{1,3}[.],?","",defn[index]).strip()

            #if word is in dictionary, then add the definitions/translations
            if word_def[0] in self.__tagalog_words:
                for definition in defn:   
                    self.__tagalog_words[word_def[0]].append(definition)
            #if not, then create a new entry, then add the definitions/translations
            else:
                self.__tagalog_words[word_def[0]] = []
                for definition in defn:   
                    self.__tagalog_words[word_def[0]].append(definition)
        
    def stemmer():
        pass
       

    def translate(self,word):
        return self.__tagalog_words[word]



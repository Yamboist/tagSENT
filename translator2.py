import re,os,stemmer


class Translator:

    #text file containing all the tagalog-english translations
    __WORDS_DIR = os.path.dirname(os.path.realpath("translator")) +"\\trainingData\\tag-eng.txt"

    __tagalog_words = {}

    __stemmer = stemmer.Stemmer()
    
    def __init__(self):
        self.train()
        pass

    """
    method used to train the model
    """
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

            #regular expression to detect the tag for each entry
            tags_re = "n\.|adv\.|adj\.|v\.|intrj\.|comp\.|gram\.|conj\.|expr\.|prep\.|pref\.|imp\.|coll\.|interrog\.|idiom."

            #some pos tag cannot be found
            try:
                pos_tag = re.findall(tags_re,defn)[0]
                
                #remove pos tag, numberings and special characters
                defn = re.sub("[A-Za-z0-9]{1,10}[.],?|^!|[?!@.,]","",defn).strip()
                defn = re.sub("([/][A-Za-z]+? )|([/][A-Za-z]+?$)","",defn).strip()

                #split the different definitions, clean each of unneccessary whitespace
                #lowercase for consistency
                defn = [self.clean_string(i).strip().lower() for i in defn.split(";")]

                #if the dictionary has already registered the word
                if self.__tagalog_words.has_key(word_def[0]):

                    #if the word-dictionary has already registered a specific pos tag
                    if self.__tagalog_words[word_def[0]].has_key(pos_tag):

                        #append it to the current
                        self.__tagalog_words[word_def[0]][pos_tag] += defn
                    else:
                        
                        #initialize the list with defn
                        self.__tagalog_words[word_def[0]][pos_tag] = defn
                else:
                    self.__tagalog_words[word_def[0]]= {}
                    self.__tagalog_words[word_def[0]][pos_tag] =defn
                           
            except:
                pass

            
            
    """
    *model should be trained first
    method used for tagalog translation, accepts a string word and a string pos_tag
    word is the word to be translated
    pos_tag is the pos tag of the word to be translated; by default it is ""
    returns a list of strings containing the english translations
    """
    
    def translate(self,word,pos_tag=""):

        #if the translation fails (dictionary lookup), stem it
        try:
            #if the pos tag is unspecified
            if pos_tag == "" or pos_tag == "AMB" or pos_tag == "UNK":

                #initialize the translations container
                translations = []

                #append all translations, regardless of pos tag
                for key in self.__tagalog_words[word].keys():
                    translations += self.__tagalog_words[word][key]
                
                return translations
            else:
                if pos_tag.lower()+"." in self.__tagalog_words[word].keys():
                    #return translation for a specific pos tag
                    return self.__tagalog_words[word][pos_tag.lower()+"."]
                elif self.__tagalog_words[word].keys()>0:
                    return self.translate(word)
                
            
        #if the translation errors due to an index not found
        except:
            try:
                if self.stem2x(word) == word:
                    return word
                return self.translate(self.stem2x(word)) + ["~"]
            except:
                return []

    def stem2x(self,word):
        word = self.__stemmer.stem(word)
        return self.__stemmer.stem(word)

    #remove non-alphabet characters
    def clean_string(self,word):
        return re.sub("[^A-Za-z0-9 ]","",word)
        

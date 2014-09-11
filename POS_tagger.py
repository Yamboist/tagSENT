import re
from nltk.util import ngrams

class POS_tagger():
   
    __word_list_dir = "preDefinedFeatures/wordtags.txt"
    __pos_tag_pattern_dir = "trainingData/sentences_tags.txt"
    __pos_tag_pattern_outputs_dir = "outputs/pos_tag_patterns_5grams.txt"
    __list_of_determiners = [word.replace('\n','') for word in open("trainingData/tagalog_determiners.txt","r").readlines()]
    __list_of_pronouns = [word.replace('\n','') for word in open("trainingData/tagalog_pronouns.txt","r").readlines()]
    __list_of_conjunctions = [word.replace('\n','') for word in open("trainingData/tagalog_conjunctions.txt","r").readlines()]
    __list_of_stoppers = [word.replace('\n','') for word in open("trainingData/tagalog_stoppers.txt","r").readlines()]
    __list_of_linking_verbs = [word.replace('\n','') for word in open("trainingData/tagalog_linking_verbs.txt","r").readlines()]
    __list_of_prepositions= [word.replace('\n','') for word in open("trainingData/tagalog_prepositions.txt","r").readlines()]
    __list_of_modifiers= [word.replace('\n','') for word in open("trainingData/tagalog_modifiers.txt","r").readlines()]

    
    __adjective_patterns = [
        "pang[A-Za-z]+",
        "pam[A-Za-z]+",
        "pa[^g][A-Za-z]+",
        "nakaka[A-Za-z]+",
        "nakapagpapa[A-Za-z]+",
        "napaka[A-Za-z]+",
        "ma[A-Za-z]+",
        "naka[A-Za-z]+",
        "maka[A-Za-z]+"
        ]

    __verb_patterns = [
        "nag[A-Za-z]+",
        "mag[A-Za-z]+",
        "pa[A-Za-z]+?in",
        "[A-Za-z]+?in",
        "[A-Za-z]+?an",
        "[A-Za-z]um[A-Za-z]+",
        "[A-Za-z]in[A-Za-z]+"
        ]

    __convert_tags = {
        "n":["NN","NNC","NNP","NNPA"],
        "pr":["PR","PRS","PRSP","PRO","PROP","PRQ","PRL","PRN","PRC","PRF"],
        "prep":["PPO","PPTS","PPIN","PPU","PPM","PPA"],
        "conj":["CC","CCA","CCD","CCC","CCP"],
        "v":["VB","VBW","VBS","VBH","VBTS","VBTR","VBTF"],
        "adj":["JJ","JJD","JJC","JJCC","JJCS","JJCN","JJN"],
        "adv":["RB","RBD","RBN","RBC","RBQ","RBT","RBF","RBW","RBI","RBM"],
        "cd": ["CD","CDB"],
        "stopper": ["PM","PMP","PME","PMQ","PMC","PMS"],
        "dt":["DTCP","DTC"],
        "vbl":["VBL"]
        }
    
    __pos_tag_patterns = []
    __words_postag_dict = {}
    
    def __init__(self):

        self.train_lookup()
        self.train_pos_tag_patterns()
        
        pass

    def train_lookup(self):
        fsreader = open(self.__word_list_dir,"r")
        contents= fsreader.readlines()
        fsreader.close()

        #fill in the lookup dictionary
        for entry in contents:
            entry = entry.replace("\n","")
            temp = entry.split(" : ")
            if temp[0] not in self.__words_postag_dict:
                self.__words_postag_dict[temp[0]] = temp[1].split(",")
            else:
                tags = temp[1].split(",")
                for tag in tags:
                    self.__words_postag_dict[temp[0]].append(tag)
                    
    def train_pos_tag_patterns(self):
        fsreader = open(self.__pos_tag_pattern_dir,"r")
        contents = fsreader.readlines()
        contents = [line.replace("\n","") for line in contents]
        fsreader.close()

        temp = []

        fswriter = open(self.__pos_tag_pattern_outputs_dir,"w")
        for line in contents:
            line = line.strip()
            iterable = self.__convert_pos_tags_of_a_line(line)            
           
            five_grams = ngrams(iterable,5)
            for pattern in five_grams:
                if pattern not in self.__pos_tag_patterns:
                    self.__pos_tag_patterns.append(pattern)
                    temp.append(str(pattern))

        fswriter.writelines(temp)
        fswriter.close()

    
    def lookup_label(self,sentence):
        sentence = sentence.strip()
        words = sentence.split(" ")
        output = []
        for i in range(len(words)):
            if i==0: words[0] = words[0].lower() 
                
            try:
                pos = self.lookup(words[i])
                if(len(pos) == 1):
                    output.append([words[i],pos[0]])
                elif(len(pos) > 1):
                    output.append([words[i],"AMB"])
            except:
                if self.__check_if_adjective_from_prefixes(words[i]):
                    output.append([words[i],"adj"])
                elif self.__check_if_verb_from_prefixes(words[i]):
                    output.append([words[i],"v"])
                else:
                    if i > 0 and words[i][0].isupper():
                        output.append([words[i],"n"])
                    else:
                        output.append([words[i],"UNK"])
                
        return output

    def pattern_label(self, labeled_sentence):
        index = 0
        for word_tag in labeled_sentence:

            if word_tag[1] == "UNK" or word_tag[1] == "AMB":
                pattern = []
                if index < 4:
                    pattern = [words[1] for words in labeled_sentence[:5]]
                    if word_tag[1] == "AMB":
                        word_tag[1] = self.get_possible_pattern_amb(pattern,index,self.lookup(word_tag[0]))
                    else:
                        word_tag[1] = self.get_possible_pattern(pattern,index)
                elif index > 4 and index+2 <len(labeled_sentence):
                    pattern = [words[1] for words in labeled_sentence[index-2:index+3]]
                    if word_tag[1] == "AMB":
                     
                        word_tag[1] = self.get_possible_pattern_amb(pattern,index,self.lookup(word_tag[0]))
                    else:
                        word_tag[1] = self.get_possible_pattern(pattern,index)
                else:
                    pattern = [words[1] for words in labeled_sentence[-5:]]
                    word_tag[1] = self.get_possible_pattern(pattern,5 - (len(labeled_sentence) - index))
                
                
            index += 1
        return labeled_sentence

    
    def predict(self,sentence):
        lookup = self.lookup_label(sentence)
        pattern_find  = self.pattern_label(lookup)
        return pattern_find


    def lookup(self,word):
        if word in self.__list_of_pronouns:
            return ["pr"]
        elif word in self.__list_of_conjunctions:
            return ["conj"]
        elif word in self.__list_of_stoppers:
            return ["stopper"]
        elif word in self.__list_of_determiners:
            return ["dt"]
        elif word in self.__list_of_stoppers:
            return ["stopper"]
        elif word in self.__list_of_linking_verbs:
            return ["vbl"]
        elif word in self.__list_of_prepositions:
            return ["prep"]
        elif word in self.__list_of_modifiers:
            return ["adv"]
        try:
            return list(set([tag.strip() for tag in self.__words_postag_dict[word]]))
        except:
            
            return None


    #------- utility methods -------------#
    def __regex_find(self,regex,string):
        q = re.findall(regex,string)
        if len(q) == 0 or q == None:
            return False
        return len(q[0]) == len(string)

    def __check_if_verb_from_prefixes(self,word):
        for pattern in self.__verb_patterns:
            if self.__regex_find(pattern,word):
                return True
        if word[0:2] == word[2:4]:
            return True
        return False

    def __check_if_adjective_from_prefixes(self,word):
        if (not word.startswith("ma")) and word.endswith("in"):
            return False
        
        for pattern in self.__adjective_patterns:
            if self.__regex_find(pattern,word):
                return True
        return False

    def check_for_patterns(self,input_pattern):
        possibles = []
        for template in self.__pos_tag_patterns:
            if len(input_pattern) > 4:
                score = 5
            else:
                score = len(input_pattern)
            for index in range(len(input_pattern)):
                if input_pattern[index] == template[index]:
                    pass
            
                else:
                    score -= 1
            
            if score >= 4 and len(input_pattern)>3:
                possibles.append(template)
            elif score == len(input_pattern)-1 and len(input_pattern)>=3:
                possibles.append(template)
                
        return possibles

    def get_possible_pattern(self,pattern,index):
        if index <= 4 and type(index) is int:
            try:
                
                return self.check_for_patterns(pattern)[0][index]
            except:
                return pattern[index]
        elif index >= 3 and type(index) is int:
            try:
                return self.check_for_patterns(pattern)[0][2]
            except:
                return pattern[2]
        return "UNK"

    def get_possible_pattern_amb(self,pattern,index,choices):
        
        if index <= 4 and type(index) is int:
            try:
                for possible in self.check_for_patterns(pattern):
                    
                    if possible[index] in choices:
                        return possible[index]
                return self.check_for_patterns(pattern)[0][index]
            except:
                return pattern[index]
        elif index > 4 and type(index) is int:
            try:
                for possible in self.check_for_patterns(pattern):
                    if possible[2] in choices:
                        return possible[2]
                return self.check_for_patterns(pattern)[0][2]
            except:
                return pattern[2]
        return "UNK"
            
        
    def __convert_pos_tag(self,pos_tag):
        for key in self.__convert_tags.keys():
            if pos_tag in self.__convert_tags[key]:
                return key
        if pos_tag.startswith("DT"):
            return "dt"
        return pos_tag
    
    def __convert_pos_tags_of_a_line(self,line):
        splitted_line = line.split(" ")
        converted = []
        for word in splitted_line:
            converted.append(self.__convert_pos_tag(word))
    
        return converted




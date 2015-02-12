import os,re

class Stemmer():
    __WORDS_DIR = os.path.dirname(os.path.realpath("stemmer")) +"\\trainingData\\words.txt"

    prefixes = [ 'ma','i', 'napaka', 'sing', 'magpapa', 'nagpapa',
                'ni', 'nakaka', 'naka', 'nagkaka', 'nakikipag',
                'nagpa', 'in', 'mag', 'um', 'mag', 'makaka','maka', 'in',
                'naka', 'taga', 'pang', 'pam', 'pag', 'kapag', 'kamag',
                'nagka', 'nag', 'ipag', 'magka', 'mang', 'pag', 'nagkaka',
                'nakakapag', 'magsi', 'pagka', 'pinag', 'na', 'pa',
                'pina', 'pang']

    
    suffixes = ['han', 'an', 'hanin', 'hang', 'nin', 'hin', 'h','ng','g','in']

    infixes = ['um','in','ar']

    words_list = []

    def __init__(self):
        self.train()
    
    def train(self):
        freader = open(self.__WORDS_DIR,"r")
        
        contents = freader.readlines()
        self.words_list = [i.replace("\n","") for i in contents]
        freader.close()
        

        
    def stem(self,word,full=False):
        inDB = False
        if not full and word in self.words_list:
            return word
        #print word

        #remove repeating elements
        if word[:2] == word[2:4]:
            word = word[2:]
            
        
        if word.find("-")>=0:
            return "ma"+word.split("-")[1]
        
        #print "[-]: "+word
        #remove prefixes
        for prefix in self.prefixes:
            if word.startswith(prefix):
                word = word[len(prefix):]
                try:
                    if re.search("g[bcdfghjklmnpqrstvwxz]",word).start() == 0:
                        word = word[1:]
                except: pass
                break
        #print "[prefix]: "+word 
        
        if word in self.words_list:
            return word
        
        #remove repeating elements
        if word[:2] == word[2:4]:
            word = word[2:]
            
        #print "[repeating]: "+word
        
        #remove suffixes
        
        for suffix in self.suffixes:
            if word.endswith(suffix):
                word = word[:-len(suffix)]

        if word in self.words_list:
            return word
        #print "[suffix]: "+word
        #remove affixes
        for infix in self.infixes:
            if word[1]+word[2] == infix:
                word = word[0] + word[3:]
        
       # print "[infix]: "+word
        #check if the word exists already in the word list
        if word in self.words_list:
            return word

                
            
        return word
    

    

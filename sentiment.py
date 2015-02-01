#sentiment classifier for english using sentiwordnet language database

import re,os

class Sentiment:

    training_data_sentiments = os.path.dirname(os.path.realpath("sentiment")) +"\\trainingData\senti.txt"

    #dictionary that contains the words and their corresponding
    #senti scores. Format is "index: [(pos_tag,(pos_score,neg_score))]"
    sentiwordnet = {}
    
    def __init__(self):
        self.train()
        pass
    
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
                print entry
                
            words = re.sub("#[0-9]+","",entry[4]).split()

            for word in words:
                if word in self.sentiwordnet:
                    self.sentiwordnet[word].append( ( pos_tag, (posi_score,nega_score,obj_score) ) )
                else:
                    self.sentiwordnet[word] = [ ( pos_tag, (posi_score,nega_score,obj_score) ) ]
                
        pass

    def predict_multi(self,iterable):
        total_polarity = [0,0,0]
        
        for entry in iterable:
            temp_polarity = [0,0,0]
            words = entry.split(" ")
            
            for word in words:
                word_polarity = self.predict(word)
                
                temp_polarity[0] += word_polarity[0]
                temp_polarity[1] += word_polarity[1]
                temp_polarity[2] += word_polarity[2]
                
            temp_polarity[0] /= len(words)
            temp_polarity[1] /= len(words)
            temp_polarity[2] /= len(words)
            
            total_polarity[0] += temp_polarity[0]
            total_polarity[1] += temp_polarity[1]
            total_polarity[2] += temp_polarity[2]


        if len(iterable) > 0:
            total_polarity[0] /= len(iterable)
            total_polarity[1] /= len(iterable)
            total_polarity[2] /= len(iterable)
        
        return total_polarity
    
    def predict(self,word,pos_tag = ""):
        pos = 0
        neg = 0
        obj = 0
        total = 0
        if pos_tag != "" or pos_tag == "AMB" or pos_tag == "UNK":
            try:
                for item in self.sentiwordnet[word]:
                    if item[0] == pos_tag:
                        pos+= float(item[1][0])
                        neg+= float(item[1][1])
                        obj+= float(item[1][2])
                    total+=1
            except:
            
                total+= 1
        else:
            try:                    
                for item in self.sentiwordnet[word]:
                    pos+= float(item[1][0])
                    neg+= float(item[1][1])
                    obj+= float(item[1][2])               
                    total+=1
            except:
                
                total+= 1
        return [pos/total,neg/total,obj/total]




#file downloaded from nltk website
#sentiwordnet should be included on the folders of nltk
from nltk.corpus.reader import sentiwordnet as swn


"""
This class is used as a module for tagSENT's sentiment generator
"""
class Sentiment:

    #file containing the training data    
    training_data_sentiments = "trainingData\\senti.txt"

    #the variable that will hold the sentiwordnet interface
    senti_machine = None
    def __init__(self):

        #train swn using training data
        self.senti_machine = swn.SentiWordNetCorpusReader(self.training_data_sentiments)
        
    def transform_POS_tag(self,pos_tag):
        if pos_tag == "adj":
            return swn.wn.ADJ
        elif pos_tag == "adv":
            return swn.wn.ADV
        elif pos_tag == "n":
            return swn.wn.NOUN
        elif pos_tag == "v":
            return swn.wn.VERB
        else:
            return pos_tag
    #method used to predict a sentiment of an english word
    #using an optional pos tag
    def predict(self,word,pos_tag=""):
        pos = 0 #variable that holds the total positive score
        neg = 0 #variable that holds the total negative score
        obj = 0 #variable that holds the total objectivity score
        total = 0 #variable that holds the total number of synsets

        pos_tag = self.transform_POS_tag(pos_tag)
        #if pos tag is undetermined, do this
        if pos_tag == "" or pos_tag == "UNK" or pos_tag == "AMB":

            #loop through all of the synsets (possible word defns.)
            for item in self.senti_machine.senti_synsets(word):

                #increment the total pos and neg scores
                pos += item.pos_score
                neg += item.neg_score
                obj += item.obj_score
                total += 1
        else:
            
            #loop through all of the synsets (possible word defns.) and using a pos tag
            for item in self.senti_machine.senti_synsets(word,pos_tag):

                #increment the total pos and neg scores
                pos += item.pos_score
                neg += item.neg_score
                obj += item.obj_score
                total +=1

        #if there are no synsets available for the word, then use 0,0,0
        try:        
            #return average scores of each as as a tuple
            return [pos/total,neg/total,obj/total]
        except Exception,e:
            print Exception, e
            return [0,0,0]


    #when a tagalog word is translated, there are multiple translations
    #this method is used to average the sentiment scores from multiple translations
    def predict_multi(self,words_list,pos_tag=""):

        #initialize the polarity variables
        pos = 0
        neg = 0
        obj = 0
        total = 0


        #loop through all the translations
        for translation in words_list:

            #temporary containers for the polarity of each translation
            temp_pos = 0
            temp_neg = 0
            temp_obj = 0

            #if there is a "or" in the text, get the left side phrase
            translation = translation.split(" or ")[0] 
            
            #a translation is sometimes consisted of a phrase, so we should get the total sentiment of the phrase
            for word in translation.split():

                #predict a word individually, store the tuple result
                prediction = self.predict(word,pos_tag)

                temp_pos += prediction[0] #positive scores are in index [0] of the returned tuple of method self.predict(word)
                temp_neg += prediction[1] #negative scores are in index [1]
                temp_obj += prediction[2] #objective scores are in index [2]
                
            #increment the counters
            pos += temp_pos
            neg += temp_neg 
            obj += temp_obj 
            total += 1
        try:
            return [pos/total,neg/total,obj/total]
        except Exception,e:
            print Exception, e
            return [pos/1,neg/1,obj/1]


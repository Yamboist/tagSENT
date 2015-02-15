import sentiment3, translator2, POS_tagger,re
import pprint
"""
this module is the integration of three modules, namely
Translator
Sentiment
POS Tagger

It is the class that is the core of the tagalog sentiment analysis
"""
class tagSENT:
    
    #instance of the translator class
    trans = translator2.Translator()

    #instance of the sentiment class
    senti = sentiment3.Sentiment()

    #instance of the part of speech tagger classs
    tagger = POS_tagger.POS_tagger()

    #variable that holds the variable for intensifiers [words that increase the polarity of a word]
    intensifiers = open("trainingData/intensifiers.txt","r").read().split("\n")

    #negators are words that flip the polarity of a word
    negators = ["hindi","wala","walang","di","Hindi","Wala","Walang","Di"]

    #attenuators are words that decrease the polarity of a word
    attenuators = ["medyo","halos","minsan"]


    def __init__(self):
        #train both models
        self.trans.train()
        #self.senti.train()
        pass


    """
    this method is used to predict each of the sentiment of *sentiment bearing* words
    such words are usually a non prepositional or non article words (n., adj., adv...)
    -
    accepts a string as a parameter, returns a list in a format [ [<word1>,[positive,negative]] , [...] , ...]
    """
    def predict_each(self,text,tags=None):
        
        #tag the words first using the pos tagger
        #the format of the tagged words are based from the output of the tagging prediction
        #[ [<word>,tag] , [<word2>,tag2] , ... ]
       
        
        if tags == None:
            tagged_words = self.tagger.predict(text)
        else:
            text = text.lower()
            tagged_words = [ [wrd,tg] for wrd,tg in zip(text.split(" "),tags.split(" "))]
            
        
        #this variable stores the total score of the prediction
        score = [0,0]
        #print tagged_words
        #raw_input()
        #this variable stores the prediction, uh yeah obviously.
        prediction = []

        wt_index = 0
        #loop through all the tagged words
        for word_tag in tagged_words:

            #store the sentiment score of the word being analyzed
            senti_score = [0,0]
            obj = [0]
            #check if the pos tag of the word is a possible sentiment bearing word
            #sentiment bearing words are words with a pos tag that is not prep., conj. or vbl.
            if word_tag[1] in ["n","v","adv","adj","AMB","UNK"]:
                
                #translate the tagalog word to english. This variable is a list of translations : [trans1, trans2, trans3]
                translated = self.trans.translate(word_tag[0],word_tag[1])
                
                #if the word is stemmed, there should be a ~ at the end, this is used so that the sentiment predictor
                #wouldn't use its pos tag anymore. The pos tag would be unused as the word has been stemmed, thus
                #the pos tag would also change
                if len(translated) > 0:
                    if translated[-1] == "~":
                        senti_score = self.senti.predict_multi(translated[:-1])
                        print senti_score
                    else:
                        #if the word is followed by a preposition, it is neutral
                        #like "sa uso", "sa bayan" , "sa Makati", noun phrases like that do not express polarity
                        if tagged_words[wt_index-1][1] == "prep" and word_tag[1] == "n":
                            
                            
                            senti_score = [0,0,1]
                        elif word_tag[0] in ["tapos"] and tagged_words[wt_index-1][1] in ["stopper","det","prep","adj"]:
                            senti_score = [0,0,1]
                            
                        else:
                            #use the prediction module of sentiment class by feeding all the translations. This variable stores: [positive, negative]
                            senti_score = self.senti.predict_multi(translated,word_tag[1])
                        

                #append to the word container its translation
                word_tag.append(translated)
                
                #if the the polarity of both is equal, most likely the word returned a [0,0] because it wasn't translated
                if senti_score[0] == senti_score[1]:

                    #check if the word contains an amplifier prefix
                    if word_tag[0].startswith("napaka") or word_tag[0].startswith("pinaka"):

                        #replace the infix napaka/ pinaka with ma, and then predict its sentiment score
                        senti_score = self.senti.predict_multi(self.trans.translate(re.sub("napaka|pinaka","ma",word_tag[0]),word_tag[1]),word_tag[1])
                
                #increase the polarity of the word by checking whether it has a amplifying prefix
                #or it is a repeating word ex: poging-pogi, matabang-mataba
                #this intensification seeks for "-" in the word
                senti_score = self.word_intensify(word_tag[0],senti_score)

                
                #add the extracted sentiment score to the total sentiment score, [0] is postive, [1] is negative
                score[0] += senti_score[0]
                score[1] += senti_score[1]
                if len(senti_score) > 2:
                    obj[0] = senti_score[2]
                
                
            #clear the score of the polarity that is lesser
            #if the positive is greater than the negative
            """if senti_score[0]>senti_score[1]:

                #clear the negative score
                senti_score[1] = 0


            #if the negative is greater than the positive
            elif senti_score[0]<senti_score[1]:

                #clear the positive score
                senti_score[0] = 0"""

            #add the current prediction of the word to the list of predicted words (prediction) variable
            if obj[0] > 0.95 or (obj[0] >= 0.9 and senti_score[0]<0.1 and senti_score[1]<0.1 and word_tag[1] == "n"):
                senti_score[0]=0
                senti_score[1]=0
                
            prediction.append([word_tag,senti_score+obj])

            wt_index +=1

            

        #use the nearby_intensify to check and apply the words that intensify its nearby word (forward)
        #ex: sobrang galing, this amplifies galing. the search for the target word to be amplified is forward
        prediction = self.nearby_intensify(prediction)

        #same as the previous method, but the search is in reverse
        #ex: ang galing niya sobra.
        prediction = self.nearby_intensify_reverse(prediction)

        #check for flipping words (negators), the search is only forward
        prediction = self.negation(prediction)
        
        #return the list containing the predictions
        return prediction

    """
    method that intensifies the word depending on its affixes
    parameters:
    word: string, the word being analyzed
    score: original polarity scores
    """
    def word_intensify(self,word,score):
        
        #if the word startswith napaka/ pinaka
        if word.startswith("napaka") or word.startswith("pinaka"):

            #if the positive score is greater than the negative, amplify it 70%
            if score[0] > score[1]:
                score[0] *= 1.7
            #vice versa
            else:
                score[1] *= 1.7

        #if the word contains a "-" amplify the polarity by 50%
        if word.find("-") >=0:
            if score[0] > score[1]:
                score[0] *= 1.5
            else:
                score[1] *= 1.5

        #return the modified score
        return score


    """
    this method checks whether there is an amplfying pattern within the prediction
    ex: ADV. PREP. N. ADJ.
    this method amplifies the ADJ, as given from this example
    parameter - 
    prediction: this can be extracted from predict_each
    """
    def nearby_intensify(self,prediction):

        #loop all over the prediction list
        for index in range(len(prediction)):

            #do this if the following condition/s is/are satisfied
            #if the word being predicted is an attenuator
            #if the word being predicted is an intensifier
            
            #if the prediction score of the word is not neutral (0,0) and the
            #pos tag of the word is either an adj/ adv, and the word is not a negator
            #(prediction[index][1] != [0,0,0] and prediction[index][0][1] in ["adv","adj"] and prediction[index][0][0] not in self.negators )
            if prediction[index][0][0] in self.attenuators or prediction[index][0][0] in self.intensifiers :
    
                #trigger variable, this changes to true if the word being intensified is already found
                trig = False

                #searches ahead of the words
                for word_score in prediction[index+1:]:

                    #if the pos tag of the word is anything but adverb 
                    if word_score[0][1] in ["adj","AMB","n","v","UNK"]:

                        #if the word is an intensifier
                        if prediction[index][0][0] in self.intensifiers:

                            #amplify thes greater polarity score by 70%
                            if word_score[1][0] > word_score[1][1]:
                                word_score[1][0] *= 1.7
                            else:
                                word_score[1][1] *= 1.7

                            #trigger the trig variable
                            trig = True

                        #if the word is an attenuator
                        if prediction[index][0][0] in self.attenuators:
                            
                            #weaken the polarity by 45%
                            word_score[1] = [word_score[1][0]*0.65,word_score[1][1]*0.65,word_score[1][2]]
                            trig = True
                            
                        #else if the pos tag of the word is an adjective 
                        elif prediction[index][0][1] == "adj":

                            #if the word is not a negator/attenuator/intensifier
                            if word_score[0][0] not in self.negators and word_score[0][0] not in self.attenuators and word_score[0][0] not in self.intensifiers:

                                #add the polarity of the describing word to the target word
                                word_score[1] = [word_score[1][0] + prediction[index][1][0] , word_score[1][1] + prediction[index][1][1],word_score[1][2]]

                                #clear the lesser scored polarity
                                if word_score[1][0]>word_score[1][1]:
                                    word_score[1][1] = 0
                                elif word_score[1][0]<word_score[1][1]:
                                    word_score[1][0] = 0

                                #trigger
                                trig = True

                        #if it hasn't passed the previous conditions 
                        else :
                            
                            #if the polarity score isn't neutral
                            if word_score[1] != [0,0]:
                                
                                #multiply the greater polarity of the target word that by the polarity of the describing word
                                if prediction[index][1][0] >prediction[index][1][1]:
                                    word_score[1][0] *= (1+prediction[index][1][0])
                                else:
                                    word_score[1][1] *= (1+prediction[index][1][1])

                                #trigger
                                trig = True

                        #if triggered, turn the polarity score of the describing word to neutral [0,0]
                        if trig:
                            prediction[index][1] = [0,0,0]
                            
                        #stop the loop
                        break

                    #stop the loop if the pos tag of the target word is a stopper
                    elif word_score[0][1] in ["stopper","conj"]:
                        break

        #return the modified prediction
        return prediction

    """
    this method is just like the nearby_intensify
    however, we reverse the prediction list so it looks backwards and not forward
    """
    def nearby_intensify_reverse(self,prediction):
        #reverse the prediction list in place
        prediction.reverse()

        #loop (forward) through all the elements of reversed prediction; essentially it looks backwards now
        for index in range(len(prediction)):

            #if the word is an intensifier then
            if prediction[index][0][0] in self.intensifiers :

                #look forward for the target word
                for word_score in prediction[index+1:]:

                    #if the word is not an adverb then
                    if word_score[0][1] in ["adj","AMB","n","v","UNK"]:

                        #amplify the polarity of the target word by 70%
                        if word_score[1][0] > word_score[1][1]:
                            word_score[1][0] *= 1.7
                        else:
                            word_score[1][1] *= 1.7

                        #turn the describing word to neutral
                        prediction[index][1] = [0,0,0]

                        #stop the loop
                        break

        #bring the prediction list into its original position by re-reversing it
        prediction.reverse()

        #return the modified prediction
        return prediction

    """
    this method utilizes the negators to achieve the flipping ability
    parameter -
    prediction: can be extracted from predict_each
    """
    def negation(self,prediction):

        #loop through the prediction list, checking if there is a negator on the list
        for index in range(len(prediction)):

            #if a negator is seen then
            if prediction[index][0][0] in self.negators:

                #loop forwards the list
                for word_score in prediction[index+1:]:

                    #if the word is "mas", stop the loop
                    if word_score[0][0] in ["mas"]:
                        break

                    #if the word is an adjective/noun/verb and it is not neutral
                    if (word_score[0][1] in ["adj","v","n"] and (word_score[1] != [0.0,0.0,0.0] and word_score[1] != [0.0,0.0,1.0] and word_score[1] != [0.0,0.0,0,0]) ) or word_score[0][1] == "adv":
                        print word_score[1]
                        if word_score[0][0] in self.intensifiers:
                            
                            #prediction[index][1] = [i*0.6 for i in prediction[index][1]]
                            pass
                        else:

                            if word_score[0][1] == "adv":
                                pass
                            else:
                                
                                #reverse the polarity
                                word_score[1] = word_score[1][:2][::-1] + [word_score[1][2]]
                               
                                #word_score[1] = word_score[1][::-1]

                                #turn the negator into a neutral polarity
                                prediction[index][1] = [0,0,0]

                                #stop the loop
                                break

                    if word_score[0][1] in ["stopper"]:
                        break
        #return the modified prediction
        return prediction

    """
    this is the method that predicts the given text and outputs the total
    parameters -
    text: string, a grammatically correct text
    output -
    total - (<prediction_label>,[positive,negative],prediction_list)
    """
    def predict(self,text,tags=None):
        
        #seperate all punctuations to be a space from its neighbors
        #example: Siya ay mabilis, ngunit mali-mali ang kanyang gawa. -> Siya ay mabilis , ngunit mali-mali ang kanyang gawa .
        text = re.sub("([A-Za-z0-9])([.;,!?])","\g<1> \g<2>",text)

        #use the predict_each method to get the prediction_list
        pred = self.predict_each(text,tags)

        #return the analyzed total of the prediction list
        return self.total(pred)


    """
    this is the method that analyzes the output of predict_each (the prediction list)
    parameters -
    prediction - a list containing the details of the prediction; can be get from predict_each method
    output -
    total - (<prediction_label>,[positive,negative],prediction_list)
    """
    def total(self,prediction):

        #this the variable that stores the total sentiment of the given text
        total_sentiment = [0,0]

        #loop through all the predictions
        for i in prediction:

            #if the positive polarity is greater than 0.039 add it to the positive total
            #0.039 is the threshold for a relevant polarity
            if i[1][0] > 0.01:
                total_sentiment[0]+= i[1][0]

            #same for negative
            if i[1][1] > 0.01:
                total_sentiment[1]+= i[1][1]

        #this variable holds the difference
        diff = 0

        #check if there is no zero value in the polarity score
        if 0 not in total_sentiment:

            #get the total of the sentiments (would be used for percentage)
            total = total_sentiment[0] + total_sentiment[1]

            #then, get the percentage of each polarity
            perc_neg = total/total_sentiment[1]
            perc_pos = total/total_sentiment[0]

            #get the difference between the percentages of the polarities
            diff = abs(perc_neg - perc_pos)


        #if the difference between the polarities is greater than .10, then
        if total_sentiment>0.05 and diff>=.10:

            #increase the negative by 50%
            #studies show that people are biased to say positive than negative words
            #thus positive scores tend to get higher than negatives
            #therefore we amplify the bias to show true polarity
            total_sentiment[1] = total_sentiment[1] * 1

        #return the corresponding greater polarity
        if total_sentiment[0] > total_sentiment[1]:
            return ("POSITIVE",total_sentiment,prediction)
        elif total_sentiment[0] < total_sentiment[1]:
            return ("NEGATIVE",total_sentiment,prediction)
        else:
            return ("NEUTRAL",total_sentiment,prediction)

    def pretty(self,text,tag=None):
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.predict(text,tag)) 
"""x = open("tests/tests.txt")
sentx =tagSENT()
contents= x.readlines()
x.close()
for i in contents:
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint( sentx.predict(i.strip()) )
    print "=============\n\n""

"""
"""sentx = tagSENT()
print "Training complete"
pp = pprint.PrettyPrinter(indent=4)
pp.pprint( sentx.predict( "ikaw linoloko mo lang ang sarili mo" ) )
""" 
x = tagSENT()
#x.pretty("Wala masyadong estudyante na dumadalaw o nagpupunta ng library upang gawin ang kanilang takdang aralin","adv adj n conj v conj v prep n conj v det pr n n stopper stopper")
x.pretty("Maayos ang pakikitungo ng mga employee at staff",
         "adj det n prep det n conj n stopper")

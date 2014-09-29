import sentiment, translator, POS_tagger,re

class tagSENT:

    trans = translator.Translator()
    senti = sentiment.Sentiment()
    tagger = POS_tagger.POS_tagger()

    intensifiers = open("trainingData/intensifiers.txt","r").read().split("\n")
    negators = ["hindi","wala","walang"]
    
    def __init__(self):
        self.trans.train()
        self.senti.train()
        pass

    def predict_each(self,text):
        tagged_words = self.tagger.predict(text)
        score = [0,0]
        #print tagged_words
        prediction = []
        for word_tag in tagged_words:
            senti_score = [0,0]
            if word_tag[1] in ["n","v","adv","adj","AMB","UNK"]:
                #print word_tag
                translated = self.trans.translate(word_tag[0])
                #print "translation: " + str(translated)
                senti_score = self.senti.predict_multi(translated)
                if senti_score[0] == senti_score[1]:
                    if word_tag[0].startswith("napaka") or word_tag[0].startswith("pinaka"):
                        senti_score = self.senti.predict_multi(self.trans.translate(re.sub("napaka|pinaka","ma",word_tag[0])))
                        
                senti_score = self.word_intensify(word_tag[0],senti_score)
                score[0] += senti_score[0]
                score[1] += senti_score[1]
                #print senti_score
               # print

            
            prediction.append([word_tag,senti_score])
      
        prediction = self.nearby_intensify(prediction)
        prediction = self.nearby_intensify_reverse(prediction)
        prediction = self.negation(prediction)
        return prediction
            
    def word_intensify(self,word,score):
        if word.startswith("napaka") or word.startswith("pinaka"):
            if score[0] > score[1]:
                score[0] *= 1.7
            else:
                score[1] *= 1.7

        if word.find("-") >=0:
            if score[0] > score[1]:
                score[0] *= 1.5
            else:
                score[1] *= 1.5
        return score

    def nearby_intensify(self,prediction):
        for index in range(len(prediction)):
            if prediction[index][0][0] in self.intensifiers:
                
                for word_score in prediction[index+1:]:
                    if word_score[0][1] in ["adj","AMB","n","v"]:
                        if word_score[1][0] > word_score[1][1]:
                            word_score[1][0] *= 1.7
                        else:
                            word_score[1][1] *= 1.7
                            
                        prediction[index][1] = [0,0]
                        break
        return prediction

    def nearby_intensify_reverse(self,prediction):
        prediction.reverse()
        for index in range(len(prediction)):
            if prediction[index][0][0] in self.intensifiers and prediction[index][1] != [0,0]:
                
                for word_score in prediction[index+1:]:
                    if word_score[0][1] in ["adj","AMB","n","v"]:
                        if word_score[1][0] > word_score[1][1]:
                            word_score[1][0] *= 1.7
                        else:
                            word_score[1][1] *= 1.7
                            
                        prediction[index][1] = [0,0]
                        break
        prediction.reverse()
        return prediction

    def negation(self,prediction):
        for index in range(len(prediction)):
            if prediction[index][0][0] in self.negators:
                for word_score in prediction[index+1:]:
                    if word_score[0][0] in ["mas"]:
                        break
                    if word_score[0][1] in ["adj","v","n"]:
                        print word_score[1]
                        word_score[1] = word_score[1][::-1]
                            
                        prediction[index][1] = [0,0]
                        break
        return prediction

    def predict(self,text):
        pred = self.predict_each(text)
        return self.total(pred)

    def total(self,prediction):
        total_sentiment = [0,0]
        for i in prediction:
            total_sentiment[0]+= i[1][0]
            total_sentiment[1]+= i[1][1]
        if total_sentiment[0] > total_sentiment[1]:
            return ("POSITIVE",total_sentiment,prediction)
        elif total_sentiment[0] < total_sentiment[1]:
            return ("NEGATIVE",total_sentiment,prediction)
        else:
            return ("NEUTRAL",total_sentiment,prediction)

   

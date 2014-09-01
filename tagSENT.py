import sentiment, translator, POS_tagger

class tagSENT:

    trans = translator.Translator()
    senti = sentiment.Sentiment()
    tagger = POS_tagger.POS_tagger()
    
    def __init__(self):
        self.trans.train()
        self.senti.train()
        pass

    def predict(self,text):
        tagged_words = self.tagger.predict(text)
        score = [0,0]
        for word_tag in tagged_words:
            
            if word_tag[1] in ["n","v","adv","adj"]:   
                translated = self.trans.translate(word_tag[0])
                print "translation: " + str(translated)
                senti_score = self.senti.predict_multi(translated)
                score[0] += senti_score[0]
                score[1] += senti_score[1]
                print word_tag[0],senti_score
                
        if score[0]>score[1]:
            return "POSITIVE"
        elif score[1]>score[0]:
            return "NEGATIVE"
        else:
            return "NEUTRAL"
        

q = tagSENT()
print q.predict("Ang kanilang serbisyo ay kulang sa husay")

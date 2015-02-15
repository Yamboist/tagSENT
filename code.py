import web, tagSENT2, json,urllib

render = web.template.render('templates/')

urls = (
    '/', 'index',
    '/api','api'
)

#initiliaze the sentiment analyzer
senti = tagSENT2.tagSENT()

class index:
    def GET(self):
        return render.index()

class api:
    
    def POST(self):
        
        
        data = web.data()
        #print data
       # print data.split("=")
        #raw_input()
        text = data.split("=")[1].replace(" &p","").strip().replace("&p","")
        #print text +"\n\n=================\n"
        #raw_input()
        tag = data.split("=")[2]
        text = text.replace("+"," ")
        text = urllib.unquote(text).decode('utf8')
        
        prediction = senti.predict(text)
        result = {}
        result["sentiment"] = prediction[0]
        result["scores"] = prediction[2]
        result["total"] = prediction[1]
        
       
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        scoreBuilder = ""
    
        for res in result["scores"]:
            tag = res[0][1]
            word = res[0][0]
            score_pos = res[1][0]
            score_neg = res[1][1]
            trans = ""

       
            try:
                for wordx in res[0][2]:
                    if trans.find(wordx) < 0:
                        trans+= wordx +","
                
            except:pass
            build = """
        <item>
            <word>%s</word>
            <tag>%s</tag>
            <positive_score>%s</positive_score>
            <negative_score>%s</negative_score>
            <translations>%s</translations>
        </item>
            """%(word,tag,score_pos,score_neg,trans[:-1])

            scoreBuilder += build
            
        whole =  """
<tagSENT>
    <prediction>
        <positive>%s</positive>
        <negative>%s</negative>
    </prediction>
    <words>
%s
    </words>
    <generalsentiment>%s</generalsentiment>
</tagSENT>
        """ % ( result["total"][0], result["total"][1],scoreBuilder,result["sentiment"] )
        
        return whole

#web.webapi.internalerror = web.debugerror
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

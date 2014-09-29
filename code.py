import web, tagSENT, json

render = web.template.render('templates/')

urls = (
    '/', 'index',
    '/api','api'
)

#initiliaze the sentiment analyzer
senti = tagSENT.tagSENT()

class index:
    def GET(self):
        return render.index()

class api:
    
    def POST(self):
        
        
        data = web.data()
        text = data.split("=")[1]
        text = text.replace("+"," ")
        
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

            build = """
        <item>
            <word>%s</word>
            <tag>%s</tag>
            <positive_score>%s</positive_score>
            <negative_score>%s</negative_score>
        </item>
            """%(word,tag,score_pos,score_neg)

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

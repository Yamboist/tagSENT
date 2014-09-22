import web, tagSENT, json

render = web.template.render('templates/')

urls = (
    '/', 'index',
    '/api','api'
)

class index:
    def GET(self):
        return render.index()

class api:
    def POST(self):

        
        data = web.data()
        text = data.split("=")[1]
        text = text.replace("+"," ")
        senti = tagSENT.tagSENT()
        prediction = senti.predict(text)
        result = {}
        result["sentiment"] = prediction[0]
        result["scores"] = prediction[2]
        result["total"] = prediction[1]
        return json.dumps(result)

#web.webapi.internalerror = web.debugerror
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

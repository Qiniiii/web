from flask import Flask, jsonify, request
from newsapi import NewsApiClient, newsapi_exception
from collections import Counter
application = Flask(__name__)


@application.route('/')
def index():
    return application.send_static_file('index.html')


@application.route('/headlines')
def topnews():
    try:
        # print(request.args.get('sources'))
        newapi = NewsApiClient(api_key='97d246f67d3a46a18ef6bf6eb3db11a9')
        if len(request.args) > 0:
            news = newapi.get_top_headlines(sources=request.args.get('sources'), page_size=30)
        else:
            news = newapi.get_top_headlines(page_size=30)

        with application.open_resource("static/stopwords_en.txt","r") as stop_file:
            stopwords=stop_file.read().splitlines()

        articles = news['articles']
        titles=[]
        print(type(articles))

        for article in articles:
            if article['title'] is not None:
                titles.extend(article['title'].replace(":","").replace(",","").split(' '))
            if article['urlToImage'] is None \
                    or article['description'] is None \
                    or article['author'] is None \
                    or article['publishedAt'] is None \
                    or article['url'] is None \
                    or article['title'] is None \
                    or article['source'] is None\
                    or article['urlToImage'] =='null' \
                    or article['description'] =='null' \
                    or article['author'] =='null' \
                    or article['publishedAt'] =='null' \
                    or article['url'] =='null' \
                    or article['title'] =='null' \
                    or article['source'] =='null' \
                    or article['urlToImage'] == '' \
                    or article['description'] == '' \
                    or article['author'] == '' \
                    or article['publishedAt'] == '' \
                    or article['url'] == '' \
                    or article['title'] == '' \
                    or article['source'] == '':
                articles.remove(article)
        print(titles)
        most_30=Counter(titles).most_common(60)
        print(most_30)
        words=[]
        i=0
        for line in most_30:
            if line[0].lower() not in stopwords and i <30:
                d = {}
                i+=1
                d['word']=line[0]
                d['size']=str(line[1])
                words.append(d)
        print(len(articles))
        print(articles)
        return jsonify({'articles': articles,'words':words})

    except newsapi_exception.NewsAPIException as e:
        return jsonify(e.exception)


@application.route('/allnews')
def allnews():
    try:
        args=request.args.to_dict()
        print(args)
        newapi = NewsApiClient(api_key='97d246f67d3a46a18ef6bf6eb3db11a9')
        if 'sources' in args:
            news = newapi.get_everything(q=args['q'],
                                         sources=args["sources"],
                                         from_param=args['from'],
                                         to=args['to'],
                                         page_size=60,
                                         sort_by='publishedAt',
                                         language='en')
        else:
            news = newapi.get_everything(q=args['q'],
                                         from_param=args['from'],
                                         to=args['to'],
                                         page_size=60,
                                         sort_by='publishedAt',
                                         language='en')
        articles = news['articles']
        for article in articles:
            if article['urlToImage'] is None \
                    or article['description'] is None \
                    or article['author'] is None \
                    or article['publishedAt'] is None \
                    or article['url'] is None \
                    or article['title'] is None \
                    or article['source'] is None\
                    or article['urlToImage'] =='null' \
                    or article['description'] =='null' \
                    or article['author'] =='null' \
                    or article['publishedAt'] =='null' \
                    or article['url'] =='null' \
                    or article['title'] =='null' \
                    or article['source'] =='null' \
                    or article['urlToImage'] == '' \
                    or article['description'] == '' \
                    or article['author'] == '' \
                    or article['publishedAt'] == '' \
                    or article['url'] == '' \
                    or article['title'] == '' \
                    or article['source'] == '':
                articles.remove(article)
        print(articles)
        return jsonify({'articles': articles})
    except newsapi_exception.NewsAPIException as e:
        return jsonify(e.exception)


@application.route('/sources')
def sourcenews():
    try:
        newapi = NewsApiClient(api_key='97d246f67d3a46a18ef6bf6eb3db11a9')
        if len(request.args) > 0:
            print(request.args.get('category'))
            news = newapi.get_sources(category=request.args.get('category'),language='en' )
        else:
            news = newapi.get_sources(language='en')
        return jsonify(news)
    except newsapi_exception.NewsAPIException as e:
        return jsonify(e.exception)


# run the app.
if __name__ == "__main__":
    #application.debug = True
    application.run()

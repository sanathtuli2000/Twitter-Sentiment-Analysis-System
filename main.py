from flask import Flask, render_template, request
from tweet_extraction import TwitterSearchAPI
from analysis_algo import analysis, result
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/graph')
def graph():
    return render_template('graph.html')

@app.route('/learn_more')
def learnmore():
    return render_template('learn_more.html')


@app.route('/search')
def search():
    query = request.args.get('query')
    TwitterSearchAPI(query)
    result = analysis(query)
    if result!=0:
        return result
    else:
        return 'No results found'

@app.route('/result/<keyword>')
def display(keyword):
    a = result(keyword)
    if a!=0:
        data = []
        data.append(['Emotion', 'Count'])
        for k,v in a['result'].items():
            data.append([k,v])
        print(data)
        return render_template('graph.html', data = data)
    else:
        return render_template('graph.html',data = [[]])

@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)


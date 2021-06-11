import pymongo
from bson.json_util import dumps
from collections import Counter
from flask import jsonify

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
mongo_db_name = mongo_client["twitter"]
collection = mongo_db_name["tweets"]

def analysis(query):



    stop_tweets = ["hey", "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours",
                   "yourself",
                   "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself",
                   "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that",
                   "these",
                   "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having",
                   "do",
                   "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until",
                   "while",
                   "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during",
                   "before",
                   "after", "above", "\"RT", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under",
                   "again",
                   "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both",
                   "each",
                   "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so",
                   "than",
                   "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]

    data = collection.find({'keyword': query})
    if(data and data.count()>0):
        final_tweets = []
        for i in range(300):
            tweet = dumps(data[i]['text'])
            tokenized_tweet = tweet.split(' ')
            for tweet in tokenized_tweet:
                if tweet not in stop_tweets:
                    final_tweets.append(tweet)

        emotion_list = []
        with open('emotions.txt', 'r') as file:
            for line in file:
                clear_line = line.replace('\n', '').replace(',', '').replace("'", '').strip()
                word, emotion = clear_line.split(':')
                if word in final_tweets:
                    emotion_list.append(emotion)

            w = Counter(emotion_list)
            mongo_db_name.result.insert_one({'keyword':query, 'result': w})
            return w
    else:
        return 0

def result(keyword):
    ans = mongo_db_name.result.find_one({'keyword': keyword},{'_id':0})
    if ans and len(ans)>0:
        return ans
    else:
        return 0
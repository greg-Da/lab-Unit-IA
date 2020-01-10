from flask import Flask, jsonify, request
import pymongo
from pymongo import MongoClient
import matchmaking

app = Flask(__name__)

client = MongoClient('mongodb+srv://greg:<MDP>@cluster0-ymglz.gcp.mongodb.net/test?retryWrites=true&w=majority')

@app.route('/entreprise', methods=['GET'])
def get_all_entreprises():
    job = client.db.entreprise 

    output = []

    for q in job.find():
        output.append({'entreprise' : q['entreprise'], 'language' : q['language'], 'salaire' : q['salaire']})

    return jsonify({'result' : output})


@app.route('/worker', methods=['GET'])
def get_all_workers():
    user = client.db.worker 

    output = []

    for q in user.find():
        output.append({'worker' : q['worker'], 'language' : q['language'], 'salaire' : q['salaire'], 'distance' : q['distance'], 'test' : q['test']})

    return jsonify({'result' : output})


@app.route('/compare/<entreprise>/<worker>', methods=['GET'])
def compare(entreprise, worker):
    job = client.db.entreprise
    user = client.db.worker

    q = job.find_one({'entreprise' : entreprise})
    query = user.find_one({'worker' : worker})

    if q:
        lang_entreprise = {'language' : q['language']}
        sal_entreprise = {'salaire' : q['salaire']}
    else:
        lang_entreprise = 'No results found'

    if query:
        lang_worker = {'language' : query['language']}
        sal_worker = {'salaire' : query['salaire']}
        distance = {'distance' : query['distance']}
        test ={'test' : query['test']}
    else:
        lang_worker = 'No results found'

    results = matchmaking(lang_entreprise, lang_worker, sal_entreprise, sal_worker, distance, test)
    return(results)

@app.route('/entreprise', methods=['POST'])
def add_entreprise():
    framework = client.db.entreprise 

    entreprise = request.json['entreprise']
    language = request.json['language']
    salaire = request.json['salaire']

    framework_id = framework.insert({'entreprise' : entreprise, 'language' : language, 'salaire' : salaire})
    new_framework = framework.find_one({'_id' : framework_id})

    output = {'entreprise' : new_framework['entreprise'], 'language' : new_framework['language'], 'salaire' : new_framework['salaire']}

    return jsonify({'result' : output})
    
    
@app.route('/worker', methods=['POST'])
def add_worker():
    framework = client.db.worker 

    worker = request.json['worker']
    language = request.json['language']
    salaire = request.json['salaire']
    distance = request.json['distance']
    test = request.json['test']

    framework_id = framework.insert({'worker' : worker, 'language' : language, 'salaire' : salaire, 'distance' : distance, 'test' : test})
    new_framework = framework.find_one({'_id' : framework_id})

    output = {'worker' : new_framework['worker'], 'language' : new_framework['language'], 'salaire' : new_framework['salaire'], 'distance' : new_framework['distance'], 'test' : new_framework['test']}

    return jsonify({'result' : output})

if __name__ == '__main__':
    app.run(debug=True)

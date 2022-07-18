import csv
from flask import Flask, jsonify
from flask import Flask,render_template,request
import pickle
import numpy as np
import diseaseprediction
final_df = pickle.load(open('final.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
meds = pickle.load(open('meds.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))

app = Flask(__name__)
with open('templates/Test2.csv', newline='') as f:
    reader = csv.reader(f)
    symptoms = next(reader)
    symptoms = symptoms[:len(symptoms) - 1]

@app.route('/',methods=['GET'])
def dropdown():
    return render_template('index.html',symptoms=symptoms)



@app.route('/disease_predict', methods=['POST'])
def disease_predict():
    disease = []
    selected_symptoms = []
    if(request.form['Symptom1']!="") and (request.form['Symptom1'] not in selected_symptoms):
        selected_symptoms.append(request.form['Symptom1'])
    if(request.form['Symptom2']!="") and (request.form['Symptom2'] not in selected_symptoms):
        selected_symptoms.append(request.form['Symptom2'])
    if(request.form['Symptom3']!="") and (request.form['Symptom3'] not in selected_symptoms):
        selected_symptoms.append(request.form['Symptom3'])
    if(request.form['Symptom4']!="") and (request.form['Symptom4'] not in selected_symptoms):
        selected_symptoms.append(request.form['Symptom4'])
    if(request.form['Symptom5']!="") and (request.form['Symptom5'] not in selected_symptoms):
        selected_symptoms.append(request.form['Symptom5'])

    disease = diseaseprediction.dosomething(selected_symptoms)

    return render_template('index.html',disease=disease,symptoms=symptoms)


@app.route('/recommend')
def recommend_ui():
    return render_template('recommender.html')

@app.route('/recommend_meds',methods = ['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]
    data = []
    for i in similar_items:
        item = []
        temp_df = meds[meds['Drug_Name'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Drug_Name')['Drug_Name'].values))
        item.extend(list(temp_df.drop_duplicates('Drug_Name')['Company_Name'].values))
        item.extend(list(temp_df.drop_duplicates('Drug_Name')['avg_rating'].values))

        data.append(item)

    print(data)
    return render_template('recommender.html',data = data)

if __name__ == '__main__':
    app.run(debug=True)

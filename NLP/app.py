# import necessary libraries
import os
import pickle
import pandas as pd
from rake_nltk import Rake
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

cosine_sim = pd.read_pickle("wines_model.pkl")
df3 = pd.read_pickle("df3.pkl")


indices = pd.Series(df3.index)

def recommendations(title, cosine_sim = cosine_sim):
    recommended_wines = []
    idx = indices[indices == title].index[0]
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)
    top_5_indexes = list(score_series.iloc[1:6].index)
    
    for i in top_5_indexes:
        
        recommended_wines.append(list("Variety: " + df3.index + ", Country: " + df3.country + ", Winery: " + df3.winery)[i])
    
    return recommended_wines



my_data = []

app = Flask(__name__)

# @app.route("/")
# def home():
#     return "Welcome!"

@app.route("/", methods=["GET", "POST"])
def wine_recommendation():
    if request.method == "POST":
        wine = request.form["variety"]
        my_data = recommendations(wine)
        

        recommendation_list = [{
        "1": my_data[0],
        "2": my_data[1],
        "3": my_data[2],
        "4": my_data[3],
        "5": my_data[4],
        
        
        }]



        return jsonify(recommendation_list)

    return render_template("form.html")


 
if __name__ == "__main__":
    app.run(debug=True)

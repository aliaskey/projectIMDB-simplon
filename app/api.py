#pip install flask joblib
# ou pour FastAPI
#pip install fastapi[all]
#Pour run dans terminal > python 1_creation_API.py

from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Charger le modèle depuis le fichier
model = joblib.load("model/modeleIMDB.joblib")




@app.route('/')
def home():
    return "API de prédiction de notes IMDB"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        # Traitement des données et prédiction
        features = [
            data['num_critic_for_reviews'], 
            data['director_fb_likes'],
            data['cast_total_fb_likes'],
            data['gross'],
            data['num_user_for_reviews'],
            data['budget'],
            data['duration'],
            data['title_year'],
            data['movie_fb_likes']
        ]
         # modèle pour faire une prédiction
        prediction = model.predict([features])
        # Renvoi de la réponse
        return jsonify({'prediction': prediction[0]})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=False)



import streamlit as st
import requests
import pandas as pd
import os
from joblib import load


# Charger le modèle
modele_charge = load('model/modeleIMDB.joblib')

# Fonction pour prédire les scores IMDB
def predict_imdb_score(features):
    # Effectuer la prédiction
    prediction = modele_charge.predict([features])
    return prediction[0]


# Définir le titre de la page
st.set_page_config(page_title="Prédiction film IMDB")


st.title("Prédiction de note IMDB de film")

movie_data = pd.read_csv("https://raw.githubusercontent.com/AntoanetaStoyanova/PROJECT-IMBD/main/app/Datas/5000_movie_correction.csv")


# Créer la liste des langues uniques
languages_list = movie_data['language'].unique()

# Sélectionner la langue à l'aide du multiselect
selected_language = st.multiselect("Sélectionner la langue du film", languages_list)

# Filtrer les données en fonction de la langue sélectionnée
filtered_data = movie_data[movie_data['language'].isin(selected_language)]

# Filtrer les données en fonction des genres sélectionnés
if not filtered_data.empty:
    
    genres_columns = ['genre1', 'genre2', 'genre3', 'genre4', 'genre5', 'genre6', 'genre7', 'genre8']
    genres_list = filtered_data[genres_columns].stack().unique()

    # Sélectionner les genres à l'aide du multiselect
    selected_genres = st.multiselect("Sélectionner le(s) genre(s) de film", genres_list)
   
    # Filtrer à nouveau les données en fonction des genres sélectionnés
    filtered_data = filtered_data[filtered_data.apply(lambda row: any(genre in selected_genres for genre in row[genres_columns] if pd.notnull(genre)), axis=1)]

    # Extraire les années uniques correspondant aux genres sélectionnés
    years_list = filtered_data['title_year'].unique()
    
    # Sélectionner les années à l'aide du multiselect
    selected_years = st.multiselect("Sélectionner l'année du film", years_list)

    # Filtrer à nouveau les données en fonction des années sélectionnées
    if selected_years:
        filtered_data = filtered_data[filtered_data['title_year'].isin(selected_years)]
        
        # Extraire les réalisateurs uniques correspondant aux genres et années sélectionnés
        directors_list = filtered_data['director_name'].unique()

        # Sélectionner le réalisateur à l'aide du multiselect
        selected_directors = st.multiselect("Sélectionner le réalisateur du film", directors_list)
        
        # Filtrer à nouveau les données en fonction des réalisateurs sélectionnés
        if selected_directors:
            filtered_data = filtered_data[filtered_data['director_name'].isin(selected_directors)]

            # Afficher les films correspondants
            if not filtered_data.empty:
                st.write("Films correspondants :")
                for index, row in filtered_data.iterrows():
                    st.write(f"Titre : {row['movie_title']}")
                    st.write(f"IMDB : {row['movie_imdb_link']}")
                    st.write(f"IMDB note réel: {row['imdb_score']}")


                # Bouton pour prédire le score IMDB
                    if st.button("Prédire IMDB note"):
                        features = [row['num_critic_for_reviews'], row['director_fb_likes'], row['cast_total_fb_likes'], row['gross'], 
                                    row['num_user_for_reviews'], row['budget'], row['duration'], row['title_year'], row['movie_fb_likes']]
                        predicted_score = predict_imdb_score(features)
                        st.write(f"IMDB note prédite: {predicted_score:.2f}")

else:
    st.write("Aucun film correspondant à la langue sélectionnée.")
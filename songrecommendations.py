import os
import requests

def get_token(clientId, clientSecret):
    # Fonction pour récupérer le token Spotify
    # Code de votre fonction existante

def get_track_recommendations(seed_tracks, token):
    # Fonction pour récupérer les recommandations de pistes Spotify
    # Code de votre fonction existante

def song_recommendation_vis(reco_df):
    # Fonction pour visualiser les recommandations de chansons
    # Code de votre fonction existante

def save_album_image(img_url, track_id):
    # Fonction pour enregistrer l'image d'album
    # Code de votre fonction existante

def get_album_image(track_id):
    # Fonction pour récupérer l'image d'album
    image_path = f'img/{track_id}.jpg'
    if os.path.exists(image_path):
        with open(image_path, 'rb') as f:
            image = f.read()
        return image
    else:
        return None

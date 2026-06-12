# mlapp/ml_models/model_manager.py
"""
Gestionnaire de sauvegarde et chargement des modèles ML en fichiers .pkl
Permet un déploiement rapide sans réentraînement
"""

import os
import pickle
import pandas as pd
import numpy as np
from datetime import datetime

# Chemins des modèles
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODELS_DIR = os.path.join(BASE_DIR, 'mlapp', 'ml_models', 'saved_models')

# Créer le dossier si nécessaire
os.makedirs(MODELS_DIR, exist_ok=True)

# Noms des fichiers
CHURN_MODEL_PATH = os.path.join(MODELS_DIR, 'churn_model.pkl')
CHURN_SCALER_PATH = os.path.join(MODELS_DIR, 'churn_scaler.pkl')
CHURN_FEATURES_PATH = os.path.join(MODELS_DIR, 'churn_features.pkl')

CLUSTERING_MODEL_PATH = os.path.join(MODELS_DIR, 'clustering_model.pkl')
CLUSTERING_SCALER_PATH = os.path.join(MODELS_DIR, 'clustering_scaler.pkl')
CLUSTERING_DATA_PATH = os.path.join(MODELS_DIR, 'clustering_data.pkl')

SATISFACTION_MODEL_PATH = os.path.join(MODELS_DIR, 'satisfaction_model.pkl')
SATISFACTION_SCALER_PATH = os.path.join(MODELS_DIR, 'satisfaction_scaler.pkl')
SATISFACTION_FEATURES_PATH = os.path.join(MODELS_DIR, 'satisfaction_features.pkl')

METADATA_PATH = os.path.join(MODELS_DIR, 'models_metadata.pkl')


# ==================== SAUVEGARDE DES MODÈLES ====================

def save_churn_model(model, scaler, features):
    """
    Sauvegarder le modèle de churn
    
    Args:
        model: Modèle XGBoost entraîné
        scaler: StandardScaler ajusté
        features: Liste des features utilisées
    """
    try:
        with open(CHURN_MODEL_PATH, 'wb') as f:
            pickle.dump(model, f)
        
        with open(CHURN_SCALER_PATH, 'wb') as f:
            pickle.dump(scaler, f)
        
        with open(CHURN_FEATURES_PATH, 'wb') as f:
            pickle.dump(features, f)
        
        print(f"✅ Modèle Churn sauvegardé dans {CHURN_MODEL_PATH}")
        update_metadata('churn')
        return True
        
    except Exception as e:
        print(f"❌ Erreur sauvegarde modèle Churn: {e}")
        return False


def save_clustering_model(kmeans_model, scaler, cluster_data):
    """
    Sauvegarder le modèle de clustering
    
    Args:
        kmeans_model: Modèle KMeans entraîné
        scaler: StandardScaler ajusté
        cluster_data: Dict avec données, stats, visualisations
    """
    try:
        with open(CLUSTERING_MODEL_PATH, 'wb') as f:
            pickle.dump(kmeans_model, f)
        
        with open(CLUSTERING_SCALER_PATH, 'wb') as f:
            pickle.dump(scaler, f)
        
        with open(CLUSTERING_DATA_PATH, 'wb') as f:
            pickle.dump(cluster_data, f)
        
        print(f"✅ Modèle Clustering sauvegardé dans {CLUSTERING_MODEL_PATH}")
        update_metadata('clustering')
        return True
        
    except Exception as e:
        print(f"❌ Erreur sauvegarde modèle Clustering: {e}")
        return False


def save_satisfaction_model(model, scaler, features):
    """
    Sauvegarder le modèle de satisfaction
    
    Args:
        model: Modèle XGBoost entraîné
        scaler: MinMaxScaler ajusté
        features: Liste des features utilisées
    """
    try:
        with open(SATISFACTION_MODEL_PATH, 'wb') as f:
            pickle.dump(model, f)
        
        with open(SATISFACTION_SCALER_PATH, 'wb') as f:
            pickle.dump(scaler, f)
        
        with open(SATISFACTION_FEATURES_PATH, 'wb') as f:
            pickle.dump(features, f)
        
        print(f"✅ Modèle Satisfaction sauvegardé dans {SATISFACTION_MODEL_PATH}")
        update_metadata('satisfaction')
        return True
        
    except Exception as e:
        print(f"❌ Erreur sauvegarde modèle Satisfaction: {e}")
        return False


# ==================== CHARGEMENT DES MODÈLES ====================

def load_churn_model():
    """
    Charger le modèle de churn depuis les fichiers .pkl
    
    Returns:
        tuple: (model, scaler, features) ou (None, None, None) si erreur
    """
    try:
        if not os.path.exists(CHURN_MODEL_PATH):
            print("⚠️ Fichier modèle Churn introuvable")
            return None, None, None
        
        with open(CHURN_MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        
        with open(CHURN_SCALER_PATH, 'rb') as f:
            scaler = pickle.load(f)
        
        with open(CHURN_FEATURES_PATH, 'rb') as f:
            features = pickle.load(f)
        
        print(f"✅ Modèle Churn chargé depuis {CHURN_MODEL_PATH}")
        return model, scaler, features
        
    except Exception as e:
        print(f"❌ Erreur chargement modèle Churn: {e}")
        return None, None, None


def load_clustering_model():
    """
    Charger le modèle de clustering depuis les fichiers .pkl
    
    Returns:
        dict: Dictionnaire avec modèle, scaler, données ou None si erreur
    """
    try:
        if not os.path.exists(CLUSTERING_MODEL_PATH):
            print("⚠️ Fichier modèle Clustering introuvable")
            return None
        
        with open(CLUSTERING_MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        
        with open(CLUSTERING_SCALER_PATH, 'rb') as f:
            scaler = pickle.load(f)
        
        with open(CLUSTERING_DATA_PATH, 'rb') as f:
            cluster_data = pickle.load(f)
        
        print(f"✅ Modèle Clustering chargé depuis {CLUSTERING_MODEL_PATH}")
        
        return {
            'model': model,
            'scaler': scaler,
            **cluster_data
        }
        
    except Exception as e:
        print(f"❌ Erreur chargement modèle Clustering: {e}")
        return None


def load_satisfaction_model():
    """
    Charger le modèle de satisfaction depuis les fichiers .pkl
    
    Returns:
        tuple: (model, scaler, features) ou (None, None, None) si erreur
    """
    try:
        if not os.path.exists(SATISFACTION_MODEL_PATH):
            print("⚠️ Fichier modèle Satisfaction introuvable")
            return None, None, None
        
        with open(SATISFACTION_MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        
        with open(SATISFACTION_SCALER_PATH, 'rb') as f:
            scaler = pickle.load(f)
        
        with open(SATISFACTION_FEATURES_PATH, 'rb') as f:
            features = pickle.load(f)
        
        print(f"✅ Modèle Satisfaction chargé depuis {SATISFACTION_MODEL_PATH}")
        return model, scaler, features
        
    except Exception as e:
        print(f"❌ Erreur chargement modèle Satisfaction: {e}")
        return None, None, None


# ==================== MÉTADONNÉES ====================

def update_metadata(model_name):
    """
    Mettre à jour les métadonnées des modèles
    
    Args:
        model_name: Nom du modèle ('churn', 'clustering', 'satisfaction')
    """
    try:
        # Charger métadonnées existantes
        if os.path.exists(METADATA_PATH):
            with open(METADATA_PATH, 'rb') as f:
                metadata = pickle.load(f)
        else:
            metadata = {}
        
        # Mettre à jour
        metadata[model_name] = {
            'last_trained': datetime.now().isoformat(),
            'version': metadata.get(model_name, {}).get('version', 0) + 1
        }
        
        # Sauvegarder
        with open(METADATA_PATH, 'wb') as f:
            pickle.dump(metadata, f)
        
        print(f"📊 Métadonnées mises à jour pour {model_name}")
        
    except Exception as e:
        print(f"⚠️ Erreur mise à jour métadonnées: {e}")


def get_metadata():
    """
    Récupérer les métadonnées de tous les modèles
    
    Returns:
        dict: Métadonnées ou {} si erreur
    """
    try:
        if not os.path.exists(METADATA_PATH):
            return {}
        
        with open(METADATA_PATH, 'rb') as f:
            return pickle.load(f)
            
    except Exception as e:
        print(f"❌ Erreur lecture métadonnées: {e}")
        return {}


def check_models_exist():
    """
    Vérifier si tous les modèles existent
    
    Returns:
        dict: Statut de chaque modèle
    """
    return {
        'churn': os.path.exists(CHURN_MODEL_PATH),
        'clustering': os.path.exists(CLUSTERING_MODEL_PATH),
        'satisfaction': os.path.exists(SATISFACTION_MODEL_PATH),
    }


def get_models_info():
    """
    Obtenir les informations sur tous les modèles
    
    Returns:
        dict: Informations détaillées
    """
    info = {
        'models_dir': MODELS_DIR,
        'models_exist': check_models_exist(),
        'metadata': get_metadata(),
    }
    
    # Taille des fichiers
    for model_name in ['churn', 'clustering', 'satisfaction']:
        model_path = globals()[f'{model_name.upper()}_MODEL_PATH']
        if os.path.exists(model_path):
            size_kb = os.path.getsize(model_path) / 1024
            info[f'{model_name}_size_kb'] = round(size_kb, 2)
    
    return info


# ==================== UTILITAIRES ====================

def delete_all_models():
    """
    Supprimer tous les modèles sauvegardés (utile pour réentraînement complet)
    """
    try:
        for file_path in [
            CHURN_MODEL_PATH, CHURN_SCALER_PATH, CHURN_FEATURES_PATH,
            CLUSTERING_MODEL_PATH, CLUSTERING_SCALER_PATH, CLUSTERING_DATA_PATH,
            SATISFACTION_MODEL_PATH, SATISFACTION_SCALER_PATH, SATISFACTION_FEATURES_PATH,
            METADATA_PATH
        ]:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"🗑️ Supprimé: {file_path}")
        
        print("✅ Tous les modèles ont été supprimés")
        return True
        
    except Exception as e:
        print(f"❌ Erreur suppression modèles: {e}")
        return False


if __name__ == '__main__':
    # Test du module
    print("🔍 Vérification des modèles...")
    info = get_models_info()
    
    print(f"\n📁 Dossier: {info['models_dir']}")
    print(f"\n📊 Modèles existants:")
    for model, exists in info['models_exist'].items():
        status = "✅" if exists else "❌"
        print(f"  {status} {model.upper()}")
    
    print(f"\n📈 Métadonnées:")
    for model, data in info['metadata'].items():
        print(f"  {model.upper()}:")
        print(f"    - Version: {data.get('version', 'N/A')}")
        print(f"    - Dernier entraînement: {data.get('last_trained', 'N/A')}")

"""
Script de test du gestionnaire de modèles
Exécutez ce script pour vérifier que model_manager.py fonctionne correctement
"""

import sys
import os

# Ajouter le chemin du projet
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

print("="*60)
print("🧪 TEST DU GESTIONNAIRE DE MODÈLES ML")
print("="*60)

try:
    # Importer le gestionnaire
    from mlapp.ml_models.model_manager import (
        get_models_info,
        check_models_exist,
        get_metadata,
        MODELS_DIR,
    )
    
    print("\n✅ Import réussi !")
    
    # Vérifier le dossier
    print(f"\n📁 Dossier des modèles :")
    print(f"   {MODELS_DIR}")
    print(f"   Existe : {os.path.exists(MODELS_DIR)}")
    
    if not os.path.exists(MODELS_DIR):
        print("\n⚠️  Création du dossier...")
        os.makedirs(MODELS_DIR, exist_ok=True)
        print("✅ Dossier créé")
    
    # Vérifier les modèles existants
    print("\n📊 Modèles existants :")
    models_exist = check_models_exist()
    for model_name, exists in models_exist.items():
        status = "✅" if exists else "❌"
        print(f"   {status} {model_name.upper()}")
    
    # Métadonnées
    print("\n📈 Métadonnées :")
    metadata = get_metadata()
    if metadata:
        for model_name, data in metadata.items():
            print(f"   {model_name.upper()}:")
            print(f"     - Version : {data.get('version', 'N/A')}")
            print(f"     - Dernier entraînement : {data.get('last_trained', 'N/A')}")
    else:
        print("   Aucune métadonnée disponible")
    
    # Informations complètes
    print("\n📋 Informations complètes :")
    info = get_models_info()
    
    for model_name in ['churn', 'clustering', 'satisfaction']:
        size_key = f'{model_name}_size_kb'
        if size_key in info:
            print(f"   {model_name.upper()} : {info[size_key]} KB")
    
    print("\n" + "="*60)
    
    # Résumé
    total_models = sum(1 for exists in models_exist.values() if exists)
    if total_models == 3:
        print("✅ TOUS LES MODÈLES SONT PRÊTS")
    elif total_models > 0:
        print(f"⚠️  {total_models}/3 modèles disponibles")
        print("   Exécutez : python manage.py train_and_save_models")
    else:
        print("❌ AUCUN MODÈLE TROUVÉ")
        print("\n📝 Pour créer les modèles :")
        print("   1. Installez Django : pip install django pandas xgboost scikit-learn")
        print("   2. Exécutez : python manage.py train_and_save_models")
    
    print("="*60)
    
except ImportError as e:
    print(f"\n❌ Erreur d'import : {e}")
    print("\n📝 Solution :")
    print("   Vérifiez que le fichier model_manager.py existe dans :")
    print(f"   {os.path.join(BASE_DIR, 'mlapp', 'ml_models', 'model_manager.py')}")
    
except Exception as e:
    print(f"\n❌ Erreur : {e}")
    import traceback
    traceback.print_exc()

print("\n")

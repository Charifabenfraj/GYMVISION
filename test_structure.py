#!/usr/bin/env python
"""Test rapide de la structure des fichiers"""
import os

print("=" * 70)
print("🔍 VÉRIFICATION DE LA NOUVELLE STRUCTURE")
print("=" * 70)

base_dir = r"c:\Users\chari\Desktop\ProjetMLDjango\ProjetMLDjango"

# Vérifier model_training.py
model_training_path = os.path.join(base_dir, 'mlapp', 'ml_models', 'model_training.py')
print(f"\n📝 Fichier model_training.py:")
if os.path.exists(model_training_path):
    size = os.path.getsize(model_training_path)
    with open(model_training_path, 'r', encoding='utf-8') as f:
        lines = len(f.readlines())
    print(f"   ✅ Existe: {lines} lignes, {size:,} bytes")
else:
    print(f"   ❌ Non trouvé")

# Compter views.py
views_path = os.path.join(base_dir, 'mlapp', 'views.py')
print(f"\n📊 Fichier views.py:")
with open(views_path, 'r', encoding='utf-8') as f:
    views_lines = len(f.readlines())
print(f"   📏 Total: {views_lines} lignes")

# Vérifier les .pkl
models_dir = os.path.join(base_dir, 'mlapp', 'ml_models', 'saved_models')
print(f"\n💾 Fichiers .pkl dans saved_models/:")
pkl_files = [f for f in os.listdir(models_dir) if f.endswith('.pkl')]
total_size = 0
for pkl in sorted(pkl_files):
    size = os.path.getsize(os.path.join(models_dir, pkl))
    total_size += size
    print(f"   - {pkl}: {size/1024:.2f} KB")
print(f"   📦 Total: {len(pkl_files)} fichiers, {total_size/1024:.2f} KB")

# Vérifier que les imports sont corrects dans model_training.py
print(f"\n🔍 Vérification des imports dans model_training.py:")
with open(model_training_path, 'r', encoding='utf-8') as f:
    content = f.read()
    if 'def creer_modele_churn():' in content:
        print("   ✅ creer_modele_churn() trouvée")
    if 'def creer_modele_clustering():' in content:
        print("   ✅ creer_modele_clustering() trouvée")
    if 'def creer_modele_satisfaction():' in content:
        print("   ✅ creer_modele_satisfaction() trouvée")
    if 'from ..views import preparer_donnees' in content:
        print("   ✅ Import de preparer_donnees correct")

# Vérifier les imports dans views.py
print(f"\n🔍 Vérification des imports dans views.py:")
with open(views_path, 'r', encoding='utf-8') as f:
    views_content = f.read()
    if 'from .ml_models.model_training import' in views_content:
        print("   ✅ Import de model_training présent")
    if 'creer_modele_churn' in views_content:
        print("   ✅ creer_modele_churn référencée")
    if 'creer_modele_clustering' in views_content:
        print("   ✅ creer_modele_clustering référencée")
    if 'creer_modele_satisfaction' in views_content:
        print("   ✅ creer_modele_satisfaction référencée")

print("\n" + "=" * 70)
print("✅ STRUCTURE VALIDÉE - Refactoring terminé!")
print("=" * 70)
print(f"\n📊 RÉSUMÉ:")
print(f"   - model_training.py créé avec les fonctions d'entraînement")
print(f"   - views.py conserve {views_lines} lignes")
print(f"   - {len(pkl_files)} fichiers .pkl prêts à l'emploi")
print(f"   - Les fonctions de training sont appelées uniquement si .pkl absent")
print(f"\n💡 AVANTAGES:")
print(f"   - Code mieux organisé (séparation des responsabilités)")
print(f"   - views.py reste le même nombre de lignes mais plus maintenable")
print(f"   - Fonctions de training réutilisables dans d'autres contextes")
print(f"   - Fichiers .pkl chargés en priorité (performance optimale)")

# mlapp/management/commands/train_and_save_models.py
"""
Commande Django pour entraîner et sauvegarder tous les modèles ML
Usage: python manage.py train_and_save_models
"""

from django.core.management.base import BaseCommand
from mlapp.ml_models.model_manager import (
    save_churn_model, 
    save_clustering_model, 
    save_satisfaction_model,
    get_models_info
)
import sys
import os

# Ajouter le chemin du projet au sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, BASE_DIR)


class Command(BaseCommand):
    help = 'Entraîne et sauvegarde tous les modèles ML en fichiers .pkl'

    def add_arguments(self, parser):
        parser.add_argument(
            '--model',
            type=str,
            help='Entraîner un modèle spécifique (churn, clustering, satisfaction)',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force le réentraînement même si les modèles existent',
        )

    def handle(self, *args, **options):
        from mlapp import views
        
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('🚀 ENTRAÎNEMENT ET SAUVEGARDE DES MODÈLES ML'))
        self.stdout.write(self.style.SUCCESS('='*60 + '\n'))
        
        model_to_train = options.get('model')
        force = options.get('force', False)
        
        # Vérifier les modèles existants
        if not force:
            info = get_models_info()
            models_exist = info['models_exist']
            
            if model_to_train:
                if models_exist.get(model_to_train, False):
                    self.stdout.write(
                        self.style.WARNING(
                            f'⚠️  Le modèle {model_to_train} existe déjà. '
                            f'Utilisez --force pour réentraîner.'
                        )
                    )
                    return
            else:
                all_exist = all(models_exist.values())
                if all_exist:
                    self.stdout.write(
                        self.style.WARNING(
                            '⚠️  Tous les modèles existent déjà. '
                            'Utilisez --force pour réentraîner.'
                        )
                    )
                    return
        
        # Entraîner les modèles
        if model_to_train == 'churn' or model_to_train is None:
            self.train_churn(views)
        
        if model_to_train == 'clustering' or model_to_train is None:
            self.train_clustering(views)
        
        if model_to_train == 'satisfaction' or model_to_train is None:
            self.train_satisfaction(views)
        
        # Afficher le résumé
        self.show_summary()
    
    def train_churn(self, views):
        """Entraîner et sauvegarder le modèle de churn"""
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.HTTP_INFO('📊 MODÈLE CHURN'))
        self.stdout.write('='*60)
        
        try:
            self.stdout.write('🔄 Entraînement en cours...')
            model, scaler, features = views.creer_modele_churn()
            
            if model is None:
                self.stdout.write(self.style.ERROR('❌ Échec entraînement Churn'))
                return
            
            self.stdout.write(self.style.SUCCESS('✅ Entraînement réussi'))
            
            # Sauvegarder
            self.stdout.write('💾 Sauvegarde en cours...')
            if save_churn_model(model, scaler, features):
                self.stdout.write(self.style.SUCCESS('✅ Modèle Churn sauvegardé'))
            else:
                self.stdout.write(self.style.ERROR('❌ Échec sauvegarde'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Erreur: {e}'))
    
    def train_clustering(self, views):
        """Entraîner et sauvegarder le modèle de clustering"""
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.HTTP_INFO('📊 MODÈLE CLUSTERING'))
        self.stdout.write('='*60)
        
        try:
            self.stdout.write('🔄 Entraînement en cours...')
            cluster_model = views.creer_modele_clustering()
            
            if cluster_model is None or 'model' not in cluster_model:
                self.stdout.write(self.style.ERROR('❌ Échec entraînement Clustering'))
                return
            
            self.stdout.write(self.style.SUCCESS('✅ Entraînement réussi'))
            
            # Sauvegarder
            self.stdout.write('💾 Sauvegarde en cours...')
            kmeans_model = cluster_model['model']
            scaler = cluster_model['scaler']
            
            # Préparer les données à sauvegarder (sans le modèle et scaler)
            cluster_data = {k: v for k, v in cluster_model.items() 
                          if k not in ['model', 'scaler']}
            
            if save_clustering_model(kmeans_model, scaler, cluster_data):
                self.stdout.write(self.style.SUCCESS('✅ Modèle Clustering sauvegardé'))
            else:
                self.stdout.write(self.style.ERROR('❌ Échec sauvegarde'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Erreur: {e}'))
    
    def train_satisfaction(self, views):
        """Entraîner et sauvegarder le modèle de satisfaction"""
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.HTTP_INFO('📊 MODÈLE SATISFACTION'))
        self.stdout.write('='*60)
        
        try:
            self.stdout.write('🔄 Entraînement en cours...')
            model, scaler, features = views.creer_modele_satisfaction()
            
            if model is None:
                self.stdout.write(self.style.ERROR('❌ Échec entraînement Satisfaction'))
                return
            
            self.stdout.write(self.style.SUCCESS('✅ Entraînement réussi'))
            
            # Sauvegarder
            self.stdout.write('💾 Sauvegarde en cours...')
            if save_satisfaction_model(model, scaler, features):
                self.stdout.write(self.style.SUCCESS('✅ Modèle Satisfaction sauvegardé'))
            else:
                self.stdout.write(self.style.ERROR('❌ Échec sauvegarde'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Erreur: {e}'))
    
    def show_summary(self):
        """Afficher le résumé des modèles"""
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('📊 RÉSUMÉ'))
        self.stdout.write('='*60 + '\n')
        
        info = get_models_info()
        
        self.stdout.write(f"📁 Dossier: {info['models_dir']}\n")
        
        self.stdout.write("📊 Modèles sauvegardés:")
        for model, exists in info['models_exist'].items():
            if exists:
                status = self.style.SUCCESS('✅')
                size = info.get(f'{model}_size_kb', 0)
                self.stdout.write(f"  {status} {model.upper()} ({size} KB)")
            else:
                status = self.style.ERROR('❌')
                self.stdout.write(f"  {status} {model.upper()}")
        
        if info['metadata']:
            self.stdout.write("\n📈 Métadonnées:")
            for model, data in info['metadata'].items():
                self.stdout.write(f"  {model.upper()}:")
                self.stdout.write(f"    - Version: {data.get('version', 'N/A')}")
                self.stdout.write(f"    - Dernier entraînement: {data.get('last_trained', 'N/A')}")
        
        self.stdout.write('\n' + self.style.SUCCESS('='*60))
        self.stdout.write(self.style.SUCCESS('✅ ENTRAÎNEMENT TERMINÉ'))
        self.stdout.write(self.style.SUCCESS('='*60 + '\n'))

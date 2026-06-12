# mlapp/ml_models/model_training.py
"""
Fonctions d'entraînement des modèles ML
Ces fonctions sont appelées UNIQUEMENT si les fichiers .pkl n'existent pas
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.model_selection import train_test_split


def creer_modele_churn():
    """
    Créer et entraîner le modèle Churn
    Appelé par views.py uniquement si churn_model.pkl n'existe pas
    """
    try:
        from xgboost import XGBClassifier
        from ..views import preparer_donnees
        
        print("🤖 Création du modèle Churn...")
        
        data = preparer_donnees()
        if data is None:
            print("⚠️ Impossible de préparer les données")
            return None, None, None
        
        df = data['cleaned']
        
        all_features = [
            'gender', 'Age', 'abonoment_type', 'visit_per_week', 'days_per_week',
            'avg_time_in_gym', 'avg_time_check_in', 'avg_time_check_out',
            'attend_group_lesson', 'personal_training', 'drink_abo', 'uses_sauna'
        ]
        
        features = [f for f in all_features if f in df.columns]
        
        if 'churn' not in df.columns:
            print("⚠️ Colonne 'churn' manquante")
            return None, None, None
        
        X = df[features]
        y = df['churn']
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        model = XGBClassifier(
            n_estimators=100,
            max_depth=4,
            learning_rate=0.1,
            random_state=42,
            eval_metric='logloss',
            use_label_encoder=False
        )
        
        model.fit(X_train_scaled, y_train)
        
        train_score = model.score(X_train_scaled, y_train)
        test_score = model.score(X_test_scaled, y_test)
        
        print(f"📈 Performance: Train={train_score:.4f}, Test={test_score:.4f}")
        
        # Sauvegarder automatiquement
        from .model_manager import save_churn_model
        save_churn_model(model, scaler, features)
        
        return model, scaler, features
        
    except Exception as e:
        print(f"❌ Erreur création modèle churn: {e}")
        return None, None, None


def creer_modele_clustering():
    """
    Créer et entraîner le modèle Clustering
    Appelé par views.py uniquement si clustering_model.pkl n'existe pas
    """
    try:
        from ..views import preparer_donnees
        
        print("🎯 Création du modèle Clustering...")
        
        data = preparer_donnees()
        if data is None:
            print("⚠️ Données non disponibles")
            return None
        
        df = data['cleaned']
        
        features = [
            'visit_per_week', 'days_per_week', 'avg_time_in_gym',
            'attend_group_lesson', 'personal_training', 'drink_abo',
            'uses_sauna', 'Age', 'abonoment_type', 'gender'
        ]
        
        features = [f for f in features if f in df.columns]
        
        if len(features) < 3:
            print(f"⚠️ Pas assez de features: {features}")
            return None
        
        X = df[features].dropna()
        
        if len(X) < 10:
            print("⚠️ Pas assez de données")
            return None
        
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
        kmeans.fit(X_scaled)
        
        df_clean = df.loc[X.index].copy()
        df_clean['cluster'] = kmeans.labels_
        
        silhouette = silhouette_score(X_scaled, kmeans.labels_)
        print(f"✅ Clustering créé - Silhouette: {silhouette:.4f}")
        
        cluster_analysis = analyser_clusters(df_clean, kmeans.labels_, features)
        visualizations = creer_visualisations_clustering(df_clean, X_scaled, kmeans)
        
        result = {
            'model': kmeans,
            'scaler': scaler,
            'features': features,
            'data': df_clean,
            'cluster_analysis': cluster_analysis,
            'visualizations': visualizations,
            'optimal_k': 4,
        }
        
        # Sauvegarder automatiquement
        from .model_manager import save_clustering_model
        cluster_data = {k: v for k, v in result.items() if k not in ['model', 'scaler']}
        save_clustering_model(kmeans, scaler, cluster_data)
        
        return result
        
    except Exception as e:
        print(f"❌ Erreur modèle clustering: {e}")
        import traceback
        traceback.print_exc()
        return None


def creer_modele_satisfaction():
    """
    Créer et entraîner le modèle Satisfaction
    Appelé par views.py uniquement si satisfaction_model.pkl n'existe pas
    """
    try:
        from xgboost import XGBClassifier
        from sklearn.preprocessing import LabelEncoder
        from ..views import preparer_donnees
        
        print("😊 Création du modèle de satisfaction...")
        
        data = preparer_donnees()
        if data is None:
            print("⚠️ Données non disponibles")
            return None, None, None
        
        df = data['cleaned']
        
        features = [
            'gender', 'Age', 'abonoment_type', 'visit_per_week', 'days_per_week',
            'avg_time_in_gym', 'avg_time_check_in', 'avg_time_check_out',
            'attend_group_lesson', 'personal_training', 'drink_abo', 'uses_sauna'
        ]
        
        features = [f for f in features if f in df.columns]
        
        # Calcul du score de satisfaction
        satisfaction_score = pd.Series(20, index=df.index)
        
        if 'visit_per_week' in df.columns:
            visit_norm = df['visit_per_week'] / 7.0
            satisfaction_score += visit_norm * 30
        
        if 'avg_time_in_gym' in df.columns:
            time_norm = np.clip(df['avg_time_in_gym'] / 180, 0, 1)
            satisfaction_score += time_norm * 20
        
        services_cols = ['attend_group_lesson', 'personal_training', 'drink_abo', 'uses_sauna']
        services_count = sum([df[col] for col in services_cols if col in df.columns])
        satisfaction_score += (services_count / 4.0) * 20
        
        if 'abonoment_type' in df.columns:
            satisfaction_score += df['abonoment_type'] * 10
        
        if 'churn' in df.columns:
            satisfaction_score += (1 - df['churn']) * 20
        
        satisfaction_score = np.clip(satisfaction_score, 0, 100)
        
        df['Satisfaction_Level'] = pd.cut(
            satisfaction_score,
            bins=[0, 50, 75, 100],
            labels=[0, 1, 2],
            include_lowest=True
        )
        
        X = df[features]
        y_raw = df['Satisfaction_Level'].astype(int)
        
        mask = ~y_raw.isna()
        X = X[mask]
        y_raw = y_raw[mask]
        
        if len(X) == 0:
            print("⚠️ Pas de données valides")
            return None, None, None
        
        le = LabelEncoder()
        y = le.fit_transform(y_raw)
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y if len(np.unique(y)) > 1 else None
        )
        
        scaler = MinMaxScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        model = XGBClassifier(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            random_state=42,
            eval_metric='mlogloss',
            use_label_encoder=False
        )
        
        model.fit(X_train_scaled, y_train)
        
        score = model.score(X_test_scaled, y_test)
        print(f"✅ Modèle satisfaction créé - Accuracy: {score:.4f}")
        
        # Sauvegarder automatiquement
        from .model_manager import save_satisfaction_model
        save_satisfaction_model(model, scaler, features)
        
        return model, scaler, features
        
    except Exception as e:
        print(f"❌ Erreur création modèle satisfaction: {e}")
        import traceback
        traceback.print_exc()
        return None, None, None


# ==================== FONCTIONS AUXILIAIRES ====================

def analyser_clusters(df, labels, features):
    """Analyser les caractéristiques de chaque cluster"""
    try:
        df_clustered = df.copy()
        df_clustered['cluster'] = labels
        
        cluster_stats = {}
        cluster_descriptions = {}
        recommendations = {}
        
        for cluster_id in sorted(df_clustered['cluster'].unique()):
            cluster_data = df_clustered[df_clustered['cluster'] == cluster_id]
            
            stats = {
                'count': len(cluster_data),
                'percentage': (len(cluster_data) / len(df_clustered)) * 100,
                'avg_visits': cluster_data['visit_per_week'].mean() if 'visit_per_week' in cluster_data.columns else 0,
                'avg_time': cluster_data['avg_time_in_gym'].mean() if 'avg_time_in_gym' in cluster_data.columns else 0,
                'premium_rate': cluster_data['abonoment_type'].mean() if 'abonoment_type' in cluster_data.columns else 0,
                'group_lesson_rate': cluster_data['attend_group_lesson'].mean() if 'attend_group_lesson' in cluster_data.columns else 0,
                'personal_training_rate': cluster_data['personal_training'].mean() if 'personal_training' in cluster_data.columns else 0,
                'avg_age': cluster_data['Age'].mean() if 'Age' in cluster_data.columns else 0,
            }
            
            cluster_stats[cluster_id] = stats
            
            if stats['avg_visits'] < 2:
                description = "Clients occasionnels"
            elif stats['avg_visits'] < 4:
                description = "Clients réguliers"
            else:
                description = "Clients passionnés"
            
            if stats['premium_rate'] > 0.7:
                description += " Premium"
            
            if stats['avg_age'] > 55:
                description += " Seniors"
            elif stats['avg_age'] < 30:
                description += " Jeunes"
            
            cluster_descriptions[cluster_id] = description
            
            if cluster_id == 0:
                recs = ["Relancer par email", "Proposer pack initiation", "Inviter à cours gratuit"]
            elif cluster_id == 1:
                recs = ["Fidéliser avec récompenses", "Proposer upgrade Premium", "Inviter événements"]
            elif cluster_id == 2:
                recs = ["Offrir contenus exclusifs", "Proposer coaching personnalisé", "Inviter ambassadeur"]
            else:
                recs = ["Service prioritaire", "Horaires adaptés", "Activités spécifiques"]
            
            recommendations[cluster_id] = recs
        
        return {
            'stats': cluster_stats,
            'descriptions': cluster_descriptions,
            'recommendations': recommendations
        }
        
    except Exception as e:
        print(f"❌ Erreur analyse clusters: {e}")
        return {}


def creer_visualisations_clustering(df, X_scaled, kmeans_model):
    """Créer des visualisations pour le clustering"""
    try:
        visualizations = {}
        
        # Clusters en 2D (PCA)
        plt.figure(figsize=(10, 8))
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(X_scaled)
        
        scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], 
                            c=kmeans_model.labels_, 
                            cmap='viridis', alpha=0.6, s=50)
        plt.colorbar(scatter, label='Cluster')
        plt.xlabel('PCA Component 1')
        plt.ylabel('PCA Component 2')
        plt.title('Visualisation des Clusters (PCA)')
        plt.grid(True, alpha=0.3)
        
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        visualizations['cluster_plot'] = base64.b64encode(buf.getvalue()).decode('utf-8')
        plt.close()
        
        # Distribution
        plt.figure(figsize=(8, 6))
        cluster_counts = pd.Series(kmeans_model.labels_).value_counts().sort_index()
        colors = plt.cm.viridis(np.linspace(0, 1, len(cluster_counts)))
        
        bars = plt.bar(cluster_counts.index.astype(str), cluster_counts.values, color=colors)
        plt.xlabel('Cluster')
        plt.ylabel('Nombre de Clients')
        plt.title('Distribution des Clusters')
        
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom')
        
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        visualizations['distribution_plot'] = base64.b64encode(buf.getvalue()).decode('utf-8')
        plt.close()
        
        return visualizations
        
    except Exception as e:
        print(f"❌ Erreur visualisations: {e}")
        return {}

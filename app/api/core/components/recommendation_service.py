import pandas as pd
import numpy as np
import pickle
from typing import Dict, Optional
from app.api.core.config import settings

class RecommendationService:
    def __init__(self):
        self.df = None
        self.similarity_matrix = None
        self.model_data = None
        self.restaurant_names = []
        self.name_to_index = {}
        self.is_loaded = False
        
    def load_models(self):
       
        try:
           
            with open(settings.MODEL_PATH, 'rb') as f:
                self.model_data = pickle.load(f)
            
           
            self.df = pd.read_csv(settings.DATA_PATH)
            
           
            self.similarity_matrix = np.load(settings.SIMILARITY_MATRIX_PATH)
            
           
            self.restaurant_names = self.df['name'].tolist()
            self.name_to_index = {name: idx for idx, name in enumerate(self.restaurant_names)}
            
            self.is_loaded = True
            print("Models loaded successfully!")
            
        except Exception as e:
            print(f"Error loading models: {e}")
            self.is_loaded = False
    
    def find_restaurant_index(self, restaurant_name: str) -> Optional[int]:
       
        if restaurant_name in self.name_to_index:
            return self.name_to_index[restaurant_name]
        
       
        for name in self.restaurant_names:
            if restaurant_name.lower() in name.lower() or name.lower() in restaurant_name.lower():
                return self.name_to_index[name]
        
        return None
    
    def get_recommendations(self, restaurant_name: str, top_n: int = 10, min_similarity: float = 0.3) -> Dict:
       
        if not self.is_loaded:
            return {"error": "Models not loaded"}
        
        restaurant_idx = self.find_restaurant_index(restaurant_name)
        
        if restaurant_idx is None:
            return {"error": f"Restaurant '{restaurant_name}' not found"}
        
       
        restaurant_similarities = self.similarity_matrix[restaurant_idx]
        
       
        similar_indices = np.argsort(restaurant_similarities)[::-1][1:top_n+1]
        similar_scores = restaurant_similarities[similar_indices]
        
       
        valid_mask = similar_scores >= min_similarity
        valid_indices = similar_indices[valid_mask]
        valid_scores = similar_scores[valid_mask]
        
        if len(valid_indices) == 0:
            return {"error": "No similar restaurants found"}
        
       
        recommendations = []
        for idx, score in zip(valid_indices, valid_scores):
            restaurant_data = self.df.iloc[idx]
            recommendations.append({
                'id': int(idx),
                'name': restaurant_data['name'],
                'location': restaurant_data['location'],
                'cuisines': restaurant_data['cuisines'],
                'cost_clean': float(restaurant_data['cost_clean']),
                'rating_clean': float(restaurant_data['rating_clean']),
                'rest_type': restaurant_data['rest_type'],
                'similarity_score': float(score)
            })
        
       
        avg_similarity = float(np.mean(valid_scores))
        
       
        cuisines = [rec['cuisines'] for rec in recommendations]
        diversity_score = len(set(cuisines)) / len(cuisines) if cuisines else 0
        
       
        locations = [rec['location'] for rec in recommendations]
        coverage_score = len(set(locations)) / len(locations) if locations else 0
        
        return {
            'query_restaurant': {
                'id': int(restaurant_idx),
                'name': self.df.iloc[restaurant_idx]['name'],
                'location': self.df.iloc[restaurant_idx]['location'],
                'cuisines': self.df.iloc[restaurant_idx]['cuisines'],
                'cost_clean': float(self.df.iloc[restaurant_idx]['cost_clean']),
                'rating_clean': float(self.df.iloc[restaurant_idx]['rating_clean']),
                'rest_type': self.df.iloc[restaurant_idx]['rest_type']
            },
            'recommendations': recommendations,
            'total_recommendations': len(recommendations),
            'avg_similarity': avg_similarity,
            'diversity_score': diversity_score,
            'coverage_score': coverage_score
        }
    
    def get_analytics(self) -> Dict:
       
        if not self.is_loaded:
            return {"error": "Models not loaded"}
        
        return {
            'total_restaurants': len(self.df),
            'total_cuisines': len(self.df['cuisines'].unique()),
            'total_locations': len(self.df['location'].unique()),
            'avg_rating': float(self.df['rating_clean'].mean()),
            'avg_cost': float(self.df['cost_clean'].mean()),
            'model_performance': {
                'similarity_matrix_shape': self.similarity_matrix.shape,
                'feature_count': len(self.model_data.get('similarity_features', [])),
                'is_loaded': self.is_loaded
            }
        }


recommendation_service = RecommendationService()

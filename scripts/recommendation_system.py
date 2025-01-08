import sys
sys.path.append("scripts")
sys.path.append("utils")

from collaborative_filtering import CollaborativeFiltering
from content_based_filtering import ContentBasedFiltering
from config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD

class RecommendationSystem:
    def __init__(self):
        self.cf = CollaborativeFiltering(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD)
        self.cbf = ContentBasedFiltering(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD)

    def recommend(self, user_id):
        recommendations = self.cf.recommend_movies(user_id)
        if not recommendations:
            print("No recommendations from Collaborative Filtering. Using Content-Based Filtering...")
            recommendations = self.cbf.recommend_movies(user_id)
        return recommendations

    def close(self):
        self.cf.close()
        self.cbf.close()

if __name__ == "__main__":
    recommender = RecommendationSystem()
    try:
        user_id = input("Enter User ID: ").strip()
        recommendations = recommender.recommend(user_id)
        print("Recommendations:", recommendations)
    finally:
        recommender.close()

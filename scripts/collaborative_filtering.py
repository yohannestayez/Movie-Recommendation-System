from neo4j import GraphDatabase
import sys
sys.path.append('utils')
class CollaborativeFiltering:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def recommend_movies(self, user_id):
        query = """
        MATCH (u1:User {id: $userId})-[:RATED]->(m:Movie)
        MATCH (u2:User)-[:RATED]->(rec:Movie)
        WHERE u1 <> u2 AND NOT (u1)-[:RATED]->(rec)
        RETURN rec.title AS Recommendation, COUNT(*) AS Score
        ORDER BY Score DESC LIMIT 10;
        """
        with self.driver.session() as session:
            result = session.run(query, userId=user_id)
            return [record["Recommendation"] for record in result]

if __name__ == "__main__":
    from config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD

    cf = CollaborativeFiltering(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD)
    try:
        recommendations = cf.recommend_movies(user_id='1')
        print("Collaborative Filtering Recommendations:", recommendations)
    finally:
        cf.close()

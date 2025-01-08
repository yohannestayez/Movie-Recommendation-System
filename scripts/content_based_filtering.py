from neo4j import GraphDatabase
import sys
sys.path.append('utils')

class ContentBasedFiltering:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def recommend_movies(self, user_id):
        query = """
        MATCH (u:User {id:'32'})-[r:RATED]->(m:Movie)
        WHERE r.rating >= 4.0
        WITH u, m.genres AS userGenres 
        MATCH (k:Movie)
        WHERE ANY(g IN k.genres WHERE g IN userGenres) 
        AND NOT (u)-[:RATED]->(k) 
        RETURN k.title AS Recommendation
        ORDER BY RAND() 
        LIMIT 10;
        """

        with self.driver.session() as session:
            result = session.run(query, userId=user_id)
            return [record["Recommendation"] for record in result]
    

if __name__ == "__main__":
    from config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD

    cbf = ContentBasedFiltering(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD)
    try:
        recommendations = cbf.recommend_movies(user_id='1')
        print("Content-Based Recommendations:", recommendations)
    finally:
        cbf.close()

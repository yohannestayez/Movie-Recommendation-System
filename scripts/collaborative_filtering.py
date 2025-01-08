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
        MATCH (u1:User {id: $userId})-[x:RATED]->(m:Movie)
        WHERE x.rating >= 3.5
        WITH u1, m
        MATCH (u2:User)-[y:RATED]->(m)
        WHERE u1 <> u2 AND y.rating >= 3.5 
        WITH u1, m, COLLECT(DISTINCT u2)[..5] AS similarUsers
        UNWIND similarUsers AS u2
        MATCH (u2)-[z:RATED]->(rec:Movie)
        WHERE NOT (u1)-[:RATED]->(rec) AND z.rating >= 3.5
        WITH rec, COLLECT(DISTINCT u2) AS recommendingUsers
        WHERE SIZE(recommendingUsers) = 5
        RETURN rec.title AS Recommendation, recommendingUsers
        ORDER BY SIZE(recommendingUsers) DESC LIMIT 10;
        """
        with self.driver.session() as session:
            result = session.run(query, userId=user_id)
            return [record["Recommendation"] for record in result]
    

if __name__ == "__main__":
    from config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD

    cf = CollaborativeFiltering(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD)
    try:
        recommendations = cf.recommend_movies(user_id='49')
        print("Collaborative Filtering Recommendations:", recommendations)
    finally:
        cf.close()

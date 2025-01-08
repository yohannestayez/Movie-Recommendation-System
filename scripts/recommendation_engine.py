# File: scripts/recommendation_engine.py

from graphdatascience import GraphDataScience
from neo4j import GraphDatabase
import sys
sys.path.append('utils')
from config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD

class RecommendationEngine:
    def __init__(self, uri, username, password):
        # Initialize GDS and Neo4j driver
        self.gds = GraphDataScience(uri, auth=(username, password))
        self.driver = GraphDatabase.driver(uri, auth=(username, password))

    def collaborative_filtering_recommendations(self, user_id, top_k=5):
        """
        Generate collaborative filtering recommendations for a user.
        """
        print(f"Generating collaborative filtering recommendations for user {user_id}...")

        # Ensure the collaborative graph is loaded
        if not self.gds.graph.exists("collaborativeGraph")["exists"]:
            raise Exception("Collaborative graph is not projected. Please project it first!")

        # Run Node Similarity on collaborativeGraph
        node_similarity_result = self.gds.run_cypher(
            """
            CALL gds.nodeSimilarity.stream('collaborativeGraph', {
                nodeLabels: ['Movie'],
                relationshipTypes: ['RATED'],
                relationshipWeightProperty: 'rating'
            })
            YIELD node1, node2, similarity
            RETURN node1, node2, similarity
            """
        )

        # Print node_similarity_result for debugging
        print("Node Similarity Result:")
        print(node_similarity_result)

        # Extract results as a list of dictionaries
        similarities = [
            {"node1": row["node1"], "node2": row["node2"], "similarity": row["similarity"]}
            for _, row in node_similarity_result.iterrows()
        ]

        # Filter results for recommendations for the given user
        query = """
        MATCH (u:User {id: $user_id})-[:RATED]->(m:Movie)
        WITH collect(id(m)) AS watchedMovies
        UNWIND $similarities AS similarity
        WITH similarity, watchedMovies
        WHERE NOT similarity.node2 IN watchedMovies
        RETURN similarity.node2 AS recommendedMovie, similarity.similarity AS score
        ORDER BY score DESC
        LIMIT $top_k
        """
        with self.driver.session() as session:
            recommendations = session.run(query, {"user_id": user_id, "similarities": similarities, "top_k": top_k}).data()

        return recommendations



    def content_based_recommendations(self, movie_id, top_k=5):
        """
        Recommend similar movies based on genres.
        """
        print(f"Generating content-based recommendations for movie {movie_id}...")

        # Ensure the content graph is loaded
        if not self.gds.graph.exists("contentGraph")["exists"]:
            raise Exception("Content-based graph is not projected. Please project it first!")

        # Run Node Similarity on contentGraph
        node_similarity_result = self.gds.run_cypher(
            """
            CALL gds.nodeSimilarity.stream('contentGraph', {
                nodeLabels: ['Movie'],
                relationshipTypes: ['SIMILAR'],
                similarityMetric: 'JACCARD'
            })
            YIELD node1, node2, similarity
            RETURN node1, node2, similarity
            """
        )

        # Print node_similarity_result for debugging
        print("Node Similarity Result:")
        print(node_similarity_result)

        # Extract results as a list of dictionaries
        similarities = [
            {"node1": row["node1"], "node2": row["node2"], "similarity": row["similarity"]}
            for _, row in node_similarity_result.iterrows()
        ]

        # Filter results for similar movies to the given movie
        query = """
        UNWIND $similarities AS similarity
        WITH similarity
        WHERE similarity.node1 = $movie_id
        RETURN similarity.node2 AS similarMovie, similarity.similarity AS score
        ORDER BY score DESC
        LIMIT $top_k
        """
        with self.driver.session() as session:
            recommendations = session.run(query, {"movie_id": movie_id, "similarities": similarities, "top_k": top_k}).data()

        return recommendations


if __name__ == "__main__":
    # Initialize the recommendation engine
    engine = RecommendationEngine(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD)

    try:
        # Collaborative Filtering Example
        user_id = "1"  # Replace with an actual user ID
        collaborative_recommendations = engine.collaborative_filtering_recommendations(user_id)
        print("Collaborative Filtering Recommendations:")
        for rec in collaborative_recommendations:
            print(f"Movie ID: {rec['recommendedMovie']}, Score: {rec['score']}")

        # Content-Based Filtering Example
        movie_id = "1"  # Replace with an actual movie ID
        content_recommendations = engine.content_based_recommendations(movie_id)
        print("\nContent-Based Recommendations:")
        for rec in content_recommendations:
            print(f"Movie ID: {rec['similarMovie']}, Score: {rec['score']}")

    finally:
        engine.driver.close()
        print("\nRecommendation engine process completed!")

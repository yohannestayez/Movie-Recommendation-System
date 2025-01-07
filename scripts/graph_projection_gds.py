from graphdatascience import GraphDataScience
from neo4j import GraphDatabase
import sys
sys.path.append('utils')
from config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD

class GDSProjection:
    def __init__(self, uri, username, password):
        # Initialize GDS and Neo4j driver
        self.gds = GraphDataScience(uri, auth=(username, password))
        self.driver = GraphDatabase.driver(uri, auth=(username, password))

    def relationship_exists(self, relationship_type):
        """
        Checks if a specific relationship type exists in the database.
        """
        query = f"""
        MATCH ()-[r:{relationship_type}]-()
        RETURN COUNT(r) > 0 AS exists
        """
        with self.driver.session() as session:
            result = session.run(query).single()
        return result["exists"]

    def graph_exists(self, graph_name):
        """
        Checks if a graph projection already exists in GDS.
        """
        return graph_name in self.gds.graph.list()["graphName"].values

    def create_genre_similarity_relationships(self, batch_size=25):
        """
        Creates the SIMILAR relationships between movies based on genre overlap in batches.
        Skips execution if the relationships already exist.
        """
        if self.relationship_exists("SIMILAR"):
            print("SIMILAR relationships already exist. Skipping creation.")
            return

        query = """
        MATCH (m1:Movie)
        WITH m1
        LIMIT $batch_size
        MATCH (m2:Movie)
        WHERE id(m1) < id(m2)
        WITH m1, m2, apoc.coll.intersection(m1.genres, m2.genres) AS sharedGenres
        WHERE size(sharedGenres) > 0
        MERGE (m1)-[r:SIMILAR]->(m2)
        SET r.similarity = size(sharedGenres) * 1.0 / size(apoc.coll.union(m1.genres, m2.genres))
        """
        while True:
            with self.driver.session() as session:
                result = session.run(query, batch_size=batch_size)
                if not result._summary().counters.contains_updates():
                    break
        print("Genre-based SIMILAR relationships created!")

    def project_collaborative_graph(self):
        """
        Projects the collaborative graph into the GDS workspace.
        Skips execution if the graph is already projected.
        """
        graph_name = "collaborativeGraph"
        if self.graph_exists(graph_name):
            print(f"Collaborative graph '{graph_name}' already exists. Skipping projection.")
            return

        self.gds.graph.project(
            graph_name,
            ["User", "Movie"],
            {
                "RATED": {
                    "properties": ["rating"]
                }
            }
        )
        print("Collaborative graph projected!")

    def project_content_graph(self):
        """
        Projects the content-based graph into the GDS workspace.
        Skips execution if the graph is already projected.
        """
        graph_name = "contentGraph"
        if self.graph_exists(graph_name):
            print(f"Content-based graph '{graph_name}' already exists. Skipping projection.")
            return

        self.gds.graph.project(
            graph_name,
            ["Movie"],
            {
                "SIMILAR": {
                    "properties": ["similarity"]
                }
            }
        )
        print("Content-based graph projected!")

if __name__ == "__main__":
    # Initialize the GDSProjection class
    gds_projection = GDSProjection(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD)

    # Step 1: Create SIMILAR relationships
    gds_projection.create_genre_similarity_relationships()

    # Step 2: Project the collaborative graph
    gds_projection.project_collaborative_graph()

    # Step 3: Project the content-based graph
    gds_projection.project_content_graph()

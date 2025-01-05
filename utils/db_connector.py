from neo4j import GraphDatabase

class Neo4jConnector:
    def __init__(self, uri, username, password):
        self.driver = GraphDatabase.driver(uri, auth=(username, password))

    def query(self, cypher_query):
        with self.driver.session() as session:
            session.run(cypher_query)

    def close(self):
        self.driver.close()

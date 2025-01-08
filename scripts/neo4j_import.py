
import sys
sys.path.append('utils')

from db_connector import Neo4jConnector
from config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD


def load_movies(connector):
    """
    Load movies into Neo4j as Movie nodes.
    """ 
    query = """
    LOAD CSV WITH HEADERS FROM 'file:///movies_cleaned.csv' AS row
    MERGE (m:Movie {id: row.id})
    SET m.title = row.title,
        m.genres = apoc.convert.fromJsonList(row.genres), 
        m.release_year = toInteger(row.release_year),
        m.popularity = toFloat(row.popularity),
        m.vote_average = toFloat(row.vote_average),
        m.vote_count = toInteger(row.vote_count);
    """
    connector.query(query)
    print("Movies data loaded into Neo4j.")

def load_users_and_ratings(connector):
    """
    Load users and RATED relationships into Neo4j.
    """
    query = """
    LOAD CSV WITH HEADERS FROM 'file:///ratings_cleaned.csv' AS row
    MERGE (u:User {id: row.userId})
    WITH u, row
    MATCH (m:Movie {id: row.movieId})
    CREATE (u)-[:RATED {rating: toFloat(row.rating)}]->(m);
    """
    connector.query(query)
    print("Ratings data and user nodes loaded into Neo4j.")

def main():
    # Initialize Neo4j connection
    connector = Neo4jConnector(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD)
    try:
        # Load data into Neo4j
        load_movies(connector)
        load_users_and_ratings(connector)
    finally:
        connector.close()
        print("Connection to Neo4j closed.")

if __name__ == "__main__":
    main()

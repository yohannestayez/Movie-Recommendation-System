# **Movie Recommendation System**
## **Overview**
This repository contains the implementation of a Movie Recommendation System built using Python and Neo4j. The system is designed to process raw movie and ratings data, store it in a graph database, and prepare the foundation for advanced recommendation algorithms.
This project sets up a Neo4j graph database to store movie and user data. The data is cleaned, preprocessed, and imported into the database as nodes and relationships, enabling the development of recommendation algorithms. Recommendation algorithms include collaborative filtering and content based filtering mechanisms using cypher.  

Key Features:  
- **Movie Data:** Stored as `Movie` nodes with properties such as title, genres, release year, popularity, and ratings.  
- **User Data:** Stored as `User` nodes with unique user IDs.  
- **Ratings Data:** Modeled as `RATED` relationships between users and movies, including the rating as a property.

---

## **Project Folder Structure**

```
.
├── .env                 # Environment variables 
├── .gitignore            
├── README.md             # Project description, instructions, and usage information
├── notebooks             # Contains Jupyter Notebooks for data exploration and analysis
│   ├── _init_.py         
│   └── data_preprocessing.ipynb  # Notebook for data cleaning and preparation
├── scripts             
│   ├── _init_.py         
│   ├── collaborative_filtering.py  # Script for collaborative filtering recommendations
│   ├── content_based_filtering.py  # Script for content-based filtering recommendations
│   ├── data_preprocessing.py  # Script for data preprocessing (alternative to the notebook)
│   ├── neo4j_import.py   # Script to import data into a Neo4j database
│   └── recommendation_system.py  # Main script for the recommendation system
├── utils                # Contains utility functions and classes
│   ├── _init_.py         
│   ├── config.py        # Configuration settings for the project
│   └── db_connector.py  # Class for connecting to the database
└── requirements.txt      
```

## **Setup Instructions**

### **1. Prerequisites**

- **Neo4j Database**  
  Install and run the Neo4j database. Download it from [Neo4j Downloads](https://neo4j.com/download/). Ensure the database is accessible at `bolt://localhost:7687`, or update the `NEO4J_URI` in `config.py`.  

- **Python Environment**  
  Install Python 3.8 or later and set up a virtual environment:  

### **2. Install Dependencies**

Install required Python libraries:  
```bash
pip install -r requirements.txt
```

### **3. Configure Environment**

Create a `.env` file in the root directory to store Neo4j credentials:  

## **Key Components**

### **1. Data Preprocessing**

- **Files:** `notebooks/data_preprocessing.ipynb`  and `scripts/data_preprocessing.py`
  - Processes raw data (`movies.csv` and `ratings.csv`) to generate cleaned datasets.
  - Contains data visualization to better uderstand the data.  
  - Operations include:
    - Parsing nested JSON fields.
    - Dropping unnecessary columns.
    - Handling missing or invalid values.  

### **2. Neo4j Data Import**

- **File:** `scripts/neo4j_import.py`  
  - Loads the cleaned data into the Neo4j database.  
  - Creates:
    - `Movie` nodes with properties like title, genres, release year, and popularity.  
    - `User` nodes based on unique user IDs.  
    - `RATED` relationships between users and movies with the rating as a property.  

### **3. Configurations**

- **File:** `utils/config.py`  
  - Stores database credentials:  
    ```python
    NEO4J_URI = "bolt://localhost:7687"
    NEO4J_USERNAME = "neo4j"
    NEO4J_PASSWORD = "your_password"
    ```

### **4. Neo4j Connector**

- **File:** `utils/db_connector.py`  
  - Provides a utility class to connect to Neo4j and execute queries.  

### **5. Collaborative Filtering**
- **File:** `scripts/collaborative_filtering.py`  
  - It connects to a Neo4j database and uses Cypher queries to find users with similar movie preferences.
  - It recommends movies to a given user based on the ratings of these similar users.

### **6. Contnet based Filtering**
- **File:** `scripts/content_based_filtering.py`
  - It connects to a Neo4j database and uses Cypher queries.
  - It finds movies with genres similar to those a user has rated highly (above a 4.0 rating).
  - It recommends these unrated movies to the user.

### **7. Recommendation system**
- **File:** `scripts/recommendation_system.py`
  - It uses two classes: CollaborativeFiltering and ContentBasedFiltering.
  - The RecommendationSystem class manages both methods.
  - It prioritizes collaborative filtering and falls back to content-based filtering if no recommendations are found.

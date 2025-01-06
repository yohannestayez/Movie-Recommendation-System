# **Movie Recommendation System**
## **Overview**
This repository contains the implementation of a Movie Recommendation System built using Python and Neo4j. The system is designed to process raw movie and ratings data, store it in a graph database, and prepare the foundation for advanced recommendation algorithms.
This project sets up a Neo4j graph database to store movie and user data. The data is cleaned, preprocessed, and imported into the database as nodes and relationships, enabling the development of recommendation algorithms.  

Key Features:  
- **Movie Data:** Stored as `Movie` nodes with properties such as title, genres, release year, popularity, and ratings.  
- **User Data:** Stored as `User` nodes with unique user IDs.  
- **Ratings Data:** Modeled as `RATED` relationships between users and movies, including the rating as a property.

---

## **Project Folder Structure**

```
notebooks/
├── __init__.py
├── data_preprocessing.ipynb     # Jupyter notebook for data cleaning and preparation
scripts/
├── __init__.py
├── data_preprocessing.py        # Python script for data preprocessing
├── neo4j_import.py              # Script to load data into Neo4j database
utils/
├── __init__.py
├── config.py                    # Configuration file for database credentials
├── db_connector.py              # Utility class for Neo4j connection and queries
.env                              # Environment file for storing sensitive credentials
.gitignore                        # List of files and folders to exclude from version control
README.md                         # Project documentation (this file)
requirements.txt                  # Python dependencies
```

## **Setup Instructions**

### **1. Prerequisites**

- **Neo4j Database**  
  Install and run the Neo4j database. Download it from [Neo4j Downloads](https://neo4j.com/download/). Ensure the database is accessible at `bolt://localhost:7687`, or update the `NEO4J_URI` in `config.py`.  

- **Python Environment**  
  Install Python 3.8 or later and set up a virtual environment:  
  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  ```

### **2. Install Dependencies**

Install required Python libraries:  
```bash
pip install -r requirements.txt
```

### **3. Configure Environment**

Create a `.env` file in the root directory to store Neo4j credentials:  
```
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password
```


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

---

## **Next Steps**

- Implement recommendation algorithms:  
  - Collaborative Filtering.  
  - Content-Based Filtering.  
- Add advanced filtering and fallback mechanisms to improve recommendations.  

---

## **Author**

Developed by Yohannes Taye.
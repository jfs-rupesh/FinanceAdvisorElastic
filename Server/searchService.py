from flask import Flask, request, jsonify
from flask_cors import CORS
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
import logging

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Connect to Elasticsearch
es = Elasticsearch(
    'https://localhost:9200', 
    basic_auth=('elastic', '=EeqNe8wd0tU+P8NoVTR'), 
    verify_certs=False
)

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

@app.route("/search", methods=["POST"])
def search():
    try:
        # Parse incoming data
        data = request.json
        query = data.get("query", "")
        filters = data.get("filters", {})

        logging.debug(f"Received query: {query}")
        logging.debug(f"Received filters: {filters}")

        # Generate embedding for the query
        query_vector = model.encode(query).tolist()
        logging.debug(f"Query vector: {query_vector}")

        # Build Elasticsearch query
        # search_query = {
        #     "script_score": {
        #         "query": {"bool": {"filter": []}},
        #         "script": {
        #             "source": "cosineSimilarity(params.query_vector, 'content_vector') + 1.0",
        #             "params": {"query_vector": query_vector}
        #         }
        #     }
        # }
        search_query = {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'content_vector') + 1.0",
                    "params": {"query_vector": query_vector}
                }
            }
            }
        logging.debug(f"Final search query: {search_query}")
        response = es.search(index="investment_advisor", body={"query": search_query, "size": 10})
        logging.debug(f"Elasticsearch response: {response}")


        # Apply filters
        # for key, value in filters.items():
        #     search_query["script_score"]["query"]["bool"]["filter"].append({"term": {key: value}})
        
        # logging.debug(f"Constructed Elasticsearch query: {search_query}")

        # Execute search
        #response = es.search(index="investment_advisor", body={"query": search_query, "size": 10})
        logging.debug(f"Elasticsearch response: {response}")

        # Parse results
        results = [
            {
                "name": hit["_source"]["name"], 
                "description": hit["_source"]["description"], 
                "score": hit["_score"]
            } 
            for hit in response["hits"]["hits"]
        ]

        logging.debug(f"Search results: {results}")
        return jsonify(results)

    except Exception as e:
        logging.error(f"Error during search: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

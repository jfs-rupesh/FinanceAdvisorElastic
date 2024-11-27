from elasticsearch import Elasticsearch, helpers
import json

from elasticsearch.helpers import BulkIndexError

# Elasticsearch connection
es = Elasticsearch(
    'https://localhost:9200', 
    basic_auth=('elastic', '=EeqNe8wd0tU+P8NoVTR'), 
    verify_certs=False
)
# Define the index name
INDEX_NAME = "investment_advisor"

# Define the index mapping
def create_index():
    mapping = {
        "mappings": {
            "properties": {
                "investment_type": {"type": "keyword"},
                "name": {"type": "text"},
                "symbol": {"type": "keyword"},
                "sector": {"type": "text"},
                "industry": {"type": "text"},
                "risk_level": {"type": "keyword"},
                "timeframe": {"type": "keyword"},
                "description": {"type": "text"},
                "content_vector": {"type": "dense_vector", "dims": 384},
                "market_capitalization": {"type": "float"},
                "pe_ratio": {"type": "float"},
                "price_to_book_ratio": {"type": "float"},
                "analyst_target_price": {"type": "float"},
                "beta": {"type": "float"},
                "52_week_high": {"type": "float"},
                "52_week_low": {"type": "float"},
                "currency": {"type": "keyword"},
                "exchange": {"type": "keyword"},
            }
        }
    }

    # Delete the index if it already exists
    if es.indices.exists(index=INDEX_NAME):
        es.indices.delete(index=INDEX_NAME)

    # Create the index
    es.indices.create(index=INDEX_NAME, body=mapping)
    print(f"Index '{INDEX_NAME}' created with mapping.")

# Bulk insert documents into Elasticsearch
def bulk_insert_documents(documents):
    actions = [
        {
            "_index": INDEX_NAME,
            "_source": doc,
        }
        for doc in documents
    ]

    try:
        helpers.bulk(es, actions)
    except BulkIndexError as e:
        print("Bulk Indexing Error Details:")
        for error in e.errors:
            print(error)
    print(f"Inserted {len(documents)} documents into the index '{INDEX_NAME}'.")

# Main script
if __name__ == "__main__":
    # Step 1: Create the index with mapping
    create_index()

    # Step 2: Load the sample JSON file
    with open("investment_data.json", "r") as f:
        documents = json.load(f)

    # Step 3: Insert documents into Elasticsearch
    bulk_insert_documents(documents)

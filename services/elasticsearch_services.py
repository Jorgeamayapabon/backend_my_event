from sqlalchemy.orm import Session
from elasticsearch import Elasticsearch
from models.category import CategoryModel
from models.event import EventModel
from models.location import CityModel

# Initialize the Elasticsearch client
es_client = Elasticsearch(
    hosts=["https://localhost:9200"], 
    basic_auth=("elastic", "pass"), 
    verify_certs=False
)

# Index name in Elasticsearch for events
index_name = "event"

def index_event_with_relations(event: EventModel, db: Session):
    """
    Indexes an event along with its related category and location into Elasticsearch.

    This function retrieves the category and location associated with the event 
    from the database and stores them alongside the event in Elasticsearch.

    Args:
        event (EventModel): The event to be indexed.
        db (Session): The SQLAlchemy database session.
    """
    # Fetch the associated category and location
    category = db.query(CategoryModel).filter(CategoryModel.id == event.category_id).first()
    location = db.query(CityModel).filter(CityModel.id == event.location_id).first()

    # Prepare the document to be indexed in Elasticsearch
    doc = {
        "name": event.name,
        "description": event.description,
        "date": event.date.isoformat(),  # Convert datetime to ISO format
        "capacity": event.capacity,
        "status": event.status.name,  # Using enum name for status
        "location_id": event.location_id,
        "location_name": location.name if location else None,  # Handle case where location might not exist
        "category_id": event.category_id,
        "category_name": category.name if category else None,  # Handle case where category might not exist
        "owner_id": event.owner_id
    }
    # Index the event document into Elasticsearch
    es_client.index(index=index_name, id=event.id, body=doc)


def search_events(query: str, filters: dict):
    """
    Searches for events in Elasticsearch based on the provided query and filters.

    This function uses a boolean query to search for events by name or description 
    and applies the given filters (e.g., category, location) to narrow the results.

    Args:
        query (str): The search query (for event name or description).
        filters (dict): A dictionary of filter terms (e.g., category_id, location_id).

    Returns:
        list: A list of events that match the search query and filters.
    """
    # Build the query body for Elasticsearch
    query_body = {
        "query": {
            "bool": {
                "must": [
                    {"multi_match": {"query": query, "fields": ["name", "description"]}}  # Search in name and description fields
                ],
                "filter": [{"term": {key: value}} for key, value in filters.items()]  # Apply filters
            }
        }
    }
    # Perform the search in Elasticsearch and return the results
    response = es_client.search(index=index_name, body=query_body)
    return [hit["_source"] for hit in response["hits"]["hits"]]  # Extract the document data from hits

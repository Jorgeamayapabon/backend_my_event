from sqlalchemy.orm import Session
from elasticsearch import Elasticsearch

from models.category import CategoryModel
from models.event import EventModel
from models.location import CityModel


es_client = Elasticsearch(hosts=["https://localhost:9200"], basic_auth=("elastic", "pass"), verify_certs=False)
index_name = "event"

def index_event_with_relations(event: EventModel, db: Session):
    category = db.query(CategoryModel).filter(CategoryModel.id == event.category_id).first()
    location = db.query(CityModel).filter(CityModel.id == event.location_id).first()

    doc = {
        "name": event.name,
        "description": event.description,
        "date": event.date.isoformat(),
        "capacity": event.capacity,
        "status": event.status.name,
        "location_id": event.location_id,
        "location_name": location.name if location else None,
        "category_id": event.category_id,
        "category_name": category.name if category else None,
        "owner_id": event.owner_id
    }
    es_client.index(index=index_name, id=event.id, body=doc)


def search_events(query: str, filters: dict):
    query_body = {
        "query": {
            "bool": {
                "must": [
                    {"multi_match": {"query": query, "fields": ["name", "description"]}}
                ],
                "filter": [{"term": {key: value}} for key, value in filters.items()]
            }
        }
    }
    response = es_client.search(index=index_name, body=query_body)
    return [hit["_source"] for hit in response["hits"]["hits"]]

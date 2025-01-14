from sqlalchemy.orm import Session

from models.category import CategoryModel


class CategoryServiceHandler:
    def __init__(self, db: Session):
        self.db = db
        
    def list_categories(self):
        return self.db.query(CategoryModel).all()
    
    def create_category(self, category):
        db_category = CategoryModel(**category.dict())
        self.db.add(db_category)
        self.db.commit()
        self.db.refresh(db_category)
        return db_category

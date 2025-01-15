from sqlalchemy.orm import Session
from models.category import CategoryModel


class CategoryServiceHandler:
    """
    A handler for category-related services.

    This class provides methods to interact with the database for category operations
    such as listing categories and creating new categories.

    Attributes:
        db (Session): The SQLAlchemy session used for database operations.
    """
    
    def __init__(self, db: Session):
        """
        Initializes the CategoryServiceHandler with the given database session.

        Args:
            db (Session): The SQLAlchemy session used to interact with the database.
        """
        self.db = db
        
    def list_categories(self):
        """
        Retrieves a list of all categories from the database.

        Returns:
            list: A list of CategoryModel instances representing all categories.
        """
        return self.db.query(CategoryModel).all()
    
    def create_category(self, category):
        """
        Creates a new category in the database.

        Args:
            category (CategoryCreate): A Pydantic model representing the category to be created.

        Returns:
            CategoryModel: The newly created category instance, including the generated ID and other fields.
        """
        db_category = CategoryModel(**category.dict())
        self.db.add(db_category)
        self.db.commit()
        self.db.refresh(db_category)
        return db_category

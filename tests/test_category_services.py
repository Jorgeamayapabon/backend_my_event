import pytest
from unittest.mock import MagicMock
from models.category import CategoryModel
from schemas.category import CategoryCreate
from services.category_services import CategoryServiceHandler  # Ajusta la ruta según tu proyecto

# Configuración de la base de datos simulada (Session)
@pytest.fixture
def mock_db():
    # Crea un mock de la sesión de SQLAlchemy
    db = MagicMock()
    return db

@pytest.fixture
def category_service(mock_db):
    return CategoryServiceHandler(db=mock_db)

# Test para 'list_categories'
def test_list_categories(category_service, mock_db):
    # Simulamos el retorno de la consulta
    mock_categories = [CategoryModel(id=1, name="Category 1"), CategoryModel(id=2, name="Category 2")]
    mock_db.query.return_value.all.return_value = mock_categories
    
    # Llamamos al método
    categories = category_service.list_categories()

    # Verificamos que la función 'query' y 'all' hayan sido llamadas correctamente
    mock_db.query.assert_called_once_with(CategoryModel)
    mock_db.query.return_value.all.assert_called_once()

    # Comprobamos que el resultado sea el esperado
    assert categories == mock_categories

# Test para 'create_category'
def test_create_category(category_service, mock_db):
    # Datos de entrada simulados (usualmente vienen de un modelo Pydantic)
    category_data = {"name": "New Category"}
    
    # Simulamos el comportamiento de la creación de la categoría
    db_category = CategoryModel(id=1, **category_data)
    mock_db.add.return_value = None  # El 'add' no devuelve nada
    mock_db.commit.return_value = None  # El 'commit' no devuelve nada
    mock_db.refresh.return_value = None  # El 'refresh' no devuelve nada
    
    # Simulamos que el modelo de la base de datos se asigna al objeto creado
    mock_db.add.return_value = db_category

    
    category_schema = CategoryCreate(**category_data)
    # Llamamos al método
    created_category = category_service.create_category(category_schema)

    # Comprobamos que la categoría creada es la que esperábamos
    assert created_category.name == "New Category"

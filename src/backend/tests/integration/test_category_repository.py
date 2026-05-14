import pytest
from participium.models.category import Category
from participium.repositories.category_repository import CategoryRepository

pytestmark = pytest.mark.integration

@pytest.fixture
def repository(db_session):
    return CategoryRepository(db_session)

# Test add():
# - aggiunta di una categoria
# - categoria trovata correttamente tramite id
# - categoria non trovata tramite id
# - categoria trovata correttamente tramite nome
# - categoria non trovata tramite nome

def test_add_category(db_session, repository):
   
    new_category = Category(name="Public Lighting", is_active=True)

    
    added_category = repository.add(new_category)
    db_session.commit()

    
    assert added_category.id is not None 
    assert added_category.name == "Public Lighting"
    assert added_category.is_active is True

    db_category = db_session.get(Category, added_category.id)
    assert db_category is not None
    assert db_category.name == "Public Lighting"


# Test get_by_id()

def test_get_by_id_found(db_session, repository):
   
    category = Category(name="Sewerage", is_active=True)
    db_session.add(category)
    db_session.commit()
    
    
    result = repository.get_by_id(category.id)

    
    assert result is not None
    assert result.id == category.id
    assert result.name == "Sewerage"

def test_get_by_id_not_found(repository): 
    
    result = repository.get_by_id(999) 
    
    
    assert result is None


# Test get_by_name()

def test_get_by_name_found(db_session, repository):
   
    category = Category(name="Roads and Urban Furniture", is_active=False)
    db_session.add(category)
    db_session.commit()
    
    
    result = repository.get_by_name("Roads and Urban Furniture")

    
    assert result is not None
    assert result.name == "Roads and Urban Furniture"
    assert result.is_active is False

def test_get_by_name_not_found(repository):
    
    result = repository.get_by_name("Categoria Inesistente")

    
    assert result is None


# Test list_all():
# - lista vuota quando non ci sono categorie
# - categorie in ordine alfabetico
# - solo categorie attive in ordine alfabetico

def test_list_all_returns_empty_when_no_categories(repository):
    
    results = repository.list_all()

    
    assert results == []

def test_list_all_returns_all_ordered_by_name(db_session, repository):
   
    db_session.add_all([
        Category(name="Waste", is_active=False),
        Category(name="Architectural Barriers", is_active=True),
        Category(name="Public Green Areas and Playgrounds", is_active=True)
    ])
    db_session.commit()
    
    
    results = repository.list_all(active_only=False)

    
    assert len(results) == 3
    assert results[0].name == "Architectural Barriers"
    assert results[1].name == "Public Green Areas and Playgrounds"
    assert results[2].name == "Waste"


def test_list_all_returns_only_active_ordered_by_name(db_session, repository):
   
    db_session.add_all([
        Category(name="Inactive", is_active=False), 
        Category(name="Waste", is_active=True),     
        Category(name="Other", is_active=True)
    ])
    db_session.commit()
    
    
    results = repository.list_all(active_only=True)

    
    assert len(results) == 2
    assert results[0].name == "Other"
    assert results[1].name == "Waste"
import pytest
from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.utils.pagination import paginate


# Create test DB model
Base = declarative_base()
class TestItem(Base):
    __tablename__ = "test_items"
    id = Column(Integer, primary_key=True, index=True)

# Create test database fixture

@pytest.fixture(scope="module")
def db():
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    # Insert 50 test records
    for i in range(50):
        session.add(TestItem())
    session.commit()
    yield session
    session.close()

# Test normal pagination

def test_paginate_first_page(db):
    query = db.query(TestItem)
    result = paginate(query, page=1, limit=10)
    assert result["page"] == 1
    assert result["limit"] == 10
    assert result["total"] == 50
    assert result["pages"] == 5
    assert len(result["items"]) == 10

# Test second page

def test_paginate_second_page(db):
    query = db.query(TestItem)
    result = paginate(query, page=2, limit=10)
    assert result["page"] == 2
    assert len(result["items"]) == 10

# Test page less than 1

def test_paginate_invalid_page(db):
    query = db.query(TestItem)
    result = paginate(query, page=0, limit=10)
    assert result["page"] == 1

# Test limit less than 1

def test_paginate_invalid_limit(db):
    query = db.query(TestItem)
    result = paginate(query, page=1, limit=0)
    assert result["limit"] == 10

# Test limit greater than 100

def test_paginate_limit_exceeds_max(db):
    query = db.query(TestItem)
    result = paginate(query, page=1, limit=200)
    assert result["limit"] == 100

# Test last page

def test_paginate_last_page(db):
    query = db.query(TestItem)
    result = paginate(query, page=5, limit=10)
    assert len(result["items"]) == 10
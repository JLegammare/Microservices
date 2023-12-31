import pytest
from src.api.persistence.db import db
from src import create_app
from unittest.mock import Mock
from src.api.persistence.category_dao_impl import CategoryDaoImpl

@pytest.fixture(scope="module")
def test_client():
    app = create_app()
    app.config["TESTING"] = True
    with app.app_context():
        yield app.test_client()


@pytest.fixture(scope="function")
def test_category_dao():
    from src.api.persistence.category_dao_impl import CategoryDaoImpl

    db_mock = Mock()
    db_session = Mock()
    db_commit = Mock()
    db_add = Mock()
    db_session.commit = db_commit
    db_session.add = db_add
    db_mock.session = db_session
    dao = CategoryDaoImpl(db_mock)
    yield dao, db_mock


@pytest.fixture(scope="module")
def test_category_service():
    from src.api.services.category_service_impl import CategoryServiceImpl

    category_dao_mock = Mock(spec=CategoryDaoImpl)
    service = CategoryServiceImpl(category_dao_mock)
    yield service, category_dao_mock


@pytest.fixture(scope="function")
def test_database():
    from src.api.models.categories import Category
    db.drop_all()
    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()

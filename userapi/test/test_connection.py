"""Connection tests — verify DB connectivity and schema."""
import pytest
from sqlalchemy import inspect, text
from userapi.src import db as _db
from userapi.src.models import User


class TestDatabaseConnection:
    def test_database_is_reachable(self, app, db):
        with app.app_context():
            result = db.session.execute(text("SELECT 1")).scalar()
            assert result == 1

    def test_users_table_exists(self, app, db):
        with app.app_context():
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            assert "users" in tables

    def test_users_table_has_correct_columns(self, app, db):
        with app.app_context():
            inspector = inspect(db.engine)
            columns = {c["name"] for c in inspector.get_columns("users")}
            assert {"id", "username", "email", "firstname", "lastname", "created_at"}.issubset(columns)

    def test_can_insert_and_retrieve_user(self, app, db):
        with app.app_context():
            user = User(username="conn_test", email="conn@test.com")
            db.session.add(user)
            db.session.commit()

            fetched = User.query.filter_by(username="conn_test").first()
            assert fetched is not None
            assert fetched.email == "conn@test.com"

    def test_can_delete_user(self, app, db):
        with app.app_context():
            user = User(username="del_conn", email="del_conn@test.com")
            db.session.add(user)
            db.session.commit()

            db.session.delete(user)
            db.session.commit()

            gone = User.query.filter_by(username="del_conn").first()
            assert gone is None

    def test_session_rollback_on_error(self, app, db):
        with app.app_context():
            user = User(username="rollback_test", email="rb@test.com")
            db.session.add(user)
            db.session.flush()

            db.session.rollback()

            not_there = User.query.filter_by(username="rollback_test").first()
            assert not_there is None

    def test_unique_constraint_username(self, app, db):
        with app.app_context():
            u1 = User(username="unique_user", email="u1@test.com")
            u2 = User(username="unique_user", email="u2@test.com")
            db.session.add(u1)
            db.session.commit()

            db.session.add(u2)
            with pytest.raises(Exception):
                db.session.commit()
            db.session.rollback()

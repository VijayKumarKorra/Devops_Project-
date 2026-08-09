"""API (functional) tests — full HTTP request/response cycle."""
import json
import pytest


def post_user(client, data):
    return client.post("/users", data=json.dumps(data),
                       content_type="application/json")


class TestHealthEndpoint:
    def test_health_returns_200(self, client):
        r = client.get("/health")
        assert r.status_code == 200

    def test_health_body_has_status(self, client):
        r = client.get("/health")
        body = r.get_json()
        assert "status" in body
        assert body["status"] == "ok"

    def test_root_endpoint(self, client):
        r = client.get("/")
        assert r.status_code == 200
        assert b"UserAPI" in r.data

    def test_api_info_endpoint(self, client):
        r = client.get("/api")
        assert r.status_code == 200
        assert r.get_json()["message"] == "UserAPI v1.0"


class TestCreateUser:
    def test_create_user_success(self, client):
        r = post_user(client, {"username": "alice", "email": "alice@example.com"})
        assert r.status_code == 201
        body = r.get_json()
        assert body["username"] == "alice"
        assert body["id"] is not None

    def test_create_user_with_all_fields(self, client):
        r = post_user(client, {
            "username": "bob",
            "email": "bob@example.com",
            "firstname": "Bob",
            "lastname": "Smith",
        })
        assert r.status_code == 201
        body = r.get_json()
        assert body["firstname"] == "Bob"
        assert body["lastname"] == "Smith"

    def test_create_user_missing_username(self, client):
        r = post_user(client, {"email": "x@x.com"})
        assert r.status_code == 422

    def test_create_user_missing_email(self, client):
        r = post_user(client, {"username": "nomail"})
        assert r.status_code == 422

    def test_create_user_invalid_email(self, client):
        r = post_user(client, {"username": "bad", "email": "notvalid"})
        assert r.status_code == 422

    def test_create_duplicate_username(self, client):
        post_user(client, {"username": "dup", "email": "dup@a.com"})
        r = post_user(client, {"username": "dup", "email": "other@a.com"})
        assert r.status_code == 409

    def test_create_duplicate_email(self, client):
        post_user(client, {"username": "user1", "email": "same@a.com"})
        r = post_user(client, {"username": "user2", "email": "same@a.com"})
        assert r.status_code == 409

    def test_create_user_no_body(self, client):
        r = client.post("/users", content_type="application/json")
        assert r.status_code == 400


class TestGetUsers:
    def test_get_all_users_empty(self, client):
        r = client.get("/users")
        assert r.status_code == 200
        assert r.get_json() == []

    def test_get_all_users_returns_list(self, client):
        post_user(client, {"username": "a", "email": "a@a.com"})
        post_user(client, {"username": "b", "email": "b@b.com"})
        r = client.get("/users")
        assert r.status_code == 200
        assert len(r.get_json()) == 2

    def test_get_user_by_id(self, client):
        created = post_user(client, {"username": "fetch", "email": "fetch@a.com"}).get_json()
        r = client.get(f"/users/{created['id']}")
        assert r.status_code == 200
        assert r.get_json()["username"] == "fetch"

    def test_get_user_not_found(self, client):
        r = client.get("/users/99999")
        assert r.status_code == 404


class TestUpdateUser:
    def test_update_user_name(self, client):
        user = post_user(client, {"username": "old", "email": "old@a.com"}).get_json()
        r = client.put(f"/users/{user['id']}",
                       data=json.dumps({"username": "new"}),
                       content_type="application/json")
        assert r.status_code == 200
        assert r.get_json()["username"] == "new"

    def test_update_user_not_found(self, client):
        r = client.put("/users/99999",
                       data=json.dumps({"firstname": "X"}),
                       content_type="application/json")
        assert r.status_code == 404

    def test_update_user_duplicate_username(self, client):
        post_user(client, {"username": "taken", "email": "t@a.com"})
        user = post_user(client, {"username": "free", "email": "f@a.com"}).get_json()
        r = client.put(f"/users/{user['id']}",
                       data=json.dumps({"username": "taken"}),
                       content_type="application/json")
        assert r.status_code == 409


class TestDeleteUser:
    def test_delete_user(self, client):
        user = post_user(client, {"username": "del", "email": "del@a.com"}).get_json()
        r = client.delete(f"/users/{user['id']}")
        assert r.status_code == 200
        assert client.get(f"/users/{user['id']}").status_code == 404

    def test_delete_user_not_found(self, client):
        r = client.delete("/users/99999")
        assert r.status_code == 404

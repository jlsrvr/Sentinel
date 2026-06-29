def test_list_cases_empty(client):
    response = client.get("/api/v1/cases/")
    assert response.status_code == 200
    assert response.json() == []
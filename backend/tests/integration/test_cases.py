def test_list_cases_empty(client):
    response = client.get("/api/v1/cases/")
    assert response.status_code == 200
    assert response.json() == []

def test_list_cases_returns_correct_shape(client, case_factory):
    case_factory.create(external_id="ext-123")

    response = client.get("/api/v1/cases/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["external_id"] == "ext-123"
    assert "severity" in data[0]
    assert "sla_deadline" in data[0]
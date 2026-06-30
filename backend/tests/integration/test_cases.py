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

def test_list_cases_takes_skip_and_limit_params(client, case_factory):
    case_factory.create(external_id="ext-1")
    case_factory.create(external_id="ext-2")
    case_factory.create(external_id="ext-3")
    case_factory.create(external_id="ext-4")
    case_factory.create(external_id="ext-5")
    skip = 1
    limit = 3

    response = client.get('/api/v1/cases/', params={"skip": skip, "limit": limit})

    assert response.status_code == 200
    data = response.json()
    assert len(data) == limit
    assert data[0]["external_id"] == "ext-2"
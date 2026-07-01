import uuid

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

def test_case_details_returns_correct_case(client, case_factory):
    case = case_factory.create(external_id="ext-1")

    response = client.get('/api/v1/cases/' + str(case.id))

    assert response.status_code == 200
    data = response.json()
    assert data['id'] == str(case.id)

def test_case_details_returns_404_when_no_case(client):
    response = client.get('/api/v1/cases/' + str(uuid.uuid4()))

    assert response.status_code == 404

def test_case_details_returns_correct_fields(client, case_factory):
    case = case_factory.create(external_id="ext-1")

    response = client.get('/api/v1/cases/' + str(case.id))

    assert response.status_code == 200
    data = response.json()
    assert 'id' in data
    assert 'external_id' in data
    assert 'content_type' in data
    assert 'content_ref' in data
    assert 'content_snapshot' in data
    assert 'severity' in data
    assert 'status' in data
    assert 'queue_id' in data
    assert 'assigned_to' in data
    assert 'assigned_at' in data
    assert 'sla_deadline' in data
    assert 'source' in data
    assert 'case_metadata' in data
    assert 'created_at' in data
    assert 'updated_at' in data
    assert 'resolved_at' in data
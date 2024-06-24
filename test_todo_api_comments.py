import requests
import pytest
import pandas as pd
import json

BASE_URL = "https://jsonplaceholder.typicode.com"

def read_excel_data(file_path, sheet_name):
    """
    Reads data from an Excel file and returns it as a DataFrame.

    Args:
        file_path (str): Path to the Excel file.
        sheet_name (str): Name of the sheet to read from.

    Returns:
        pd.DataFrame: DataFrame containing the data from the Excel sheet.
    """
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    return df

@pytest.fixture
def base_url():
    """
    Fixture to provide the base URL for the API.

    Returns:
        str: Base URL of the API.
    """
    return BASE_URL

@pytest.fixture(scope='module')
def excel_data():
    """
    Fixture to load Excel data once and share it among all tests.

    Returns:
        pd.DataFrame: DataFrame containing the data from the Excel sheet.
    """
    file_path = "api_test_data.xlsx"
    sheet_name = "Sheet1"
    return read_excel_data(file_path, sheet_name)

def get_expected_values(excel_data, endpoint, method):
    """
    Fetches the expected values for a given endpoint and method from the Excel data.

    Args:
        excel_data (pd.DataFrame): DataFrame containing the Excel data.
        endpoint (str): API endpoint.
        method (str): HTTP method.

    Returns:
        tuple: Expected status code, content type, and payload (if any) for the given endpoint and method.
    """
    endpoint_data = excel_data[(excel_data['endpoint'] == endpoint) & (excel_data['method'] == method)]
    expected_status_code = endpoint_data['status_code'].values[0]
    expected_content_type = endpoint_data['content_type'].values[0]
    payload = endpoint_data['payload'].values[0] if 'payload' in endpoint_data.columns else None
    return expected_status_code, expected_content_type, payload

def test_get_comments(base_url, excel_data):
    """
    Test case for the GET /comments endpoint.

    Args:
        base_url (str): Base URL of the API.
        excel_data (pd.DataFrame): DataFrame containing the Excel data.
    Underscore(_) is work in place of payload for GET request we don't have payload.
    """
    expected_status_code, expected_content_type, _ = get_expected_values(excel_data, '/comments', 'GET')
    response = requests.get(f"{base_url}/comments", timeout=10)
    assert response.status_code == expected_status_code
    assert response.headers["Content-Type"] == expected_content_type
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_single_comment(base_url, excel_data):
    """
    Test case for the GET /comments/1 endpoint.

    Args:
        base_url (str): Base URL of the API.
        excel_data (pd.DataFrame): DataFrame containing the Excel data.
    """
    comment_id = 1
    expected_status_code, expected_content_type, _ = get_expected_values(excel_data, '/comments', 'GET')
    response = requests.get(f"{base_url}/comments/{comment_id}", timeout=10)
    assert response.status_code == expected_status_code
    assert response.headers["Content-Type"] == expected_content_type
    data = response.json()
    assert isinstance(data, dict)
    assert data["id"] == comment_id
    
def test_post_comment(base_url, excel_data):
    """
    Test case for the POST /comments endpoint.

    Args:
        base_url (str): Base URL of the API.
        excel_data (pd.DataFrame): DataFrame containing the Excel data.
    """
    expected_status_code, expected_content_type, payload = get_expected_values(excel_data, '/comments', 'POST')
    payload = json.loads(payload) if payload else None
    response = requests.post(f"{base_url}/comments", json=payload, timeout=10)
    assert response.status_code == expected_status_code
    assert response.headers["Content-Type"] == expected_content_type
    data = response.json()
    assert data['name'] == payload['name']
    assert data['email'] == payload['email']
    assert data['body'] == payload['body']
    assert data['postId'] == payload['postId']

def test_put_comment(base_url, excel_data):
    """
    Test case for the PUT /comments/1 endpoint.

    Args:
        base_url (str): Base URL of the API.
        excel_data (pd.DataFrame): DataFrame containing the Excel data.
    """
    expected_status_code, expected_content_type, payload = get_expected_values(excel_data, '/comments/1', 'PUT')
    payload = json.loads(payload) if payload else None
    response = requests.put(f"{base_url}/comments/1", json=payload, timeout=10)
    assert response.status_code == expected_status_code
    assert response.headers["Content-Type"] == expected_content_type
    data = response.json()
    assert data['name'] == payload['name']
    assert data['email'] == payload['email']
    assert data['body'] == payload['body']
    assert data['postId'] == payload['postId']

def test_patch_comment(base_url, excel_data):
    """
    Test case for the PATCH /comments/1 endpoint.

    Args:
        base_url (str): Base URL of the API.
        excel_data (pd.DataFrame): DataFrame containing the Excel data.
    """
    expected_status_code, expected_content_type, payload = get_expected_values(excel_data, '/comments/1', 'PATCH')
    payload = json.loads(payload) if payload else None
    response = requests.patch(f"{base_url}/comments/1", json=payload, timeout=10)
    assert response.status_code == expected_status_code
    assert response.headers["Content-Type"] == expected_content_type
    data = response.json()
    assert data['name'] == payload['name']

def test_delete_comment(base_url, excel_data):
    """
    Test case for the DELETE /comments/1 endpoint.

    Args:
        base_url (str): Base URL of the API.
        excel_data (pd.DataFrame): DataFrame containing the Excel data.
    Underscore(_) is work in place of payload for DELETE request we don't have payload.
    """
    expected_status_code, expected_content_type, _ = get_expected_values(excel_data, '/comments/1', 'DELETE')
    response = requests.delete(f"{base_url}/comments/1", timeout=10)
    assert response.status_code == expected_status_code
    assert response.headers["Content-Type"] == expected_content_type
    assert response.json() == {}



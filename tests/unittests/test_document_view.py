import pytest
from playwright.sync_api import Page, expect
import json

# Mock data
MOCK_PATIENTS = {
    "patients": [
        {
            "id": 1,
            "name": "Anna Andersson",
            "personalNumber": "19800101-1234"
        }
    ]
}

MOCK_DOCUMENTS = {
    "documents": [
        {
            "id": 1,
            "patient_id": 1,
            "title": "Test Document 1",
            "type": "Journal",
            "category": "Test",
            "unit": "Test Unit",
            "professional": "Doctor",
            "date": "2024-02-15",
            "abstract": "Test abstract 1",
            "content": "Test content 1"
        },
        {
            "id": 2,
            "patient_id": 1,
            "title": "Test Document 2",
            "type": "Journal",
            "category": "Test",
            "unit": "Test Unit",
            "professional": "Doctor",
            "date": "2024-02-14",
            "abstract": "Test abstract 2",
            "content": "Test content 2"
        }
    ]
}

@pytest.fixture
def setup_mocks(page: Page):
    # Mock patient search
    page.route("**/patients**", lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body=json.dumps(MOCK_PATIENTS)
    ))
    
    # Mock documents
    page.route("**/documents**", lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body=json.dumps(MOCK_DOCUMENTS)
    ))

def test_patient_documents(page: Page, setup_mocks):
    # Start at the root URL, which should redirect to patient selection
    page.goto("http://localhost:5174")
    
    # Wait for redirect and page to load
    page.wait_for_selector(".patient-select", timeout=5000)
    print("\nOn patient selection page")
    
    # Type "Anna" in the search box
    search_input = page.locator("input[placeholder='Sök patient...']")
    search_input.fill("Anna")
    print("\nSearched for 'Anna'")
    
    # Wait for search results and click on Anna Andersson
    patient_button = page.wait_for_selector(".patient-item:has-text('Anna Andersson')", timeout=5000)
    print("\nFound patient button:", patient_button.text_content())
    patient_button.click()
    
    # Wait for navigation and document list to load
    page.wait_for_selector(".document-section", timeout=5000)
    print("\nOn document list page")
    
    # Wait for documents to load and be visible
    page.wait_for_selector(".document", timeout=5000)
    
    # Get all document titles
    documents = page.locator("article.document h3")
    print("\nFound documents:", [documents.nth(i).text_content() for i in range(documents.count())])
    
    # Verify documents are shown
    expected_titles = [
        "Test Document 1",
        "Test Document 2"
    ]
    
    # Check number of documents
    expect(documents).to_have_count(2)
    
    # Check each document title
    for i, title in enumerate(expected_titles):
        expect(documents.nth(i)).to_have_text(title) 
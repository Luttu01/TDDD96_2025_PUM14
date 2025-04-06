from playwright.sync_api import Page, expect
import pytest
import json
import re

@pytest.fixture
def test_items():
    """Fixture providing test data"""
    return [
        {
            "id": 1,
            "patient_id": 1,
            "title": "Test Document",
            "type": "Läkaranteckning",
            "category": "Cardiology",
            "unit": "Kardiologiska kliniken",
            "professional": "Läkare",
            "date": "2024-01-01T12:00:00",
            "abstract": "Test abstract",
            "content": "Test content"
        }
    ]

@pytest.fixture
def setup_page(page: Page, test_items):
    """Fixture for common page setup"""
    # Mock the API response
    page.route("**/documents", lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body=json.dumps({"documents": test_items})
    ))
    
    # Navigate to the app
    page.goto("http://localhost:5173")
    
    # Wait for the document view to be mounted
    page.wait_for_selector(".document-view", state="visible", timeout=5000)
    
    return page

def test_document_view_exists(setup_page: Page):
    """Test that the document view exists"""
    document_view = setup_page.locator(".document-view")
    expect(document_view).to_be_visible()

def test_empty_document_view(setup_page: Page):
    """Test that the document view is empty when no document is selected"""
    document_view = setup_page.locator(".document-view")
    expect(document_view).to_have_class(re.compile(".*empty.*"))
    
    # Verify the empty state message
    empty_message = document_view.locator("p")
    expect(empty_message).to_have_text("Välj ett dokument för att visa dess innehåll")
    
    # Verify that document content elements are not present
    expect(document_view.locator("header")).to_have_count(0)
    expect(document_view.locator(".content")).to_have_count(0)

def test_document_view_shows_document(setup_page: Page, test_items):
    """Test that the document view correctly displays a document"""
    test_doc = test_items[0]
    
    # Click the document in the list to select it
    setup_page.locator(f".document-button:has-text('{test_doc['title']}')").click()
    
    # Verify the document view is not empty
    document_view = setup_page.locator(".document-view")
    expect(document_view).not_to_have_class("empty")
    
    # Verify document content is displayed correctly
    expect(document_view.locator("h2")).to_have_text(test_doc["title"])
    expect(document_view.locator(".type")).to_have_text(test_doc["type"])
    expect(document_view.locator(".category")).to_have_text(test_doc["category"])
    expect(document_view.locator(".unit")).to_have_text(test_doc["unit"])
    expect(document_view.locator(".professional")).to_have_text(test_doc["professional"])
    expect(document_view.locator(".abstract p")).to_have_text(test_doc["abstract"])
    expect(document_view.locator(".main-content p")).to_have_text(test_doc["content"])
    
    # Verify date is formatted correctly (Swedish format)
    date = document_view.locator(".date").text_content()
    assert date == "2024-01-01", "Date should be formatted in Swedish format (YYYY-MM-DD)"

def test_document_view_updates_content(setup_page: Page, test_items):
    """Test that the document view updates when given a different document"""
    test_doc = test_items[0]
    additional_doc = {
        "id": 2,
        "patient_id": 1,
        "title": "Second Document",
        "type": "Remiss",
        "category": "Neurology",
        "unit": "Kardiologiska kliniken",
        "professional": "Specialistläkare",
        "date": "2024-01-02T12:00:00",
        "abstract": "Another test abstract",
        "content": "Another test content"
    }
    
    # Mock the API to include both documents
    setup_page.route("**/documents", lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body=json.dumps({"documents": [test_doc, additional_doc]})
    ))
    
    # Reload the page to get the new documents
    setup_page.reload()
    
    # Click the first document
    setup_page.locator(f".document-button:has-text('{test_doc['title']}')").click()
    
    # Verify first document content
    document_view = setup_page.locator(".document-view")
    expect(document_view.locator("h2")).to_have_text(test_doc["title"])
    
    # Click the second document
    setup_page.locator(f".document-button:has-text('{additional_doc['title']}')").click()
    
    # Verify content updates to second document
    expect(document_view.locator("h2")).to_have_text(additional_doc["title"])
    expect(document_view.locator(".type")).to_have_text(additional_doc["type"])
    expect(document_view.locator(".abstract p")).to_have_text(additional_doc["abstract"])


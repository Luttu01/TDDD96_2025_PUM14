from playwright.sync_api import Page, expect
import pytest
from datetime import datetime, timedelta
import json

@pytest.fixture
def test_items():
    """Fixture providing test data with specific dates"""
    base_date = datetime(2024, 1, 1)  # Start of Jan 1, 2024 (midnight)
    return [
        {
            "id": 1,
            "patient_id": 1,
            "title": "Early Document",
            "type": "Läkaranteckning",
            "category": "Cardiology",
            "unit": "Kardiologiska kliniken",
            "professional": "Läkare",
            "date": "2023-12-27T00:00:00",  # Fixed date Dec 27
            "abstract": "Test abstract 1",
            "content": "Test content 1"
        },
        {
            "id": 2,
            "patient_id": 1,
            "title": "Middle Document",
            "type": "Case Report",
            "category": "Neurology",
            "unit": "Neurologiska avdelningen",
            "professional": "Specialistläkare",
            "date": "2024-01-01T00:00:00",  # Fixed date Jan 1
            "abstract": "Test abstract 2",
            "content": "Test content 2"
        },
        {
            "id": 3,
            "patient_id": 1,
            "title": "Late Document",
            "type": "Läkaranteckning",
            "category": "Oncology",
            "unit": "Onkologiska kliniken",
            "professional": "Läkare",
            "date": "2024-01-06T00:00:00",  # Fixed date Jan 6
            "abstract": "Test abstract 3",
            "content": "Test content 3"
        }
    ]

@pytest.fixture
def setup_page(page: Page, test_items):
    """Fixture for common page setup with mocked data"""
    # Mock the initial data load
    page.route("**/documents", lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body=json.dumps({"documents": test_items})
    ))
    
    page.goto("http://localhost:5173")
    page.wait_for_selector(".list-view", state="visible", timeout=5000)
    return page

def expand_all_groups(page: Page):
    """Helper function to expand all unit groups"""
    headers = page.locator(".unit-header").all()
    for header in headers:
        # Only click if the group is collapsed (expand icon is ▶)
        expand_icon = header.locator(".expand-icon")
        if expand_icon.text_content() == "▶":
            header.click()
            # Wait a bit for expansion animation
            page.wait_for_timeout(100)

def print_visible_documents(page: Page):
    """Helper function to print currently visible documents"""
    documents = page.locator(".document-item").all()
    print("\nCurrently visible documents:")
    for doc in documents:
        title = doc.locator("h3").text_content()
        date = doc.locator(".date").text_content()
        print(f"- {title} ({date})")

def test_date_filter_updates_list(setup_page: Page, test_items):
    """Test that setting date filters correctly updates the displayed list"""
    # Initially all documents should be visible
    unit_headers = setup_page.locator(".unit-header")
    expect(unit_headers).to_have_count(3)  # One for each unit
    
    # Expand all groups to see documents
    expand_all_groups(setup_page)
    
    # Verify all documents are initially visible
    documents = setup_page.locator(".document-item")
    expect(documents).to_have_count(3)
    print_visible_documents(setup_page)
    
    # Set start date to Dec 31, 2023 (should exclude only the early document)
    start_date = setup_page.locator("#start-date")
    start_date.fill("2023-12-31")
    print("\nApplied start date filter: 2023-12-31")
    
    # Wait for the list to update
    setup_page.wait_for_timeout(1000)
    
    # Expand any visible groups
    expand_all_groups(setup_page)
    
    # Wait for documents to be visible
    setup_page.wait_for_selector(".document-item", state="visible", timeout=5000)
    
    # Should now only see documents from Dec 31 onwards (2 documents)
    documents = setup_page.locator(".document-item")
    print_visible_documents(setup_page)
    expect(documents).to_have_count(2)
    
    # Verify the correct documents are shown
    titles = setup_page.locator(".document-item h3").all()
    title_texts = [title.text_content() for title in titles]
    assert "Middle Document" in title_texts, "Middle Document should be present"
    assert "Late Document" in title_texts, "Late Document should be present"
    assert "Early Document" not in title_texts, "Early Document should not be present"
    
    # Set end date to Jan 2, 2024 (should exclude the late document)
    end_date = setup_page.locator("#end-date")
    end_date.fill("2024-01-02")
    print("\nApplied end date filter: 2024-01-02")
    
    # Wait for the list to update
    setup_page.wait_for_timeout(1000)
    
    # Expand any visible groups
    expand_all_groups(setup_page)
    
    # Wait for documents to be visible
    setup_page.wait_for_selector(".document-item", state="visible", timeout=5000)
    
    # Should now only see the middle document
    documents = setup_page.locator(".document-item")
    print_visible_documents(setup_page)
    expect(documents).to_have_count(1)
    expect(documents.first.locator("h3")).to_have_text("Middle Document")
    
    # Clear dates using reset button
    reset_button = setup_page.locator(".reset-button")
    reset_button.click()
    print("\nReset filters")
    
    # Wait for the list to update
    setup_page.wait_for_timeout(1000)
    
    # Wait for unit headers to be present after reset
    setup_page.wait_for_selector(".unit-header", state="visible", timeout=5000)
    
    # Expand all groups again after reset
    expand_all_groups(setup_page)
    
    # Wait for documents to be visible
    setup_page.wait_for_selector(".document-item", state="visible", timeout=5000)
    
    # Should see all documents again
    documents = setup_page.locator(".document-item")
    print_visible_documents(setup_page)
    expect(documents).to_have_count(3)
    
    # Verify all documents are present
    titles = setup_page.locator(".document-item h3").all()
    title_texts = [title.text_content() for title in titles]
    assert "Early Document" in title_texts, "Early Document should be present after reset"
    assert "Middle Document" in title_texts, "Middle Document should be present after reset"
    assert "Late Document" in title_texts, "Late Document should be present after reset"

def test_start_date_edge_case(setup_page: Page, test_items):
    """Test the edge case where start date equals a document's date (should include the document)"""
    # Initially all documents should be visible
    unit_headers = setup_page.locator(".unit-header")
    expect(unit_headers).to_have_count(3)
    
    # Expand all groups to see documents
    expand_all_groups(setup_page)
    
    # Verify all documents are initially visible
    documents = setup_page.locator(".document-item")
    expect(documents).to_have_count(3)
    print_visible_documents(setup_page)
    
    # Set start date to exactly match Middle Document's date (2024-01-01)
    # This should include Middle Document and Late Document, but exclude Early Document
    start_date = setup_page.locator("#start-date")
    start_date.fill("2024-01-01")
    print("\nApplied start date filter: 2024-01-01")
    
    # Wait for the list to update
    setup_page.wait_for_timeout(1000)
    
    # Expand any visible groups
    expand_all_groups(setup_page)
    
    # Wait for documents to be visible
    setup_page.wait_for_selector(".document-item", state="visible", timeout=5000)
    
    # Should see both Middle Document (exact match) and Late Document
    documents = setup_page.locator(".document-item")
    print_visible_documents(setup_page)
    expect(documents).to_have_count(2)
    
    # Verify the correct documents are shown
    titles = setup_page.locator(".document-item h3").all()
    title_texts = [title.text_content() for title in titles]
    assert "Middle Document" in title_texts, "Middle Document should be included (exact date match)"
    assert "Late Document" in title_texts, "Late Document should be included (after start date)"
    assert "Early Document" not in title_texts, "Early Document should be excluded (before start date)"

def test_end_date_edge_case(setup_page: Page, test_items):
    """Test the edge case where end date equals a document's date (should include the document)"""
    # Initially all documents should be visible
    unit_headers = setup_page.locator(".unit-header")
    expect(unit_headers).to_have_count(3)
    
    # Expand all groups to see documents
    expand_all_groups(setup_page)
    
    # Verify all documents are initially visible
    documents = setup_page.locator(".document-item")
    expect(documents).to_have_count(3)
    print_visible_documents(setup_page)
    
    # Set end date to exactly match Middle Document's date (2024-01-01)
    # This should include Early Document AND Middle Document, but exclude Late Document
    end_date = setup_page.locator("#end-date")
    end_date.fill("2024-01-01")
    print("\nApplied end date filter: 2024-01-01")
    
    # Wait for the list to update
    setup_page.wait_for_timeout(1000)
    
    # Expand any visible groups
    expand_all_groups(setup_page)
    
    # Wait for documents to be visible
    setup_page.wait_for_selector(".document-item", state="visible", timeout=5000)
    
    # Should see both Early Document and Middle Document (exact match)
    documents = setup_page.locator(".document-item")
    print_visible_documents(setup_page)
    expect(documents).to_have_count(2)
    
    # Verify the correct documents are shown
    titles = setup_page.locator(".document-item h3").all()
    title_texts = [title.text_content() for title in titles]
    assert "Early Document" in title_texts, "Early Document should be included (before end date)"
    assert "Middle Document" in title_texts, "Middle Document should be included (equal to end date)"
    assert "Late Document" not in title_texts, "Late Document should be excluded (after end date)"

def test_type_filter_updates_list(setup_page: Page, test_items):
    """Test that setting type filter correctly updates the displayed list"""
    # Initially all documents should be visible
    unit_headers = setup_page.locator(".unit-header")
    expect(unit_headers).to_have_count(3)  # One for each unit
    
    # Expand all groups to see documents
    expand_all_groups(setup_page)
    
    # Verify all documents are initially visible
    documents = setup_page.locator(".document-item")
    expect(documents).to_have_count(3)
    print_visible_documents(setup_page)
    
    # Set type filter to "Läkaranteckning"
    type_filter = setup_page.locator("#type-filter")
    type_filter.select_option("Läkaranteckning")
    print("\nApplied type filter: Läkaranteckning")
    
    # Wait for the list to update
    setup_page.wait_for_timeout(1000)
    
    # Expand any visible groups
    expand_all_groups(setup_page)
    
    # Wait for documents to be visible
    setup_page.wait_for_selector(".document-item", state="visible", timeout=5000)
    
    # Should now only see Läkaranteckning documents (2 documents)
    documents = setup_page.locator(".document-item")
    print_visible_documents(setup_page)
    expect(documents).to_have_count(2)
    
    # Verify each visible document is of type Läkaranteckning
    types = setup_page.locator(".document-item .type").all()
    for type_element in types:
        expect(type_element).to_have_text("Läkaranteckning")
    
    # Clear filter using reset button
    reset_button = setup_page.locator(".reset-button")
    reset_button.click()
    print("\nReset filters")
    
    # Wait for the list to update
    setup_page.wait_for_timeout(1000)
    
    # Expand all groups again after reset
    expand_all_groups(setup_page)
    
    # Should see all documents again
    documents = setup_page.locator(".document-item")
    print_visible_documents(setup_page)
    expect(documents).to_have_count(3)

def test_category_filter_updates_list(setup_page: Page, test_items):
    """Test that setting category filter correctly updates the displayed list"""
    # Initially all documents should be visible
    unit_headers = setup_page.locator(".unit-header")
    expect(unit_headers).to_have_count(3)
    
    # Expand all groups to see documents
    expand_all_groups(setup_page)
    
    # Verify all documents are initially visible
    documents = setup_page.locator(".document-item")
    expect(documents).to_have_count(3)
    print_visible_documents(setup_page)
    
    # Set category filter to "Cardiology"
    category_filter = setup_page.locator("#category-filter")
    category_filter.select_option("Cardiology")
    print("\nApplied category filter: Cardiology")
    
    # Wait for the list to update
    setup_page.wait_for_timeout(1000)
    
    # Expand any visible groups
    expand_all_groups(setup_page)
    
    # Wait for documents to be visible
    setup_page.wait_for_selector(".document-item", state="visible", timeout=5000)
    
    # Should now only see Cardiology documents (1 document)
    documents = setup_page.locator(".document-item")
    print_visible_documents(setup_page)
    expect(documents).to_have_count(1)
    
    # Verify the document is from Cardiology category
    categories = setup_page.locator(".document-item .category").all()
    for category in categories:
        expect(category).to_have_text("Cardiology")
    
    # Clear filter using reset button
    reset_button = setup_page.locator(".reset-button")
    reset_button.click()
    print("\nReset filters")
    
    # Wait for the list to update
    setup_page.wait_for_timeout(1000)
    
    # Expand all groups again after reset
    expand_all_groups(setup_page)
    
    # Should see all documents again
    documents = setup_page.locator(".document-item")
    print_visible_documents(setup_page)
    expect(documents).to_have_count(3)

def test_unit_filter_updates_list(setup_page: Page, test_items):
    """Test that setting unit filter correctly updates the displayed list"""
    # Initially all documents should be visible
    unit_headers = setup_page.locator(".unit-header")
    expect(unit_headers).to_have_count(3)
    
    # Expand all groups to see documents
    expand_all_groups(setup_page)
    
    # Verify all documents are initially visible
    documents = setup_page.locator(".document-item")
    expect(documents).to_have_count(3)
    print_visible_documents(setup_page)
    
    # Set unit filter to "Kardiologiska kliniken"
    unit_filter = setup_page.locator("#unit-filter")
    unit_filter.select_option("Kardiologiska kliniken")
    print("\nApplied unit filter: Kardiologiska kliniken")
    
    # Wait for the list to update
    setup_page.wait_for_timeout(1000)
    
    # Wait for documents to be visible
    setup_page.wait_for_selector(".document-item", state="visible", timeout=5000)
    
    # Should now only see documents from Kardiologiska kliniken (1 document)
    documents = setup_page.locator(".document-item")
    print_visible_documents(setup_page)
    expect(documents).to_have_count(1)
    
    # Verify we only have one unit header and it's Kardiologiska kliniken
    unit_headers = setup_page.locator(".unit-header")
    expect(unit_headers).to_have_count(1)
    expect(unit_headers.first.locator(".unit-name")).to_have_text("Kardiologiska kliniken")
    
    # Clear filter using reset button
    reset_button = setup_page.locator(".reset-button")
    reset_button.click()
    print("\nReset filters")
    
    # Wait for the list to update
    setup_page.wait_for_timeout(1000)
    
    # Expand all groups again after reset
    expand_all_groups(setup_page)
    
    # Should see all documents again
    documents = setup_page.locator(".document-item")
    print_visible_documents(setup_page)
    expect(documents).to_have_count(3)

def test_professional_filter_updates_list(setup_page: Page, test_items):
    """Test that setting professional filter correctly updates the displayed list"""
    # Initially all documents should be visible
    unit_headers = setup_page.locator(".unit-header")
    expect(unit_headers).to_have_count(3)
    
    # Expand all groups to see documents
    expand_all_groups(setup_page)
    
    # Verify all documents are initially visible
    documents = setup_page.locator(".document-item")
    expect(documents).to_have_count(3)
    print_visible_documents(setup_page)
    
    # Set professional filter to "Läkare"
    professional_filter = setup_page.locator("#professional-filter")
    professional_filter.select_option("Läkare")
    print("\nApplied professional filter: Läkare")
    
    # Wait for the list to update
    setup_page.wait_for_timeout(1000)
    
    # Expand any visible groups
    expand_all_groups(setup_page)
    
    # Wait for documents to be visible
    setup_page.wait_for_selector(".document-item", state="visible", timeout=5000)
    
    # Should now only see documents from Läkare (2 documents)
    documents = setup_page.locator(".document-item")
    print_visible_documents(setup_page)
    expect(documents).to_have_count(2)
    
    # Verify each document is from a Läkare
    professionals = setup_page.locator(".document-item .professional").all()
    for professional in professionals:
        expect(professional).to_have_text("Läkare")
    
    # Clear filter using reset button
    reset_button = setup_page.locator(".reset-button")
    reset_button.click()
    print("\nReset filters")
    
    # Wait for the list to update
    setup_page.wait_for_timeout(1000)
    
    # Expand all groups again after reset
    expand_all_groups(setup_page)
    
    # Should see all documents again
    documents = setup_page.locator(".document-item")
    print_visible_documents(setup_page)
    expect(documents).to_have_count(3)

def test_combined_filters_update_list(setup_page: Page, test_items):
    """Test that combining multiple filters correctly updates the displayed list"""
    # Initially all documents should be visible
    unit_headers = setup_page.locator(".unit-header")
    expect(unit_headers).to_have_count(3)
    
    # Expand all groups to see documents
    expand_all_groups(setup_page)
    
    # Verify all documents are initially visible
    documents = setup_page.locator(".document-item")
    expect(documents).to_have_count(3)
    print_visible_documents(setup_page)
    
    # Apply multiple filters:
    # - Type: Läkaranteckning
    # - Unit: Kardiologiska kliniken
    # - Professional: Läkare
    setup_page.locator("#type-filter").select_option("Läkaranteckning")
    setup_page.locator("#unit-filter").select_option("Kardiologiska kliniken")
    setup_page.locator("#professional-filter").select_option("Läkare")
    print("\nApplied multiple filters")
    
    # Wait for the list to update
    setup_page.wait_for_timeout(1000)
    
    # Expand any visible groups
    expand_all_groups(setup_page)
    
    # Wait for documents to be visible
    setup_page.wait_for_selector(".document-item", state="visible", timeout=5000)
    
    # Should now only see documents matching all criteria (1 document)
    documents = setup_page.locator(".document-item")
    print_visible_documents(setup_page)
    expect(documents).to_have_count(1)
    
    # Verify the document matches all criteria
    document = setup_page.locator(".document-item").first
    expect(document.locator(".type")).to_have_text("Läkaranteckning")
    expect(setup_page.locator(".unit-name")).to_have_text("Kardiologiska kliniken")
    expect(document.locator(".professional")).to_have_text("Läkare")
    
    # Clear filters using reset button
    reset_button = setup_page.locator(".reset-button")
    reset_button.click()
    print("\nReset filters")
    
    # Wait for the list to update
    setup_page.wait_for_timeout(1000)
    
    # Expand all groups again after reset
    expand_all_groups(setup_page)
    
    # Should see all documents again
    documents = setup_page.locator(".document-item")
    print_visible_documents(setup_page)
    expect(documents).to_have_count(3)

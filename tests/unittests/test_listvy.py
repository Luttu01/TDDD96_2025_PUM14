import pytest
from playwright.sync_api import Page, expect
import json
from datetime import datetime, timedelta
import random
import sys

class ListvyPage:
    """Page Object Model för listvyn"""
    def __init__(self, page):
        self.page = page
        self.journal_list = page.locator(".documents")
        self.journal_items = page.locator(".document-item")
        self.empty_message = page.locator(".empty-message")
        self.pagination = page.locator(".pagination")
    
    def goto(self):
        """Navigera till listvyn"""
        self.page.goto("http://localhost:5173")
        
        # Wait for patient selection
        self.page.wait_for_selector(".patient-select", timeout=2000)
        search_input = self.page.locator("input[placeholder='Sök patient...']")
        search_input.fill("Anna")
        
        # Wait for and click the patient item
        patient_item = self.page.wait_for_selector(".patient-item:has-text('Anna Andersson')", timeout=2000)
        patient_item.click()

        # Wait for document list
        try:
            self.page.wait_for_selector(".documents", timeout=2000)
        except Exception as e:
            self.page.screenshot(path="error_load.png")
            raise Exception(f"Failed to load documents: {str(e)}")

    def select_journal(self, index: int):
        """Select a journal by index"""
        # Wait for documents to be available
        self.page.wait_for_selector(".document-item", timeout=2000)
        
        # Get all document items
        items = self.page.locator(".document-item")
        count = items.count()
        
        if count == 0:
            raise Exception("No document items found")
        
        if index >= count:
            raise IndexError(f"Index {index} out of range, only {count} items available")
        
        # Click the item
        items.nth(index).click()
        self.page.wait_for_timeout(200)  # Wait for selection to take effect
        
        # Verify selection
        selected = self.page.locator(".document-item.selected")
        expect(selected).to_have_count(1)

    def select_multiple_journals(self, indexes: list[int]):
        """Select multiple journals using Ctrl/Cmd+click"""
        # Wait for documents to be available
        self.page.wait_for_selector(".document-item", timeout=2000)
        
        # Get all document items
        items = self.page.locator(".document-item")
        count = items.count()
        
        if count == 0:
            raise Exception("No document items found")
        
        modifier = 'Meta' if 'darwin' in sys.platform else 'Control'
        for index in indexes:
            if index >= count:
                raise IndexError(f"Index {index} out of range, only {count} items available")
            items.nth(index).click(modifiers=[modifier])
            self.page.wait_for_timeout(200)  # Wait for selection to take effect
        
        # Verify selection
        selected = self.page.locator(".document-item.selected")
        expect(selected).to_have_count(len(indexes))

    def click_outside(self):
        """Click outside of any journal item"""
        # Click in the empty area of the documents container
        container = self.page.locator(".documents")
        expect(container).to_be_visible()
        
        # Click in the top padding area
        bbox = container.bounding_box()
        self.page.mouse.click(bbox["x"] + 10, bbox["y"] + 10)
        self.page.wait_for_timeout(200)  # Wait for deselection to take effect
        
        # Verify deselection
        selected = self.page.locator(".document-item.selected")
        expect(selected).to_have_count(0)

def setup_api_mocks(page, documents=None):
    """Setup all API route mocks needed for testing"""
    # Mock patient search endpoint
    def handle_patients(route):
        route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({
                "patients": [{
                    "id": 1,
                    "name": "Anna Andersson",
                    "personalNumber": "19800101-1234"
                }]
            })
        )
    page.route("**/patients**", handle_patients)
    
    # Mock single patient endpoint
    def handle_patient(route):
        route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({
                "id": 1,
                "name": "Anna Andersson",
                "personalNumber": "19800101-1234"
            })
        )
    page.route("**/patients/1", handle_patient)
    
    # Mock documents endpoint
    def handle_documents(route):
        docs = documents if documents is not None else generate_mock_documents(10)
        route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({"documents": docs})
        )
    page.route("**/documents**", handle_documents)
    
    # Mock options endpoint
    page.route("**/options", lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body=json.dumps({
            "categories": ["Cardiology", "Neurology", "Oncology"],
            "types": ["Journal", "Case Report", "Research Article"],
            "units": ["Kardiologiska kliniken", "Neurologiska avdelningen"],
            "professionals": ["Läkare", "Specialistläkare", "Sjuksköterska"],
            "sortOptions": [
                {"value": "date", "label": "Sortera efter datum"},
                {"value": "title", "label": "Sortera efter titel"}
            ]
        })
    ))

@pytest.fixture
def listvy(page):
    setup_api_mocks(page)
    return ListvyPage(page)

@pytest.fixture
def empty_listvy(page):
    setup_api_mocks(page, documents=[])
    return ListvyPage(page)

@pytest.fixture
def large_listvy(page):
    setup_api_mocks(page, documents=generate_mock_documents(120))
    return ListvyPage(page)

@pytest.fixture
def grouped_listvy(page):
    # Generate documents with same unit to test grouping
    docs = []
    units = ["Kardiologiska kliniken", "Neurologiska avdelningen"]
    for unit in units:
        for i in range(5):
            docs.append({
                "id": len(docs) + 1,
                "title": f"Test Document {len(docs) + 1}",
                "date": datetime.now().isoformat(),
                "type": "Journal",
                "category": "Test",
                "unit": unit,
                "professional": "Doctor",
                "abstract": f"Test abstract {len(docs) + 1}",
                "content": f"Test content {len(docs) + 1}"
            })
    
    setup_api_mocks(page, documents=docs)
    return ListvyPage(page)

# Rendering and Layout Tests
def test_list_exists(listvy):
    """Verify that the journal list exists and is visible.
    
    Krav: K1.1-1
    """
    listvy.goto()
    expect(listvy.journal_list).to_be_visible()

def test_chronological_order(listvy):
    """Verify that journals are displayed in chronological order.
    
    Krav: K1.1-1
    """
    listvy.goto()
    dates = listvy.journal_items.evaluate_all(
        "elements => elements.map(el => el.getAttribute('data-date'))"
    )
    assert dates == sorted(dates, reverse=True)

def test_metadata_display(listvy):
    """Verify that all metadata is displayed correctly.
    
    Krav: K1.1-1
    """
    listvy.goto()
    first_item = listvy.journal_items.first
    
    # Check that all metadata elements exist and are visible
    expect(first_item.locator(".title")).to_be_visible()
    expect(first_item.locator(".date")).to_be_visible()
    expect(first_item.locator(".unit")).to_be_visible()
    expect(first_item.locator(".professional")).to_be_visible()

def test_empty_list(empty_listvy):
    """Verify that empty state message is shown when no journals exist.
    
    Krav: K1.1-1
    """
    empty_listvy.goto()
    expect(empty_listvy.empty_message).to_be_visible()
    expect(empty_listvy.empty_message).to_contain_text("Inga journaler tillgängliga")

def test_pagination(large_listvy):
    """Verify that pagination works correctly with many journals.
    
    Krav: K1.1-1
    """
    large_listvy.goto()
    expect(large_listvy.pagination).to_be_visible()
    
    # Check that we can navigate between pages
    next_button = large_listvy.pagination.locator("button:has-text('Nästa')")
    expect(next_button).to_be_enabled()
    next_button.click()
    
    # Verify that we see different items on the next page
    first_item_title = large_listvy.journal_items.first.locator("h3").text_content()
    assert first_item_title != "Test Document 1"

# Interaction Tests
def test_single_selection(listvy):
    """Verify that a single journal can be selected."""
    listvy.goto()
    
    # Wait for documents to be visible
    listvy.page.wait_for_selector(".document-item", timeout=2000)
    
    # Select first item
    listvy.select_journal(0)
    
    # Verify selection
    selected = listvy.page.locator(".document-item.selected")
    expect(selected).to_have_count(1)

def test_multiple_selection(listvy):
    """Verify that multiple journals can be selected with Ctrl+click."""
    listvy.goto()
    
    # Wait for documents to be visible
    listvy.page.wait_for_selector(".document-item", timeout=2000)
    
    # Select multiple items
    listvy.select_multiple_journals([0, 1, 2])
    
    # Verify selection
    selected = listvy.page.locator(".document-item.selected")
    expect(selected).to_have_count(3)

def test_deselection(listvy):
    """Verify that clicking outside deselects journals."""
    listvy.goto()
    
    # Wait for documents to be visible
    listvy.page.wait_for_selector(".document-item", timeout=2000)
    
    # Select an item first
    listvy.select_journal(0)
    
    # Verify initial selection
    selected = listvy.page.locator(".document-item.selected")
    expect(selected).to_have_count(1)
    
    # Click outside
    listvy.click_outside()
    
    # Wait for deselection
    listvy.page.wait_for_timeout(200)  # Give time for state to update
    
    # Verify deselection
    selected = listvy.page.locator(".document-item.selected")
    expect(selected).to_have_count(0)

def test_invalid_data(listvy):
    """Verify that invalid document data is handled gracefully.
    
    Krav: K1.1-1
    """
    # Mock invalid document data
    invalid_doc = {
        "id": "invalid",  # Should be number
        "title": None,    # Should be string
        "date": "invalid-date"  # Should be ISO date
    }
    
    listvy.page.route("**/documents**", lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body=json.dumps({"documents": [invalid_doc]})
    ))
    
    listvy.goto()
    
    # Wait for and verify error message is not hidden
    error_message = listvy.page.locator("[data-testid='date-error']")
    expect(error_message).not_to_have_class("hidden")

def test_grouping(grouped_listvy):
    """Verify that journals are grouped by unit."""
    grouped_listvy.goto()
    
    # Wait for document groups
    grouped_listvy.page.wait_for_selector(".document-group", timeout=2000)
    
    # Get all document groups
    groups = grouped_listvy.page.locator(".document-group")
    
    # Get all unit buttons
    unit_buttons = grouped_listvy.page.locator(".group-header")
    
    # Get unit names
    unit_texts = unit_buttons.evaluate_all("elements => elements.map(el => el.textContent.trim())")
    
    # Verify counts and content
    expect(groups).to_have_count(2)
    assert any("Kardiologiska kliniken" in text for text in unit_texts)
    assert any("Neurologiska avdelningen" in text for text in unit_texts)

def test_filter_updates(listvy):
    """Verify that the list updates when filters are applied.
    
    Krav: K1.2-5
    """
    listvy.goto()
    
    # Wait for initial documents to load
    listvy.page.wait_for_selector(".document-item", timeout=2000)
    initial_count = listvy.page.locator(".document-item").count()
    
    # Setup filtered response
    filtered_docs = generate_mock_documents(3)  # Only 3 documents match filter
    filtered_docs[0]["unit"] = "Kardiologiska kliniken"
    filtered_docs[1]["unit"] = "Kardiologiska kliniken"
    filtered_docs[2]["unit"] = "Kardiologiska kliniken"
    
    # Create route handler that returns filtered docs when filter params present
    def handle_documents(route):
        url = route.request.url
        if "unit=Kardiologiska" in url:
            route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps({"documents": filtered_docs})
            )
        else:
            route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps({"documents": generate_mock_documents(10)})
            )
    
    # Update the route handler
    listvy.page.route("**/documents**", handle_documents)
    
    # Select filter option
    filter_select = listvy.page.locator("select[name='category']")
    filter_select.select_option("Kard")
    
    # Wait for filtered results
    listvy.page.wait_for_timeout(500)  # Wait for request and render
    
    # Verify list was updated
    filtered_count = listvy.page.locator(".document-item").count()
    assert filtered_count == 3
    assert filtered_count < initial_count
    
    # Verify filtered content
    units = listvy.page.locator(".document-item .unit").all_text_contents()
    assert all("Kardiologiska kliniken" in unit for unit in units)

def generate_mock_documents(count: int = 100) -> list:
    """Generate mock documents for testing."""
    documents = []
    base_date = datetime.now() - timedelta(days=730)
    
    for i in range(count):
        doc_date = base_date + timedelta(days=random.randint(0, 730))
        documents.append({
            "id": i + 1,
            "title": f"Test Document {i + 1}",
            "date": doc_date.isoformat(),
            "type": "Journal",
            "category": "Test",
            "unit": "Test Unit",
            "professional": "Doctor",
            "abstract": f"Test abstract {i + 1}",
            "content": f"Test content {i + 1}"
        })
    
    return sorted(documents, key=lambda x: x["date"], reverse=True) 
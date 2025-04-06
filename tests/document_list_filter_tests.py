from playwright.sync_api import Page, expect
import pytest
from datetime import datetime, timedelta
import json
import urllib.parse

@pytest.fixture
def test_items():
    """Fixture providing test data with specific dates"""
    base_date = datetime(2024, 1, 1, 12, 0)  # Fixed date for consistent testing
    return [
        {
            "id": 1,
            "patient_id": 1,
            "title": "Läkaranteckning 1",
            "type": "Läkaranteckning",
            "category": "Cardiology",
            "unit": "Kardiologiska kliniken",
            "professional": "Läkare",
            "date": (base_date - timedelta(days=2)).isoformat(),  # Dec 30
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
            "date": (base_date - timedelta(days=1)).isoformat(),  # Dec 31
            "abstract": "Test abstract 2",
            "content": "Test content 2"
        },
        {
            "id": 3,
            "patient_id": 1,
            "title": "Läkaranteckning 2",
            "type": "Läkaranteckning",
            "category": "Oncology",
            "unit": "Onkologiska kliniken",
            "professional": "Läkare",
            "date": base_date.isoformat(),  # Jan 1
            "abstract": "Test abstract 3",
            "content": "Test content 3"
        },
        {
            "id": 4,
            "patient_id": 1,
            "title": "Kirurgi anteckning",
            "type": "Läkaranteckning",
            "category": "Surgery",
            "unit": "Kirurgen",
            "professional": "Kirurg",
            "date": base_date.isoformat(),
            "abstract": "Test abstract 4",
            "content": "Test content 4"
        },
        {
            "id": 5,
            "patient_id": 1,
            "title": "Omvårdnadsanteckning",
            "type": "Anteckning",
            "category": "Nursing",
            "unit": "Medicinkliniken",
            "professional": "Sjuksköterska",
            "date": base_date.isoformat(),
            "abstract": "Omvårdnadsbedömning och åtgärder",
            "content": "Test content 5"
        },
        {
            "id": 6,
            "patient_id": 1,
            "title": "Patient med feber",
            "type": "Anteckning",
            "category": "Emergency",
            "unit": "Akuten",
            "professional": "Läkare",
            "date": base_date.isoformat(),
            "abstract": "Patient inkom med hög feber och huvudvärk",
            "content": "Test content 6"
        }
    ]

@pytest.fixture
def setup_page(page: Page, test_items):
    """Setup the page for testing with mock data"""
    def handle_document_request(route):
        url = route.request.url
        params = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(url).query))
        filtered_items = test_items.copy()

        # Apply each filter if present
        if 'type' in params:
            filtered_items = [item for item in filtered_items if item['type'] == params['type']]
        if 'unit' in params:
            filtered_items = [item for item in filtered_items if item['unit'] == params['unit']]
        if 'professional' in params:
            filtered_items = [item for item in filtered_items if item['professional'] == params['professional']]
        if 'search' in params:
            search_terms = params['search'].lower().split()
            filtered_items = [
                item for item in filtered_items
                if all(
                    any(
                        term in field.lower()
                        for field in [
                            item['title'],
                            item['abstract'],
                            item['professional'],
                            item['type'],
                            item['category'],
                            item['unit']
                        ]
                    )
                    for term in search_terms
                )
            ]

        route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({"documents": filtered_items})
        )

    # Clear any existing route handlers
    page.unroute("**/*")
    
    # Add our comprehensive route handler for all document endpoints
    page.route("**/documents**", handle_document_request)
    
    # Navigate to the page and wait for initial load
    page.goto("http://localhost:5173")
    page.wait_for_selector(".list-view", state="visible", timeout=5000)
    
    return page

async def apply_filter(page: Page, filter_params: dict):
    """Helper function to apply filters by directly triggering API call"""
    # Construct the URL with filter parameters
    params = urllib.parse.urlencode(filter_params)
    url = f"http://localhost:3333/documents?{params}"
    
    # Trigger the API call by evaluating JavaScript
    await page.evaluate(f"""
        fetch("{url}")
            .then(response => response.json())
            .then(data => {{
                // Dispatch a custom event that the app listens for in tests
                window.dispatchEvent(new CustomEvent('test:set-items', {{
                    detail: data.documents
                }}));
            }});
    """)
    
    # Wait for the list to update
    await page.wait_for_timeout(100)  # Small delay to ensure state updates

def test_filter_by_type_lakaranteckning(setup_page: Page, test_items):
    """Test that filtering by type 'Läkaranteckning' only shows läkaranteckningar"""
    # Apply type filter directly through API
    setup_page.evaluate("async () => { await window.testApplyFilter({'type': 'Läkaranteckning'}) }")
    
    # Wait for the filtered results
    setup_page.wait_for_selector(".list-view", state="visible")

    # Expand all groups
    unit_headers = setup_page.locator(".unit-header").all()
    for header in unit_headers:
        header.click()
        
    # Verify all documents are of type Läkaranteckning
    items = setup_page.locator(".document-item .type").all()
    for item in items:
        expect(item).to_have_text("Läkaranteckning")

def test_filter_by_unit_kirurgen(setup_page: Page):
    """Test that filtering by unit 'Kirurgen' only shows documents from that unit"""
    # Apply unit filter directly through API
    setup_page.evaluate("async () => { await window.testApplyFilter({'unit': 'Kirurgen'}) }")
    
    # Wait for the filtered results
    setup_page.wait_for_selector(".list-view", state="visible")
    
    # Verify we only have one unit group (Kirurgen)
    expect(setup_page.locator(".unit-header")).to_have_count(1)
    expect(setup_page.locator(".unit-header .unit-name")).to_have_text("Kirurgen")

def test_filter_by_professional_sjukskoterska(setup_page: Page):
    """Test that filtering by professional 'Sjuksköterska' only shows documents from nurses"""
    # Apply professional filter directly through API
    setup_page.evaluate("async () => { await window.testApplyFilter({'professional': 'Sjuksköterska'}) }")
    
    # Wait for the filtered results
    setup_page.wait_for_selector(".list-view", state="visible")
    
    # Verify we only have documents from nurses
    setup_page.locator(".unit-header").first.click()
    professionals = setup_page.locator(".document-item .professional").all()
    for professional in professionals:
        expect(professional).to_have_text("Sjuksköterska")

def test_combined_filter_type_and_unit(setup_page: Page):
    """Test that combining filters works correctly"""
    # Apply combined filters directly through API
    setup_page.evaluate("""async () => { 
        await window.testApplyFilter({
            'type': 'Läkaranteckning',
            'unit': 'Kirurgen'
        }) 
    }""")
    
    # Wait for the filtered results
    setup_page.wait_for_selector(".list-view", state="visible")
    
    # Verify we only have one unit group
    expect(setup_page.locator(".unit-header")).to_have_count(1)
    expect(setup_page.locator(".unit-header .unit-name")).to_have_text("Kirurgen")
    
    # Expand the group and verify documents
    setup_page.locator(".unit-header").first.click()
    documents = setup_page.locator(".document-item").all()
    for doc in documents:
        expect(doc.locator(".type")).to_have_text("Läkaranteckning")

def test_search_text_feber(setup_page: Page):
    """Test that searching for 'feber' only shows documents containing that word"""
    # Apply search filter directly through API
    setup_page.evaluate("async () => { await window.testApplyFilter({'search': 'feber'}) }")
    
    # Wait for the filtered results
    setup_page.wait_for_selector(".list-view", state="visible")
    
    # Expand all groups and verify content
    setup_page.locator(".unit-header").first.click()
    documents = setup_page.locator(".document-item").all()
    for doc in documents:
        text_content = doc.evaluate("""node => {
            return node.textContent.toLowerCase();
        }""")
        assert "feber" in text_content

def test_multi_word_search(setup_page: Page):
    """Test that searching for multiple words finds documents containing all words"""
    # Apply multi-word search directly through API
    setup_page.evaluate("async () => { await window.testApplyFilter({'search': 'läkare cardiology'}) }")
    
    # Wait for the filtered results
    setup_page.wait_for_selector(".list-view", state="visible")
    
    # Expand all groups and verify content
    setup_page.locator(".unit-header").first.click()
    documents = setup_page.locator(".document-item").all()
    for doc in documents:
        text_content = doc.evaluate("""node => {
            return node.textContent.toLowerCase();
        }""")
        assert "läkare" in text_content and "cardiology" in text_content 
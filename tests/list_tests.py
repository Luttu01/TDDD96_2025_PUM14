from playwright.sync_api import Page, expect
import pytest
from datetime import datetime, timedelta
import json

@pytest.fixture
def test_items():
    """Fixture providing test data with specific dates"""
    base_date = datetime(2024, 1, 1, 12, 0)  # Fixed date for consistent testing
    return [
        {
            "CompositionId": "1",
            "DateTime": (base_date - timedelta(days=2)).isoformat(),  # Dec 30
            "DisplayDateTime": (base_date - timedelta(days=2)).strftime("%Y-%m-%d %H:%M"),
            "Dokument_ID": "DOC001",
            "Dokument_skapad_av_yrkestitel_ID": "L001",
            "Dokument_skapad_av_yrkestitel_Namn": "Läkare",
            "Dokumentationskod": "Läkaranteckning",
            "Dokumentnamn": "Läkaranteckning 1",
            "Tidsstämpel_för_sparat_dokument": (base_date - timedelta(days=2)).isoformat(),
            "Vårdenhet_Identifierare": "KK001",
            "Vårdenhet_Namn": "Kardiologiska kliniken"
        },
        {
            "CompositionId": "2",
            "DateTime": (base_date - timedelta(days=1)).isoformat(),  # Dec 31
            "DisplayDateTime": (base_date - timedelta(days=1)).strftime("%Y-%m-%d %H:%M"),
            "Dokument_ID": "DOC002",
            "Dokument_skapad_av_yrkestitel_ID": "SL001",
            "Dokument_skapad_av_yrkestitel_Namn": "Specialistläkare",
            "Dokumentationskod": "Case Report",
            "Dokumentnamn": "Middle Document",
            "Tidsstämpel_för_sparat_dokument": (base_date - timedelta(days=1)).isoformat(),
            "Vårdenhet_Identifierare": "NA001",
            "Vårdenhet_Namn": "Neurologiska avdelningen"
        },
        {
            "CompositionId": "3",
            "DateTime": base_date.isoformat(),  # Jan 1
            "DisplayDateTime": base_date.strftime("%Y-%m-%d %H:%M"),
            "Dokument_ID": "DOC003",
            "Dokument_skapad_av_yrkestitel_ID": "L002",
            "Dokument_skapad_av_yrkestitel_Namn": "Läkare",
            "Dokumentationskod": "Läkaranteckning",
            "Dokumentnamn": "Läkaranteckning 2",
            "Tidsstämpel_för_sparat_dokument": base_date.isoformat(),
            "Vårdenhet_Identifierare": "OK001",
            "Vårdenhet_Namn": "Onkologiska kliniken"
        }
    ]

@pytest.fixture
def sorted_items(test_items):
    """Fixture providing items sorted by date (newest first)"""
    return sorted(
        test_items,
        key=lambda x: datetime.fromisoformat(x["DateTime"]),
        reverse=True
    )

@pytest.fixture
def setup_page(page: Page, test_items):
    """Setup the page for testing with mock data"""
    # Mock the fetch response before navigation
    page.route("**/api/journals", lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body=json.dumps(test_items)
    ))

    page.goto("http://localhost:5173")
    page.wait_for_selector(".list-view", state="visible", timeout=5000)
    return page

# Section 1: Lista och visning
def test_1_1_lista_existerar(setup_page: Page):
    """Test 1.1: Lista existerar - Navigera till basvyn, journallistan renderas och är synlig"""
    list_container = setup_page.locator("ul.list-view")
    expect(list_container).to_be_visible()

def test_1_2_kronologisk_ordning(setup_page: Page):
    """Test 1.2: Kronologisk ordning - Journaler visas sorterade med nyaste först"""
    # Expand all units
    unit_headers = setup_page.locator(".unit-header").all()
    for header in unit_headers:
        header.click()
    
    # Get all document dates
    dates = setup_page.eval_on_selector_all("ul.list-view .date", r"""
        elements => elements.map(el => {
            const date = new Date(el.textContent.replace(/(\d+)-(\d+)-(\d+)/, '$3-$2-$1'));
            return date.getTime();
        })
    """)
    
    # Verify dates are in descending order
    assert dates == sorted(dates, reverse=True), "Documents should be sorted newest first"

def test_1_3_metadata_visning(setup_page: Page, test_items):
    """Test 1.3: Metadata-visning - All metadata visas korrekt för varje journal"""
    # Expand all units
    unit_headers = setup_page.locator(".unit-header").all()
    for header in unit_headers:
        header.click()
    
    # For each item in test data, find its corresponding document in the UI
    for item in test_items:
        # Find the document container by its unique title
        document_title = item['Dokumentnamn']
        document_container = setup_page.locator(f"h3:has-text('{document_title}')").first
        expect(document_container).to_be_visible()
        
        # Get the parent container that has all metadata
        parent_container = document_container.locator('xpath=./..').first
        
        # Check that professional role is displayed (somewhere in this document's container)
        professional_role = item['Dokument_skapad_av_yrkestitel_Namn']
        expect(parent_container.locator(f":text('{professional_role}')").first).to_be_visible()
        
        # Check that document type is displayed
        doc_type = item['Dokumentationskod']
        expect(parent_container.locator(f":text('{doc_type}')").first).to_be_visible()

def test_1_4_tom_lista(setup_page: Page):
    """Test 1.4: Tom lista - Ingen journaldata visas när listan är tom"""
    # Mock the fetch response to return an empty list
    setup_page.route("**/api/journals", lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body=json.dumps([])
    ))
    
    # Refresh the page to trigger the empty state
    setup_page.reload()
    
    # Check if the listview is empty
    unit_groups = setup_page.locator(".unit-group")
    expect(unit_groups).to_have_count(0)

def test_1_6_gruppering(setup_page: Page, test_items):
    """Test 1.6: Gruppering - Journaler grupperas efter vårdenhet"""
    # Get all unique units from test data
    unique_units = set(item["Vårdenhet_Namn"] for item in test_items)
    
    # Check that each unit has a group header
    for unit in unique_units:
        unit_header = setup_page.locator(f".unit-header:has-text('{unit}')")
        expect(unit_header).to_be_visible()
        
        # Verify item count in header matches data
        unit_items_count = len([item for item in test_items if item["Vårdenhet_Namn"] == unit])
        count_text = setup_page.locator(f".unit-header:has-text('{unit}') .item-count").text_content()
        assert f"({unit_items_count})" in count_text, f"Expected {unit_items_count} items for unit {unit}"

def test_1_7_kollapsa_grupp(setup_page: Page):
    """Test 1.7: Kollapsa grupp - Gruppen kollapsar när man klickar på rubriken"""
    # First expand a group
    first_unit = setup_page.locator(".unit-header").first
    first_unit.click()
    
    # Verify group is expanded
    unit_items = setup_page.locator(".unit-items")
    expect(unit_items).to_be_visible()
    expect(first_unit).to_have_attribute("aria-expanded", "true")
    
    # Click to collapse
    first_unit.click()
    
    # Verify group is collapsed
    expect(setup_page.locator(".unit-items")).to_have_count(0)
    expect(first_unit).to_have_attribute("aria-expanded", "false")

def test_1_8_expandera_grupp(setup_page: Page, test_items):
    """Test 1.8: Expandera grupp - Gruppen expanderar och visar alla journaler"""
    # Initially all groups should be collapsed
    expect(setup_page.locator(".unit-items")).to_have_count(0)
    
    # Get all unit headers
    unit_headers = setup_page.locator(".unit-header").all()
    
    # Click each header to expand
    for header in unit_headers:
        unit_name = header.locator(".unit-name").text_content()
        
        # Verify initially collapsed
        expect(header).to_have_attribute("aria-expanded", "false")
        
        # Click to expand
        header.click()
        
        # Verify this specific group is expanded by checking its items
        items_in_group = setup_page.locator(f".unit-group:has-text('{unit_name}') .unit-items")
        expect(items_in_group).to_be_visible()
        expect(header).to_have_attribute("aria-expanded", "true")
        
        # Verify all documents for this unit are shown
        unit_documents = [item for item in test_items if item["Vårdenhet_Namn"] == unit_name]
        items_in_group = setup_page.locator(f".unit-group:has-text('{unit_name}') .unit-items li")
        expect(items_in_group).to_have_count(len(unit_documents))

# Section 2: Interaktion
def test_2_1_markera_journal(setup_page: Page):
    """Test 2.1: Markera journal - Klick på en journal markerar den med blå kant och bakgrund"""
    # Expand all units first
    unit_headers = setup_page.locator(".unit-header").all()
    for header in unit_headers:
        header.click()
    
    # Click on the first document button
    first_document = setup_page.locator(".document-button").first
    first_document.click()
    
    # Check selection status by inspecting the class attribute
    class_attr = first_document.evaluate("el => el.className")
    assert "selected" in class_attr, "Expected 'selected' class to be present"
    
    # Also check the aria attribute
    document_li = setup_page.locator(".unit-items li").first
    expect(document_li).to_have_attribute("aria-selected", "true")

def test_2_2_avmarkera_journal(setup_page: Page):
    """Test 2.2: Avmarkera journal - Klick utanför markerad journal avmarkerar den"""
    # Expand all units first
    unit_headers = setup_page.locator(".unit-header").all()
    for header in unit_headers:
        header.click()
    
    # Select a document
    first_document = setup_page.locator(".document-button").first
    first_document.click()
    
    # Check selection status
    class_attr = first_document.evaluate("el => el.className")
    assert "selected" in class_attr, "Expected 'selected' class to be present"
    
    # Click outside the document list (on the page body)
    setup_page.click("body", position={"x": 10, "y": 10})
    
    # Verify document is no longer selected
    class_attr = first_document.evaluate("el => el.className")
    assert "selected" not in class_attr, "Expected 'selected' class to be absent"
    
    # Also verify the aria attribute
    document_li = setup_page.locator(".unit-items li").first
    expect(document_li).to_have_attribute("aria-selected", "false")

def test_2_3_markera_flera_journaler(setup_page: Page):
    """Test 2.3: Markera flera journaler - Ctrl+klick på flera journaler markerar samtliga"""
    # Expand all units first
    unit_headers = setup_page.locator(".unit-header").all()
    for header in unit_headers:
        header.click()
    
    # Get the first two document buttons
    documents = setup_page.locator(".document-button").all()
    
    # Make sure we have at least two documents to test with
    assert len(documents) >= 2, "Need at least 2 documents to test multiple selection"
    
    # Select the first document
    documents[0].click()
    
    # Use Meta key (Cmd on macOS) for multi-selection
    setup_page.keyboard.down("Meta")  # Command key on macOS
    documents[1].click()
    setup_page.keyboard.up("Meta")
    
    # Verify both documents are selected
    class_attr1 = documents[0].evaluate("el => el.className")
    class_attr2 = documents[1].evaluate("el => el.className")
    assert "selected" in class_attr1, "Expected 'selected' class to be present in first document"
    assert "selected" in class_attr2, "Expected 'selected' class to be present in second document"
    
    # Also verify the aria attribute for both
    document_items = setup_page.locator(".unit-items li").all()
    expect(document_items[0]).to_have_attribute("aria-selected", "true")
    expect(document_items[1]).to_have_attribute("aria-selected", "true") 
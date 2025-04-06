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

def test_listview_exists(setup_page: Page):
    """Test that the listview component exists and is visible"""
    list_container = setup_page.locator("ul.list-view")
    expect(list_container).to_be_visible()

def test_listview_renders_items(setup_page: Page, sorted_items):
    """Test that items are correctly rendered in the listview"""
    # Check if all unit groups are rendered
    unit_groups = setup_page.locator(".unit-group")
    expect(unit_groups).to_have_count(3)  # One for each unique unit
    
    # Check unit headers
    for item in sorted_items:
        unit_header = setup_page.locator(f".unit-header:has-text('{item['Vårdenhet_Namn']}')")
        expect(unit_header).to_be_visible()

def test_listview_chronological_order(setup_page: Page):
    """Test that items are displayed in chronological order (newest first)"""
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

def test_unit_grouping(setup_page: Page, test_items):
    """Test that documents are grouped by healthcare unit"""
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

def test_collapse_group(setup_page: Page):
    """Test that clicking a unit header collapses the group"""
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

def test_expand_group(setup_page: Page, test_items):
    """Test that clicking unit headers expands the groups"""
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

def test_empty_listview(setup_page: Page):
    """Test that the listview is empty when there are no items"""
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
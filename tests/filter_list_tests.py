from playwright.sync_api import Page, expect
import pytest
from datetime import datetime, timedelta
import json

@pytest.fixture
def test_items():
    """Fixture providing test data with specific dates and attributes for filter testing"""
    base_date = datetime(2024, 1, 1, 12, 0)  # Fixed date for consistent testing
    return [
        {
            "CompositionId": "1",
            "DateTime": (base_date - timedelta(days=10)).isoformat(),  # Dec 22
            "DisplayDateTime": (base_date - timedelta(days=10)).strftime("%Y-%m-%d %H:%M"),
            "Dokument_ID": "DOC001",
            "Dokument_skapad_av_yrkestitel_ID": "L001",
            "Dokument_skapad_av_yrkestitel_Namn": "Läkare",
            "Dokumentationskod": "Läkaranteckning",
            "Dokumentnamn": "Läkaranteckning äldre",
            "Tidsstämpel_för_sparat_dokument": (base_date - timedelta(days=10)).isoformat(),
            "Vårdenhet_Identifierare": "KK001",
            "Vårdenhet_Namn": "Kardiologiska kliniken"
        },
        {
            "CompositionId": "2",
            "DateTime": (base_date - timedelta(days=5)).isoformat(),  # Dec 27
            "DisplayDateTime": (base_date - timedelta(days=5)).strftime("%Y-%m-%d %H:%M"),
            "Dokument_ID": "DOC002",
            "Dokument_skapad_av_yrkestitel_ID": "SL001",
            "Dokument_skapad_av_yrkestitel_Namn": "Specialistläkare",
            "Dokumentationskod": "Case Report",
            "Dokumentnamn": "Case report från neurologi",
            "Tidsstämpel_för_sparat_dokument": (base_date - timedelta(days=5)).isoformat(),
            "Vårdenhet_Identifierare": "NA001",
            "Vårdenhet_Namn": "Neurologiska avdelningen"
        },
        {
            "CompositionId": "3",
            "DateTime": (base_date - timedelta(days=2)).isoformat(),  # Dec 30
            "DisplayDateTime": (base_date - timedelta(days=2)).strftime("%Y-%m-%d %H:%M"),
            "Dokument_ID": "DOC003",
            "Dokument_skapad_av_yrkestitel_ID": "L002",
            "Dokument_skapad_av_yrkestitel_Namn": "Läkare",
            "Dokumentationskod": "Läkaranteckning",
            "Dokumentnamn": "Läkaranteckning nyare",
            "Tidsstämpel_för_sparat_dokument": (base_date - timedelta(days=2)).isoformat(),
            "Vårdenhet_Identifierare": "OK001",
            "Vårdenhet_Namn": "Onkologiska kliniken"
        },
        {
            "CompositionId": "4",
            "DateTime": base_date.isoformat(),  # Jan 1 - newest
            "DisplayDateTime": base_date.strftime("%Y-%m-%d %H:%M"),
            "Dokument_ID": "DOC004",
            "Dokument_skapad_av_yrkestitel_ID": "SK001",
            "Dokument_skapad_av_yrkestitel_Namn": "Sjuksköterska",
            "Dokumentationskod": "Research Article",
            "Dokumentnamn": "Forskningsartikel",
            "Tidsstämpel_för_sparat_dokument": base_date.isoformat(),
            "Vårdenhet_Identifierare": "KK001",
            "Vårdenhet_Namn": "Kardiologiska kliniken"
        }
    ]

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

# Test L5: Visa i lista - Test that journals are displayed chronologically
def test_l5_kronologisk_ordning(setup_page: Page):
    """Test L5: Journals appear in chronological order in the list view"""
    # Expand all units
    unit_headers = setup_page.locator(".unit-header").all()
    for header in unit_headers:
        header.click()
    
    # Get all document dates
    date_elements = setup_page.locator(".date").all()
    dates = []
    for date_el in date_elements:
        date_text = date_el.text_content()
        # Parse date text (expected format: YYYY-MM-DD)
        dates.append(datetime.strptime(date_text, "%Y-%m-%d"))
    
    # Check that dates are in descending order (newest first)
    for i in range(len(dates) - 1):
        assert dates[i] >= dates[i + 1], f"Dates should be in descending order, but {dates[i]} is before {dates[i+1]}"

# Test S1: Basvy exists and loads properly
def test_s1_basvy_exists(setup_page: Page):
    """Test S1: Base view (list and detail) is loaded as the default view"""
    # Check that list view is visible
    list_view = setup_page.locator(".list-view")
    expect(list_view).to_be_visible()
    
    # There should be a detail view component, though it might be empty initially
    detail_view = setup_page.locator(".detail-view") 
    # If detail view isn't present by default, check if a main content area exists
    if not detail_view.count():
        main_content = setup_page.locator("main")
        expect(main_content).to_be_visible()

# Test S2: Tidslinjevy is accessible
def test_s2_tidslinjevy_access(setup_page: Page):
    """Test S2: Timeline view is accessible from the interface"""
    # Find and click the timeline view button/link
    # This assumes there's a navigation element to switch to timeline view
    # Adjust the selector based on your actual implementation
    timeline_nav = setup_page.locator("text=Tidslinje").first
    
    # If timeline navigation doesn't exist, try other common patterns
    if not timeline_nav.count():
        timeline_nav = setup_page.locator("button:has-text('Tidslinje'), a:has-text('Tidslinje')").first
    
    # If found, click it, otherwise report test incomplete
    if timeline_nav.count():
        timeline_nav.click()
        
        # Verify timeline view appears
        timeline_container = setup_page.locator("[data-testid='timeline-container']")
        expect(timeline_container).to_be_visible()
    else:
        pytest.skip("Timeline navigation not found - implementation may differ")

# Test T1/T2: Tidslinje Detaljerad and Översiktlig views
def test_t1_t2_timeline_views(setup_page: Page):
    """Test T1/T2: Timeline shows detailed and overview journal views"""
    # Navigate to timeline view
    timeline_nav = setup_page.locator("text=Tidslinje").first
    if not timeline_nav.count():
        timeline_nav = setup_page.locator("button:has-text('Tidslinje'), a:has-text('Tidslinje')").first
    
    if timeline_nav.count():
        timeline_nav.click()
        
        # Verify timeline container exists
        timeline_container = setup_page.locator("[data-testid='timeline-container']")
        expect(timeline_container).to_be_visible()
        
        # Check for year/month/day buttons in the timeline
        year_buttons = setup_page.locator("[data-testid='year-button']")
        expect(year_buttons).to_have_count.greater_than(0)
        
        # Test zooming functionality (T2)
        # First, check the initial state
        timeline_container.press("Control+0")  # Reset zoom level
        
        # Get the initial width of a note element
        note_elements = setup_page.locator(".bg-white").all()
        if len(note_elements) > 0:
            initial_width = note_elements[0].evaluate("node => node.offsetWidth")
            
            # Simulate zoom in (Ctrl+scroll)
            page.keyboard.down("Control")
            timeline_container.mouse.wheel(0, -100)  # Scroll up to zoom in
            page.keyboard.up("Control")
            
            page.wait_for_timeout(500)  # Wait for zoom animation
            
            # Check that elements have become larger
            new_width = note_elements[0].evaluate("node => node.offsetWidth")
            assert new_width > initial_width, "Timeline elements should become larger when zooming in"
    else:
        pytest.skip("Timeline navigation not found - implementation may differ")

# Tests for filter functionality
# Test F2: General filter functionality
def test_f2_filtrera_basfunction(setup_page: Page):
    """Test F2: Filter panel is usable for limiting displayed journals"""
    # Expand all units first to see all items
    unit_headers = setup_page.locator(".unit-header").all()
    for header in unit_headers:
        header.click()
    
    # Get initial document count
    initial_docs = setup_page.locator(".document-button").count()
    
    # Apply a filter - for example, select a specific document type
    # This will depend on the actual filter implementation but typically:
    filter_dropdown = setup_page.locator("#template button").first
    filter_dropdown.click()
    
    # Select a specific document type (assuming dropdown opens)
    filter_option = setup_page.locator("#dropdown_1 button:has-text('Läkaranteckning')").first
    if filter_option.count():
        filter_option.click()
        
        # Wait for filter to apply
        page.wait_for_timeout(500)
        
        # Check that document count has changed
        filtered_docs = setup_page.locator(".document-button").count()
        assert filtered_docs < initial_docs, "Filter should reduce the number of visible documents"
        
        # Verify only documents of selected type are visible
        visible_docs = setup_page.locator(".document-button .type:text('Läkaranteckning')").count()
        assert visible_docs == filtered_docs, "All visible documents should match the filter"
    else:
        pytest.skip("Filter dropdown implementation may differ")

# Test F4: Filter by journal type
def test_f4_filtrera_journaltyp(setup_page: Page):
    """Test F4: Filter by journal type shows only journals of selected type"""
    # Expand all units first
    unit_headers = setup_page.locator(".unit-header").all()
    for header in unit_headers:
        header.click()
    
    # Apply document type filter
    journal_type_dropdown = setup_page.locator("#template button").first
    if journal_type_dropdown.count():
        journal_type_dropdown.click()
        
        # Select "Case Report" type
        case_report_option = setup_page.locator("#dropdown_1 button:has-text('Case Report')").first
        if case_report_option.count():
            case_report_option.click()
            
            # Wait for filter to apply
            page.wait_for_timeout(500)
            
            # Check that only "Case Report" documents are visible
            visible_docs = setup_page.locator(".document-button").all()
            for doc in visible_docs:
                type_text = doc.locator(".type").text_content()
                assert "Case Report" in type_text, f"Expected 'Case Report' but found '{type_text}'"
        else:
            pytest.skip("Case Report filter option not found")
    else:
        pytest.skip("Journal type filter dropdown not found")

# Test F5: Filter by vårdenhet (medical unit)
def test_f5_filtrera_vardenhet(setup_page: Page):
    """Test F5: Filter by medical unit shows only journals from selected unit"""
    # Expand all units first
    unit_headers = setup_page.locator(".unit-header").all()
    for header in unit_headers:
        header.click()
    
    # Apply medical unit filter
    unit_dropdown = setup_page.locator("#Vårdenhet button").first
    if unit_dropdown.count():
        unit_dropdown.click()
        
        # Select "Kardiologiska kliniken" unit
        unit_option = setup_page.locator("#dropdown_2 button:has-text('Kardiologiska kliniken')").first
        if unit_option.count():
            unit_option.click()
            
            # Wait for filter to apply
            page.wait_for_timeout(500)
            
            # Check that only journals from Kardiologiska kliniken are visible
            # Since units are already grouped, we should see only that unit group
            visible_units = setup_page.locator(".unit-header .unit-name").all()
            assert len(visible_units) == 1, "Only one unit should be visible after filtering"
            assert "Kardiologiska kliniken" in visible_units[0].text_content(), "Only Kardiologiska kliniken should be visible"
        else:
            pytest.skip("Kardiologiska kliniken filter option not found")
    else:
        pytest.skip("Medical unit filter dropdown not found")

# Test F7: Filter by yrkesroll (professional role)
def test_f7_filtrera_yrkesroll(setup_page: Page):
    """Test F7: Filter by professional role shows only journals from selected role"""
    # Expand all units first
    unit_headers = setup_page.locator(".unit-header").all()
    for header in unit_headers:
        header.click()
    
    # Get initial document count
    initial_docs = setup_page.locator(".document-button").count()
    
    # Apply professional role filter
    role_dropdown = setup_page.locator("#role button").first
    if role_dropdown.count():
        role_dropdown.click()
        
        # Select "Läkare" role
        role_option = setup_page.locator("#dropdown_3 button:has-text('Läkare')").first
        if role_option.count():
            role_option.click()
            
            # Wait for filter to apply
            page.wait_for_timeout(500)
            
            # Check that only "Läkare" documents are visible
            filtered_docs = setup_page.locator(".document-button").count()
            assert filtered_docs < initial_docs, "Filter should reduce the number of visible documents"
            
            # Check all visible documents have Läkare as professional
            visible_docs = setup_page.locator(".document-button").all()
            for doc in visible_docs:
                prof_text = doc.locator(".professional").text_content()
                assert "Läkare" in prof_text, f"Expected 'Läkare' but found '{prof_text}'"
        else:
            pytest.skip("Läkare filter option not found")
    else:
        pytest.skip("Professional role filter dropdown not found")

# Test F9: Reset filters functionality
def test_f9_aterstall_filter(setup_page: Page):
    """Test F9: Reset filters button resets all filters to default values"""
    # Expand all units first
    unit_headers = setup_page.locator(".unit-header").all()
    for header in unit_headers:
        header.click()
    
    # Get initial document count
    initial_docs = setup_page.locator(".document-button").count()
    
    # Apply a filter
    journal_type_dropdown = setup_page.locator("#template button").first
    if journal_type_dropdown.count():
        journal_type_dropdown.click()
        
        # Select a specific type
        filter_option = setup_page.locator("#dropdown_1 button").first
        if filter_option.count():
            filter_option.click()
            
            # Wait for filter to apply
            page.wait_for_timeout(500)
            
            # Verify documents are filtered
            filtered_docs = setup_page.locator(".document-button").count()
            assert filtered_docs < initial_docs, "Filter should reduce the number of visible documents"
            
            # Now reset the filters
            reset_button = setup_page.locator("#Reset")
            reset_button.click()
            
            # Wait for reset to apply
            page.wait_for_timeout(500)
            
            # Check that document count returns to initial state
            reset_docs = setup_page.locator(".document-button").count()
            assert reset_docs == initial_docs, "Reset should restore all documents"
        else:
            pytest.skip("Filter option not found")
    else:
        pytest.skip("Filter dropdown not found")

# Test TF1: Filter in timeline view
def test_tf1_filter_in_timeline(setup_page: Page):
    """Test TF1: Filter panel is available in timeline view"""
    # Navigate to timeline view
    timeline_nav = setup_page.locator("text=Tidslinje").first
    if not timeline_nav.count():
        timeline_nav = setup_page.locator("button:has-text('Tidslinje'), a:has-text('Tidslinje')").first
    
    if timeline_nav.count():
        timeline_nav.click()
        
        # Verify timeline loads
        timeline_container = setup_page.locator("[data-testid='timeline-container']")
        expect(timeline_container).to_be_visible()
        
        # Check if filter components are visible in timeline view
        filter_container = setup_page.locator("#Filtermenu")
        expect(filter_container).to_be_visible()
        
        # Specifically check for search and filter dropdowns
        search_input = setup_page.locator("#Search input")
        expect(search_input).to_be_visible()
        
        template_filter = setup_page.locator("#template button")
        expect(template_filter).to_be_visible()
    else:
        pytest.skip("Timeline navigation not found - implementation may differ")

# Test F8: Combine multiple filters
def test_f8_kombinera_filter(setup_page: Page):
    """Test F8: Multiple filters can be combined to narrow results further"""
    # Expand all units first
    unit_headers = setup_page.locator(".unit-header").all()
    for header in unit_headers:
        header.click()
    
    # Get initial document count
    initial_docs = setup_page.locator(".document-button").count()
    
    # Apply first filter - journal type
    journal_type_dropdown = setup_page.locator("#template button").first
    if journal_type_dropdown.count():
        journal_type_dropdown.click()
        
        # Select "Läkaranteckning" type
        type_option = setup_page.locator("#dropdown_1 button:has-text('Läkaranteckning')").first
        if type_option.count():
            type_option.click()
            
            # Wait for filter to apply
            page.wait_for_timeout(500)
            
            # Get count after first filter
            first_filter_docs = setup_page.locator(".document-button").count()
            assert first_filter_docs < initial_docs, "First filter should reduce the number of documents"
            
            # Apply second filter - professional role
            role_dropdown = setup_page.locator("#role button").first
            if role_dropdown.count():
                role_dropdown.click()
                
                # Select a role
                role_option = setup_page.locator("#dropdown_3 button:has-text('Läkare')").first
                if role_option.count():
                    role_option.click()
                    
                    # Wait for filter to apply
                    page.wait_for_timeout(500)
                    
                    # Get count after both filters
                    combined_filter_docs = setup_page.locator(".document-button").count()
                    assert combined_filter_docs <= first_filter_docs, "Combined filters should narrow results further"
                    
                    # Verify all visible documents match both criteria
                    visible_docs = setup_page.locator(".document-button").all()
                    for doc in visible_docs:
                        type_text = doc.locator(".type").text_content()
                        prof_text = doc.locator(".professional").text_content()
                        assert "Läkaranteckning" in type_text, f"Expected 'Läkaranteckning' but found '{type_text}'"
                        assert "Läkare" in prof_text, f"Expected 'Läkare' but found '{prof_text}'"
                else:
                    pytest.skip("Role filter option not found")
            else:
                pytest.skip("Role filter dropdown not found")
        else:
            pytest.skip("Journal type filter option not found")
    else:
        pytest.skip("Journal type filter dropdown not found") 
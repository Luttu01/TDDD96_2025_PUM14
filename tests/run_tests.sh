#!/bin/bash

# Run tests shell script
# Usage: ./run_tests.sh [filter|document_view|listvy|all]

# Set up colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Create results directory if it doesn't exist
mkdir -p tests/unittests/results

# Function to run tests
run_tests() {
    TEST_TYPE=$1
    REPORT_NAME=$2
    
    echo -e "${YELLOW}Running $TEST_TYPE tests...${NC}"
    
    if [ "$TEST_TYPE" == "all" ]; then
        python3 -m pytest tests/unittests/ --html=tests/unittests/results/$REPORT_NAME.html --self-contained-html
    else
        python3 -m pytest tests/unittests/test_$TEST_TYPE.py --html=tests/unittests/results/$REPORT_NAME.html --self-contained-html
    fi
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ $TEST_TYPE tests passed!${NC}"
        echo -e "${GREEN}Report generated at: tests/unittests/results/$REPORT_NAME.html${NC}"
    else
        echo -e "${RED}✗ $TEST_TYPE tests failed!${NC}"
        echo -e "${RED}Check the report at: tests/unittests/results/$REPORT_NAME.html${NC}"
    fi
}

# Main script logic
TEST_PARAM=${1:-all}

case $TEST_PARAM in
    filter)
        run_tests "filter" "filter_report"
        ;;
    document_view)
        run_tests "document_view" "document_view_report"
        ;;
    listvy)
        run_tests "listvy" "listvy_report"
        ;;
    all)
        run_tests "all" "full_report"
        ;;
    *)
        echo -e "${RED}Invalid test type. Use: filter, document_view, listvy, or all${NC}"
        exit 1
        ;;
esac

echo -e "${YELLOW}Test execution completed.${NC}" 
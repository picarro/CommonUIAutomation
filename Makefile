.PHONY: help install test test-visual test-interaction test-state test-snapshot test-all clean setup

help:
	@echo "Storybook Automation Framework - Available Commands:"
	@echo ""
	@echo "  make setup          - Set up the project (install dependencies, browsers)"
	@echo "  make install        - Install Python dependencies"
	@echo "  make test           - Run all tests"
	@echo "  make test-visual    - Run visual regression tests"
	@echo "  make test-interaction - Run interaction tests"
	@echo "  make test-state     - Run state tests"
	@echo "  make test-snapshot  - Run snapshot tests"
	@echo "  make test-controls  - Run Storybook controls tests"
	@echo "  make test-property  - Run property checker tests"
	@echo "  make test-all       - Run all tests with HTML report"
	@echo "  make test-visible   - Run tests with visible browser"
	@echo "  make test-controls-visible - Run controls tests with visible browser"
	@echo "  make clean          - Clean generated files (screenshots, snapshots, reports)"
	@echo "  make browsers       - Install Playwright browsers"

setup:
	@bash setup.sh

install:
	@pip install -r requirements.txt

browsers:
	@playwright install

test:
	@pytest

test-visual:
	@pytest -m visual

test-interaction:
	@pytest -m interaction

test-state:
	@pytest -m state

test-snapshot:
	@pytest -m snapshot

test-controls:
	@pytest -m controls

test-property:
	@pytest -m property

test-visible:
	@HEADLESS=false SLOW_MO=300 pytest -v -s

test-controls-visible:
	@HEADLESS=false SLOW_MO=300 pytest -m controls -v -s

test-property-visible:
	@HEADLESS=false SLOW_MO=300 pytest -m property -v -s

test-all:
	@pytest --html=reports/report.html --self-contained-html

clean:
	@rm -rf screenshots/* snapshots/* reports/*
	@find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@echo "Cleaned generated files"


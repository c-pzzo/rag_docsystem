# tests/test_parser.py

import pytest
from src.processing.parser import READMEParser

def test_parse_basic_readme():
    # Sample README content
    readme_content = """# [TS-ML-2024-001] Time Series Forecasting API

## Overview
API service for sales forecasting using SARIMA and Prophet models. Provides endpoints for both single-item and bulk predictions of final sale prices.

## Key Features
- Multi-model forecasting
- Handles seasonal patterns

## Technical Stack
- Python 3.10
- FastAPI"""

    parser = READMEParser(readme_content)
    result = parser.parse()
    
    assert result['project_id'] == 'TS-ML-2024-001'
    assert result['name'] == 'Time Series Forecasting API'
    assert 'API service for sales forecasting' in result['sections']['overview']
    assert result['full_content'] == readme_content

def test_invalid_readme_format():
    # README without project ID
    invalid_content = """# Simple Project
## Overview
Some overview text"""
    
    parser = READMEParser(invalid_content)
    with pytest.raises(ValueError) as exc_info:
        parser.parse()
    assert "Project ID not found" in str(exc_info.value)

def test_missing_overview_section():
    # README without overview
    content_no_overview = """# [TS-ML-2024-001] Project Name
## Key Features
Some features"""
    
    parser = READMEParser(content_no_overview)
    with pytest.raises(ValueError) as exc_info:
        parser.parse()
    assert "Overview section not found" in str(exc_info.value)
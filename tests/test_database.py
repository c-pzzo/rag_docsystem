# tests/test_database.py

import pytest
from src.database.operations import MongoDB
from src.processing.parser import READMEParser
from src.processing.embeddings import TextEmbeddings

def test_database_connection():
    db = MongoDB()
    assert db.test_connection() == True

def test_project_insertion():
    db = MongoDB()
    
    # Create test data
    test_readme = """# [TEST-001] Test Project
    
## Overview
Test project overview
    """
    
    # Parse README
    parser = READMEParser(test_readme)
    parsed_data = parser.parse()
    
    # Generate embeddings
    embedder = TextEmbeddings()
    embedded_sections = embedder.generate_section_embeddings(parsed_data['sections'])
    
    # Add embeddings to parsed data
    parsed_data['sections'] = embedded_sections
    
    # Insert into DB
    result = db.insert_project(parsed_data)
    assert result == True
    
    # Clean up
    db.delete_project('TEST-001')

def test_duplicate_project():
    db = MongoDB()
    
    test_data = {
        'project_id': 'TEST-002',
        'name': 'Test Project',
        'sections': {
            'overview': {
                'content': 'Test overview',
                'vector': [0.1, 0.2, 0.3]
            }
        }
    }
    
    # First insertion should succeed
    assert db.insert_project(test_data) == True
    
    # Second insertion should fail
    with pytest.raises(ValueError) as exc_info:
        db.insert_project(test_data)
    assert "Project already exists" in str(exc_info.value)
    
    # Clean up
    db.delete_project('TEST-002')
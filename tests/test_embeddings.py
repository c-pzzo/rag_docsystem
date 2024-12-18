# tests/test_embeddings.py

import pytest
from src.processing.embeddings import TextEmbeddings

def test_embedding_generation():
    embedder = TextEmbeddings()
    text = "This is a test overview section"
    embedding = embedder.generate_embedding(text)
    
    # Check if embedding is a list of floats with the expected dimension
    assert isinstance(embedding, list)
    assert all(isinstance(x, float) for x in embedding)
    assert len(embedding) > 0  # Should have proper dimension

def test_empty_text():
    embedder = TextEmbeddings()
    with pytest.raises(ValueError) as exc_info:
        embedder.generate_embedding("")
    assert "Empty text cannot be embedded" in str(exc_info.value)

def test_section_embeddings():
    embedder = TextEmbeddings()
    sections = {
        'overview': 'This is the overview section',
        'key_features': 'These are the key features'
    }
    
    embedded_sections = embedder.generate_section_embeddings(sections)
    
    assert 'overview' in embedded_sections
    assert 'vector' in embedded_sections['overview']
    assert 'content' in embedded_sections['overview']
    assert isinstance(embedded_sections['overview']['vector'], list)
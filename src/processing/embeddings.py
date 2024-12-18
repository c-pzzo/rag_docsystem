# src/processing/embeddings.py

import os
from typing import Dict, List, Union
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

class TextEmbeddings:
    """Handler for generating embeddings from text using Google's Gemini."""
    
    def __init__(self):
        """Initialize the embeddings model."""
        load_dotenv()
        
        if not os.getenv('GOOGLE_API_KEY'):
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
            
        self.model = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",  # Gemini's embedding model
            task_type="retrieval_query",   # Optimized for search
            google_api_key=os.getenv('GOOGLE_API_KEY')
        )
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single piece of text.
        
        Args:
            text: String to generate embedding for
            
        Returns:
            List of floats representing the embedding
        """
        if not text.strip():
            raise ValueError("Empty text cannot be embedded")
            
        return self.model.embed_query(text)
    
    def generate_section_embeddings(
        self, 
        sections: Dict[str, str]
    ) -> Dict[str, Dict[str, Union[str, List[float]]]]:
        """
        Generate embeddings for multiple document sections.
        
        Args:
            sections: Dictionary of section name to content
            
        Returns:
            Dictionary of section names to their content and embeddings
        """
        embedded_sections = {}
        
        for section_name, content in sections.items():
            if content:  # Only process non-empty sections
                embedded_sections[section_name] = {
                    'content': content,
                    'vector': self.generate_embedding(content)
                }
                
        return embedded_sections

if __name__ == "__main__":
    # Example usage
    embedder = TextEmbeddings()
    
    # Test single embedding
    test_text = "This is a test overview section"
    embedding = embedder.generate_embedding(test_text)
    print(f"Generated embedding dimension: {len(embedding)}")
    
    # Test multiple sections
    test_sections = {
        'overview': 'This is the overview section',
        'key_features': 'These are the key features'
    }
    embedded_sections = embedder.generate_section_embeddings(test_sections)
    print("\nGenerated embeddings for sections:", list(embedded_sections.keys()))
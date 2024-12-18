# src/database/operations.py

import os
from typing import Dict, Any, List
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import numpy as np

class MongoDB:
    """Handler for MongoDB operations."""
    
    def __init__(self):
        """Initialize MongoDB connection."""
        load_dotenv()
        
        if not os.getenv('MONGODB_URI'):
            raise ValueError("MONGODB_URI not found in environment variables")
            
        self.client = MongoClient(
            os.getenv('MONGODB_URI'),
            server_api=ServerApi('1')
        )
        self.db = self.client.rag_system  # database name
        self.projects = self.db.projects   # collection name
        
        # Create unique index on project_id
        self.projects.create_index("project_id", unique=True)
    
    def test_connection(self) -> bool:
        """Test if connection is working."""
        try:
            self.client.admin.command('ping')
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False
    
    def insert_project(self, project_data: Dict[str, Any]) -> bool:
        """
        Insert a new project into the database.
        
        Args:
            project_data: Dictionary containing project information
            
        Returns:
            bool: True if successful, raises error otherwise
        """
        try:
            self.projects.insert_one(project_data)
            return True
        except Exception as e:
            if "duplicate key error" in str(e):
                raise ValueError("Project already exists")
            raise e
    
    def delete_project(self, project_id: str) -> bool:
        """Delete a project by its ID."""
        result = self.projects.delete_one({"project_id": project_id})
        return result.deleted_count > 0

    def get_project(self, project_id: str) -> Dict:
        """Retrieve a project by its ID."""
        return self.projects.find_one({"project_id": project_id})
        
    def search_projects(self, query_vector: list, limit: int = 3) -> list:
        """
        Search for projects using vector similarity.
        
        Args:
            query_vector: Embedded vector of the search query
            limit: Maximum number of results to return
            
        Returns:
            List of projects sorted by relevance
        """
        # Find all projects
        projects = list(self.projects.find({}))
        
        # Calculate similarity scores
        results = []
        for project in projects:
            if 'sections' in project and 'overview' in project['sections']:
                overview_vector = project['sections']['overview']['vector']
                # Calculate cosine similarity
                similarity = self._calculate_similarity(query_vector, overview_vector)
                
                results.append({
                    'project_id': project['project_id'],
                    'name': project['name'],
                    'overview': project['sections']['overview']['content'],
                    'similarity': similarity
                })
        
        # Sort by similarity score
        results.sort(key=lambda x: x['similarity'], reverse=True)
        
        return results[:limit]

    def _calculate_similarity(self, vec1: list, vec2: list) -> float:
        """Calculate cosine similarity between two vectors."""
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        
        cosine_sim = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
        normalized_score = (cosine_sim + 1) * 50
        return float(normalized_score)

    def __del__(self):
        """Close MongoDB connection when object is destroyed."""
        if hasattr(self, 'client'):
            self.client.close()
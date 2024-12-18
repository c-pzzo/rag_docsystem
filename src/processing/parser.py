# src/processing/parser.py

import re
from typing import Dict, Optional

class READMEParser:
    """Parser for standardized README files with project information."""
    
    def __init__(self, content: str):
        """Initialize parser with README content."""
        self.content = content
        self.sections = {}
    
    def _extract_project_id(self) -> tuple[str, str]:
        """Extract project ID and name from the title."""
        pattern = r'#\s*\[([^\]]+)\]\s*(.+)$'
        match = re.search(pattern, self.content, re.MULTILINE)
        
        if not match:
            raise ValueError("Project ID not found in README title")
            
        return match.group(1).strip(), match.group(2).strip()
    
    def _extract_section(self, section_name: str) -> Optional[str]:
        """Extract content of a specific section."""
        pattern = f'## {section_name}\\s+(.*?)(?=##|$)'
        match = re.search(pattern, self.content, re.DOTALL)
        
        if match:
            return match.group(1).strip()
        return None
    
    def parse(self) -> Dict:
        """
        Parse README content into structured format.
        
        Returns:
            Dict containing:
            - project_id: string
            - name: string
            - sections: dict of section contents
            - full_content: original README content
        """
        # Extract project ID and name
        project_id, name = self._extract_project_id()
        
        # Extract overview (required)
        overview = self._extract_section('Overview')
        if not overview:
            raise ValueError("Overview section not found in README")
            
        # Extract other sections
        sections = {
            'overview': overview,
            'key_features': self._extract_section('Key Features'),
            'technical_stack': self._extract_section('Technical Stack')
        }
        
        return {
            'project_id': project_id,
            'name': name,
            'sections': sections,
            'full_content': self.content
        }
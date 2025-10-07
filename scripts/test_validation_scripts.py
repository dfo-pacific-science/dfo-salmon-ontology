"""
Unit tests for validation scripts.
"""

import unittest
import os
import sys

# Add scripts directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))

class TestValidationScripts(unittest.TestCase):
    """Test cases for validation scripts."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.ontology_path = os.path.join(
            os.path.dirname(__file__), '..', '..', 'ontology', 'dfo-salmon.ttl'
        )
    
    def test_ontology_file_exists(self):
        """Test that the main ontology file exists."""
        self.assertTrue(os.path.exists(self.ontology_path), 
                       "Main ontology file should exist")
    
    def test_validation_script_exists(self):
        """Test that validation script exists."""
        script_path = os.path.join(
            os.path.dirname(__file__), '..', '..', 'scripts', 'test_shacl_validation.py'
        )
        self.assertTrue(os.path.exists(script_path), 
                       "SHACL validation script should exist")

if __name__ == '__main__':
    unittest.main()

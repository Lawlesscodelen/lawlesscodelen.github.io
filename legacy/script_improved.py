#!/usr/bin/env python3
"""
Static site generator for personal website.
Generates HTML files from Jinja2 templates and JSON configuration.
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional

from jinja2 import Environment, FileSystemLoader
from markdown2 import markdown


class SiteGenerator:
    """Generates static HTML pages from templates and configuration."""
    
    def __init__(self, config_path: str = 'config.json', template_dir: str = './env'):
        """Initialize the site generator.
        
        Args:
            config_path: Path to the JSON configuration file
            template_dir: Directory containing Jinja2 templates
        """
        self.config_path = Path(config_path)
        self.template_dir = Path(template_dir)
        self.config: Dict[str, Any] = {}
        self.env: Optional[Environment] = None
        
    def load_config(self) -> bool:
        """Load configuration from JSON file.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.config_path.exists():
                print(f"Error: Configuration file {self.config_path} not found")
                return False
                
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            return True
            
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in {self.config_path}: {e}")
            return False
        except Exception as e:
            print(f"Error reading configuration: {e}")
            return False
    
    def setup_templates(self) -> bool:
        """Setup Jinja2 template environment.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.template_dir.exists():
                print(f"Error: Template directory {self.template_dir} not found")
                return False
                
            self.env = Environment(loader=FileSystemLoader(str(self.template_dir)))
            return True
            
        except Exception as e:
            print(f"Error setting up templates: {e}")
            return False
    
    def generate_page(self, template_name: str, output_file: str, 
                     page_name: str, **kwargs) -> bool:
        """Generate a single HTML page.
        
        Args:
            template_name: Name of the template file
            output_file: Output HTML file path
            page_name: Name of the page for navigation
            **kwargs: Additional template variables
            
        Returns:
            True if successful, False otherwise
        """
        try:
            template = self.env.get_template(template_name)
            
            # Prepare template variables
            template_vars = {
                'config': self.config,
                'page_name': page_name,
                **kwargs
            }
            
            # Render and write
            output_path = Path(output_file)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(template.render(**template_vars))
            
            print(f"Generated: {output_file}")
            return True
            
        except Exception as e:
            print(f"Error generating {output_file}: {e}")
            return False
    
    def generate_all_pages(self) -> bool:
        """Generate all website pages.
        
        Returns:
            True if all pages generated successfully, False otherwise
        """
        pages_config = [
            # (template, output_file, page_name, extra_vars)
            ('portada.html', 'index.html', 'index', {}),
            ('cuadro.html', 'sobremi.html', 'sobremi', {}),
            ('lista.html', 'articulos.html', 'articulos', {'items': self.config.get('articulos', [])}),
            ('lista.html', 'libros.html', 'libros', {'items': self.config.get('libros', [])}),
            ('lista.html', 'videos.html', 'videos', {'items': self.config.get('videos', [])}),
        ]
        
        success = True
        for template, output, page_name, extra_vars in pages_config:
            if not self.generate_page(template, output, page_name, **extra_vars):
                success = False
        
        return success
    
    def validate_config(self) -> List[str]:
        """Validate configuration structure.
        
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        required_sections = ['web_metadata', 'navbar']
        
        for section in required_sections:
            if section not in self.config:
                errors.append(f"Missing required section: {section}")
        
        # Validate web_metadata
        if 'web_metadata' in self.config:
            required_metadata = ['title', 'description', 'url']
            for field in required_metadata:
                if field not in self.config['web_metadata']:
                    errors.append(f"Missing required field in web_metadata: {field}")
        
        # Check for content sections
        content_sections = ['articulos', 'libros', 'videos']
        for section in content_sections:
            if section in self.config:
                items = self.config[section]
                if not isinstance(items, list):
                    errors.append(f"Section {section} should be a list")
                else:
                    for i, item in enumerate(items):
                        if not isinstance(item, dict):
                            errors.append(f"Item {i} in {section} should be an object")
                        elif 'title' not in item:
                            errors.append(f"Item {i} in {section} missing required field: title")
        
        return errors
    
    def build(self) -> bool:
        """Build the complete website.
        
        Returns:
            True if successful, False otherwise
        """
        print("Starting website build...")
        
        # Load configuration
        if not self.load_config():
            return False
        
        # Validate configuration
        errors = self.validate_config()
        if errors:
            print("Configuration validation errors:")
            for error in errors:
                print(f"  - {error}")
            return False
        
        # Setup templates
        if not self.setup_templates():
            return False
        
        # Generate all pages
        if not self.generate_all_pages():
            return False
        
        print("Website build completed successfully!")
        return True


def main():
    """Main entry point."""
    generator = SiteGenerator()
    
    if not generator.build():
        sys.exit(1)


if __name__ == '__main__':
    main()
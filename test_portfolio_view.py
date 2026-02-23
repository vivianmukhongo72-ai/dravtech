#!/usr/bin/env python
"""
Simple test script to verify portfolio category functionality.
Run this with: python test_portfolio_view.py
"""

import os
import sys
import django

# Setup Django environment
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'DravTech'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DravTech.settings')
django.setup()

from django.test import Client
from django.urls import reverse
from main.models import Service, Project


def test_portfolio_view():
    """Test the home view with portfolio data."""
    print("Testing Portfolio Category Functionality")
    print("=" * 50)
    
    client = Client()
    
    # Test home page
    response = client.get(reverse('home'))
    
    print(f"Home page status: {response.status_code}")
    
    if response.status_code == 200:
        context = response.context
        
        # Check if portfolio data is in context
        if 'projects' in context:
            projects = context['projects']
            print(f"✓ Projects in context: {len(projects)}")
        else:
            print("✗ Projects NOT found in context")
        
        if 'categories' in context:
            categories = context['categories']
            print(f"✓ Categories in context: {len(categories)}")
            for cat in categories:
                print(f"  - {cat.title} (slug: {cat.slug})")
        else:
            print("✗ Categories NOT found in context")
        
        if 'projects_by_category' in context:
            projects_by_category = context['projects_by_category']
            print(f"✓ Projects by category in context: {len(projects_by_category)} categories")
            for category, category_projects in projects_by_category.items():
                print(f"  - {category.title}: {len(category_projects)} projects")
        else:
            print("✗ Projects by category NOT found in context")
    
    # Test database state
    print("\nDatabase State:")
    print("-" * 20)
    
    services = Service.objects.filter(is_active=True)
    print(f"Active Services: {services.count()}")
    for service in services:
        project_count = Project.objects.filter(related_services=service, is_active=True).count()
        print(f"  - {service.title}: {project_count} projects")
    
    projects = Project.objects.filter(is_active=True)
    print(f"Active Projects: {projects.count()}")
    for project in projects:
        service_names = [s.title for s in project.related_services.filter(is_active=True)]
        print(f"  - {project.title}: {', '.join(service_names)}")
    
    print("\n✓ Test completed successfully!")
    return response


if __name__ == '__main__':
    try:
        test_portfolio_view()
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()

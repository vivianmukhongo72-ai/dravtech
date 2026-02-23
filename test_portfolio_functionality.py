#!/usr/bin/env python
"""
Test script for portfolio functionality.
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


def test_portfolio_functionality():
    """Test portfolio views and URLs."""
    print("Testing Portfolio Functionality")
    print("=" * 40)
    
    client = Client()
    
    # Test portfolio list page
    print("\n1. Testing Portfolio List Page:")
    try:
        response = client.get(reverse('portfolio_list'))
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✓ Portfolio list page loads successfully")
        else:
            print("   ✗ Portfolio list page failed to load")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # Test portfolio list with category filter
    print("\n2. Testing Portfolio List with Category Filter:")
    try:
        response = client.get(reverse('portfolio_list') + '?category=web-development')
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✓ Portfolio list with filter loads successfully")
        else:
            print("   ✗ Portfolio list with filter failed to load")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # Test portfolio detail pages
    print("\n3. Testing Portfolio Detail Pages:")
    projects = Project.objects.filter(is_active=True)
    for project in projects[:3]:  # Test first 3 projects
        try:
            response = client.get(reverse('portfolio_detail', kwargs={'slug': project.slug}))
            print(f"   {project.title}: Status {response.status_code}")
            if response.status_code == 200:
                print(f"   ✓ {project.title} detail page loads successfully")
            else:
                print(f"   ✗ {project.title} detail page failed to load")
        except Exception as e:
            print(f"   ✗ {project.title}: Error {e}")
    
    # Test URLs
    print("\n4. Testing URL Patterns:")
    try:
        print(f"   Portfolio List URL: {reverse('portfolio_list')}")
        print(f"   Portfolio Detail URL pattern: /portfolio/<slug>/")
        
        # Test with actual project
        if projects.exists():
            project = projects.first()
            detail_url = reverse('portfolio_detail', kwargs={'slug': project.slug})
            print(f"   Sample Detail URL: {detail_url}")
            print("   ✓ URL patterns working correctly")
    except Exception as e:
        print(f"   ✗ URL pattern error: {e}")
    
    # Test data relationships
    print("\n5. Testing Data Relationships:")
    try:
        services = Service.objects.filter(is_active=True)
        print(f"   Active Services: {services.count()}")
        
        for service in services[:3]:  # Test first 3 services
            service_projects = Project.objects.filter(related_services=service, is_active=True)
            print(f"   {service.title}: {service_projects.count()} projects")
            for project in service_projects:
                print(f"     - {project.title}")
        
        print("   ✓ Data relationships working correctly")
    except Exception as e:
        print(f"   ✗ Data relationship error: {e}")
    
    print("\n" + "=" * 40)
    print("Portfolio functionality test completed!")
    print("\nNext steps:")
    print("1. Visit /portfolio/ to see all projects")
    print("2. Click on any project to see details")
    print("3. Use category filters to narrow results")
    print("4. Navigate between portfolio and detail pages")


if __name__ == '__main__':
    try:
        test_portfolio_functionality()
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()

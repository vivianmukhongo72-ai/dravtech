#!/usr/bin/env python
"""
Test script for portfolio section with category-based display.
This script creates sample data and tests the portfolio functionality.
"""

import os
import sys
import django

# Setup Django environment
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DravTech.DravTech.settings')
django.setup()

from django.test import TestCase, Client
from django.urls import reverse
from django.utils.text import slugify
from main.models import Service, Project


def create_sample_data():
    """Create sample services and projects for testing."""
    print("Creating sample services...")
    
    # Create sample services (these will act as categories)
    services_data = [
        {
            'title': 'Web Development',
            'description': 'Custom web applications and websites built with modern technologies.',
            'icon_class': 'bi bi-globe',
            'is_featured': True,
            'display_order': 1
        },
        {
            'title': 'Mobile Apps',
            'description': 'Native and cross-platform mobile applications for iOS and Android.',
            'icon_class': 'bi bi-phone',
            'is_featured': True,
            'display_order': 2
        },
        {
            'title': 'Cybersecurity',
            'description': 'Security assessments, penetration testing, and security infrastructure.',
            'icon_class': 'bi bi-shield-check',
            'is_featured': True,
            'display_order': 3
        },
        {
            'title': 'Data Analytics',
            'description': 'Data visualization, business intelligence, and analytics solutions.',
            'icon_class': 'bi bi-graph-up',
            'is_featured': False,
            'display_order': 4
        }
    ]
    
    services = []
    for service_data in services_data:
        service, created = Service.objects.get_or_create(
            title=service_data['title'],
            defaults=service_data
        )
        services.append(service)
        print(f"{'Created' if created else 'Found'} service: {service.title}")
    
    print("\nCreating sample projects...")
    
    # Create sample projects linked to services
    projects_data = [
        {
            'title': 'E-Commerce Platform',
            'summary': 'A full-featured e-commerce platform with payment integration and inventory management.',
            'description': 'Built a scalable e-commerce solution for a retail client with advanced features including real-time inventory, multiple payment gateways, and admin dashboard.',
            'link': 'https://example-ecommerce.com',
            'is_featured': True,
            'display_order': 1,
            'services': ['Web Development', 'Data Analytics']
        },
        {
            'title': 'Banking Mobile App',
            'summary': 'Secure mobile banking application with biometric authentication.',
            'description': 'Developed a comprehensive mobile banking app with secure transactions, biometric login, and real-time notifications.',
            'link': 'https://example-bank.com',
            'is_featured': True,
            'display_order': 2,
            'services': ['Mobile Apps', 'Cybersecurity']
        },
        {
            'title': 'Security Audit System',
            'summary': 'Automated security vulnerability scanning and reporting platform.',
            'description': 'Created an enterprise security audit system that scans web applications for vulnerabilities and generates detailed reports.',
            'link': 'https://example-security.com',
            'is_featured': True,
            'display_order': 3,
            'services': ['Cybersecurity', 'Web Development']
        },
        {
            'title': 'Analytics Dashboard',
            'summary': 'Real-time business intelligence dashboard with interactive visualizations.',
            'description': 'Built a comprehensive analytics dashboard for tracking KPIs, generating reports, and visualizing business metrics.',
            'link': 'https://example-analytics.com',
            'is_featured': False,
            'display_order': 4,
            'services': ['Data Analytics', 'Web Development']
        },
        {
            'title': 'Healthcare App',
            'summary': 'Patient management mobile app for healthcare providers.',
            'description': 'Developed a HIPAA-compliant mobile application for patient management, appointment scheduling, and telemedicine.',
            'link': 'https://example-health.com',
            'is_featured': False,
            'display_order': 5,
            'services': ['Mobile Apps', 'Cybersecurity']
        }
    ]
    
    projects = []
    for project_data in projects_data:
        service_names = project_data.pop('services')
        
        project, created = Project.objects.get_or_create(
            title=project_data['title'],
            defaults=project_data
        )
        
        # Link services to project
        for service_name in service_names:
            try:
                service = Service.objects.get(title=service_name)
                project.related_services.add(service)
            except Service.DoesNotExist:
                print(f"Warning: Service '{service_name}' not found")
        
        projects.append(project)
        print(f"{'Created' if created else 'Found'} project: {project.title}")
    
    return services, projects


def test_portfolio_by_categories():
    """Test portfolio display grouped by categories (services)."""
    print("\n" + "="*50)
    print("TESTING PORTFOLIO BY CATEGORIES")
    print("="*50)
    
    services, projects = create_sample_data()
    
    # Get all active services that will act as categories
    categories = Service.objects.filter(is_active=True).order_by('display_order', 'title')
    print(f"\nFound {categories.count()} categories:")
    
    for category in categories:
        print(f"  - {category.title} (slug: {category.slug})")
    
    # Get all active projects
    all_projects = Project.objects.filter(is_active=True).prefetch_related('related_services')
    print(f"\nFound {all_projects.count()} active projects")
    
    # Group projects by categories
    projects_by_category = {}
    
    for project in all_projects:
        project_services = project.related_services.filter(is_active=True)
        
        for service in project_services:
            if service not in projects_by_category:
                projects_by_category[service] = []
            projects_by_category[service].append(project)
    
    print(f"\nProjects grouped by categories:")
    for category, category_projects in projects_by_category.items():
        print(f"\n  {category.title} ({len(category_projects)} projects):")
        for project in category_projects:
            print(f"    - {project.title}")
    
    return projects_by_category


def test_home_view_with_portfolio():
    """Test the home view to ensure portfolio data is available."""
    print("\n" + "="*50)
    print("TESTING HOME VIEW WITH PORTFOLIO")
    print("="*50)
    
    client = Client()
    
    # Test home page
    response = client.get(reverse('home'))
    
    print(f"Home page status: {response.status_code}")
    
    if response.status_code == 200:
        context = response.context
        
        # Check if projects are in context
        if 'projects' in context:
            projects = context['projects']
            print(f"Projects in context: {len(projects)}")
        else:
            print("Projects NOT found in context")
        
        # Check if categories are in context
        if 'categories' in context:
            categories = context['categories']
            print(f"Categories in context: {len(categories)}")
        else:
            print("Categories NOT found in context")
    
    return response


def update_home_view():
    """Update the home view to include portfolio data by categories."""
    print("\n" + "="*50)
    print("UPDATING HOME VIEW FOR PORTFOLIO CATEGORIES")
    print("="*50)
    
    views_file = '/home/vivian/Documents/DravTech/DravTech/main/views.py'
    
    # Read current views.py
    with open(views_file, 'r') as f:
        content = f.read()
    
    # Find the home function and update it
    import re
    
    # Pattern to match the home function
    pattern = r'(def home\(request\):.*?stats = SiteStat\.objects\.filter\(is_active=True\))'
    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        # New code to add after stats query
        new_code = '''    stats = SiteStat.objects.filter(is_active=True)
    
    # Portfolio data grouped by categories (services)
    projects = Project.objects.filter(is_active=True).prefetch_related('related_services')
    categories = Service.objects.filter(is_active=True).order_by('display_order', 'title')
    
    # Group projects by categories for filtering
    projects_by_category = {}
    for project in projects:
        for service in project.related_services.filter(is_active=True):
            if service not in projects_by_category:
                projects_by_category[service] = []
            projects_by_category[service].append(project)'''
        
        # Replace the matched content
        updated_content = content.replace(match.group(1), new_code)
        
        # Update the context in the render call
        context_pattern = r'(\{[\s\S]*?\'services\': services,[\s\S]*?\'featured_products\': featured_products,[\s\S]*?\'stats\': stats,[\s\S]*?\})'
        context_match = re.search(context_pattern, updated_content)
        
        if context_match:
            new_context = '''        {
            'services': services,
            'featured_products': featured_products,
            'stats': stats,
            'projects': projects,
            'categories': categories,
            'projects_by_category': projects_by_category,
        }'''
            updated_content = updated_content.replace(context_match.group(1), new_context)
        
        # Write the updated content
        with open(views_file, 'w') as f:
            f.write(updated_content)
        
        print("Home view updated successfully!")
        return True
    else:
        print("Could not find home function to update")
        return False


if __name__ == '__main__':
    print("Portfolio Category Test Script")
    print("=" * 40)
    
    try:
        # Test portfolio by categories
        projects_by_category = test_portfolio_by_categories()
        
        # Update home view
        if update_home_view():
            print("\nHome view updated. Portfolio should now display by categories.")
        
        print("\nTest completed successfully!")
        
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()

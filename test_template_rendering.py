#!/usr/bin/env python
"""
Test template rendering for portfolio categories.
"""

import os
import sys
import django

# Setup Django environment
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'DravTech'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DravTech.settings')
django.setup()

from django.template import Context, Template
from main.models import Service, Project


def test_template_rendering():
    """Test the portfolio template rendering logic."""
    print("Testing Portfolio Template Rendering")
    print("=" * 40)
    
    # Get data
    projects = Project.objects.filter(is_active=True).prefetch_related('related_services')
    categories = Service.objects.filter(is_active=True).order_by('display_order', 'title')
    
    # Group projects by categories
    projects_by_category = {}
    for project in projects:
        for service in project.related_services.filter(is_active=True):
            if service not in projects_by_category:
                projects_by_category[service] = []
            projects_by_category[service].append(project)
    
    # Test filter template snippet
    filter_template = """
    <ul class="portfolio-filters isotope-filters">
      <li data-filter="*" class="filter-active">All Projects</li>
      {% if categories %}
        {% for cat in categories %}
          <li data-filter=".filter-{{ cat.slug|escape }}">{{ cat.title }}</li>
        {% endfor %}
      {% endif %}
    </ul>
    """
    
    template = Template(filter_template)
    context = Context({'categories': categories})
    rendered = template.render(context)
    
    print("Filter HTML:")
    print(rendered)
    
    # Test project items template snippet
    project_template = """
    {% for project in projects %}
      <div class="portfolio-item isotope-item {% for c in project.related_services.all %}filter-{{ c.slug }} {% endfor %}">
        <h4>{{ project.title }}</h4>
        <p>{{ project.summary|truncatewords:10 }}</p>
        <small>Services: {% for c in project.related_services.all %}{{ c.title }}{% if not forloop.last %}, {% endif %}{% endfor %}</small>
      </div>
    {% endfor %}
    """
    
    template = Template(project_template)
    context = Context({'projects': projects})
    rendered = template.render(context)
    
    print("\nProject Items HTML:")
    print(rendered)
    
    print(f"\n✓ Template rendering test completed!")
    print(f"  - Categories: {len(categories)}")
    print(f"  - Projects: {len(projects)}")
    print(f"  - Projects by category: {len(projects_by_category)}")


if __name__ == '__main__':
    try:
        test_template_rendering()
    except Exception as e:
        print(f"Error during template testing: {e}")
        import traceback
        traceback.print_exc()

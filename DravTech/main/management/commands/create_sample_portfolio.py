from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files import File
from pathlib import Path
from main.models import Project, Service
from django.utils import timezone


class Command(BaseCommand):
    help = 'Create sample portfolio data with services as categories'

    def add_arguments(self, parser):
        parser.add_argument('--overwrite', action='store_true', help='Overwrite existing sample data if present')

    def handle(self, *args, **options):
        self.stdout.write("Creating sample services...")
        
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
            status = 'Created' if created else 'Found'
            self.stdout.write(f"  {status} service: {service.title}")
        
        self.stdout.write("\nCreating sample projects...")
        
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
            
            if options.get('overwrite'):
                Project.objects.filter(title=project_data['title']).delete()
            
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
                    self.stdout.write(self.style.WARNING(f"Warning: Service '{service_name}' not found"))
            
            projects.append(project)
            status = 'Created' if created else 'Found'
            self.stdout.write(f"  {status} project: {project.title}")
        
        # Display summary
        self.stdout.write(self.style.SUCCESS(f"\nSummary:"))
        self.stdout.write(f"  Services: {len(services)}")
        self.stdout.write(f"  Projects: {len(projects)}")
        
        # Show projects by category
        self.stdout.write(self.style.SUCCESS(f"\nProjects by category:"))
        for service in services:
            service_projects = Project.objects.filter(related_services=service, is_active=True)
            self.stdout.write(f"  {service.title}: {service_projects.count()} projects")
            for project in service_projects:
                self.stdout.write(f"    - {project.title}")
        
        self.stdout.write(self.style.SUCCESS("\nSample data created successfully!"))

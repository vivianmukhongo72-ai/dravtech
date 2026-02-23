from django.core.management.base import BaseCommand
from django.utils.text import slugify
from services.models import ServiceCategory, Service, ServiceHighlight, ServiceProcessStep, ServiceFAQ, CaseStudy


class Command(BaseCommand):
    help = 'Populate services with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Creating service categories...')
        
        # Create service categories
        categories_data = [
            {
                'name': 'Software & Digital Systems',
                'slug': 'software-digital-systems',
                'description': 'Custom software development and digital transformation solutions',
                'icon': 'lucide-code',
                'display_order': 1
            },
            {
                'name': 'AI & Data Solutions',
                'slug': 'ai-data-solutions',
                'description': 'Artificial intelligence and data analytics services',
                'icon': 'lucide-brain',
                'display_order': 2
            },
            {
                'name': 'Creative & Graphic Design',
                'slug': 'creative-graphic-design',
                'description': 'Branding, UI/UX design and creative services',
                'icon': 'lucide-palette',
                'display_order': 3
            },
            {
                'name': 'Cloud & Infrastructure',
                'slug': 'cloud-infrastructure',
                'description': 'Cloud deployment and infrastructure management',
                'icon': 'lucide-cloud',
                'display_order': 4
            }
        ]
        
        categories = []
        for cat_data in categories_data:
            category, created = ServiceCategory.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            categories.append(category)
            if created:
                self.stdout.write(f'  Created category: {category.name}')
        
        self.stdout.write('Creating services...')
        
        # Create services
        services_data = [
            {
                'title': 'Custom Web Application Development',
                'slug': 'custom-web-application-development',
                'category': categories[0],  # Software & Digital Systems
                'tagline': 'Build scalable, secure web applications tailored to your business needs',
                'overview': 'We design and develop custom web applications using modern frameworks and best practices. Our solutions are built to scale, secure, and deliver exceptional user experiences.',
                'primary_cta_type': Service.CTA_BOOK,
                'primary_cta_label': 'Book Consultation',
                'is_featured': True,
                'display_order': 1,
                'meta_title': 'Custom Web Application Development | DravTech',
                'meta_description': 'Professional custom web application development services. Build scalable, secure web apps tailored to your business needs.'
            },
            {
                'title': 'Mobile App Development',
                'slug': 'mobile-app-development',
                'category': categories[0],  # Software & Digital Systems
                'tagline': 'Native and cross-platform mobile applications for iOS and Android',
                'overview': 'Create powerful mobile applications that engage users and drive business growth. We handle everything from concept to deployment.',
                'primary_cta_type': Service.CTA_QUOTE,
                'primary_cta_label': 'Get Quote',
                'is_featured': True,
                'display_order': 2,
                'meta_title': 'Mobile App Development Services | DravTech',
                'meta_description': 'Professional mobile app development for iOS and Android. Native and cross-platform solutions.'
            },
            {
                'title': 'Machine Learning Solutions',
                'slug': 'machine-learning-solutions',
                'category': categories[1],  # AI & Data Solutions
                'tagline': 'Leverage AI and ML to transform your data into insights',
                'overview': 'Implement cutting-edge machine learning solutions that automate processes, predict outcomes, and provide actionable insights from your data.',
                'primary_cta_type': Service.CTA_CONTACT,
                'primary_cta_label': 'Contact Experts',
                'is_featured': True,
                'display_order': 3,
                'meta_title': 'Machine Learning Solutions | DravTech',
                'meta_description': 'Professional machine learning and AI solutions. Transform your data into actionable insights.'
            },
            {
                'title': 'Data Analytics & Visualization',
                'slug': 'data-analytics-visualization',
                'category': categories[1],  # AI & Data Solutions
                'tagline': 'Turn complex data into clear, actionable insights',
                'overview': 'Transform your raw data into meaningful insights with our advanced analytics and visualization services.',
                'primary_cta_type': Service.CTA_BOOK,
                'primary_cta_label': 'Book Demo',
                'is_featured': False,
                'display_order': 4,
                'meta_title': 'Data Analytics & Visualization | DravTech',
                'meta_description': 'Professional data analytics and visualization services. Turn complex data into actionable insights.'
            },
            {
                'title': 'Brand Identity Design',
                'slug': 'brand-identity-design',
                'category': categories[2],  # Creative & Graphic Design
                'tagline': 'Create memorable brand identities that resonate with your audience',
                'overview': 'Develop comprehensive brand identities including logos, color schemes, typography, and brand guidelines that set you apart.',
                'primary_cta_type': Service.CTA_QUOTE,
                'primary_cta_label': 'Get Quote',
                'is_featured': False,
                'display_order': 5,
                'meta_title': 'Brand Identity Design Services | DravTech',
                'meta_description': 'Professional brand identity design services. Create memorable brands that resonate with your audience.'
            },
            {
                'title': 'UI/UX Design',
                'slug': 'ui-ux-design',
                'category': categories[2],  # Creative & Graphic Design
                'tagline': 'Design intuitive interfaces that users love',
                'overview': 'Create beautiful, intuitive user interfaces and experiences that delight users and drive engagement.',
                'primary_cta_type': Service.CTA_BOOK,
                'primary_cta_label': 'Book Discovery',
                'is_featured': True,
                'display_order': 6,
                'meta_title': 'UI/UX Design Services | DravTech',
                'meta_description': 'Professional UI/UX design services. Create intuitive interfaces that users love.'
            },
            {
                'title': 'Cloud Migration Services',
                'slug': 'cloud-migration-services',
                'category': categories[3],  # Cloud & Infrastructure
                'tagline': 'Seamlessly migrate your infrastructure to the cloud',
                'overview': 'Plan and execute smooth cloud migrations that minimize downtime and maximize performance benefits.',
                'primary_cta_type': Service.CTA_BOOK,
                'primary_cta_label': 'Start Migration',
                'is_featured': False,
                'display_order': 7,
                'meta_title': 'Cloud Migration Services | DravTech',
                'meta_description': 'Professional cloud migration services. Seamlessly migrate your infrastructure to the cloud.'
            },
            {
                'title': 'DevOps & Infrastructure Management',
                'slug': 'devops-infrastructure-management',
                'category': categories[3],  # Cloud & Infrastructure
                'tagline': 'Optimize your development and deployment workflows',
                'overview': 'Implement DevOps best practices and manage your infrastructure for optimal performance and reliability.',
                'primary_cta_type': Service.CTA_CONTACT,
                'primary_cta_label': 'Contact Team',
                'is_featured': False,
                'display_order': 8,
                'meta_title': 'DevOps & Infrastructure Management | DravTech',
                'meta_description': 'Professional DevOps and infrastructure management services. Optimize your development workflows.'
            }
        ]
        
        services = []
        for service_data in services_data:
            service, created = Service.objects.get_or_create(
                slug=service_data['slug'],
                defaults=service_data
            )
            services.append(service)
            if created:
                self.stdout.write(f'  Created service: {service.title}')
        
        self.stdout.write('Creating service highlights...')
        
        # Create service highlights for featured services
        highlights_data = [
            # Web App Development highlights
            {
                'service': services[0],
                'title': 'Scalable Architecture',
                'description': 'Built to grow with your business',
                'icon': 'lucide-trending-up',
                'display_order': 1
            },
            {
                'service': services[0],
                'title': 'Security First',
                'description': 'Enterprise-grade security built-in',
                'icon': 'lucide-shield-check',
                'display_order': 2
            },
            {
                'service': services[0],
                'title': 'Modern Tech Stack',
                'description': 'Latest frameworks and best practices',
                'icon': 'lucide-zap',
                'display_order': 3
            },
            # Mobile App Development highlights
            {
                'service': services[1],
                'title': 'Native Performance',
                'description': 'Optimized for device performance',
                'icon': 'lucide-smartphone',
                'display_order': 1
            },
            {
                'service': services[1],
                'title': 'Cross-Platform',
                'description': 'Reach users on all devices',
                'icon': 'lucide-monitor',
                'display_order': 2
            },
            # Machine Learning highlights
            {
                'service': services[2],
                'title': 'Custom Models',
                'description': 'Tailored to your specific needs',
                'icon': 'lucide-brain',
                'display_order': 1
            },
            {
                'service': services[2],
                'title': 'Real-time Processing',
                'description': 'Process data as it arrives',
                'icon': 'lucide-activity',
                'display_order': 2
            },
            # UI/UX Design highlights
            {
                'service': services[5],
                'title': 'User-Centered Design',
                'description': 'Focus on user needs and goals',
                'icon': 'lucide-users',
                'display_order': 1
            },
            {
                'service': services[5],
                'title': 'Responsive Design',
                'description': 'Perfect on all screen sizes',
                'icon': 'lucide-layout',
                'display_order': 2
            }
        ]
        
        for highlight_data in highlights_data:
            highlight, created = ServiceHighlight.objects.get_or_create(
                service=highlight_data['service'],
                title=highlight_data['title'],
                defaults=highlight_data
            )
            if created:
                self.stdout.write(f'  Created highlight: {highlight.title}')
        
        self.stdout.write('Creating service process steps...')
        
        # Create process steps for featured services
        process_steps_data = [
            # Web App Development process
            {
                'service': services[0],
                'step_number': 1,
                'title': 'Discovery & Planning',
                'description': 'Understanding your requirements and creating a detailed project plan'
            },
            {
                'service': services[0],
                'step_number': 2,
                'title': 'Design & Prototyping',
                'description': 'Creating wireframes, mockups, and interactive prototypes'
            },
            {
                'service': services[0],
                'step_number': 3,
                'title': 'Development',
                'description': 'Building the application using modern technologies and best practices'
            },
            {
                'service': services[0],
                'step_number': 4,
                'title': 'Testing & QA',
                'description': 'Comprehensive testing to ensure quality and reliability'
            },
            {
                'service': services[0],
                'step_number': 5,
                'title': 'Deployment & Support',
                'description': 'Launching the application and providing ongoing support'
            },
            # Machine Learning process
            {
                'service': services[2],
                'step_number': 1,
                'title': 'Data Assessment',
                'description': 'Analyzing your data sources and requirements'
            },
            {
                'service': services[2],
                'step_number': 2,
                'title': 'Model Development',
                'description': 'Building and training custom ML models'
            },
            {
                'service': services[2],
                'step_number': 3,
                'title': 'Integration',
                'description': 'Integrating ML models into your existing systems'
            }
        ]
        
        for step_data in process_steps_data:
            step, created = ServiceProcessStep.objects.get_or_create(
                service=step_data['service'],
                title=step_data['title'],
                defaults=step_data
            )
            if created:
                self.stdout.write(f'  Created process step: {step.title}')
        
        self.stdout.write(self.style.SUCCESS('Services data populated successfully!'))

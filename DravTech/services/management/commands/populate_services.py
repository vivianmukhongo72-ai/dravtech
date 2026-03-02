from django.core.management.base import BaseCommand
from django.utils.text import slugify
from services.models import ServiceCategory, Service, ServiceHighlight, ServiceProcessStep, ServiceFAQ, CaseStudy


class Command(BaseCommand):
    help = 'Populate services with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Creating service categories...')

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
            },
            {
                'name': 'IT Consultancy',
                'slug': 'it-consultancy',
                'description': 'Strategic IT advisory and consulting services to align technology with your business goals',
                'icon': 'lucide-headphones',
                'display_order': 5
            },
            {
                'name': 'Cybersecurity',
                'slug': 'cybersecurity',
                'description': 'End-to-end cybersecurity services to protect your business from threats',
                'icon': 'lucide-shield',
                'display_order': 6
            },
            {
                'name': 'Partnerships & Investments',
                'slug': 'partnerships-investments',
                'description': 'Structured partnership models, joint ventures, and investment opportunities',
                'icon': 'lucide-handshake',
                'display_order': 7
            },
            {
                'name': 'Intellectual Property',
                'slug': 'intellectual-property',
                'description': 'Acquisition, licensing, and management of software patents, trademarks, and digital IP',
                'icon': 'lucide-lightbulb',
                'display_order': 8
            },
        ]

        categories = []
        for cat_data in categories_data:
            category, created = ServiceCategory.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            categories.append(category)
            if created:
                self.stdout.write(f'  ✅ Created category: {category.name}')
            else:
                self.stdout.write(f'  📝 Already exists: {category.name}')

        self.stdout.write('Creating services...')

        services_data = [
            # ── Software & Digital Systems ──
            {
                'title': 'Custom Web Application Development',
                'slug': 'custom-web-application-development',
                'category': categories[0],
                'tagline': 'Build scalable, secure web applications tailored to your business needs',
                'overview': 'We design and develop custom web applications using modern frameworks and best practices. Our solutions are built to scale, are secure, and deliver exceptional user experiences.',
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
                'category': categories[0],
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
                'title': 'Enterprise System Design',
                'slug': 'enterprise-system-design',
                'category': categories[0],
                'tagline': 'Robust enterprise-grade systems built for scale and reliability',
                'overview': 'We architect and deliver enterprise systems that streamline operations, integrate seamlessly with existing tools, and are built to handle growth.',
                'primary_cta_type': Service.CTA_CONTACT,
                'primary_cta_label': 'Contact Us',
                'is_featured': False,
                'display_order': 3,
                'meta_title': 'Enterprise System Design | DravTech',
                'meta_description': 'Enterprise-grade system design and architecture for growing businesses.'
            },

            # ── AI & Data Solutions ──
            {
                'title': 'Machine Learning Solutions',
                'slug': 'machine-learning-solutions',
                'category': categories[1],
                'tagline': 'Leverage AI and ML to transform your data into insights',
                'overview': 'Implement cutting-edge machine learning solutions that automate processes, predict outcomes, and provide actionable insights from your data.',
                'primary_cta_type': Service.CTA_CONTACT,
                'primary_cta_label': 'Contact Experts',
                'is_featured': True,
                'display_order': 4,
                'meta_title': 'Machine Learning Solutions | DravTech',
                'meta_description': 'Professional machine learning and AI solutions. Transform your data into actionable insights.'
            },
            {
                'title': 'Data Analytics & Visualization',
                'slug': 'data-analytics-visualization',
                'category': categories[1],
                'tagline': 'Turn complex data into clear, actionable insights',
                'overview': 'Transform your raw data into meaningful insights with our advanced analytics and visualization services.',
                'primary_cta_type': Service.CTA_BOOK,
                'primary_cta_label': 'Book Demo',
                'is_featured': False,
                'display_order': 5,
                'meta_title': 'Data Analytics & Visualization | DravTech',
                'meta_description': 'Professional data analytics and visualization services. Turn complex data into actionable insights.'
            },
            {
                'title': 'Intelligent Automation',
                'slug': 'intelligent-automation',
                'category': categories[1],
                'tagline': 'Automate repetitive tasks with smart AI-powered workflows',
                'overview': 'We build intelligent automation solutions that reduce manual work, eliminate errors, and free your team to focus on what matters most.',
                'primary_cta_type': Service.CTA_QUOTE,
                'primary_cta_label': 'Get Quote',
                'is_featured': False,
                'display_order': 6,
                'meta_title': 'Intelligent Automation | DravTech',
                'meta_description': 'AI-powered automation solutions that streamline your business workflows.'
            },

            # ── Creative & Graphic Design ──
            {
                'title': 'Brand Identity Design',
                'slug': 'brand-identity-design',
                'category': categories[2],
                'tagline': 'Create memorable brand identities that resonate with your audience',
                'overview': 'Develop comprehensive brand identities including logos, color schemes, typography, and brand guidelines that set you apart.',
                'primary_cta_type': Service.CTA_QUOTE,
                'primary_cta_label': 'Get Quote',
                'is_featured': False,
                'display_order': 7,
                'meta_title': 'Brand Identity Design Services | DravTech',
                'meta_description': 'Professional brand identity design services. Create memorable brands that resonate with your audience.'
            },
            {
                'title': 'UI/UX Design',
                'slug': 'ui-ux-design',
                'category': categories[2],
                'tagline': 'Design intuitive interfaces that users love',
                'overview': 'Create beautiful, intuitive user interfaces and experiences that delight users and drive engagement.',
                'primary_cta_type': Service.CTA_BOOK,
                'primary_cta_label': 'Book Discovery',
                'is_featured': True,
                'display_order': 8,
                'meta_title': 'UI/UX Design Services | DravTech',
                'meta_description': 'Professional UI/UX design services. Create intuitive interfaces that users love.'
            },

            # ── Cloud & Infrastructure ──
            {
                'title': 'Cloud Migration Services',
                'slug': 'cloud-migration-services',
                'category': categories[3],
                'tagline': 'Seamlessly migrate your infrastructure to the cloud',
                'overview': 'Plan and execute smooth cloud migrations that minimize downtime and maximize performance benefits.',
                'primary_cta_type': Service.CTA_BOOK,
                'primary_cta_label': 'Start Migration',
                'is_featured': False,
                'display_order': 9,
                'meta_title': 'Cloud Migration Services | DravTech',
                'meta_description': 'Professional cloud migration services. Seamlessly migrate your infrastructure to the cloud.'
            },
            {
                'title': 'DevOps & Infrastructure Management',
                'slug': 'devops-infrastructure-management',
                'category': categories[3],
                'tagline': 'Optimize your development and deployment workflows',
                'overview': 'Implement DevOps best practices and manage your infrastructure for optimal performance and reliability.',
                'primary_cta_type': Service.CTA_CONTACT,
                'primary_cta_label': 'Contact Team',
                'is_featured': False,
                'display_order': 10,
                'meta_title': 'DevOps & Infrastructure Management | DravTech',
                'meta_description': 'Professional DevOps and infrastructure management services. Optimize your development workflows.'
            },

            # ── IT Consultancy ──
            {
                'title': 'IT Strategy & Advisory',
                'slug': 'it-strategy-advisory',
                'category': categories[4],
                'tagline': 'Align your technology investments with your business goals',
                'overview': 'Our IT consultants work closely with your leadership team to assess current systems, identify gaps, and deliver a clear technology roadmap for growth.',
                'primary_cta_type': Service.CTA_BOOK,
                'primary_cta_label': 'Book Consultation',
                'is_featured': False,
                'display_order': 11,
                'meta_title': 'IT Strategy & Advisory | DravTech',
                'meta_description': 'Expert IT strategy and advisory services to align technology with your business goals.'
            },
            {
                'title': 'IT Support & Managed Services',
                'slug': 'it-support-managed-services',
                'category': categories[4],
                'tagline': 'Reliable ongoing IT support so your business never skips a beat',
                'overview': 'We provide proactive IT support and managed services that keep your systems running smoothly, reduce downtime, and resolve issues fast.',
                'primary_cta_type': Service.CTA_CONTACT,
                'primary_cta_label': 'Get Support',
                'is_featured': False,
                'display_order': 12,
                'meta_title': 'IT Support & Managed Services | DravTech',
                'meta_description': 'Reliable IT support and managed services for businesses of all sizes.'
            },

            # ── Cybersecurity ──
            {
                'title': 'Cybersecurity Audit & Assessment',
                'slug': 'cybersecurity-audit-assessment',
                'category': categories[5],
                'tagline': 'Identify vulnerabilities before attackers do',
                'overview': 'Our security experts conduct thorough audits of your systems, networks, and applications to uncover vulnerabilities and recommend actionable fixes.',
                'primary_cta_type': Service.CTA_BOOK,
                'primary_cta_label': 'Book Audit',
                'is_featured': False,
                'display_order': 13,
                'meta_title': 'Cybersecurity Audit & Assessment | DravTech',
                'meta_description': 'Professional cybersecurity audits to identify and fix vulnerabilities in your systems.'
            },
            {
                'title': 'Data Protection & Compliance',
                'slug': 'data-protection-compliance',
                'category': categories[5],
                'tagline': 'Stay compliant and keep your customer data safe',
                'overview': 'We help businesses implement data protection frameworks, meet regulatory requirements, and build customer trust through strong security practices.',
                'primary_cta_type': Service.CTA_CONTACT,
                'primary_cta_label': 'Talk to Us',
                'is_featured': False,
                'display_order': 14,
                'meta_title': 'Data Protection & Compliance | DravTech',
                'meta_description': 'Data protection and compliance services to keep your business secure and compliant.'
            },

            # ── Partnerships & Investments ──
            {
                'title': 'Strategic Partnerships',
                'slug': 'strategic-partnerships',
                'category': categories[6],
                'tagline': 'Build lasting partnerships that drive mutual growth',
                'overview': 'We work with businesses, agencies, and investors to form strategic partnerships that open new markets, share expertise, and accelerate growth for all parties.',
                'primary_cta_type': Service.CTA_CONTACT,
                'primary_cta_label': 'Let\'s Partner',
                'is_featured': False,
                'display_order': 15,
                'meta_title': 'Strategic Partnerships | DravTech',
                'meta_description': 'Strategic partnership opportunities with DravTech for businesses and investors.'
            },

            # ── Intellectual Property ──
            {
                'title': 'IP Licensing & Management',
                'slug': 'ip-licensing-management',
                'category': categories[7],
                'tagline': 'Protect and monetize your digital innovations',
                'overview': 'We help businesses identify, protect, license, and monetize their intellectual property — from software patents to proprietary algorithms and digital platforms.',
                'primary_cta_type': Service.CTA_CONTACT,
                'primary_cta_label': 'Talk to Us',
                'is_featured': False,
                'display_order': 16,
                'meta_title': 'IP Licensing & Management | DravTech',
                'meta_description': 'Protect and manage your intellectual property with DravTech\'s IP services.'
            },
        ]

        services = []
        for service_data in services_data:
            service, created = Service.objects.get_or_create(
                slug=service_data['slug'],
                defaults=service_data
            )
            services.append(service)
            if created:
                self.stdout.write(f'  ✅ Created service: {service.title}')
            else:
                self.stdout.write(f'  📝 Already exists: {service.title}')

        self.stdout.write('Creating service highlights...')

        highlights_data = [
            {'service': services[0], 'title': 'Scalable Architecture', 'description': 'Built to grow with your business', 'icon': 'lucide-trending-up', 'display_order': 1},
            {'service': services[0], 'title': 'Security First', 'description': 'Enterprise-grade security built-in', 'icon': 'lucide-shield-check', 'display_order': 2},
            {'service': services[0], 'title': 'Modern Tech Stack', 'description': 'Latest frameworks and best practices', 'icon': 'lucide-zap', 'display_order': 3},
            {'service': services[1], 'title': 'Native Performance', 'description': 'Optimized for device performance', 'icon': 'lucide-smartphone', 'display_order': 1},
            {'service': services[1], 'title': 'Cross-Platform', 'description': 'Reach users on all devices', 'icon': 'lucide-monitor', 'display_order': 2},
            {'service': services[3], 'title': 'Custom Models', 'description': 'Tailored to your specific needs', 'icon': 'lucide-brain', 'display_order': 1},
            {'service': services[3], 'title': 'Real-time Processing', 'description': 'Process data as it arrives', 'icon': 'lucide-activity', 'display_order': 2},
            {'service': services[7], 'title': 'User-Centered Design', 'description': 'Focus on user needs and goals', 'icon': 'lucide-users', 'display_order': 1},
            {'service': services[7], 'title': 'Responsive Design', 'description': 'Perfect on all screen sizes', 'icon': 'lucide-layout', 'display_order': 2},
        ]

        for highlight_data in highlights_data:
            highlight, created = ServiceHighlight.objects.get_or_create(
                service=highlight_data['service'],
                title=highlight_data['title'],
                defaults=highlight_data
            )
            if created:
                self.stdout.write(f'  ✅ Created highlight: {highlight.title}')

        self.stdout.write('Creating service process steps...')

        process_steps_data = [
            # Web App Development
            {'service': services[0], 'step_number': 1, 'title': 'Discovery & Planning', 'description': 'Understanding your requirements and creating a detailed project plan'},
            {'service': services[0], 'step_number': 2, 'title': 'Design & Prototyping', 'description': 'Creating wireframes, mockups, and interactive prototypes'},
            {'service': services[0], 'step_number': 3, 'title': 'Development', 'description': 'Building the application using modern technologies and best practices'},
            {'service': services[0], 'step_number': 4, 'title': 'Testing & QA', 'description': 'Automated and manual testing covering unit, integration, and user acceptance testing'},
            {'service': services[0], 'step_number': 5, 'title': 'Deployment & Handover', 'description': 'Production deployment, documentation handover, and 30-day post-launch support'},
            # Machine Learning
            {'service': services[3], 'step_number': 1, 'title': 'Data Assessment', 'description': 'Analyzing your data sources, quality, and requirements'},
            {'service': services[3], 'step_number': 2, 'title': 'Model Development', 'description': 'Building and training custom ML models on your data'},
            {'service': services[3], 'step_number': 3, 'title': 'Integration', 'description': 'Integrating ML models into your existing systems and workflows'},
            # Cybersecurity Audit
            {'service': services[12], 'step_number': 1, 'title': 'Scoping', 'description': 'Defining the systems, networks, and applications to be assessed'},
            {'service': services[12], 'step_number': 2, 'title': 'Assessment', 'description': 'Running vulnerability scans, penetration tests, and manual reviews'},
            {'service': services[12], 'step_number': 3, 'title': 'Reporting', 'description': 'Delivering a detailed report with findings and prioritized recommendations'},
            {'service': services[12], 'step_number': 4, 'title': 'Remediation Support', 'description': 'Guiding your team through fixing identified vulnerabilities'},
        ]

        for step_data in process_steps_data:
            step, created = ServiceProcessStep.objects.get_or_create(
                service=step_data['service'],
                title=step_data['title'],
                defaults=step_data
            )
            if created:
                self.stdout.write(f'  ✅ Created process step: {step.title}')

        self.stdout.write(self.style.SUCCESS('\n🎉 All services data populated successfully!'))
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from services.models import Service, CaseStudy


class Command(BaseCommand):
    help = 'Populate case studies for services'

    def handle(self, *args, **options):
        self.stdout.write('Creating case studies for services...')
        
        # Get existing services to reference
        services = Service.objects.filter(is_active=True)
        
        case_studies_data = [
            # Web Application Development case studies
            {
                'service': services.filter(slug='web-application-development').first(),
                'title': 'E-Commerce Platform Launch',
                'slug': 'ecommerce-platform-launch',
                'summary': 'Built and launched a comprehensive e-commerce platform with real-time inventory management, secure payment processing, and mobile-responsive design. Resulted in 40% increase in online sales and 60% reduction in cart abandonment.',
                'results': '40% sales increase, 60% cart abandonment reduction, 99.9% uptime, 50% faster page load times',
                'display_order': 1
            },
            {
                'service': services.filter(slug='web-application-development').first(),
                'title': 'Enterprise Resource Planning System',
                'slug': 'erp-system-implementation',
                'summary': 'Developed and deployed a custom ERP system integrating inventory, finance, and HR modules. Streamlined operations and reduced manual data entry by 75%.',
                'results': '75% reduction in manual data entry, 100% inventory accuracy, real-time reporting, 30% operational efficiency gain',
                'display_order': 2
            },
            {
                'service': services.filter(slug='machine-learning-solutions').first(),
                'title': 'Predictive Maintenance Analytics',
                'slug': 'predictive-maintenance-analytics',
                'summary': 'Implemented ML-powered predictive maintenance system for manufacturing equipment. Reduced downtime by 45% and maintenance costs by 30% through proactive interventions.',
                'results': '45% downtime reduction, 30% cost savings, 95% prediction accuracy, 2-week early warning system',
                'display_order': 1
            },
            {
                'service': services.filter(slug='machine-learning-solutions').first(),
                'title': 'Customer Churn Prediction Model',
                'slug': 'customer-churn-prediction',
                'summary': 'Developed machine learning model to predict customer churn with 85% accuracy. Enabled proactive retention strategies reducing churn by 25%.',
                'results': '85% prediction accuracy, 25% churn reduction, $2M annual savings, improved customer retention',
                'display_order': 2
            },
            # Mobile App Development case studies
            {
                'service': services.filter(slug='mobile-app-development').first(),
                'title': 'Fitness Tracking App Launch',
                'slug': 'fitness-tracking-app',
                'summary': 'Designed and developed cross-platform fitness tracking app with social features, workout planning, and progress analytics. Achieved 100K+ downloads in first month.',
                'results': '100K+ downloads, 4.8/5 app rating, 85% user retention rate, integration with wearables',
                'display_order': 1
            },
            {
                'service': services.filter(slug='mobile-app-development').first(),
                'title': 'Real Estate Inspection App',
                'slug': 'real-estate-inspection',
                'summary': 'Created mobile app for property inspectors with offline capabilities, photo documentation, and automated reporting. Reduced inspection time by 40% and improved report accuracy.',
                'results': '40% time savings, 95% report accuracy, offline capability, digital photo integration',
                'display_order': 2
            },
            # UI/UX Design case studies
            {
                'service': services.filter(slug='ui-ux-design').first(),
                'title': 'Banking App Redesign',
                'slug': 'banking-app-redesign',
                'summary': 'Redesigned mobile banking application focusing on user experience and accessibility. Increased user engagement by 60% and reduced support calls by 35%.',
                'results': '60% engagement increase, 35% support reduction, WCAG 2.1 AA compliance, 4.8/5 user satisfaction',
                'display_order': 1
            },
            {
                'service': services.filter(slug='ui-ux-design').first(),
                'title': 'E-Learning Platform UX',
                'slug': 'elearning-platform-ux',
                'summary': 'Conducted comprehensive UX redesign for e-learning platform. Improved course completion rates by 45% and user satisfaction scores by 30%.',
                'results': '45% completion rate increase, 30% satisfaction improvement, 50% reduction in support tickets, intuitive navigation',
                'display_order': 2
            },
            # AI & Data Solutions case studies
            {
                'service': services.filter(slug='data-analytics-dashboards').first(),
                'title': 'Sales Analytics Dashboard',
                'slug': 'sales-analytics-dashboard',
                'summary': 'Built real-time sales analytics dashboard with interactive visualizations and predictive forecasting. Enabled data-driven decision making across sales teams.',
                'results': 'Real-time data processing, 50% faster reporting, 25% improvement in forecast accuracy, enterprise-wide adoption',
                'display_order': 1
            },
            {
                'service': services.filter(slug='data-analytics-visualization').first(),
                'title': 'Supply Chain Visualization',
                'slug': 'supply-chain-visualization',
                'summary': 'Developed interactive supply chain visualization tool providing real-time tracking and optimization insights. Reduced logistics costs by 20% and improved delivery times.',
                'results': '20% cost reduction, 35% delivery time improvement, real-time visibility, 99% accuracy in predictions',
                'display_order': 2
            },
            # Cloud & Infrastructure case studies
            {
                'service': services.filter(slug='cloud-migration-services').first(),
                'title': 'Enterprise Cloud Migration',
                'slug': 'enterprise-cloud-migration',
                'summary': 'Led complete cloud migration of enterprise infrastructure with zero downtime. Migrated 500+ users and 200+ applications while maintaining 99.9% uptime.',
                'results': 'Zero downtime migration, 500+ users migrated, 200+ applications moved, 99.9% uptime maintained, 40% cost reduction',
                'display_order': 1
            },
            {
                'service': services.filter(slug='devops-infrastructure-management').first(),
                'title': 'CI/CD Pipeline Implementation',
                'slug': 'cicd-pipeline-implementation',
                'summary': 'Implemented comprehensive CI/CD pipeline reducing deployment time by 70% and increasing deployment frequency by 300%. Improved code quality and reduced manual intervention.',
                'results': '70% deployment time reduction, 300% frequency increase, 90% automated testing, 50% reduction in production bugs',
                'display_order': 2
            }
        ]
        
        created_count = 0
        for case_data in case_studies_data:
            if case_data['service']:
                case_study, created = CaseStudy.objects.get_or_create(
                    slug=case_data['slug'],
                    defaults=case_data
                )
                if created:
                    created_count += 1
                    self.stdout.write(f'  Created case study: {case_study.title}')
                else:
                    self.stdout.write(f'  Case study already exists: {case_study.title}')
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} new case studies!'))

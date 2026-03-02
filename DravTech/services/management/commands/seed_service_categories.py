from django.core.management.base import BaseCommand
from services.models import ServiceCategory, Service


class Command(BaseCommand):
    help = 'Seed service categories and update existing services'

    def handle(self, *args, **options):
        categories_data = [
            {
                "name": "Software & Digital Systems",
                "short_description": "Custom software development and digital solutions",
                "icon": "laptop-code",
                "display_order": 1,
                "is_active": True,
            },
            {
                "name": "AI & Data Solutions",
                "short_description": "Artificial intelligence and data analytics services",
                "icon": "brain",
                "display_order": 2,
                "is_active": True,
            },
            {
                "name": "Creative & Graphic Design",
                "short_description": "Branding, UI/UX design and creative services",
                "icon": "palette",
                "display_order": 3,
                "is_active": True,
            },
            {
                "name": "Cloud & Infrastructure",
                "short_description": "Cloud deployment and IT infrastructure services",
                "icon": "cloud",
                "display_order": 4,
                "is_active": True,
            },
            {
                "name": "IT Consultancy",
                "short_description": "Expert IT advisory and consulting services",
                "icon": "headset",
                "display_order": 5,
                "is_active": True,
            },
            {
                "name": "Cybersecurity",
                "short_description": "Security solutions to protect your business",
                "icon": "shield-halved",
                "display_order": 6,
                "is_active": True,
            },
            {
                "name": "Partnerships & Investments",
                "short_description": "Joint ventures and strategic partnerships",
                "icon": "handshake",
                "display_order": 7,
                "is_active": True,
            },
            {
                "name": "Intellectual Property",
                "short_description": "Acquisition and management of IP assets",
                "icon": "lightbulb",
                "display_order": 8,
                "is_active": True,
            },
        ]

        # Create or update categories
        for cat_data in categories_data:
            category, created = ServiceCategory.objects.get_or_create(
                name=cat_data["name"],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'✅ Created category: {category.name}')
            else:
                category.short_description = cat_data["short_description"]
                category.icon = cat_data["icon"]
                category.display_order = cat_data["display_order"]
                category.is_active = cat_data["is_active"]
                category.save()
                self.stdout.write(f'📝 Updated category: {category.name}')

        # Auto-assign categories to services that don't have one yet
        services = Service.objects.filter(category__isnull=True)

        if not services.exists():
            self.stdout.write('ℹ️  All services already have a category assigned.')
        else:
            for service in services:
                title_lower = service.title.lower()

                if any(keyword in title_lower for keyword in ['software', 'app', 'web', 'system', 'digital', 'mobile', 'platform']):
                    category_name = "Software & Digital Systems"

                elif any(keyword in title_lower for keyword in ['ai', 'data', 'analytics', 'intelligence', 'machine', 'automation', 'ml']):
                    category_name = "AI & Data Solutions"

                elif any(keyword in title_lower for keyword in ['design', 'creative', 'brand', 'ui', 'ux', 'graphic', 'logo', 'visual']):
                    category_name = "Creative & Graphic Design"

                elif any(keyword in title_lower for keyword in ['cloud', 'infrastructure', 'devops', 'deployment', 'hosting', 'server']):
                    category_name = "Cloud & Infrastructure"

                elif any(keyword in title_lower for keyword in ['consult', 'advisory', 'it support', 'strategy']):
                    category_name = "IT Consultancy"

                elif any(keyword in title_lower for keyword in ['security', 'cyber', 'protect', 'firewall', 'threat', 'audit']):
                    category_name = "Cybersecurity"

                elif any(keyword in title_lower for keyword in ['partner', 'invest', 'venture', 'joint']):
                    category_name = "Partnerships & Investments"

                elif any(keyword in title_lower for keyword in ['ip', 'patent', 'license', 'trademark', 'intellectual', 'property']):
                    category_name = "Intellectual Property"

                else:
                    # Default fallback
                    category_name = "Software & Digital Systems"
                    self.stdout.write(f'⚠️  No keyword match for "{service.title}" — defaulting to Software & Digital Systems')

                category = ServiceCategory.objects.filter(name=category_name).first()
                if category:
                    service.category = category
                    service.save()
                    self.stdout.write(f'🔗 Assigned "{service.title}" → "{category.name}"')

        self.stdout.write(
            self.style.SUCCESS('✅ Done. All categories seeded and services updated.')
        )
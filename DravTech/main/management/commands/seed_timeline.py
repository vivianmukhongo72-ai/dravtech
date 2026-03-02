from django.core.management.base import BaseCommand
from main.models import TimelineEntry

class Command(BaseCommand):
    help = 'Seed timeline entries for the about page'

    def handle(self, *args, **options):
        timeline_entries = [
            {
                "year_label": "2023",
                "title": "Dravtech Founded",
                "description": (
                    "Dravtech Private Limited was officially founded by Fredrick Mbugua Wainaina and "
                    "Samuel Kibunja Macharia. Built on years of hustle — from selling data charts to "
                    "running Microsoft training programs and working as data enumerators at Kenya Power — "
                    "the two co-founders turned their experience into a bold technology vision, assembling "
                    "a founding team of six to bring Dravtech Solutions to life."
                ),
                "is_active": True,
                "display_order": 1,
            },
            {
                "year_label": "2024",
                "title": "First Major Client",
                "description": (
                    "Dravtech secured its first major client, marking a turning point from idea to "
                    "proven business. The team delivered a full software solution, validating their "
                    "technical capabilities and setting the standard for client-focused delivery."
                ),
                "is_active": True,
                "display_order": 2,
            },
            {
                "year_label": "2025",
                "title": "Team Expansion",
                "description": (
                    "With growing demand, Dravtech expanded its team — bringing in talented engineers, "
                    "designers, and consultants to scale delivery across software development, AI, "
                    "cloud services, and IT consultancy. Internal governance and role-based equity "
                    "structures were formalized to support sustainable growth."
                ),
                "is_active": True,
                "display_order": 3,
            },
            {
                "year_label": "2026 & Beyond",
                "title": "Regional Expansion — The Goal",
                "description": (
                    "The vision is clear: take Dravtech beyond Kenya and into the wider East African "
                    "market. By delivering world-class software, AI, and digital solutions, the team "
                    "is laying the groundwork to become a leading technology partner for businesses "
                    "across the continent. The journey has just begun."
                ),
                "is_active": True,
                "display_order": 4,
            },
        ]

        # Clear existing entries
        TimelineEntry.objects.all().delete()
        
        # Create new entries
        for entry in timeline_entries:
            TimelineEntry.objects.create(**entry)
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ Successfully seeded {len(timeline_entries)} TimelineEntry records.')
        )
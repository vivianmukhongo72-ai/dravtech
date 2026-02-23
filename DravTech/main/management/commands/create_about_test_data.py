from django.core.management.base import BaseCommand
from django.utils import timezone
from main.models import (
    AboutPage,
    TimelineEntry,
    CompanyValue,
    TeamMember,
    Project,
    Testimonial,
    HowWeWorkStep,
    Service,
)


class Command(BaseCommand):
    help = 'Create test content for the About page'

    def add_arguments(self, parser):
        parser.add_argument(
            '--overwrite',
            action='store_true',
            help='Overwrite existing About page content if present',
        )

    def handle(self, *args, **options):
        overwrite = options.get('overwrite', False)

        # Create or update AboutPage
        if AboutPage.objects.filter(is_active=True).exists():
            if overwrite:
                AboutPage.objects.filter(is_active=True).update(is_active=False)
                self.stdout.write(self.style.WARNING('Deactivated existing AboutPage entries.'))
            else:
                self.stdout.write(
                    self.style.NOTICE(
                        'Active AboutPage already exists (use --overwrite to recreate).'
                    )
                )
                return

        about_page = AboutPage.objects.create(
            is_active=True,
            hero_headline='Building Integrated Creative Solutions',
            hero_subtitle=(
                'We bring together technology, media, design, and research to deliver '
                'impactful solutions driven by engineers, designers, economists, and data experts.'
            ),
            hero_cta_label='Request Consultation',
            hero_cta_url='/request-demo/',
            mission_title='Our Mission',
            mission_body=(
                'To design and deliver practical, innovative, and evidence-driven solutions '
                'that empower organizations, communities, and institutions to achieve meaningful '
                'and sustainable impact.'
            ),
            vision_title='Our Vision',
            vision_body=(
                'To grow Dravtech into a leading and trusted technology-driven company '
                'recognized for multidisciplinary thinking, ethical innovation, and measurable results.'
            ),
            how_we_work_title='How We Work',
            how_we_work_intro=(
                'Our approach combines research, strategic planning, collaborative development, '
                'and continuous refinement to deliver solutions that make a difference.'
            ),
        )

        # Create Timeline Entries
        timeline_data = [
            {
                'year_label': '2019',
                'title': 'The Beginning',
                'description': (
                    'Dravtech began as a grassroots initiative founded by Samuel and Frederick, '
                    'starting with selling art to students during first-year admissions—an early '
                    'expression of creativity and entrepreneurship.'
                ),
                'display_order': 1,
            },
            {
                'year_label': '2020',
                'title': 'Learning Through Failure',
                'description': (
                    'The idea evolved into offering basic computer training. While the venture did not '
                    'succeed as a business, it provided critical lessons in problem-solving, sustainability, '
                    'and resilience.'
                ),
                'display_order': 2,
            },
            {
                'year_label': '2023',
                'title': 'Rebirth with Experience',
                'description': (
                    'After gaining professional experience at KEPSA, the founders revisited the Dravtech '
                    'vision with renewed clarity, industry insight, and structure.'
                ),
                'display_order': 3,
            },
            {
                'year_label': 'Today',
                'title': 'Building for Impact',
                'description': (
                    'With a multidisciplinary team of shareholders and collaborators, Dravtech is focused '
                    'on delivering integrated solutions across technology, media, design, and research.'
                ),
                'display_order': 4,
            },
        ]

        if overwrite:
            TimelineEntry.objects.all().delete()

        for entry_data in timeline_data:
            TimelineEntry.objects.create(**entry_data, is_active=True)

        # Create Company Values
        values_data = [
            {
                'title': 'Integrity & Accountability',
                'description': 'We take responsibility for our work and our outcomes.',
                'display_order': 1,
            },
            {
                'title': 'Evidence Over Assumptions',
                'description': 'We believe good decisions are grounded in research and data.',
                'display_order': 2,
            },
            {
                'title': 'Collaboration Across Disciplines',
                'description': (
                    'The best solutions emerge when diverse expertise works together.'
                ),
                'display_order': 3,
            },
            {
                'title': 'Creativity with Purpose',
                'description': 'Design and innovation must solve real problems.',
                'display_order': 4,
            },
            {
                'title': 'Long-Term Impact',
                'description': 'We prioritize sustainable outcomes over quick wins.',
                'display_order': 5,
            },
        ]

        if overwrite:
            CompanyValue.objects.all().delete()

        for value_data in values_data:
            CompanyValue.objects.create(**value_data, is_active=True)

        # Create Team Members (sample - you can add more)
        team_data = [
            {
                'name': 'Samuel',
                'role': 'Co-Founder & Engineer',
                'bio': (
                    'Co-founder with a passion for building scalable solutions and '
                    'leading technical teams.'
                ),
                'display_order': 1,
            },
            {
                'name': 'Frederick',
                'role': 'Co-Founder & Strategist',
                'bio': (
                    'Co-founder focused on strategic planning and business development.'
                ),
                'display_order': 2,
            },
            {
                'name': 'Engineering Team',
                'role': 'Software Engineers',
                'bio': (
                    'Experienced developers specializing in modern web technologies, '
                    'APIs, and secure systems.'
                ),
                'display_order': 3,
            },
            {
                'name': 'Design Team',
                'role': 'Designers & UX Specialists',
                'bio': (
                    'Creative professionals who ensure our solutions are intuitive, '
                    'accessible, and visually compelling.'
                ),
                'display_order': 4,
            },
            {
                'name': 'Research Team',
                'role': 'Researchers & Analysts',
                'bio': (
                    'Data experts and researchers who ground our decisions in evidence '
                    'and measurable outcomes.'
                ),
                'display_order': 5,
            },
        ]

        if overwrite:
            TeamMember.objects.all().delete()

        for member_data in team_data:
            TeamMember.objects.create(**member_data, is_active=True)

        # Create Sample Projects (if Service exists, link them)
        project_data = [
            {
                'title': 'Enterprise Web Platform',
                'summary': (
                    'A comprehensive web application built for a leading organization, '
                    'featuring secure authentication, real-time data processing, and '
                    'scalable architecture.'
                ),
                'description': (
                    'This project involved building a full-stack web platform with modern '
                    'technologies, ensuring security, performance, and user experience.'
                ),
                'is_featured': True,
                'display_order': 1,
            },
            {
                'title': 'Data Analytics Dashboard',
                'summary': (
                    'An interactive dashboard that transforms complex data into actionable '
                    'insights for decision-makers.'
                ),
                'description': (
                    'Developed using advanced data visualization techniques and real-time '
                    'data processing capabilities.'
                ),
                'is_featured': True,
                'display_order': 2,
            },
            {
                'title': 'Mobile Application Suite',
                'summary': (
                    'A cross-platform mobile application suite designed for seamless user '
                    'experience across iOS and Android.'
                ),
                'description': (
                    'Built with modern mobile frameworks, ensuring consistent performance '
                    'and user experience across platforms.'
                ),
                'is_featured': True,
                'display_order': 3,
            },
        ]

        if overwrite:
            Project.objects.filter(is_featured=True).delete()

        # Get first service if available for linking
        first_service = Service.objects.filter(is_active=True).first()

        for project_item in project_data:
            project = Project.objects.create(
                **project_item,
                is_active=True,
                published_at=timezone.now(),
            )
            if first_service:
                project.related_services.add(first_service)

        # Create Testimonials
        testimonials_data = [
            {
                'quote': (
                    'DravTech transformed our legacy platform into a secure, modern application—'
                    'with clear milestones and measurable results.'
                ),
                'author_name': 'Sophia Anderson',
                'organization': 'Tech Solutions Inc.',
                'role': 'Marketing Director',
                'is_anonymous': False,
                'display_order': 1,
            },
            {
                'quote': (
                    'Their engineering team delivered a robust API and a responsive frontend '
                    'that scaled with our user base — technical excellence from day one.'
                ),
                'author_name': 'Marcus Webb',
                'organization': 'Innovation Labs',
                'role': 'Tech Lead',
                'is_anonymous': False,
                'display_order': 2,
            },
            {
                'quote': (
                    'We improved our security posture and response time thanks to DravTech\'s '
                    'practical guidance and hands-on fixes.'
                ),
                'author_name': '',
                'organization': 'Confidential Client',
                'role': '',
                'is_anonymous': True,
                'display_order': 3,
            },
        ]

        if overwrite:
            Testimonial.objects.all().delete()

        for testimonial_data in testimonials_data:
            Testimonial.objects.create(**testimonial_data, is_active=True)

        # Create How We Work Steps
        steps_data = [
            {
                'step_number': 1,
                'title': 'Research & Discovery',
                'description': (
                    'We start by understanding your context, challenges, and goals through '
                    'thorough research and stakeholder engagement.'
                ),
            },
            {
                'step_number': 2,
                'title': 'Strategic Planning',
                'description': (
                    'We create a clear roadmap aligned with your objectives, identifying '
                    'key milestones and success metrics.'
                ),
            },
            {
                'step_number': 3,
                'title': 'Collaborative Development',
                'description': (
                    'We build solutions iteratively, maintaining close collaboration and '
                    'incorporating feedback throughout the process.'
                ),
            },
            {
                'step_number': 4,
                'title': 'Testing & Refinement',
                'description': (
                    'We rigorously test and refine our solutions, ensuring quality, '
                    'performance, and user satisfaction.'
                ),
            },
            {
                'step_number': 5,
                'title': 'Launch & Support',
                'description': (
                    'We support smooth launches and provide ongoing maintenance to ensure '
                    'long-term success.'
                ),
            },
        ]

        if overwrite:
            HowWeWorkStep.objects.all().delete()

        for step_data in steps_data:
            HowWeWorkStep.objects.create(**step_data, is_active=True)

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Successfully created About page test content:\n'
                f'   - AboutPage: 1 entry\n'
                f'   - Timeline Entries: {len(timeline_data)}\n'
                f'   - Company Values: {len(values_data)}\n'
                f'   - Team Members: {len(team_data)}\n'
                f'   - Featured Projects: {len(project_data)}\n'
                f'   - Testimonials: {len(testimonials_data)}\n'
                f'   - How We Work Steps: {len(steps_data)}\n\n'
                f'Visit /about/ to see the content!'
            )
        )

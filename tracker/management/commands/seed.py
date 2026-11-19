import random
from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from tracker.models import Expense

STORES = {
    'Food': ['Spinneys', 'Roadster', 'Zaatar w Zeit', 'Malak el Tawook'],
    'Transport': ['Uber', 'Total Station', 'Bus Pass'],
    'Bills': ['EDL', 'Ogero', 'Touch', 'Generator'],
    'Shopping': ['ABC Mall', 'Zara', 'Amazon'],
    'Entertainment': ['Grand Cinemas', 'Spotify', 'Steam'],
    'Other': ['Pharmacy', 'Stationery', 'Gift'],
}


class Command(BaseCommand):
    help = 'Create a demo user and fill the database with random expenses'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=300)
        parser.add_argument('--username', default='demo')
        parser.add_argument('--password', default='demo12345')

    def handle(self, *args, **options):
        User = get_user_model()
        user, created = User.objects.get_or_create(username=options['username'])
        if created:
            user.set_password(options['password'])
            user.save()

        today = timezone.localdate()
        expenses = []
        for _ in range(options['count']):
            category = random.choice(list(STORES))
            expenses.append(Expense(
                user=user,
                category=category,
                store=random.choice(STORES[category]),
                amount=Decimal(random.randint(200, 20000)) / 100,
                date=today - timedelta(days=random.randint(0, 400)),
                description=random.choice(['', '', 'weekly', 'monthly', 'one-off']),
            ))
        Expense.objects.bulk_create(expenses)

        self.stdout.write(self.style.SUCCESS(
            f'{len(expenses)} expenses created for {user.username}'
        ))
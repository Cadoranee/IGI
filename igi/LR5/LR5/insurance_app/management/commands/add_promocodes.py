from django.core.management.base import BaseCommand
from insurance_app.models import PromoCode
from datetime import timedelta, date

class Command(BaseCommand):
    help = 'Добавляет 5 тестовых промокодов'

    def handle(self, *args, **kwargs):
        promocodes = [
            {'code': 'PROMO10', 'description': 'Скидка 10% на все виды страхования', 'discount_percent': 10, 'is_active': True, 'valid_until': date.today() + timedelta(days=30)},
            {'code': 'LIFE15', 'description': 'Скидка 15% на страхование жизни', 'discount_percent': 15, 'is_active': True, 'valid_until': date.today() + timedelta(days=60)},
            {'code': 'HOME20', 'description': 'Скидка 20% на страхование имущества', 'discount_percent': 20, 'is_active': True, 'valid_until': date.today() + timedelta(days=90)},
            {'code': 'AUTO25', 'description': 'Скидка 25% на автострахование', 'discount_percent': 25, 'is_active': True, 'valid_until': date.today() + timedelta(days=45)},
            {'code': 'HEALTH30', 'description': 'Скидка 30% на страхование здоровья', 'discount_percent': 30, 'is_active': True, 'valid_until': date.today() + timedelta(days=15)},
        ]
        for promo in promocodes:
            obj, created = PromoCode.objects.get_or_create(code=promo['code'], defaults=promo)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Промокод {promo['code']} успешно добавлен."))
            else:
                self.stdout.write(self.style.WARNING(f"Промокод {promo['code']} уже существует.")) 
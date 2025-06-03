import os
import django

# Настройка окружения Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insurance_project.settings')
django.setup()

from insurance_app.models import PromoCode

# Список промокодов для добавления
promocodes = [
    {'code': 'PROMO1', 'description': 'Скидка 10% на все виды страхования', 'discount_percent': 10, 'is_active': True},
    {'code': 'PROMO2', 'description': 'Скидка 15% на страхование жизни', 'discount_percent': 15, 'is_active': True},
    {'code': 'PROMO3', 'description': 'Скидка 20% на страхование имущества', 'discount_percent': 20, 'is_active': True},
    {'code': 'PROMO4', 'description': 'Скидка 25% на страхование автомобиля', 'discount_percent': 25, 'is_active': True},
    {'code': 'PROMO5', 'description': 'Скидка 30% на страхование здоровья', 'discount_percent': 30, 'is_active': True},
]

# Добавление промокодов в базу данных
for promo in promocodes:
    PromoCode.objects.create(**promo)

print('Промокоды успешно добавлены в базу данных.') 
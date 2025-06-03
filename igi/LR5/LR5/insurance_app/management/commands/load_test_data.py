from django.core.management.base import BaseCommand
from insurance_app.models import InsuranceType, Branch
from decimal import Decimal

class Command(BaseCommand):
    help = 'Загружает тестовые данные для видов страхования и филиалов'

    def handle(self, *args, **kwargs):
        # Создаем виды страхования
        insurance_types = [
            {
                'name': 'Страхование жизни',
                'description': 'Страхование жизни и здоровья от несчастных случаев и болезней',
                'agent_commission': Decimal('5.00')
            },
            {
                'name': 'Страхование имущества',
                'description': 'Страхование квартиры, дома, дачи от пожара, затопления и других рисков',
                'agent_commission': Decimal('7.00')
            },
            {
                'name': 'Автострахование',
                'description': 'Страхование автомобиля (КАСКО, ОСАГО) от ущерба и гражданской ответственности',
                'agent_commission': Decimal('10.00')
            },
            {
                'name': 'Страхование путешествий',
                'description': 'Страхование выезжающих за рубеж от медицинских расходов и других рисков',
                'agent_commission': Decimal('8.00')
            },
            {
                'name': 'Страхование бизнеса',
                'description': 'Страхование предпринимательских рисков и имущества бизнеса',
                'agent_commission': Decimal('12.00')
            }
        ]

        # Создаем филиалы
        branches = [
            {
                'address': 'ул. Ленина, 10, Минск',
                'phone': '+375 17 123-45-67',
                'name': 'Центральный офис'
            },
            {
                'address': 'пр. Независимости, 25, Минск',
                'phone': '+375 17 234-56-78',
                'name': 'Офис на Независимости'
            },
            {
                'address': 'ул. Советская, 15, Гомель',
                'phone': '+375 23 345-67-89',
                'name': 'Гомельский филиал'
            },
            {
                'address': 'ул. К. Маркса, 30, Витебск',
                'phone': '+375 21 456-78-90',
                'name': 'Витебский филиал'
            },
            {
                'address': 'ул. Октябрьская, 5, Брест',
                'phone': '+375 16 567-89-01',
                'name': 'Брестский филиал'
            }
        ]

        # Создаем записи в базе данных
        for insurance_type in insurance_types:
            InsuranceType.objects.get_or_create(
                name=insurance_type['name'],
                defaults={
                    'description': insurance_type['description'],
                    'agent_commission': insurance_type['agent_commission']
                }
            )
            self.stdout.write(
                self.style.SUCCESS(f'Создан вид страхования: {insurance_type["name"]}')
            )

        for branch in branches:
            Branch.objects.get_or_create(
                address=branch['address'],
                defaults={
                    'phone': branch['phone'],
                    'name': branch['name']
                }
            )
            self.stdout.write(
                self.style.SUCCESS(f'Создан филиал: {branch["address"]}')
            ) 
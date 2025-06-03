from django.core.management.base import BaseCommand
from insurance_app.models import InsuranceType, Branch, InsuranceAgent, PromoCode
from decimal import Decimal
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Создает тестовые данные для приложения'

    def handle(self, *args, **kwargs):
        # Создаем филиалы
        branches = [
            Branch.objects.create(
                name='Центральный офис',
                address='ул. Ленина, 1',
                phone='+7 (999) 111-22-33'
            ),
            Branch.objects.create(
                name='Северный филиал',
                address='пр. Мира, 15',
                phone='+7 (999) 444-55-66'
            ),
            Branch.objects.create(
                name='Южный филиал',
                address='ул. Гагарина, 7',
                phone='+7 (999) 777-88-99'
            )
        ]

        # Создаем виды страхования
        insurance_types = [
            InsuranceType.objects.create(
                name='Страхование жизни',
                description='Страхование жизни и здоровья',
                agent_commission=Decimal('5.00')
            ),
            InsuranceType.objects.create(
                name='Страхование имущества',
                description='Страхование квартиры, дома, дачи',
                agent_commission=Decimal('7.00')
            ),
            InsuranceType.objects.create(
                name='Автострахование',
                description='Страхование автомобиля (КАСКО, ОСАГО)',
                agent_commission=Decimal('10.00')
            ),
            InsuranceType.objects.create(
                name='Страхование путешествий',
                description='Страхование выезжающих за рубеж',
                agent_commission=Decimal('8.00')
            ),
            InsuranceType.objects.create(
                name='Страхование бизнеса',
                description='Страхование предпринимательских рисков',
                agent_commission=Decimal('12.00')
            )
        ]

        # Создаем страховых агентов
        agents = [
            InsuranceAgent.objects.create(
                first_name='Иван',
                last_name='Иванов',
                branch=branches[0],
                phone='+7 (999) 123-45-67',
                email='ivanov@example.com',
                years_of_experience=5
            ),
            InsuranceAgent.objects.create(
                first_name='Петр',
                last_name='Петров',
                branch=branches[1],
                phone='+7 (999) 234-56-78',
                email='petrov@example.com',
                years_of_experience=3
            ),
            InsuranceAgent.objects.create(
                first_name='Анна',
                last_name='Сидорова',
                branch=branches[2],
                phone='+7 (999) 345-67-89',
                email='sidorova@example.com',
                years_of_experience=7
            ),
            InsuranceAgent.objects.create(
                first_name='Мария',
                last_name='Козлова',
                branch=branches[0],
                phone='+7 (999) 456-78-90',
                email='kozlova@example.com',
                years_of_experience=4
            ),
            InsuranceAgent.objects.create(
                first_name='Алексей',
                last_name='Смирнов',
                branch=branches[1],
                phone='+7 (999) 567-89-01',
                email='smirnov@example.com',
                years_of_experience=6
            )
        ]

        # Создаем промокоды
        promocodes = [
            PromoCode.objects.create(
                code='WELCOME2024',
                description='Скидка для новых клиентов',
                discount_percent=Decimal('10.00'),
                is_active=True,
                valid_until=date.today() + timedelta(days=30)
            ),
            PromoCode.objects.create(
                code='SUMMER2024',
                description='Летняя скидка на все виды страхования',
                discount_percent=Decimal('15.00'),
                is_active=True,
                valid_until=date.today() + timedelta(days=60)
            ),
            PromoCode.objects.create(
                code='FAMILY2024',
                description='Скидка при страховании всей семьи',
                discount_percent=Decimal('20.00'),
                is_active=True,
                valid_until=date.today() + timedelta(days=90)
            )
        ]

        self.stdout.write(self.style.SUCCESS('Тестовые данные успешно созданы')) 
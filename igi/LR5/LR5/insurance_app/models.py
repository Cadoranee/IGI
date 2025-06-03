from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import random
import string
import re
from django.core.validators import RegexValidator

# Create your models here.

class InsuranceType(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    agent_commission = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Комиссия агента (%)')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Вид страхования'
        verbose_name_plural = 'Виды страхования'

class InsuranceAgent(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=100, verbose_name='Отчество', default='')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Email')
    experience_years = models.IntegerField(verbose_name='Опыт работы (лет)')
    specialization = models.TextField(verbose_name='Специализация', default='')
    photo = models.ImageField(upload_to='agents/', verbose_name='Фотография', null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    class Meta:
        verbose_name = 'Страховой агент'
        verbose_name_plural = 'Страховые агенты'
        ordering = ['-experience_years']

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"

    def get_full_name(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"

class Client(models.Model):
    # Связь один-к-одному с моделью User (один пользователь = один клиент)
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    first_name = models.CharField(max_length=100, verbose_name='Имя', blank=True, null=True)
    last_name = models.CharField(max_length=100, verbose_name='Фамилия', blank=True, null=True)
    middle_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Отчество')
    phone = models.CharField(
        max_length=20,
        verbose_name='Телефон',
        validators=[
            RegexValidator(
                regex=r'^\+375\s\(\d{2}\)\s\d{3}-\d{2}-\d{2}$',
                message='Номер телефона должен быть в формате: +375 (29) XXX-XX-XX'
            )
        ]
    )
    address = models.CharField(max_length=200, verbose_name='Адрес')
    email = models.EmailField(verbose_name='Email', blank=True, null=True)
    date_of_birth = models.DateField(verbose_name='Дата рождения', blank=True, null=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name if self.middle_name else ''}"

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

class Branch(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название филиала')
    address = models.CharField(max_length=200, verbose_name="Адрес филиала")
    phone = models.CharField(max_length=20, verbose_name='Телефон')

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'Филиал'
        verbose_name_plural = 'Филиалы'

class InsuranceContract(models.Model):
    contract_number = models.CharField(max_length=14, unique=True, editable=False)
    
    # Связь один-ко-многим с моделью Client (один клиент может иметь много договоров)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент')
    
    # Связь один-ко-многим с моделью InsuranceType (один вид страхования может быть в многих договорах)
    insurance_type = models.ForeignKey(InsuranceType, on_delete=models.CASCADE, verbose_name='Вид страхования')
    
    # Связь один-ко-многим с моделью Branch (один филиал может иметь много договоров)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name='Филиал')
    
    # Связь один-ко-многим с моделью InsuranceAgent (один агент может иметь много договоров)
    agent = models.ForeignKey(InsuranceAgent, on_delete=models.CASCADE, verbose_name='Страховой агент', null=True, blank=True)
    
    insurance_sum = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Страховая сумма')
    tariff_rate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Тарифная ставка (%)')
    start_date = models.DateField(verbose_name='Дата начала')
    end_date = models.DateField(verbose_name='Дата окончания')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def save(self, *args, **kwargs):
        if not self.contract_number:
            # Генерируем номер договора: 8 цифр + 6 букв
            numbers = ''.join(random.choices(string.digits, k=8))
            letters = ''.join(random.choices(string.ascii_uppercase, k=6))
            self.contract_number = f"{numbers}{letters}"
        super().save(*args, **kwargs)

    @property
    def is_active(self):
        today = timezone.now().date()
        return self.start_date <= today <= self.end_date

    def __str__(self):
        return f"Договор №{self.contract_number}"

    def calculate_agent_income(self):
        return (self.insurance_sum * self.tariff_rate / 100) * (self.insurance_type.agent_commission / 100)

    class Meta:
        verbose_name = 'Договор страхования'
        verbose_name_plural = 'Договоры страхования'

class PromoCode(models.Model):
    code = models.CharField(max_length=20, unique=True, verbose_name='Код')
    description = models.TextField(verbose_name='Описание')
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Скидка (%)')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    valid_until = models.DateField(verbose_name='Действует до')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f"{self.code} - {self.discount_percent}%"

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'

class News(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    short_content = models.CharField(max_length=200, verbose_name='Краткое содержание')
    image = models.ImageField(upload_to='news/', verbose_name='Изображение', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']

class GlossaryTerm(models.Model):
    term = models.CharField('Термин', max_length=200)
    definition = models.TextField('Определение')
    category = models.CharField('Категория', max_length=50, choices=[
        ('general', 'Общие термины'),
        ('insurance', 'Страхование'),
        ('contract', 'Договор'),
        ('payment', 'Оплата'),
        ('faq', 'Часто задаваемые вопросы')
    ])
    is_faq = models.BooleanField('Это FAQ', default=False)
    created_at = models.DateTimeField('Дата добавления', default=timezone.now)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Термин'
        verbose_name_plural = 'Словарь терминов'
        ordering = ['category', 'term']

    def __str__(self):
        return f"{self.term} ({self.get_category_display()})"

class Vacancy(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название вакансии')
    description = models.TextField(verbose_name='Описание')
    requirements = models.TextField(verbose_name='Требования')
    salary = models.CharField(max_length=100, verbose_name='Зарплата')
    location = models.CharField(max_length=100, verbose_name='Местоположение')
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 звезда'),
        (2, '2 звезды'),
        (3, '3 звезды'),
        (4, '4 звезды'),
        (5, '5 звезд'),
    ]
    
    # Связь один-ко-многим с моделью Client (один клиент может оставить много отзывов)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name='Оценка')
    text = models.TextField(verbose_name='Текст отзыва')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Отзыв от {self.client} - {self.rating} звезд'

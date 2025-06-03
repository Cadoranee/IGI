from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import InsuranceType, Client, InsuranceContract, InsuranceAgent, Branch, PromoCode, News, GlossaryTerm, Vacancy, Review
from .forms import InsuranceTypeForm, ClientForm, InsuranceContractForm, CustomUserCreationForm, CustomAuthenticationForm, ReviewForm
from django import forms
from django.utils import timezone
import logging
from .utils import get_weather, get_exchange_rates
from django.db.models import Avg, Count, Sum, Q
from django.db.models.functions import ExtractYear
from datetime import date
import statistics

logger = logging.getLogger('insurance_app')

def home(request):
    logger.info('Пользователь зашел на главную страницу')
    insurance_types = InsuranceType.objects.all()[:5]
    branches = Branch.objects.all()[:5]
    promocodes = PromoCode.objects.filter(is_active=True).order_by('-valid_until')[:5]
    
    # Получаем погоду для Минска
    weather = get_weather('Minsk')
    
    # Получаем курсы валют
    exchange_rates = get_exchange_rates()
    
    context = {
        'insurance_types': insurance_types,
        'branches': branches,
        'promocodes': promocodes,
        'weather': weather,
        'exchange_rates': exchange_rates,
    }
    return render(request, 'insurance_app/home.html', context)

def insurance_type_list(request):
    logger.info('Просмотр списка видов страхования')
    types = InsuranceType.objects.all()
    return render(request, 'insurance_app/insurance_type_list.html', {'types': types})

def client_list(request):
    clients = Client.objects.all()
    return render(request, 'insurance_app/client_list.html', {'clients': clients})

def create_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Клиент успешно создан')
            return redirect('insurance_app:client_list')
    else:
        form = ClientForm()
    return render(request, 'insurance_app/client_form.html', {'form': form})

@login_required
def contract_list(request):
    logger.info(f'Пользователь {request.user.username} просматривает список договоров')
    contracts = InsuranceContract.objects.filter(client__user=request.user)
    return render(request, 'insurance_app/contract_list.html', {'contracts': contracts})

def register(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        client_form = ClientForm(request.POST)
        if user_form.is_valid() and client_form.is_valid():
            user = user_form.save()
            client = client_form.save(commit=False)
            client.user = user
            client.email = user.email
            client.save()
            logger.info(f'Зарегистрирован новый пользователь: {user.username}')
            login(request, user)
            messages.success(request, 'Регистрация успешно завершена. Добро пожаловать в личный кабинет!')
            return redirect('insurance_app:profile')
        else:
            logger.warning('Ошибка при регистрации пользователя')
    else:
        user_form = CustomUserCreationForm()
        client_form = ClientForm()
    return render(request, 'insurance_app/register.html', {'user_form': user_form, 'client_form': client_form})

@login_required
def create_contract(request):
    if request.method == 'POST':
        form = InsuranceContractForm(request.POST)
        if form.is_valid():
            contract = form.save(commit=False)
            contract.client = request.user.client
            contract.save()
            logger.info(f'Создан новый договор №{contract.contract_number} для пользователя {request.user.username}')
            messages.success(request, 'Договор успешно создан')
            return redirect('insurance_app:contract_list')
        else:
            logger.warning(f'Ошибка при создании договора пользователем {request.user.username}')
    else:
        form = InsuranceContractForm()
        # Если передан параметр insurance_type, устанавливаем его как начальное значение
        insurance_type_id = request.GET.get('insurance_type')
        if insurance_type_id:
            try:
                insurance_type = InsuranceType.objects.get(id=insurance_type_id)
                form.initial['insurance_type'] = insurance_type
            except InsuranceType.DoesNotExist:
                pass
    return render(request, 'insurance_app/contract_form.html', {'form': form})

def insurance_type_detail(request, pk):
    insurance_type = get_object_or_404(InsuranceType, pk=pk)
    logger.info(f'Просмотр деталей вида страхования: {insurance_type.name}')
    return render(request, 'insurance_app/insurance_type_detail.html', {
        'insurance_type': insurance_type
    })

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                logger.info(f'Пользователь {username} успешно вошел в систему')
                messages.success(request, 'Вы успешно вошли в систему')
                return redirect('insurance_app:home')
            else:
                logger.warning(f'Неудачная попытка входа для пользователя {username}')
                messages.error(request, 'Неверное имя пользователя или пароль')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'insurance_app/login.html', {'form': form})

def logout_view(request):
    if request.user.is_authenticated:
        logger.info(f'Пользователь {request.user.username} вышел из системы')
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы')
    return redirect('insurance_app:home')

def news_list(request):
    logger.info('Пользователь просматривает список новостей')
    news = News.objects.all()
    return render(request, 'insurance_app/news_list.html', {'news': news})

def about(request):
    logger.info('Пользователь зашел на страницу "О компании"')
    return render(request, 'insurance_app/about.html')

def glossary(request):
    terms = GlossaryTerm.objects.all().order_by('category', 'term')
    categories = dict(GlossaryTerm._meta.get_field('category').choices)
    faqs = GlossaryTerm.objects.filter(is_faq=True).order_by('term')
    
    return render(request, 'insurance_app/glossary.html', {
        'terms': terms,
        'categories': categories,
        'faqs': faqs
    })

def faq(request):
    faqs = GlossaryTerm.objects.filter(is_faq=True).order_by('created_at')
    return render(request, 'insurance_app/faq.html', {'faqs': faqs})

@login_required
def profile(request):
    user = request.user
    try:
        client = Client.objects.get(user=user)
    except Client.DoesNotExist:
        client = None
        messages.info(request, 'Для полного доступа к функциям личного кабинета, пожалуйста, заполните свои данные.')
    
    contracts = InsuranceContract.objects.filter(client=client).order_by('-created_at') if client else []
    
    # Получаем погоду для Минска
    weather = get_weather('Minsk')
    
    # Получаем курсы валют
    exchange_rates = get_exchange_rates()
    
    context = {
        'user': user,
        'client': client,
        'contracts': contracts,
        'weather': weather,
        'exchange_rates': exchange_rates,
    }
    return render(request, 'insurance_app/profile.html', context)

@login_required
def contract_detail(request, contract_number):
    contract = get_object_or_404(InsuranceContract, contract_number=contract_number, client__user=request.user)
    logger.info(f'Пользователь {request.user.username} просматривает договор №{contract.contract_number}')
    return render(request, 'insurance_app/contract_detail.html', {
        'contract': contract
    })

def agents(request):
    agents = InsuranceAgent.objects.filter(is_active=True)
    return render(request, 'insurance_app/agents.html', {'agents': agents})

def vacancies(request):
    vacancies = Vacancy.objects.filter(is_active=True)
    return render(request, 'insurance_app/vacancies.html', {'vacancies': vacancies})

def privacy_policy(request):
    return render(request, 'insurance_app/privacy_policy.html')

def reviews(request):
    reviews = Review.objects.all()
    return render(request, 'insurance_app/reviews.html', {'reviews': reviews})

@login_required
def add_review(request):
    # Проверяем, есть ли у пользователя связанный клиент
    try:
        client = request.user.client
    except Client.DoesNotExist:
        # Если клиента нет, создаем его
        client = Client.objects.create(
            user=request.user,
            email=request.user.email,
            first_name=request.user.first_name or '',
            last_name=request.user.last_name or '',
            phone='+375 (29) 000-00-00'  # Значение по умолчанию
        )
        messages.info(request, 'Для вас был создан профиль клиента. Пожалуйста, заполните свои данные в личном кабинете.')
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.client = client
            review.save()
            messages.success(request, 'Ваш отзыв успешно добавлен')
            return redirect('insurance_app:reviews')
    else:
        form = ReviewForm()
    return render(request, 'insurance_app/add_review.html', {'form': form})

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    # Проверяем, что отзыв принадлежит текущему пользователю
    if review.client.user != request.user:
        messages.error(request, 'У вас нет прав на удаление этого отзыва')
        return redirect('insurance_app:reviews')
    
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Отзыв успешно удален')
        return redirect('insurance_app:reviews')
    
    return render(request, 'insurance_app/delete_review.html', {'review': review})

def statistics_view(request):
    # Получаем параметры поиска и сортировки
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', '')
    sort_order = request.GET.get('order', 'asc')
    
    # Базовый запрос для клиентов
    clients = Client.objects.all()
    
    # Применяем поиск
    if search_query:
        clients = clients.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(middle_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query)
        )
    
    # Применяем сортировку
    if sort_by == 'name':
        clients = clients.order_by('last_name', 'first_name' if sort_order == 'asc' else '-last_name', '-first_name')
    elif sort_by == 'age':
        clients = clients.order_by('date_of_birth' if sort_order == 'asc' else '-date_of_birth')
    elif sort_by == 'contracts':
        clients = clients.annotate(contract_count=Count('insurancecontract')).order_by(
            'contract_count' if sort_order == 'asc' else '-contract_count'
        )
    else:
        clients = clients.order_by('last_name', 'first_name')
    
    # Добавляем количество договоров для каждого клиента
    clients = clients.annotate(contract_count=Count('insurancecontract'))
    
    # Рассчитываем страховые премии
    contracts = InsuranceContract.objects.all()
    premiums = []
    for contract in contracts:
        premium = contract.insurance_sum * contract.tariff_rate / 100
        premiums.append(premium)
    
    # Общая сумма страховых взносов
    total_premium = sum(premiums)
    
    # Статистика по страховым взносам
    avg_premium = statistics.mean(premiums) if premiums else 0
    median_premium = statistics.median(premiums) if premiums else 0
    
    # Статистика по возрасту клиентов
    client_ages = []
    for client in clients:
        if client.date_of_birth:
            age = date.today().year - client.date_of_birth.year
            client_ages.append(age)
    
    avg_age = statistics.mean(client_ages) if client_ages else 0
    median_age = statistics.median(client_ages) if client_ages else 0
    
    # Популярность типов страхования
    insurance_types_stats = []
    for contract in contracts:
        premium = contract.insurance_sum * contract.tariff_rate / 100
        insurance_type_name = contract.insurance_type.name
        found = False
        for stat in insurance_types_stats:
            if stat['name'] == insurance_type_name:
                stat['count'] += 1
                stat['total_premium'] += premium
                found = True
                break
        if not found:
            insurance_types_stats.append({
                'name': insurance_type_name,
                'count': 1,
                'total_premium': premium
            })
    
    # Сортируем статистику по количеству договоров
    insurance_types_stats.sort(key=lambda x: x['count'], reverse=True)
    
    # Наиболее прибыльный тип страхования
    most_profitable = max(insurance_types_stats, key=lambda x: x['total_premium']) if insurance_types_stats else None
    
    context = {
        'clients': clients,
        'total_premium': total_premium,
        'avg_premium': round(avg_premium, 2),
        'median_premium': round(median_premium, 2),
        'avg_age': round(avg_age, 1),
        'median_age': round(median_age, 1),
        'insurance_types_stats': insurance_types_stats,
        'most_profitable': most_profitable,
        'search_query': search_query,
        'sort_by': sort_by,
        'sort_order': sort_order,
    }
    return render(request, 'insurance_app/statistics.html', context)

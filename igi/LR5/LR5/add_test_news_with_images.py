import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insurance_project.settings')
django.setup()

from django.utils import timezone
from insurance_app.models import News
from django.core.files import File
from PIL import Image
import requests
from io import BytesIO

# Список тестовых новостей с URL изображений
test_news = [
    {
        'title': 'Новые виды страхования в 2025 году',
        'content': 'Мы рады представить новые программы страхования, разработанные специально для наших клиентов. Теперь вы можете застраховать не только имущество, но и свои цифровые активы.',
        'short_content': 'Расширение линейки страховых продуктов в 2025 году',
        'image_url': 'https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=800'
    },
    {
        'title': 'Повышение качества обслуживания',
        'content': 'Наша компания внедряет новую систему обслуживания клиентов. Теперь вы можете получить консультацию онлайн 24/7, а также оформлять договоры через мобильное приложение.',
        'short_content': 'Внедрение инновационных технологий в обслуживании клиентов',
        'image_url': 'https://images.unsplash.com/photo-1552581234-26160f608093?w=800'
    },
    {
        'title': 'Скидки на страхование для молодых семей',
        'content': 'Специальное предложение для молодых семей! При оформлении договора страхования вы получаете скидку 15% на первый год страхования и бесплатную юридическую консультацию.',
        'short_content': 'Специальные условия для молодых семей',
        'image_url': 'https://images.unsplash.com/photo-1511895426328-dc8714191300?w=800'
    },
    {
        'title': 'Открытие нового филиала',
        'content': 'Мы рады сообщить об открытии нового филиала в центре города. Теперь наши клиенты могут получить все услуги в удобном месте с современным дизайном и комфортной зоной ожидания.',
        'short_content': 'Расширение сети офисов компании',
        'image_url': 'https://images.unsplash.com/photo-1497366754035-f200968a6e72?w=800'
    },
    {
        'title': 'Обновление мобильного приложения',
        'content': 'Вышло обновление нашего мобильного приложения! Теперь вы можете не только оформлять договоры, но и получать уведомления о продлении, оплачивать страховые взносы и общаться с агентом.',
        'short_content': 'Новые функции в мобильном приложении',
        'image_url': 'https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=800'
    }
]

# Создаем директорию для изображений, если она не существует
os.makedirs('media/news', exist_ok=True)

# Добавление новостей в базу данных
for i, news_item in enumerate(test_news):
    # Скачиваем изображение
    response = requests.get(news_item['image_url'])
    if response.status_code == 200:
        # Открываем изображение с помощью PIL
        img = Image.open(BytesIO(response.content))
        
        # Сохраняем изображение во временный файл
        temp_path = f'media/news/temp_{i}.jpg'
        img.save(temp_path)
        
        # Создаем новость с изображением
        news = News.objects.create(
            title=news_item['title'],
            content=news_item['content'],
            short_content=news_item['short_content'],
            created_at=timezone.now()
        )
        
        # Добавляем изображение к новости
        with open(temp_path, 'rb') as f:
            news.image.save(f'news_{i}.jpg', File(f), save=True)
        
        # Удаляем временный файл
        os.remove(temp_path)
    else:
        print(f"Не удалось загрузить изображение для новости: {news_item['title']}")

print('Тестовые новости с изображениями успешно добавлены!') 
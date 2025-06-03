from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib import admin

app_name = 'insurance_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('insurance-types/', views.insurance_type_list, name='insurance_type_list'),
    path('insurance-types/<int:pk>/', views.insurance_type_detail, name='insurance_type_detail'),
    path('clients/', views.client_list, name='client_list'),
    path('clients/create/', views.create_client, name='create_client'),
    path('contracts/', views.contract_list, name='contract_list'),
    path('contracts/create/', views.create_contract, name='create_contract'),
    re_path(r'^contracts/(?P<contract_number>[0-9]{8}[A-Z]{6})/$', views.contract_detail, name='contract_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('news/', views.news_list, name='news_list'),
    path('glossary/', views.glossary, name='glossary'),
    path('agents/', views.agents, name='agents'),
    path('vacancies/', views.vacancies, name='vacancies'),
    path('faq/', views.faq, name='faq'),
    path('profile/', views.profile, name='profile'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('reviews/', views.reviews, name='reviews'),
    path('reviews/add/', views.add_review, name='add_review'),
    path('reviews/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path('statistics/', views.statistics_view, name='statistics'),
    path('admin/', admin.site.urls),
] 
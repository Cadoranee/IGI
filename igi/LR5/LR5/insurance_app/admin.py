from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import InsuranceType, Client, InsuranceContract, Branch, InsuranceAgent, PromoCode

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone')
    search_fields = ('name', 'address', 'phone')

@admin.register(InsuranceAgent)
class InsuranceAgentAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'phone', 'email', 'experience_years', 'is_active')
    list_filter = ('is_active', 'experience_years')
    search_fields = ('first_name', 'last_name', 'middle_name', 'phone', 'email')
    fieldsets = (
        ('Основная информация', {
            'fields': ('first_name', 'last_name', 'middle_name', 'photo')
        }),
        ('Контактная информация', {
            'fields': ('phone', 'email')
        }),
        ('Профессиональная информация', {
            'fields': ('experience_years', 'specialization')
        }),
        ('Статус', {
            'fields': ('is_active',)
        }),
    )

@admin.register(InsuranceType)
class InsuranceTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'agent_commission')
    search_fields = ('name', 'description')

@admin.register(InsuranceContract)
class InsuranceContractAdmin(admin.ModelAdmin):
    list_display = ('contract_number', 'client', 'insurance_type', 'branch', 'agent', 
                   'insurance_sum', 'tariff_rate', 'start_date', 'end_date', 'agent_income')
    list_filter = ('branch', 'insurance_type', 'agent')
    search_fields = ('contract_number', 'client__user__email')
    date_hierarchy = 'start_date'

    def agent_income(self, obj):
        income = obj.calculate_agent_income()
        return format_html('<strong>{:.2f}</strong>', income)
    agent_income.short_description = 'Доход агента'

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address')
    search_fields = ('user__email', 'phone', 'address')

@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'description', 'discount_percent', 'is_active', 'valid_until')
    list_filter = ('is_active', 'valid_until')
    search_fields = ('code', 'description')
    date_hierarchy = 'valid_until'

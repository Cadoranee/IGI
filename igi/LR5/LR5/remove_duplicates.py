import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insurance_project.settings')
django.setup()

from django.db.models import Min, Count
from insurance_app.models import InsuranceType, Client, InsuranceContract, Branch, InsuranceAgent, PromoCode

def remove_duplicates():
    # Удаляем дубликаты InsuranceType
    duplicates = InsuranceType.objects.values('name').annotate(min_id=Min('id')).values('min_id')
    InsuranceType.objects.exclude(id__in=duplicates).delete()
    print("Удалены дубликаты InsuranceType")

    # Удаляем дубликаты Client
    duplicates = Client.objects.values('user').annotate(min_id=Min('id')).values('min_id')
    Client.objects.exclude(id__in=duplicates).delete()
    print("Удалены дубликаты Client")

    # Удаляем дубликаты Branch
    duplicates = Branch.objects.values('name', 'address').annotate(min_id=Min('id')).values('min_id')
    Branch.objects.exclude(id__in=duplicates).delete()
    print("Удалены дубликаты Branch")

    # Удаляем дубликаты InsuranceAgent
    duplicates = InsuranceAgent.objects.values('first_name', 'last_name', 'email').annotate(min_id=Min('id')).values('min_id')
    InsuranceAgent.objects.exclude(id__in=duplicates).delete()
    print("Удалены дубликаты InsuranceAgent")

    # Удаляем дубликаты PromoCode
    duplicates = PromoCode.objects.values('code').annotate(min_id=Min('id')).values('min_id')
    PromoCode.objects.exclude(id__in=duplicates).delete()
    print("Удалены дубликаты PromoCode")

if __name__ == '__main__':
    remove_duplicates() 
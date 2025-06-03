from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import InsuranceType, Client, InsuranceContract, Branch, InsuranceAgent, Review
from django.core.exceptions import ValidationError
from datetime import date, timedelta

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите email'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Подтвердите пароль'
        })
    )
    
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # Используем email как username
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Введите email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Введите пароль'
        })
    )

class InsuranceTypeForm(forms.ModelForm):
    class Meta:
        model = InsuranceType
        fields = ['name', 'description', 'agent_commission']
        widgets = {
            'agent_commission': forms.NumberInput(attrs={'step': '0.01'}),
        }

class ClientForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        label='Дата рождения',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'placeholder': 'Введите дату рождения'
        }),
        required=True
    )

    class Meta:
        model = Client
        fields = ['last_name', 'first_name', 'middle_name', 'phone', 'address', 'date_of_birth']
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+375 (29) XXX-XX-XX'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'})
        }

    def clean_date_of_birth(self):
        dob = self.cleaned_data['date_of_birth']
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        if age < 18:
            raise ValidationError('Вам должно быть не менее 18 лет для регистрации.')
        return dob

class InsuranceContractForm(forms.ModelForm):
    class Meta:
        model = InsuranceContract
        fields = ['insurance_type', 'branch', 'agent', 'insurance_sum', 'tariff_rate', 'start_date', 'end_date']
        widgets = {
            'insurance_type': forms.Select(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Выберите тип страхования'
            }),
            'branch': forms.Select(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Выберите филиал'
            }),
            'agent': forms.Select(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Выберите агента'
            }),
            'insurance_sum': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Введите страховую сумму',
                'title': 'Сумма, на которую заключается договор страхования'
            }),
            'tariff_rate': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Введите тарифную ставку',
                'title': 'Процент от страховой суммы, который заплатит клиент'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control form-control-lg',
                'type': 'date',
                'placeholder': 'Выберите дату начала'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control form-control-lg',
                'type': 'date',
                'placeholder': 'Выберите дату окончания'
            }),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.Select(
                attrs={'class': 'form-control'},
                choices=Review.RATING_CHOICES
            ),
            'text': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Напишите ваш отзыв...'
                }
            )
        } 
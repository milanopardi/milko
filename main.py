# 1. ساختار پروژه
'''
nat_coins_project/
│
├── manage.py
│
├── nat_coins_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
└── nat_coins/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── views.py
    ├── urls.py
    └── templates/
        ├── base.html
        ├── index.html
        └── invoice.html
    └── static/
        ├── css/
        │   └── styles.css
        └── js/
            └── app.js
    └── translations/
        └── fa.json
'''

# 2. settings.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'your-secret-key-here'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'nat_coins',  # اپلیکیشن اختصاصی ما
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'nat_coins_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# 3. models.py
from django.db import models

class NatCoinTransaction(models.Model):
    amount_toman = models.DecimalField(max_digits=10, decimal_places=2)
    amount_nat_coins = models.DecimalField(max_digits=10, decimal_places=4)
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount_toman} Toman - {self.amount_nat_coins} Nat Coins"

# 4. views.py
from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import NatCoinTransaction

def load_translations(lang='fa'):
    with open('nat_coins/translations/fa.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def index(request):
    translations = load_translations()
    return render(request, 'index.html', {'translations': translations})

def calculate_coins(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        amount = data.get('amount', 0)
        current_price = 10000  # قیمت هر سکه نت به تومان

        total_price = float(amount) * current_price
        
        # ذخیره تراکنش
        transaction = NatCoinTransaction.objects.create(
            amount_toman=total_price,
            amount_nat_coins=amount
        )

        return JsonResponse({
            'total_price': total_price,
            'current_price': current_price
        })

def generate_invoice(request):
    translations = load_translations()
    return render(request, 'invoice.html', {'translations': translations})

# 5. urls.py (پروژه)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('nat_coins.urls')),
]

# 6. urls.py (اپلیکیشن)
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('calculate/', views.calculate_coins, name='calculate'),
    path('invoice/', views.generate_invoice, name='invoice'),
]

# 7. base.html
'''
{% load static %}
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>{{ translations.app_title }}</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link rel="stylesheet" href="{% static 'css/styles.css' %}">
</head>
<body>
    {% block content %}{% endblock %}
    <script src="{% static 'js/app.js' %}"></script>
</body>
</html>
'''

# 8. index.html
'''
{% extends "base.html" %}
{% load static %}

{% block content %}
<div class="container">
    <!-- محتوای قبلی index.html -->
</div>
{% endblock %}
'''

# 9. invoice.html
'''
{% extends "base.html" %}
{% load static %}

{% block content %}
<div class="container">
    <!-- محتوای قبلی invoice.html -->
</div>
{% endblock %}
'''

# 10. راه‌اندازی اولیه
'''
1. نصب جانگو:
   pip install django

2. ایجاد پروژه:
   django-admin startproject nat_coins_project
   cd nat_coins_project
   python manage.py startapp nat_coins

3. کپی فایل‌های بالا در پوشه‌های مربوطه

4. اجرای مایگریشن‌ها:
   python manage.py makemigrations
   python manage.py migrate

5. اجرای سرور:
   python manage.py runserver
'''
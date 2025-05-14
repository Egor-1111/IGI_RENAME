from datetime import date
from decimal import Decimal
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import requests
import logging
from django.db.models import Count, Q
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, SelectEmployeeForm, ReviewForm
from django.http import HttpResponseForbidden
from .models import Client, Review,Vacancy,Tour,Employee, Order,PromoCode, UserSessionLog
from .forms import OrderForm, TourForm, PromoCodeForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
import io
import pandas as pd
from django.utils import timezone
import calendar
from datetime import datetime

logger = logging.getLogger(__name__)

# Главная страница с последней добавленной путевкой
def home(request):
    latest_tour = Tour.objects.order_by('-id').first()
    return render(request, 'main/home.html', {'latest_tour': latest_tour})

# Список туров
def tour_list(request):
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', 'base_price')

    tours = Tour.objects.all()

    if query:
        tours = tours.filter(
            Q(title__icontains=query) |
            Q(country__name__icontains=query)
        )

    if sort_by in ['base_price', '-base_price']:
        tours = tours.order_by(sort_by)

    return render(request, 'main/tour_list.html', {'tours': tours, 'query': query,'sort_by': sort_by})


# Детали тура
def tour_detail(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    weather = get_weather(tour.hotel.city)
    converted_price = convert_from_byn(tour.base_price, "USD")
    return render(request, 'main/tour_detail.html', {'tour': tour, 'weather': weather, 'converted_price': converted_price })
# Список клиентов (для проверки работы CRUD)
def client_list(request):
    clients = Client.objects.all()
    return render(request, 'main/client_list.html', {'clients': clients})


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # создаем клиента
            Client.objects.create(
                user=user,
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                patronymic=form.cleaned_data.get("patronymic", ""),
                address=form.cleaned_data["address"],
                phone=form.cleaned_data["phone"],
                birth_date=form.cleaned_data["birth_date"]
            )
            login(request, user)
            return redirect("select_employee")  # или на любую нужную страницу
    else:
        form = RegisterForm()
    return render(request, "main/register.html", {"form": form})
# Вход
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "main/login.html", {"form": form})

# Выход
def logout_view(request):
    logout(request)
    return redirect("home")

# Личный кабинет
@login_required
def profile_view(request):
    return render(request, "main/profile.html")

@login_required
def book_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)

    try:
        client = Client.objects.get(user=request.user)
    except Client.DoesNotExist:
        return HttpResponseForbidden("Вы не зарегистрированы как клиент.")

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.tour = tour
            order.client = client
            order.promo_code = form.cleaned_data.get("promo_code")
            order.save()
            return redirect('profile')  # перенаправление в личный кабинет
    else:
        form = OrderForm()

    return render(request, 'main/book_tour.html', {'form': form, 'tour': tour})

@login_required
def profile_view(request):
    try:
        client = Client.objects.get(user=request.user)
        orders = Order.objects.filter(client=client)
        used_promo_ids = orders.exclude(promo_code__isnull=True).values_list('promo_code__id', flat=True)
        used_promos = PromoCode.objects.filter(id__in=used_promo_ids)
        available_promos = PromoCode.objects.filter(
            is_active=True,
            valid_until__gte=date.today()
        ).exclude(id__in=used_promo_ids)
    except Client.DoesNotExist:
        orders = []
        used_promos = []
        available_promos = []
    return render(request, 'main/profile.html', {'orders': orders,'used_promos': used_promos,'available_promos': available_promos})

@login_required
def employee_dashboard(request):
    try:
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        return HttpResponseForbidden("Вы не являетесь сотрудником.")

    orders = Order.objects.filter(employee=employee) if employee else []
    clients = Client.objects.filter(employee=employee)
    tours = Tour.objects.all()
    return render(request, 'main/employee_dashboard.html', {'employee': employee, 'orders': orders , 'clients': clients , 'tours': tours})

# views.py

@login_required
def select_employee(request):
    try:
        client = request.user.client
    except Client.DoesNotExist:
        return HttpResponseForbidden("Вы не зарегистрированы как клиент.")

    if request.method == 'POST':
        form = SelectEmployeeForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = SelectEmployeeForm(instance=client)

    return render(request, 'main/select_employee.html', {'form': form})

@login_required
def add_review(request):
    if request.method == "POST":
        form = ReviewForm(request.POST, user=request.user)
        if form.is_valid():
            review = form.save(commit=False)
            review.client = Client.objects.get(user=request.user)
            review.save()
            return redirect('my_reviews')
    else:
        form = ReviewForm(user=request.user)
    return render(request, 'main/add_review.html', {'form': form})



@login_required
def all_reviews_view(request):

    from .models import Review
    reviews = Review.objects.select_related('client', 'tour')
    return render(request, 'main/all_reviews.html', {'reviews': reviews})


@login_required
def my_reviews(request):
    try:
        client = Client.objects.get(user=request.user)
        reviews = Review.objects.filter(client=client)
    except Client.DoesNotExist:
        reviews = []

    return render(request, 'main/my_reviews.html', {'reviews': reviews})

def get_weather(city):
    api_key = 'ab032113dbdc460da821bddb431f0dfe'
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=ru&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            'temp': data['main']['temp'],
            'desc': data['weather'][0]['description'],
        }
    return None

def get_exchange_rate(currency_code):
    url = f"https://www.nbrb.by/api/exrates/rates/{currency_code}?parammode=2"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        rate = Decimal(str(data["Cur_OfficialRate"]))
        scale = Decimal(str(data["Cur_Scale"]))
        return rate / scale
    except Exception as e:
        logger.error(f"Ошибка при получении курса валюты {currency_code}: {e}")
        return None


def convert_from_byn(amount_byn, to_currency="USD"):

    rate = get_exchange_rate(to_currency)
    if rate is None or rate == 0:
        return None
    return round(amount_byn / rate, 2)


@login_required
@staff_member_required
def create_promo_code(request):
    if request.method == 'POST':
        form = PromoCodeForm(request.POST)
        if form.is_valid():
            promo = form.save(commit=False)
            promo.created_by = request.user
            promo.save()
            return redirect('employee_dashboard')
    else:
        form = PromoCodeForm()
    return render(request, 'main/create_promo.html', {'form': form})

def tour_distribution_chart(request):
    tour_stats = Order.objects.values('tour__title').annotate(total=Count('id'))
    labels = [item['tour__title'] for item in tour_stats]
    values = [item['total'] for item in tour_stats]

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png).decode('utf-8')

    return render(request, 'main/tour_chart.html', {'chart': graphic})

def vacancy_list(request):
    vacancies = Vacancy.objects.all().order_by('-created_at')
    return render(request, 'main/vacancy_list.html', {'vacancies': vacancies})

def privacy_policy_view(request):
    return render(request, 'main/privacy_policy.html')

@staff_member_required
def tour_create(request):
    if request.method == 'POST':
        form = TourForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('tour_list')
    else:
        form = TourForm()
    return render(request, 'main/tour_form.html', {'form': form})

@staff_member_required
def tour_edit(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    if request.method == 'POST':
        form = TourForm(request.POST, request.FILES, instance=tour)
        if form.is_valid():
            form.save()
            return redirect('tour_detail', pk=pk)
    else:
        form = TourForm(instance=tour)
    return render(request, 'main/tour_form.html', {'form': form, 'tour': tour})

@staff_member_required
def tour_delete(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    if request.method == 'POST':
        tour.delete()
        return redirect('tour_list')
    return render(request, 'main/tour_confirm_delete.html', {'tour': tour})


def user_time_chart(request):
    logs = UserSessionLog.objects.exclude(logout_time__isnull=True)
    data = []

    for log in logs:
        duration = log.duration_minutes()
        if duration:
            data.append({'user': log.user.username, 'duration_minutes': duration})

    df = pd.DataFrame(data)
    if df.empty:
        average = 0
    else:
        average = df['duration_minutes'].mean()

    plt.figure(figsize=(10, 6))
    if not df.empty:
        plt.bar(df['user'], df['duration_minutes'], color='skyblue', label='Пользователь')
        plt.axhline(y=average, color='red', linestyle='--', label=f'Среднее: {average:.1f} мин')
    plt.title('Время, проведённое пользователями на сайте')
    plt.ylabel('Минуты')
    plt.xlabel('Пользователи')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    chart_data = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()

    return render(request, 'main/user_time_chart.html', {'chart_data': chart_data})


def time_info_view(request):
    now = timezone.now()

    # Временная зона пользователя (можно получить из профиля или браузера — здесь просто UTC+3 как пример)
    user_timezone = 'Europe/Moscow'  # заменишь на динамическое значение при необходимости

    # Календарь на текущий месяц в виде текста
    cal = calendar.TextCalendar(calendar.MONDAY)
    calendar_text = cal.formatmonth(now.year, now.month)

    # Пример одного тура (для отображения дат создания/изменения)
    tours = Tour.objects.all()

    return render(request, 'main/time_info.html', {'now': now,'user_timezone': user_timezone,'calendar_text': calendar_text,'tours': tours})
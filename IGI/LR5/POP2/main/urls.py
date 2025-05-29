from django.urls import path,re_path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Главная страница
    path('tours/', views.tour_list, name='tour_list'),  # Список туров
    path('tours/<int:pk>/', views.tour_detail, name='tour_detail'),  # Детали тура
    path('clients/', views.client_list, name='client_list'),  # Список клиентов (для проверки)
    path('register/', views.register_view, name='register'), # Регистрация
    path('login/', views.login_view, name='login'), # Авторизация
    path('logout/', views.logout_view, name='logout'), # Выход
    path('profile/', views.profile_view, name='profile'), # Профиль
    path('tour/<int:tour_id>/book/', views.book_tour, name='book_tour'),
    path('dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path("select-employee/", views.select_employee, name="select_employee"),
    path('reviews/', views.all_reviews_view, name='all_reviews'),
    path('add_review/', views.add_review, name='add_review'),
    path('my_reviews/', views.my_reviews, name='my_reviews'),
    path('create_promo/', views.create_promo_code, name='create_promo'),
    re_path(r'^chart/$', views.tour_distribution_chart, name='tour_chart'),
    re_path(r'^privacy/$', views.privacy_policy_view, name='privacy_policy'),
    re_path(r'^vacancies/$', views.vacancy_list, name='vacancy_list'),
    re_path(r'^tours/create/$', views.tour_create, name='tour_create'),
    path('tours/<int:pk>/edit/', views.tour_edit, name='tour_edit'),
    path('tours/<int:pk>/delete/', views.tour_delete, name='tour_delete'),
    path('user-time-chart/', views.user_time_chart, name='user_time_chart'),
    path('time_info/', views.time_info_view, name='time_info'),
    path('faq/', views.faq_view, name='faq'),
    path('about/', views.about_view, name='about'),
    path('news/', views.news_list, name='news_list'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    path('contacts/', views.contact_list, name='contact_list'),
]


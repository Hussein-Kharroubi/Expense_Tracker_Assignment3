from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('expenses/<int:expense_id>/edit/', views.edit_expense, name='edit_expense'),
    path('expenses/<int:expense_id>/delete/', views.delete_expense, name='delete_expense'),
    path('expenses/edit/', views.expense_list, {'mode': 'edit'}, name='edit_list'),
    path('expenses/delete/', views.expense_list, {'mode': 'delete'}, name='delete_list'),
    path('search/', views.search_expense, name='search_expenses'),
    path('profile/', views.profile, name='profile'),
    path('history/', views.history, name='history'),

]

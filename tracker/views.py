from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from .forms import ExpenseForm
from .models import Expense
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, Q

@login_required
def profile(request):
    return render(request, 'profile.html')

def index(request):
	if request.user.is_authenticated:
		return redirect('dashboard')
	LoginForm = AuthenticationForm(request, data=request.POST, prefix='login')
	RegisterForm = UserCreationForm(data=request.POST, prefix='register')
	if request.method == 'POST':
		if 'login' in request.POST:
			LoginForm = AuthenticationForm( data=request.POST, prefix='login')
			if LoginForm.is_valid():
				user = LoginForm.get_user()
				login(request, user)
				return redirect('dashboard')
		elif 'register' in request.POST:
			RegisterForm = UserCreationForm(data=request.POST, prefix='register')
			if RegisterForm.is_valid():
				login(request, RegisterForm.save())
				return redirect('dashboard')
			print(RegisterForm.errors)
	return render(request, 'index.html', {'LoginForm': LoginForm, 'RegisterForm': RegisterForm})


@login_required
def history(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date', '-timestamp')
    return render(request, 'history.html', {'expenses': expenses})


@login_required
def add_expense(request):
	if request.method == 'POST':
		form = ExpenseForm(request.POST)
		if form.is_valid():
			expenseform = form.cleaned_data
			Expense.objects.create(
				user=request.user,
				category=expenseform['category'],
				store=expenseform['store'],
				amount=expenseform['amount'],
				date=expenseform['date'],
				description=expenseform['description'],
			)
			return redirect('dashboard')
	else:
		form = ExpenseForm()
	return render(request, 'add_expense.html', {'form': form})

@login_required
def expense_list(request, mode):
    q = request.GET.get('q', '').strip()
    category = request.GET.get('category', '')

    expenses = Expense.objects.filter(user=request.user).order_by('-date', '-timestamp')
    if q:
        expenses = expenses.filter(Q(store__icontains=q) | Q(description__icontains=q))
    if category:
        expenses = expenses.filter(category=category)
    expenses = expenses[:50]

    if mode == 'edit':
        title, action, label = 'Edit expense', 'edit_expense', 'Edit'
    else:
        title, action, label = 'Delete expense', 'delete_expense', 'Delete'
    return render(request, 'pick_expense.html', {
        'expenses': expenses, 'title': title, 'action': action, 'label': label,
        'q': q, 'category': category, 'categories': Expense.Category.choices})


@login_required
def edit_expense(request, expense_id):

	expense = get_object_or_404(Expense, id=expense_id, user=request.user)
	if request.method == 'POST':
		form = ExpenseForm(request.POST, instance=expense)
		if form.is_valid():
			form.save()
			messages.success(request, 'Expense updated.')
			return redirect('edit_list')
	else:
		form = ExpenseForm(instance=expense)
	return render(request, 'edit_expense.html', {'form': form, 'expense': expense})


@login_required
def delete_expense(request, expense_id):

	expense = get_object_or_404(Expense, id=expense_id, user=request.user)
	if request.method == 'POST':
		expense.delete()
		messages.success(request, 'Expense deleted.')
		return redirect('delete_list')
	return render(request, 'delete_expense.html', {'expense': expense})


@login_required
def dashboard(request):
	expenses = Expense.objects.filter(user=request.user).order_by('-date', '-timestamp')
	today = timezone.localdate()
	total_this_month = expenses.filter(date__year=today.year, date__month=today.month).aggregate(total=Sum('amount'))['total'] or 0
	spending_by_category = expenses.values('category').annotate(total=Sum('amount')).order_by('category')
	recent_expenses = expenses.filter(date__gte=today - timedelta(days=13), date__lte=today)
	monthly_summary = expenses.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('amount')).order_by('-month')
	return render(request, 'dashboard.html', {
		 'total_this_month': total_this_month,
		'spending_by_category': spending_by_category, 'recent_expenses': recent_expenses,
		'monthly_summary': monthly_summary, 'today': today})




@login_required
def search_expense(request):
		
	expense = Expense.objects.none() # this basically makes sure that once user presses the button, the initial table for results is empty
		
	if request.GET:
		expense = Expense.objects.filter(user=request.user).order_by('-date', '-timestamp')

	category = request.GET.get('category')
	start_date = request.GET.get('start_date')
	end_date = request.GET.get('end_date')
	min_amount = request.GET.get('min_amount')
	max_amount = request.GET.get('max_amount')

	error = None


	if start_date and end_date and start_date > end_date: # here we will check for errors that could occur
			error = "From Date cannot be after To Date."

	if min_amount and float(min_amount) < 0:
			error = "Minimum amount cannot be negative."

	if max_amount and float(max_amount) < 0:
			error = "Maximum amount cannot be negative."

	if min_amount and max_amount and float(min_amount) > float(max_amount):
			error = "Minimum amount cannot exceed Maximum amount."

	if error is None: # now here we will apply the filters that will be rendered in the html 
			if category:
					expense = expense.filter(category=category)

			if start_date:
					expense = expense.filter(date__gte=start_date)

			if end_date:
					expense = expense.filter(date__lte=end_date)

			if min_amount:
					expense = expense.filter(amount__gte=min_amount)

			if max_amount:
					expense = expense.filter(amount__lte=max_amount)
	else:
			expense = Expense.objects.none()

	return render(request, 'search.html', { 
			'expenses': expense,
			'error': error
	})


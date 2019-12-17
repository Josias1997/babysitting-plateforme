from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.db.models import Q
from django.contrib import messages
from .models import User, Schedule, Booking, Comment
from decimal import Decimal

# Create your views here.
def index(request):
	if not request.user.is_authenticated:
		return redirect('login')
	sitter_bookings = []
	bookings_made = []
	if request.user.is_sitter:
		sitter_bookings = Booking.objects.filter(sitter__id=request.user.id)
	if request.user.is_parent:
		bookings_made = Booking.objects.filter(parent__id=request.user.id)
	return render(request, 'backend/index.html', {
		'bookings': sitter_bookings,
		'bookings_made': bookings_made
	})


def user_login(request):
	if request.method == 'POST':
		user_login = request.POST['login']
		if User.objects.filter(username=user_login).exists():
			password = request.POST['password']
			user = User.objects.get(username=user_login)
			if user.check_password(password):
				login(request, user)
				return redirect('index')
			else:
				messages.error(request, "Mot de passe incorrect")
		elif User.objects.filter(email=user_login).exists():
			password = request.POST['password']
			user = User.objects.get(email=user_login)
			if user.check_password(password):
				login(request, user)
				return redirect('index')
			else:
				messages.error(request, "Mot de passe incorrect")
		else:
			messages.error(request, "Email ou nom d'utilisateur incorrect")
			
	return render(request, 'backend/login.html')


def register(request):
	if request.method == 'POST':
		first_name = request.POST['firstName']
		last_name = request.POST['lastName']
		username = request.POST['login']
		email = request.POST['email']
		password  = request.POST['password']
		confirmed_password = request.POST['cPassword']
		is_parent = False
		if 'parent' in request.POST:
			is_parent = True
		is_sitter = False
		if 'sitter' in request.POST:
			is_sitter = True
		if password == confirmed_password:
			user = User(username=username, email=email, first_name=first_name, last_name=last_name, is_sitter=is_sitter, is_parent=is_parent)
			user.set_password(password)
			user.save()
			return redirect('login')
	return render(request, 'backend/register.html')


def user_logout(request):
	logout(request)
	return redirect('index')


def add_schedule(request):
	if request.method == 'POST':
		date = request.POST['date']
		if not Schedule.objects.filter(date=date).exists():
			schedule = Schedule(date=date)
			schedule.save()
			user = request.user
			user.schedules.add(schedule)
			user.save()
			messages.success(request, 'Date ajoutée avec succès')
		else:
			messages.error(request, 'Vous avez déjà ajouter cette date')
	return redirect('index')


def set_pricing(request):
	if request.method == 'POST':
		price = request.POST['price']
		user = request.user
		user.set_pricing(price)
		user.save()
		messages.success(request, 'Tarif ajouté avec succès')
	return redirect('index')

def search_for_sitters(request):
	if request.method == 'POST':
		date = request.POST['date']
		sitters = User.objects.filter(Q(is_sitter=True) & ~Q(id=request.user.id) & Q(schedules__date=date))
		return render(request, 'backend/search-results.html', {
				'sitters': sitters,
				'date': date
		})
	return redirect('index')


def book_sitter(request, parent_id, sitter_id, date):
	if request.method == 'GET':
		sitter = User.objects.get(id=sitter_id)
		parent = User.objects.get(id=parent_id)
		schedule = Schedule.objects.get(date=date)
		booking = Booking(parent=parent, sitter=sitter, date=schedule)
		booking.save()
		sitter_schedule = Schedule.objects.get(Q(date=date) & Q(sitters_concerned__id=sitter_id))
		sitter_schedule.set_is_booked(True)
		sitter_schedule.save()
		messages.success(request, 'Sitter réservé avec succès')
	return redirect('search-sitters')


def give_feedback(request, sitter_id, booking_id):
	return render(request, 'backend/feedback.html', {
		'sitter_id': sitter_id,
		'booking_id': booking_id
	})


def send_feedback(request):
	if request.method == 'POST':
		mark = request.POST['mark']
		feedback = request.POST['feedback']
		sitter_id = request.POST['sitter_id']
		booking_id = request.POST['booking_id']
		sitter = User.objects.get(id=sitter_id)
		booking = Booking.objects.get(id=booking_id)
		comment = Comment(author=request.user, booking=booking, content=feedback)
		comment.save()
		sitter.increase_number_marks()
		sitter.update_avg_mark(Decimal(mark))
		sitter.save()
	return redirect('index')

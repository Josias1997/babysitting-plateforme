from django.urls import path
from .views import (index, user_login, register, user_logout, add_schedule, 
	set_pricing, search_for_sitters, book_sitter, give_feedback, send_feedback)

urlpatterns = [
	path('', index, name='index'),
	path('login', user_login, name='login'),
	path('register', register, name='register'),
	path('logout', user_logout, name='logout'),
	path('add-schedule', add_schedule, name='add-schedule'),
	path('set-pricing', set_pricing, name='set-pricing'),
	path('search-sitters', search_for_sitters, name='search-sitters'),
	path('book-sitter/<int:parent_id>/<int:sitter_id>/<str:date>', book_sitter, name='book-sitter'),
	path('give_feedback/<int:sitter_id>/<int:booking_id>', give_feedback, name='give-feedback'),
	path('send-feedback', send_feedback, name='send-feedback')
]
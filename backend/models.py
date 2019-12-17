from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.
class Schedule(models.Model):
	date = models.DateField(default=timezone.now)
	is_booked = models.BooleanField(default=False)

	def set_is_booked(self, value):
		self.is_booked = value


class User(AbstractUser):
	is_sitter = models.BooleanField(default=False)
	is_parent = models.BooleanField(default=False)
	pricing = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
	avg_mark = models.DecimalField(max_digits=2, decimal_places=1, default=0)
	number_marks = models.IntegerField(default=0)
	schedules = models.ManyToManyField(Schedule, related_name='sitters_concerned', blank=True)

	def __str__(self):
		return self.username

	def set_pricing(self, pricing):
		self.pricing = pricing

	def update_avg_mark(self, new_mark):
		self.avg_mark = (self.avg_mark + new_mark) / self.number_marks

	def increase_number_marks(self):
		self.number_marks = self.number_marks + 1


class Booking(models.Model):
	parent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings_made')
	sitter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings_obtained')
	date = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='bookings')
	booked_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.parent.username} {self.sitter.username} {self.date.date}'

	def date_has_passed(self):
		return self.date.date < timezone.now



class Comment(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_comments")
	booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="booking_comments")
	content = models.TextField()

	def __str__(self):
		return self.author.username







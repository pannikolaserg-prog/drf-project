from django_filters import rest_framework as filters
from .models import Payment


class PaymentFilter(filters.FilterSet):
    payment_date = filters.DateFromToRangeFilter()  # Фильтр по диапазону дат
    course = filters.NumberFilter()  # Фильтр по курсу
    lesson = filters.NumberFilter()  # Фильтр по уроку
    payment_method = filters.ChoiceFilter(choices=Payment.PAYMENT_METHODS)  # Фильтр по способу оплаты

    class Meta:
        model = Payment
        fields = ['payment_date', 'course', 'lesson', 'payment_method']


from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, status
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView, get_object_or_404)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course
from .filters import PaymentFilter
from .models import Payment, User, Subscription
from .serializers import (PaymentSerializer, UserProfileSerializer,
                          UserSerializer)

from rest_framework import generics, permissions

from .services import create_stripe_payment


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response({"message": f"Пользователь {user.email} удален"})


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = PaymentFilter
    ordering_fields = ["payment_date"]  # Можно сортировать по дате
    ordering = ["-payment_date"]  # По умолчанию сортировка: сначала новые


class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class SubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        course = get_object_or_404(Course, id=request.data.get('course_id'))

        sub = Subscription.objects.filter(user=user, course=course)

        if sub.exists():
            sub.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course)
            message = "Подписка добавлена"

        return Response({"message": message})


# class CreatePaymentView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#         amount = request.data.get('amount', 1000)  # 1000 = 10.00 USD
#
#         try:
#             # Создаём сессию в Stripe
#             session = stripe.checkout.Session.create(
#                 payment_method_types=['card'],
#                 line_items=[{
#                     'price_data': {
#                         'currency': 'usd',
#                         'product_data': {
#                             'name': f'Оплата от {request.user.email}',
#                         },
#                         'unit_amount': int(amount),  # в копейках
#                     },
#                     'quantity': 1,
#                 }],
#                 mode='payment',
#                 success_url='http://localhost:8000/api/payments/success/',
#                 cancel_url='http://localhost:8000/api/payments/cancel/',
#             )
#
#             # Сохраняем в БД (если нужна модель Status_Pay)
#             # Status_Pay.objects.create(
#             #     user=request.user,
#             #     amount=amount,
#             #     session_id=session.id,
#             #     link=session.url
#             # )
#
#             return Response({
#                 'payment_url': session.url,
#                 'session_id': session.id
#             })
#
#         except Exception as e:
#             return Response({'error': str(e)}, status=400)


class PaymentSuccessView(APIView):
    def get(self, request):
        return Response({'message': 'Оплата успешна!'})


class PaymentCancelView(APIView):
    def get(self, request):
        return Response({'message': 'Оплата отменена'})


class Status_PayCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        amount = request.data.get('amount')
        course_id = request.data.get('course_id')

        if not amount:
            return Response(
                {'error': 'Сумма обязательна'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Используем сервис для создания платежа
        result = create_stripe_payment(
            user=request.user,
            amount=amount,
            course_id=course_id
        )

        if result['success']:
            return Response({
                'payment_url': result['payment_url'],
                'session_id': result['session_id'],
                'payment_id': result['payment_id'],
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {'error': result['error']},
                status=status.HTTP_400_BAD_REQUEST
            )

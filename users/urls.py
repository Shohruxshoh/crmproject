from django.urls import path
from .views import PhoneTokenObtainView, RegisterView, PhoneTokenObtainAminView, RegionCreateAndListView, \
    DistrictCreateAndListView, OperatorUpdateView, OperatorListView, UserMeView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('operators/', OperatorListView.as_view()),
    path('register-operator/', RegisterView.as_view()),
    path('operator-update/<int:pk>', OperatorUpdateView.as_view()),
    path('login-admin/', PhoneTokenObtainAminView.as_view(), name='login-admin'),
    path('login-operator/', PhoneTokenObtainView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('region/', RegionCreateAndListView.as_view()),
    path('district/', DistrictCreateAndListView.as_view()),


    path('user-me/', UserMeView.as_view()),

]

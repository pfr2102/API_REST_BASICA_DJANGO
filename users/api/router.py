from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from users.api.views import UserApiViewSet, UserView, GroupView

router_user = DefaultRouter()

router_user.register(
    prefix='users', 
    basename='users',
    viewset=UserApiViewSet
)

#esta ruta se trabaja diferente porque es para saber los datos del usuario que se autentica 
urlpatterns = [
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/me/', UserView.as_view()),
    path('group/', GroupView.as_view(), name='group-list'),
]

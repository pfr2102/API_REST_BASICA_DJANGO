from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated, DjangoModelPermissions
from icard.permissions import CustomDjangoModelPermission #no es mas que DjangoModelPermissions nomas que sobre-escrito para que pueda bloquear lo get tambien
from django.contrib.auth.hashers import make_password

#importaciones necesarias para hacer solicitudes http personalizadas
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

#importaciones personales de nuestro proyecto
from users.models import User
from users.api.serializers import UserSerializer


class UserApiViewSet(ModelViewSet):
    #permission_classes = [IsAdminUser]
    #de esta otra forma toma los permisos prestablecidos por rest framework y no los que le agregaste en el panel de administracion
    permission_classes = [CustomDjangoModelPermission] 
    #de esta forma toma los permisos del modelo que tu le agregaste desde el panel de administracion de django los cuales
    #recuerda que se asignan a traves de un grupo al cual se le asignan los permisos como tipo roles
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('id')

    #SOBRE-ESCRIBIMOS EL METODO CREATE DE LA SUPERCLASE DE LA QUE HEREDAMOS PARA QUE ENCRIPTE EL PASSWORD ANTES DE INSERTARLO EN LA BD
    def create(self, request, *args, **kwargs):
        request.data['password'] = make_password(request.data['password'])
        return super().create(request, *args, **kwargs)
    
    #SOBRE- ESCRIBIMOS EL METODO DEL PATCH DE LA SUPERCLASE PARA QUE DETECTE CUANDO SE MODIFICO LA CONTRASEÑA Y LA ENCRIPTE DE NUEVO
    def partial_update(self, request, *args, **kwargs):
        password = request.data.get('password')
        if password is not None:
            request.data['password'] = make_password(password)
        return super().partial_update(request, *args, **kwargs)
    
    
    #EJEMPLO DE COMO CREAR TU PROPIA SOLICITUD HTTP PERSONALISADA    
    @action(detail=False, methods=['get'])
    def custom_greeting(self, request):
        try:
            # Tu lógica aquí
            data = {"message": "¡Hola! Bienvenido a mi API."}
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            # Maneja la excepción de manera específica o general
            data = {"error": f"Error inesperado: {str(e)}"}
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

#creamos otra vista para obtener los datos del usuario que se autentica
class UserView(APIView):
    permission_classes = [IsAuthenticated]  
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from django.contrib.auth.models import Group
from rest_framework.permissions import IsAdminUser, IsAuthenticated, DjangoModelPermissions
from icard.permissions import CustomDjangoModelPermission #no es mas que DjangoModelPermissions nomas que sobre-escrito para que pueda bloquear lo get tambien
from django.contrib.auth.hashers import make_password

#importaciones necesarias para hacer solicitudes http personalizadas
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

#importaciones personales de nuestro proyecto
from users.models import User
from users.api.serializers import UserSerializer, GroupSerializer


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
    #TAMBIEN SE ASIGNA EL NUEVO GRUPO EN CASO DE EXISTIR EN LA SOLICITUD DE ACTUALIZACION (REQUEST)
    def partial_update(self, request, *args, **kwargs):
        """
        Actualizar un usuario con un nuevo grupo asignado.

        Permite crear un usuario y asignarle un nuevo grupo existente. 
        El grupo debe ser proporcionado en el campo 'group'. 
        internamente esto actualiza la tabla (users_user_group) la cual administra las relaciones entre grupos y usuarios como tabla intermediaria.
        """
        try:
            with transaction.atomic():  # Inicia una transacción
                # Obtener el ID del nuevo grupo enviado en la solicitud a actualizar 
                group_id = request.data.get('group')  
                if group_id is not None: 
                    # Obtener el usuario
                    user = self.get_object()  
                    # Eliminar todos los grupos asociados actualmente al usuario
                    user.groups.clear()
                    # Agregar el nuevo grupo al usuario
                    user.groups.add(group_id)

                password = request.data.get('password')
                if password is not None:
                    request.data['password'] = make_password(password)
                return super().partial_update(request, *args, **kwargs)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    #SOBRE- ESCRIBIMOS EL METODO DEL PATCH DE LA SUPERCLASE PARA QUE DETECTE CUANDO SE MODIFICO LA CONTRASEÑA Y LA ENCRIPTE DE NUEVO
    """ def partial_update(self, request, *args, **kwargs):
        password = request.data.get('password')
        if password is not None:
            request.data['password'] = make_password(password)
        return super().partial_update(request, *args, **kwargs) """
    
    
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
        
    # Nueva acción para la creación de usuario y asignación de grupos   
    @action(detail=False, methods=['post'])
    def create_with_group(self, request, *args, **kwargs):
        """
        Crea un usuario con un grupo asignado.

        Permite crear un usuario y asignarle un grupo existente. El grupo debe ser proporcionado en el campo 'group'.
        """
        # Verifica si se proporcionó un grupo
        if 'group' not in request.data:
            return Response({"error": "Se requiere el ID del grupo."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            with transaction.atomic():  # Inicia una transacción
                # Encripta la contraseña antes de la creación
                request.data['password'] = make_password(request.data['password'])
                # Crea el usuario utilizando el método create del ModelViewSet
                user_response = super().create(request, *args, **kwargs)
                # Obtiene el usuario creado a partir de la respuesta
                user_data = user_response.data
                # Obtiene el ID del grupo a asignar
                group_id = request.data.get('group')
                # Verifica si se proporcionó un ID de grupo
                if group_id is not None:
                    user_instance = User.objects.get(id=user_data['id'])
                    user_instance.groups.add(group_id)
                # Devuelve la respuesta con los datos del usuario creado
                return user_response
        except User.DoesNotExist:
            return Response({"error": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"Error inesperado: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @action(detail=False, methods=['post'])
    def create_users_with_groupsM(self, request, *args, **kwargs):
        """
        Crea usuarios con grupos asignados de forma masiva.

        Permite crear usuarios en grandes cantidades proporcionando una lista de datos de usuarios.
        Cada dato de usuario debe tener el formato requerido por el serializador UserSerializer.
        Además, cada usuario puede incluir un campo 'group' para especificar el ID del grupo al que se asignará.
        """
        serializer = UserSerializer(data=request.data, many=isinstance(request.data, list))
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    for user_data in serializer.validated_data:
                        user_data['password'] = make_password(user_data['password']) # Encripta la contraseña
                        user_instance = User.objects.create(**user_data)
                        # Obtiene el ID del grupo a asignar
                        group_id = user_data.get('group')
                        # Verifica si se proporcionó un ID de grupo
                        if group_id is not None:
                            user_instance.groups.add(group_id)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




#creamos otra vista para obtener los datos del usuario que se autentica
class UserView(APIView):
    permission_classes = [IsAuthenticated]  
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
#creamos una vista para obtener todos los grupos
class GroupView(APIView):
    permission_classes = [CustomDjangoModelPermission] 
    #permission_classes = [IsAuthenticated]  # O cualquier permiso que desees

    def get_queryset(self):
        return Group.objects.all().order_by('id')
    
    def get(self, request):
        groups = self.get_queryset()
        #groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)
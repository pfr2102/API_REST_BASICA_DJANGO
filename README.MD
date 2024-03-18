# API-REST ESTANDAR DJANGO

## Clonar el Repositorio

Para comenzar a trabajar en este proyecto en tu máquina local, sigue estos pasos:

1. Abre tu terminal.

2. Crea un entorno virtual dentro de la misma carpeta donde clones este proyecto.

   ```bash
   python -m venv envs/Nombre_del_entorno
   .\envs\Nombre_del_entorno\Scripts\Activate
   pip install django

   ```

3. Utiliza el siguiente comando para clonar el repositorio en tu máquina:

   ```bash
   git clone https://github.com/pfr2102/API_REST_BASICA_DJANGO.git
   ```

## Instala dependencias del proyecto dentro del entorno virtual

    pip install -r requirements.txt

## Crea las migraciones de los modelos y corre el proyecto (todo dentro del entorno virrual)

    python manage.py makemigrations

    python manage.py migrate

    python manage.py runserver

## Crea un Super Usuario para poder acceder al panel de administracion de django

    python manage.py createsuperuser


[!NOTE]
## Push y Pull desde tu repositorio local

- **git push**: Con este comando, mandas al repositorio remoto todas las modificaciones de tu repositorio local. Por lo tanto, cada vez que lo uses, debes estar seguro de que tu proyecto esté en una versión estable y sin fallas. En caso de necesitar realizar pruebas o cambios experimentales, se recomienda crear una rama para ello y hacer todos los push que quieras en esa rama sin afectar la rama `main`, que contiene la versión estable del proyecto.

- **git pull**: Utiliza este comando para actualizar los cambios que haya recibido el repositorio remoto en GitHub, pero ten en cuenta que se aplicará solo a la rama `main`. Esto asegura que tu repositorio local esté al día con la última versión del proyecto en el repositorio remoto.


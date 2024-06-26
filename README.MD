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

> [!NOTE]
> cuando creas un superusuario por terminal de comandos es importante que en el archivo model.py de users comentes las 2 ultimas lineas esto ya que de no comentarlas solo te pedira el email y tambien necesita pedirte el username si no no te lo crea correctamente. despues de crearlo ya las puedes descomentar para que al autentificarte te pida como nombre de usuario el correo

> [!NOTE]
> ## Push y Pull desde tu repositorio local
>
   > - **git push** <-- con esto mandas al repo remoto todas las modificaciones de tu repo local, asi que cada vez que lo uses tienes que estar seguro de que tu proyecto este en una version estable y sin fallas o en  todo caso hacer una rama para hacer calis y hacer todos los push que quieras sin afectar la rama main que tiene la version estable.
>
   > - **git pull** <-- con esto actualizas los cambios que haya recibido el repo remoto en git-hub (solo de la rama main)

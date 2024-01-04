# Speer Notes Project

This is a Django-based project for managing/sharing notes.


## Framework/DB/3rd Party Tools

- Framework: Django
- Database: PostgreSQL
- 3rd Party Tools: Docker, Docker-compose, Django REST Framework, GinIndex, Django ratelimit
  

## Run the app:

   1. Clone the repository and move inside the repository

      ```git clone https://github.com/Milan097/Notes.git && cd Notes```
      
   2. Start the docker containers
      
      ```docker-compose up -d --built```
      
   3. Access the app at
      
      ```http://0.0.0.0:8000/```
   

## Run the testcases:

   ```docker-compose exec web python manage.py test```

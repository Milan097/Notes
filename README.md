# Speer Notes Project

This is a Django-based project for managing/sharing notes.

## Framework/DB/3rd Party Tools

- Framework: Django
- Database: PostgreSQL
- 3rd Party Tools: Docker, Docker-compose, Django REST Framework, GinIndex, Django ratelimit

## Setup Instructions

1. Run the app:
   ```docker-compose up -d --built```

2. Run the testcases:
   ```docker-compose exec web python manage.py test```

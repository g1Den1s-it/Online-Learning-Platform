# Online Learning Platform


An online platform where users can participate as either a teacher or a student, 
allowing them to create courses or enroll in existing ones to learn.

### Technologies Used
* Django 
* Django rest framework
* Celery
* Redis

### Installation
1. Clone from GitHub
   ```bash
   git clone https://github.com/g1Den1s-it/Online-Learning-Platform.git
   ```
2. Install requirements
   ```bash
   pip install -r requirements.txt
   ```
3. Run Redis in docker or install it
   ```bash
   docker run --name redis -p 6379:6379 redis:latest
   ```
4. Run Django migration
    ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. Run Django
    ```bash
   python manage.py runserver
   ```
6. Run celery in second terminal 
    ```bash
   celery -A online_learning_platform worker -l info
   ```
from django.apps import AppConfig


class ApitestConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apitest'

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

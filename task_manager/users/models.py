from django.contrib.auth.models import User as DjangoUser

class User(DjangoUser):

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
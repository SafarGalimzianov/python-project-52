from django.contrib.auth.models import User as DjangoUser

class User(DjangoUser):
    class Meta:
        proxy = True

    def __str__(self):
        return self.first_name + ' ' + self.last_name
from django.db.models import Model

from apps.users.models import CustomUser


class SharedService():

    def set_canceled(self, instance: Model, user: CustomUser):
        instance.set_canceled()
        instance.canceled_name = user.get_full_name
        instance.save()

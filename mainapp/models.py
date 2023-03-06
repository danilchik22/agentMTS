# Create your models here.
from pathlib import Path
from time import time
from django.db import models
from authapp import models as modUs
from django.utils.translation import gettext_lazy as _


def photo_house(instance, filename):
    # file will be uploaded to
    #   MEDIA_ROOT / user_<username> / avatars / <filename>
    num = int(time() * 1000)
    suff = Path(filename).suffix
    return "user_{0}/photo_houses/{1}".format(
        instance.user.username, f"pic_{num}{suff}"
    )


class Street(models.Model):
    """
    Модель для создания улиц
    """
    name_street = models.CharField(
        unique=True, max_length=100, verbose_name="name_street"
    )

    def __str__(self):
        return f"{self.name_street}"


class Address(models.Model):
    """
    Модель для создания адресов. Адрес состоит из трех полей: id адреса,
    улица адреса и номер дома. Работаем по одному городу.
    """
    number_of_house = models.CharField(
        max_length=10, verbose_name="number_of_house")
    street = models.ForeignKey(Street, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Adress of work")
        verbose_name_plural = _("Adresses")

    def __str__(self):
        return f"{self.street.name_street}  {self.number_of_house}"


class Work(models.Model):
    """
    Модель для создания 1го рабочего прохода.
    """
    user = models.ForeignKey(modUs.CustomUser, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Created", editable=False
    )
    photo = models.ImageField(
        upload_to=photo_house,
        blank=True,
        null=True,
        verbose_name="Photo of ad",
    )
    is_deleted = models.BooleanField(default=False)

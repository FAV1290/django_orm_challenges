from django.db import models
from django.utils.translation import gettext_lazy


class SubmssionStatus(models.IntegerChoices):
    DELETED = 1
    BANNED = 2
    SHADOWBANNED = 3
    NOT_PUBLISHED = 4
    PUBLISHED = 5


class LaptopManufacturer(models.TextChoices):
    ASUS = 'asus', gettext_lazy('Asus')
    DELL = 'dell', gettext_lazy('Dell')
    ACER = 'acer', gettext_lazy('Acer')
    APPLE = 'apple', gettext_lazy('Apple')
    MICROSOFT = 'ms', gettext_lazy('Microsoft')
    HP = 'hp', gettext_lazy('Hewlett-Packard')
    LENOVO = 'lenovo', gettext_lazy('Lenovo')
    SAMSUNG = 'samsung', gettext_lazy('Samsung')
    MSI = 'msi', gettext_lazy('MSI')
    TOSHIBA = 'toshiba', gettext_lazy('Toshiba')
    ALIENWARE = 'alienware', gettext_lazy('AlienWare')
    RAZER = 'razer', gettext_lazy('Razer')
    HUAWEI = 'huawei', gettext_lazy('Huawei')
    XIAOMI = 'xiaomi', gettext_lazy('Xiaomi')

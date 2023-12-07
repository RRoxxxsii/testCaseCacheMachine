from django.db import models


class Item(models.Model):
    title = models.CharField('Наименование', max_length=255)
    price = models.DecimalField('Стоимость', decimal_places=2, max_digits=12)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.title

from django.db import models

class Item(models.Model):
    text = models.TextField(verbose_name="To-Do item text")
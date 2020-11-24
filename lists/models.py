from django.db import models

class List(models.Model):
    pass

class Item(models.Model):
    text = models.TextField(verbose_name="To-Do item text")
    List = models.ForeignKey(List, on_delete=models.CASCADE,
                             verbose_name="Parent List")

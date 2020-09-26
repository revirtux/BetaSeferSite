from django.db import models
from django.db.models import CharField, ImageField


class House(models.Model):
    name = CharField(max_length=20, default="Untitled")
    motto = CharField(max_length=256)
    image = ImageField(upload_to="houses", blank=True, null=True)
    banner = ImageField(upload_to="banners", blank=True, null=True)
    title_color = CharField(max_length=8, default="", blank=True)
    back_color = CharField(max_length=8, default="", blank=True)
    nav_color = CharField(max_length=8, default="", blank=True)
    headers_color = CharField(max_length=8, default="", blank=True)
    text_color = CharField(max_length=8, default="", blank=True)
    footer_color = CharField(max_length=8, default="", blank=True)

    def __str__(self):
        return f"{self.name}"

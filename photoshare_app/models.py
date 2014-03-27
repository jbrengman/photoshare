from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Photo(models.Model):
    owner = models.ForeignKey(User)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag)
    height = models.IntegerField(blank=True, null=True, default=0)
    width = models.IntegerField(blank=True, null=True, default=0)
    image = models.ImageField(
        upload_to='%Y/%m/%d',
        height_field='height',
        width_field='width')

    def __unicode__(self):
        return self.owner.username + ' photo #' + str(self.pk)


class Album(models.Model):
    owner = models.ForeignKey(User)
    title = models.CharField(max_length=100)
    photos = models.ManyToManyField(Photo)
    cover = models.ForeignKey(Photo, related_name='album_cover', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title

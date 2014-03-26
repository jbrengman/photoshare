from django.contrib import admin
from django.core.urlresolvers import reverse
from photoshare_app.models import Photo, Tag, Album


class TagInLineAdmin(admin.TabularInline):
    model = Photo.tags.through
    extra = 1


class TagAdmin(admin.ModelAdmin):

    inlines = [TagInLineAdmin, ]

    list_display = ('__unicode__',)


class PhotoInLineAdmin(admin.TabularInline):
    model = Album.photos.through
    extra = 1


class PhotoAdmin(admin.ModelAdmin):

    inlines = [PhotoInLineAdmin, ]

    list_display = (
        '__unicode__',  'created_date', 'modified_date', 'owner_link')

    def owner_link(self, photo):
        url = reverse('admin:auth_user_change', args=(photo.owner.pk, ))
        name = photo.owner.username
        return '<a href="%s">%s</a>' % (url, name)

    owner_link.allow_tags = True
    owner_link.short_description = 'Photo owner'


class AlbumAdmin(admin.ModelAdmin):

    list_display = (
        '__unicode__', 'created_date', 'modified_date', 'owner_link')

    def owner_link(self, album):
        url = reverse('admin:auth_user_change', args=(album.owner.pk, ))
        name = album.owner.username
        return '<a href="%s">%s</a>' % (url, name)

    owner_link.allow_tags = True
    owner_link.short_description = 'Album owner'


admin.site.register(Photo, PhotoAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Album, AlbumAdmin)

from django.forms import ModelForm, ModelMultipleChoiceField
from photoshare_app.models import Tag, Photo, Album


class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['name', ]  # 'photo_set', ]


class PhotoForm(ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(PhotoForm, self).__init__(*args, **kwargs)
        self.fields['albums'].queryset = (
            self.fields['albums'].queryset.filter(owner__pk=user.pk))

    tags = ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)
    albums = ModelMultipleChoiceField(queryset=Album.objects.all())

    class Meta:
        model = Photo
        fields = ['image', 'albums', 'tags', ]


class NewAlbumForm(ModelForm):
    class Meta:
        model = Album
        fields = ['title', ]


class AlbumForm(ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'photos', 'cover', ]


class EditPhotoForm(ModelForm):
    class Meta:
        model = Photo
        fields = ['tags', ]

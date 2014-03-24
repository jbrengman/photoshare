from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from photoshare_app.admin import TagAdmin, PhotoAdmin, AlbumAdmin
from photoshare_app.models import User, Tag, Photo, Album


class PhotoAdminTestCase(TestCase):

    fixtures = ['photoshare_fixture.json', 'user_fixture.json', ]

    def setUp(self):
        admin = AdminSite()
        self.ma = PhotoAdmin(Photo, admin)
        for owner in User.objects.all():
            photo = Photo(owner=owner)
            photo.save()

    def test_owner_link(self):
        expected_link_path = '/admin/auth/user/%s'
        for photo in Photo.objects.all():
            expected = expected_link_path % photo.owner.pk
            actual = self.ma.owner_link(photo)
            self.assertTrue(expected in actual)


class AlbumAdminTestCase(TestCase):

    fixtures = ['photoshare_fixture.json', 'user_fixture.json', ]

    def setUp(self):
        admin = AdminSite()
        self.ma = AlbumAdmin(Album, admin)
        for owner in User.objects.all():
            album = Album(owner=owner, title='test_title')
            album.save()

    def test_owner_link(self):
        expected_link_path = '/admin/auth/user/%s'
        for album in Album.objects.all():
            expected = expected_link_path % album.owner.pk
            actual = self.ma.owner_link(album)
            self.assertTrue(expected in actual)

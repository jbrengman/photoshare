from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from photoshare_app.models import User, Tag, Photo, Album
from photoshare_app.forms import (
    TagForm, PhotoForm, NewAlbumForm, AlbumForm)


def home_view(request):
    if request.user.is_authenticated():
        user_name = request.user.username
        try:
            albums = (Album.objects.filter(
                owner__username=user_name).select_related('cover'))
            sorted_albums = albums.order_by('-created_date')
        except User.DoesNotExist:
            raise Http404
        context = {'albums': sorted_albums, 'username': user_name}
        return render(request, 'album_list.html', context)
    else:
        authform = AuthenticationForm()
        context = {'authform': authform}
        return render(request, 'login.html', context)


def albums_view(request, user_name):
    try:
        albums = (Album.objects.filter(
            owner__username=user_name).select_related('cover'))
        sorted_albums = albums.order_by('-created_date')
    except User.DoesNotExist:
        raise Http404
    context = {'albums': sorted_albums, 'username': user_name}
    return render(request, 'album_list.html', context)


def album_view(request, user_name, album_id):
    try:
        album = Album.objects.select_related('photos').get(pk=album_id)
        name = album.owner.username
    except Album.DoesNotExist:
        raise Http404
    context = {'album': album, 'username': name}
    return render(request, 'album_view.html', context)


def photo_view(request, photo_id):
    try:
        photo = Photo.objects.get(pk=photo_id)
    except Photo.DoesNotExist:
        raise Http404
    context = {'photo': photo}
    return render(request, 'photo.html', context)


def tag_view(request, tag_name):
    try:
        photos = Photo.objects.filter(tags__name=tag_name)
    except Photo.DoesNotExist:
        raise Http404
    context = {'tag_name': tag_name, 'photos': photos}
    return render(request, 'tag.html', context)


def tags_list_view(request):
    try:
        tags = Tag.objects.all()  # .select_related('photo_set.first')
    except Tag.DoesNotExist:
        raise Http404
    context = {'tags': tags}
    return render(request, 'tag_list.html', context)


def login_view(request):
    if request.method != 'POST':
        return redirect(home_view)
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect(home_view)
        else:
            pass
            # Return a 'disabled account' error message
    else:
        pass
        # Return an 'invalid login' error message.


def logout_view(request):
    logout(request)
    return redirect(home_view)


def register_view(request):
    return redirect('/accounts/register')


def create_album_view(request, user_name):
    if request.method == 'POST':
        form = AlbumForm(request.POST)
        if form.is_valid():
            album = form.save(commit=False)
            album.owner = request.user
            album.save()
            album.title = form.cleaned_data.get('title')
            photos = form.cleaned_data.get('photos')
            for photo in photos:
                album.photos.add(photo)
            album.save()
            return redirect(album_view, request.user.username, album.pk)
    else:
        context = {'album_form': NewAlbumForm()}
        return render(request, 'create_album.html', context)


def edit_album_view(request, user_name, album_id):
    try:
        album = Album.objects.get(pk=album_id)
    except Album.AlbumNotFound:
        raise Http404
    if request.method == 'POST':
        form = AlbumForm(request.POST, instance=album)
        if form.is_valid():
            update_album = form.save(commit=False)
            update_album.title = form.cleaned_data.get('title')
            photos = form.cleaned_data.get('photos')
            for photo in photos:
                album.photos.add(photo)
            update_album.save()
            return redirect(album_view, request.user.username, album.pk)
    else:
        album_form = AlbumForm(instance=album)
        context = {'album_form': album_form, 'album': album}
        return render(request, 'edit_album.html', context)


def create_tag_view(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.name = form.cleaned_data.get('name')
            tag.save()
            return redirect(tag_view, tag.name)
    else:
        context = {'tag_form': TagForm()}
        return render(request, 'create_tag.html', context)


def create_photo_view(request):
    if request.method == 'POST':
        form = PhotoForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.owner = request.user
            photo.save()
            # photo.image = form.cleaned_data.get('image')
            tags = form.cleaned_data.get('tags')
            for tag in tags:
                photo.tags.add(tag)
            photo.save()
            return redirect(photo_view, photo.pk)
    else:
        context = {'photo_form': PhotoForm(request.user)}
        return render(request, 'create_photo.html', context)


def edit_photo_view(request, photo_id):
    try:
        photo = Photo.objects.get(pk=photo_id)
    except Photo.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        form = PhotoForm(request.user, request.POST, instance=photo)
        if form.is_valid():
            update_photo = form.save(commit=False)
            tags = form.cleaned_data.get('tags')
            for tag in tags:
                update_photo.tags.add(tag)
            update_photo.save()
            return redirect(photo_view, photo.pk)
    else:
        context = {'edit_photo_form': PhotoForm(request.user, instance=photo), 'photo': photo}
        # photo_form = PhotoForm(request.user, instance=photo)
        # photo_form.fields['albums'].queryset
        # context = {'edit_photo_form': photo_form, 'photo': photo}
        return render(request, 'edit_photo.html', context)

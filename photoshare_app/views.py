from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from photoshare_app.models import User, Tag, Photo, Album


def home_view(request):
    if request.user.is_authenticated():
        user_name = request.user.username
        try:
            albums = Album.objects.filter(owner__username=user_name)
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
        albums = Album.objects.filter(owner__username=user_name)
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
    return render(request, 'register.html', {})

from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from main.query import *
import uuid

# Logout (normal)
def logout_user(request): 
    if 'email' in request.session:
        request.session.flush()
    return HttpResponseRedirect(reverse("main:login"))

#Login with dummy user
@csrf_exempt
def login_user(request):
    # Membuat dummy user jika tidak ada
    # create_dummy_user('username_dummy', 'password_dummy')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if (cek_akun(email)):
            results = login_akun(email, password)
            if (results is not None):
                request.session['email'] = results[0]
                request.session['isPengguna'] = True

                if (cek_artist(email)):
                    request.session['isArtist'] = True
                if (cek_songwriter(email)):
                    request.session['isSongwriter'] = True
                if (cek_podcaster(email)):
                    request.session['isPodcaster'] = True
                if (cek_premium(email)):
                    request.session['isPremium'] = True
                if (cek_nonpremium(email)):
                    request.session['isNonPremium'] = True
                
                return HttpResponseRedirect(reverse("main:dashboard"))
            else:
                messages.info(request, 'Email or password is incorrect')
        
        elif (cek_label(email)):
            results = login_label(email, password)
            if (results is not None):
                request.session['email'] = results[2]
                request.session['isLabel'] = True
                return HttpResponseRedirect(reverse("main:dashboard"))
            else:
                messages.info(request, 'Email or password is incorrect')
        else:
            messages.info(request, 'Email or password is incorrect')
    
    context = {}
    return render(request, 'login.html', context)

# Create your views here.
def show_dashboard(request):
    if 'email' not in request.session:
        return HttpResponseRedirect(reverse("main:login"))
    
    email = request.session.get('email')
    
    if (cek_akun(email)):
        result = get_akun_data(email)
        nama = result[2]
        gender = "Male" if result[3] == 1 else "Female"
        tempat_lahir = result[4]
        tanggal_lahir = result[5]
        kota_asal = result[7]
        is_verified = result[6]
        tanggal_lahir_formatted = tanggal_lahir.strftime("%d %B %Y")
        tempat_tanggal_lahir = f"{tempat_lahir}, {tanggal_lahir_formatted}"

        if (get_playlist is not None):
            playlists = [playlist[0] for playlist in get_playlist(email)]

        songs = []
        if (request.session.get('isArtist')):
            songs += [song[0] for song in get_songs_artist(email)]
        if (request.session.get('isSongwriter')):
            songs += [song[0] for song in get_songs_songwriter(email)]
        
        podcasts = []
        if (request.session.get('isPodcaster')):
            podcasts += [podcast[0] for podcast in get_podcasts(email)]

        context = {
            'nama': nama,
            'email': email,
            'kota_asal': kota_asal,
            'gender': gender,
            'tempat_tanggal_lahir': tempat_tanggal_lahir,
            'isPengguna': request.session.get('isPengguna'),
            'playlists': playlists,
            'is_verified': is_verified,
            'is_premium': request.session.get('isPremium'),

            'isArtist': request.session.get('isArtist'),
            'isSongwriter': request.session.get('isSongwriter'),
            'songs': songs,
            
            'isPodcaster': request.session.get('isPodcaster'),
            'podcasts': podcasts,
        }

    else:
        result = get_label_data(email)
        nama = result[1]
        kontak = result[4]
        
        albums = [album[0] for album in get_album(email)]
    
        context = {
            'nama': nama,
            'email': email,
            'isLabel': request.session.get('isLabel'),
            'kontak': kontak,
            'albums': albums
        }
    
    return render(request, "dashboard.html", context)

def show_register(request):
    return render(request, "register.html")

@csrf_exempt
def show_register_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        nama = request.POST.get('nama')
        gender = request.POST.get('gender')
        tempat_lahir = request.POST.get('tempat_lahir')
        tanggal_lahir = request.POST.get('tanggal_lahir')
        kota_asal = request.POST.get('kota_asal')

        roles = request.POST.getlist('roles')
        is_podcaster = 'podcaster' in roles
        is_artist = 'artist' in roles
        is_songwriter = 'songwriter' in roles

        is_verified = is_podcaster or is_artist or is_songwriter

        is_valid = email and password and nama and gender and tempat_lahir and tanggal_lahir and kota_asal
        if not is_valid:
            return render(request, "registerUser.html", {'error_message': 'Mohon masukkan data dengan benar!'})
        if cek_existing_email(email):
            return render(request, "registerUser.html", {'error_message': 'Email sudah terdaftar!'})
        else:
            register_user(email, password, nama, gender, tempat_lahir, tanggal_lahir, is_verified, kota_asal)
            if is_podcaster:
                register_podcaster(email)
            if is_artist:
                register_artist(uuid.uuid4(), uuid.uuid4(), email)
            if is_songwriter:
                register_songwriter(uuid.uuid4(), uuid.uuid4(), email)
            return HttpResponseRedirect(reverse("main:login"))

    return render(request, "registerUser.html")

@csrf_exempt
def show_register_label(request):
    if request.method == "POST":
        id = uuid.uuid4()
        email = request.POST.get('email')
        password = request.POST.get('password')
        nama = request.POST.get('nama')
        kontak = request.POST.get('kontak')

        is_valid = email and password and nama and kontak
        if not is_valid:
            return render(request, "registerLabel.html", {'error_message': 'Mohon masukkan data dengan benar!'})
        if cek_existing_email(email):
            return render(request, "registerLabel.html", {'error_message': 'Email sudah terdaftar!'})
        else:
            register_label(id, email, password, nama, kontak, uuid.uuid4())
            return HttpResponseRedirect(reverse("main:login"))

    return render(request, "registerLabel.html")
    


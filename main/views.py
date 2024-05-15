from datetime import datetime
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.urls import reverse
# from django.contrib.auth.models import User
from django.db import connection as conn
from django.views.decorators.csrf import csrf_exempt
from main.query import *

def tes_query(request):
    context = {
        'name': 'C15',
        'class': 'BASDAT C'
    }
    
    with conn.cursor() as cursor:
        # Mengatur schema database
        cursor.execute("set search_path to marmut;")
        
        cursor.execute("SELECT * FROM PLAYLIST;")
        
        results = cursor.fetchall()

        print("total ada %d" % (len(results)))
        # Mengeprint setiap baris dari hasil query
        for result in results:
            print(result)

    # Kembali ke halaman tertentu atau tampilkan suatu response
    return render(request, 'main.html', context)  # Sisipkan template yang sesuai

@login_required(login_url='/login')
#Main Page
def show_main(request):
    context = {
        'name': 'C15',
        'class': 'BASDAT C'
    }

    return render(request, "main.html", context)

## Create your views here (normal)
# def login_user(request):
#    if request.method == 'POST':
#        username = request.POST.get('username')
#        user = authenticate(request, username=username, password=password)
#        if user is not None:
#            login(request, user)
#            return redirect('main:show_main')
#        else:
#            messages.info(request, 'Sorry, incorrect username or password. Please try again.')
#    context = {}
#    return render(request, 'login.html', context)

# Logout (normal)
def logout_user(request): 
    if 'email' in request.session:
        request.session.flush()
        print("berhasil diflush")
    return HttpResponseRedirect(reverse("main:login"))


#For dummy user
# def create_dummy_user(username, password):
#     # Cek apakah pengguna dengan username yang sama sudah ada
#     if not User.objects.filter(username=username).exists():
#         # Buat pengguna baru
#         user = User.objects.create_user(username=username, password=password)
#         # Simpan pengguna
#         user.save()

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
                
                print("sukses")
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

# def login_user(request):
#     context = {}
#     return render(request, 'login.html', context)

# Create your views here.
def show_dashboard(request):
    if 'email' not in request.session:
        return HttpResponseRedirect(reverse("main:login"))
    
    email = request.session.get('email')
    
    result = get_akun_data(email)
    nama = result[2]
    gender = "Male" if result[3] == 1 else "Female"
    tempat_lahir = result[4]
    tanggal_lahir = result[5]
    kota_asal = result[7]

    tanggal_lahir_formatted = tanggal_lahir.strftime("%d %B %Y")
    tempat_tanggal_lahir = f"{tempat_lahir}, {tanggal_lahir_formatted}"

    songs = [song[0] for song in get_songs(email)]

    context = {
        'nama': nama,
        'email': email,
        'kota_asal': kota_asal,
        'gender': gender,
        'tempat_tanggal_lahir': tempat_tanggal_lahir,
        'isPengguna': request.session.get('isPengguna'),
        'playlists': [],

        'isArtist': request.session.get('isArtist'),
        'isSongwriter': request.session.get('isSongwriter'),
        'songs': songs,
        
        'isPodcaster': request.session.get('isPodcaster'),
        'podcasts': ["Johnny Cash's Heaven on Earth", "A Day In The Grand Canyon", "Cash's Life Journey"],
        
        'isLabel': request.session.get('isLabel'),
        'kontak': "0123456789",
        'albums': ["Dune: Part Two", "Barbie", "The Batman"]
    }
    
    return render(request, "dashboard.html", context)

def show_register(request):
    return render(request, "register.html")

def show_register_user(request):
    return render(request, "registerUser.html")

def show_register_label(request):
    return render(request, "registerLabel.html")

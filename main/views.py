from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import connection as conn
from django.views.decorators.csrf import csrf_exempt
import uuid

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
    logout(request)
    return redirect('main:login')


#For dummy user
def create_dummy_user(username, password):
    # Cek apakah pengguna dengan username yang sama sudah ada
    if not User.objects.filter(username=username).exists():
        # Buat pengguna baru
        user = User.objects.create_user(username=username, password=password)
        # Simpan pengguna
        user.save()

#Login with dummy user
def login_user(request):
    # Membuat dummy user jika tidak ada
    create_dummy_user('username_dummy', 'password_dummy')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main:dashboard')
        else:
            messages.info(request, 'Sorry, incorrect username or password. Please try again.')
    context = {}
    return render(request, 'login.html', context)

# Create your views here.
def show_dashboard(request):
    context = {
        'nama': "Dafton",
        'email': "daffa.mohamad@ui.ac.id",
        'kota_asal': "DKI Jakarta",
        'gender': "Male",
        'tempat_lahir': "Jakarta",
        'tanggal_lahir': "14 Juni 2004",
        'isPengguna': False,
        'playlists': [],

        'isArtist': False,
        'isSongwriter': True,
        'songs': ["Hurt", "Ring of Fire"],
        
        'isPodcaster': True,
        'podcasts': ["Johnny Cash's Heaven on Earth", "A Day In The Grand Canyon", "Cash's Life Journey"],
        
        'isLabel': False,
        'kontak': "0123456789",
        'albums': ["Dune: Part Two", "Barbie", "The Batman"]
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

        with conn.cursor() as cursor:
            cursor.execute("SELECT email FROM AKUN WHERE email = %s", [email])
            existing_email = cursor.fetchone()

            if existing_email:
                return render(request, "registerUser.html", {'error_message': 'Email sudah terdaftar!'})
            else:
                cursor.execute("""
                    INSERT INTO AKUN (email, password, nama, gender, tempat_lahir, tanggal_lahir, is_verified, kota_asal)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, [email, password, nama, gender, tempat_lahir, tanggal_lahir, is_verified, kota_asal])
                
                cursor.execute("""
                    INSERT INTO nonpremium (email)
                    VALUES (%s)
                """, [email])
                
                if is_podcaster:
                    cursor.execute("""
                        INSERT INTO podcaster (email)
                        VALUES (%s)
                    """, [email])
                    
                if is_artist:
                    id = uuid.uuid4()
                    cursor.execute("""
                        INSERT INTO artist (id, email_akun)
                        VALUES (%s, %s)
                    """, [id, email])
                    
                if is_songwriter:
                    id = uuid.uuid4()
                    cursor.execute("""
                        INSERT INTO songwriter (id, email_akun)
                        VALUES (%s, %s)
                    """, [id, email])
                
    return render(request, "registerUser.html")

@csrf_exempt
def show_register_label(request):
    if request.method == "POST":
        id = uuid.uuid4()
        email = request.POST.get('email')
        password = request.POST.get('password')
        nama = request.POST.get('nama')
        kontak = request.POST.get('kontak')

        with conn.cursor() as cursor:
            cursor.execute("SELECT email FROM LABEL WHERE email = %s", [email])
            existing_email = cursor.fetchone()

            if existing_email:
                return render(request, "registerLabel.html", {'error_message': 'Email sudah terdaftar!'})
            else:
                cursor.execute("""
                    INSERT INTO LABEL (id, email, password, nama, kontak)
                    VALUES (%s,%s,%s,%s,%s)
                """, [id,email,password,nama,kontak])
        """
        cursor.execute("SELECT nama FROM label;")
        rows = cursor.fetchall()
        
        items = [
            {
            'name': row[0],
            }
            for row in rows
        ]"""

    return render(request, "registerLabel.html")
    


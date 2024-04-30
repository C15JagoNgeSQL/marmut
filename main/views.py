from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

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
            return redirect('main:show_main')
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
        'isPengguna': True,
        'playlists': [],

        'isArtist': False,
        'isSongwriter': False,
        'songs': ["Hurt", "Ring of Fire"],
        
        'isPodcaster': False,
        'podcasts': ["Johnny Cash's Heaven on Earth", "A Day In The Grand Canyon", "Cash's Life Journey"],
        
        'isLabel': False,
        'kontak': "0123456789",
        'albums': ["Dune: Part Two", "Barbie", "The Batman"]
    }
    return render(request, "dashboard.html", context)

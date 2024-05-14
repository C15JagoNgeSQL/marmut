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

def temporary_chart_detail_view(request):
    # Data yang akan dimasukkan ke dalam template
    context = {
        'chart_type': 'Daily Top 20',
        'songs': [
            {'title': 'Song1', 'artist': 'Artist1', 'release_date': '09/03/2024', 'total_plays': 21000},
            {'title': 'Song2', 'artist': 'Artist2', 'release_date': '02/03/2024', 'total_plays': 19000}
        ]
    }
    return render(request, 'chart_detail.html', context)


def temporary_crud_kelola_podcast_view(request):
    context = {
        'judul_playlist': 'Playlist1',
        'pembuat': 'Pembuat1',
        'jumlah_lagu': 12,
        'total_durasi': '8 jam 20 menit',
        'tanggal_dibuat': '18/03/24',
        'deskripsi': 'Lorem Ipsum ...',
        'daftar_lagu': [
            {'judul': 'Song1', 'artis': 'Artist1', 'durasi': '2 menit'},
            {'judul': 'Song2', 'artis': 'Artist2', 'durasi': '3 menit'},
            {'judul': 'Song3', 'artis': 'Artist3', 'durasi': '4 menit'}
        ]
    }
    return render(request, 'crud_kelola_podcast.html', context)

def temporary_lihat_chart_view(request):
    chart_data = [
        {"title": "Actions Daily Top 20", "url": "chart_detail.html"},
        {"title": "Weekly Top 20", "url": "chart_detail.html"},
        # Add more chart data as needed
    ]
    return render(request, 'lihat_chart.html', {'chart_data': chart_data})


def temporary_r_podcast_view(request):
    podcast_data = {
        'judul': 'The Daily',
        'genres': ['Comedy', 'Motivation'],
        'podcaster': 'Jeffrey Mitchell',
        'durasi': '8 jam 20 menit',
        'tanggal_rilis': '18/03/24',
        'tahun': '2024',
        'episodes': [
            {
                'judul_episode': 'The Power of Positive Thinking',
                'deskripsi': 'Join us as we explore the transformative effects of maintaining a positive mindset in our daily lives',
                'durasi': '24 menit',
                'tanggal': '30/06/2021'
            },
            {
                'judul_episode': 'Journey Through Ancient Civilizations',
                'deskripsi': 'Embark on a captivating journey through the ruins and relics of ancient civilizations as we unravel their mysteries',
                'durasi': '1 jam 43 menit',
                'tanggal': '01/10/2019'
            }
        ]
    }
    return render(request, 'r_podcast.html', {'podcast_data': podcast_data})

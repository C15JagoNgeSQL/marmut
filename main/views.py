from django.shortcuts import render

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
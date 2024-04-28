from django.shortcuts import render

# Create your views here.
def show_dashboard(request):
    context = {
        'nama': "Daffa Mohamad Fathoni",
        'email': "daffafathoni@gmail.com",
        'kota_asal': "Jakarta Timur",
        'gender': "Male",
        'tempat_lahir': "Jakarta",
        'tanggal_lahir': "14 Juni 2004",
        'role': "Artist",
        'playlists': ["Bubu lucu"],
        'songs': ["dada gugu", "meow meow"],
        'podcasts': [],
        'albums': []
    }
    return render(request, "dashboard.html", context)
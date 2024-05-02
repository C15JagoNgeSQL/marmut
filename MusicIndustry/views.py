from django.shortcuts import render

# Create your views here.

def show_royalti(request):
    context = {
        'nama': "Taylor Swift",
        'email': "taylorswift@gmail.com",
        'total_keseluruhan_play': 999999,
        'total_keseluruhan_download': 100000,
        'isi_tabel': [
            {
                'judul_lagu': "I Can Do It With A Broken Heart",
                'judul_album': "The Tortured Poets Department",
                'total_play': 50000,
                'total_download': 1000,
                'total_royalti_didapat': 1000000
            },
            {
                'judul_lagu': "I Can Do It With A Broken Heart",
                'judul_album': "The Tortured Poets Department",
                'total_play': 50000,
                'total_download': 1000,
                'total_royalti_didapat': 1000000
            },
            {
                'judul_lagu': "I Can Do It With A Broken Heart",
                'judul_album': "The Tortured Poets Department",
                'total_play': 50000,
                'total_download': 1000,
                'total_royalti_didapat': 1000000
            },
            {
                'judul_lagu': "I Can Do It With A Broken Heart",
                'judul_album': "The Tortured Poets Department",
                'total_play': 50000,
                'total_download': 1000,
                'total_royalti_didapat': 1000000
            },
            {
                'judul_lagu': "I Can Do It With A Broken Heart",
                'judul_album': "The Tortured Poets Department",
                'total_play': 50000,
                'total_download': 1000,
                'total_royalti_didapat': 1000000
            }
        ]
    }
    return render(request, "cek_royalti.html", context)

def kelola_album(request):
    context = {
        'nama': "Luke Chiang",
        'email': "luchiang@gmail.com",
        'isLabel': False,
        'kontak': "08123456789",
        'total_album': 2,
        'total_lagu': 4,
        'isi_tabel': [
            {
                'judul': "Album 1",
                'label': "LabelA",
                'jumlah_lagu': 0,
                'total_durasi': 0,
            },
            {
                'judul': "Album2",
                'label': "LabelB",
                'jumlah_lagu': 2,
                'total_durasi': 4,
            }
        ]
    }
    return render(request, "kelola_album.html", context)

def create_album(request):
    return render(request, "create_album.html")

def daftar_lagu(request):
    context = {
        'nama': "Album 1",
        'total_lagu': 999999,
        'total_durasi': 100000,
        'isi_tabel': [
            {
                'judul': "Lagu1",
                'durasi': "2 menit",
                'total_play': 3,
                'total_download': 0,
            },
            {
                'judul': "Lagu1",
                'durasi': "3 menit",
                'total_play': 2,
                'total_download': 2,
            }
        ]
    }
    return render(request, "daftar_lagu.html", context)

def create_lagu(request):
    context = {
        'isSongwriter' : False
    }
    return render(request, "create_lagu.html", context)
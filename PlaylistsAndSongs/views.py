from django.shortcuts import render

def show_kelola_playlist(request):
    playlists = [
        {
            'judul': "Morning Vibes",
            'jumlah_lagu': "5",
            'total_durasi': "44",
        },
        {
            'judul': "Workout Beats",
            'jumlah_lagu': "7",
            'total_durasi': "47",
        }
    ]
    return render(request, "kelolaPlaylist.html", {'playlists': playlists})

def show_tambah_playlist(request):
    return render(request, "tambahPlaylist.html")

def show_ubah_playlist(request):
    playlist = {
        'judul': "Morning Vibes",
        'deskripsi' : "Start your day with these uplifting tunes!"
    }
    return render(request, "ubahPlaylist.html", {'playlist': playlist})

def show_detail_playlist(request):
    detail = {
        'judul': "Morning Vibes",
        'pembuat': "Rafi",
        'jumlah_lagu': "5",
        'total_durasi': "44 menit",
        'tanggal_dibuat': "26/03/2024",
        'deskripsi': "Start your day with these uplifting tunes!",
        'songs': [
            {
                'judul': "See You Again",
                'nama_artist': "Valerie Jordan",
                'durasi': "5"
            },
            {
                'judul': "Hotline Bling",
                'nama_artist': "Michael Wade",
                'durasi': "3"
            }
        ]
    }
    return render(request, "detailPlaylist.html", {'detail': detail})

def show_tambah_lagu(request):
    songs = [
        ('1', 'See You Again - Valerie Jordan'),
        ('2', 'Hotline Bling - Michael Wade')
    ]
    return render(request, "tambahLagu.html", {'songs': songs})
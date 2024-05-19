from django.shortcuts import render
from django.db import connection as conn
from django.http import HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import uuid
from django.utils import timezone
from PlaylistsAndSongs.query import *

def show_kelola_user_playlist(request):
    if 'email' not in request.session:
        return HttpResponseRedirect(reverse("main:login"))
    
    email = request.session.get('email')

    playlists = get_user_playlist_data(email)

    return render(request, "kelola_playlist.html", {'playlists': playlists})

@csrf_exempt
def show_tambah_playlist(request):
    if request.method == "POST":
        if 'email' not in request.session:
            return HttpResponseRedirect(reverse("main:login"))
        
        email_pembuat = request.session.get('email')
        id_user_playlist = uuid.uuid4()
        judul = request.POST.get('judul')
        deskripsi = request.POST.get('deskripsi')
        tanggal_dibuat = timezone.now().date()
        id_playlist = uuid.uuid4()

        tambah_playlist(email_pembuat, id_user_playlist, judul, deskripsi, tanggal_dibuat, id_playlist)
        return HttpResponseRedirect(reverse("PlaylistAndSongs:kelola_playlist"))

    return render(request, "tambahPlaylist.html")

@csrf_exempt
def show_ubah_playlist(request, user_playlist_id):
    data_user_playlist = get_user_playlist_from_user_playlist_id(user_playlist_id)

    playlist = {
        'judul': data_user_playlist[2],
        'deskripsi': data_user_playlist[3]
    }

    if request.method == 'POST':
        judul = request.POST.get('judul')
        deskripsi = request.POST.get('deskripsi')

        edit_playlist(judul, deskripsi, user_playlist_id)
        return HttpResponseRedirect(reverse("PlaylistAndSongs:kelola_playlist"))

    return render(request, "ubahPlaylist.html", {'playlist': playlist})

def show_hapus_playlist(request, id_user_playlist):
    id_playlist = get_user_playlist_from_user_playlist_id(id_user_playlist)[6]

    delete_user_playlist(id_user_playlist, id_playlist)
    return HttpResponseRedirect(reverse("PlaylistAndSongs:kelola_playlist"))

def show_detail_playlist(request, id_user_playlist):
    detail_playlist = get_user_playlist_from_user_playlist_id(id_user_playlist)
    songs = get_song_data(id_user_playlist)

    if detail_playlist[7] < 60:
        total_durasi = f"{detail_playlist[7]} menit"
    else:
        jam = detail_playlist[7] // 60
        menit = detail_playlist[7] % 60
        if menit > 0:
            total_durasi = f"{jam} jam {menit} menit"
        else:
            total_durasi = f"{jam} jam"

    detail = {
        'id_user_playlist': detail_playlist[1],
        'judul': detail_playlist[2],
        'pembuat': detail_playlist[10],
        'jumlah_lagu': detail_playlist[4],
        'total_durasi': total_durasi,
        'tanggal_dibuat': detail_playlist[5],
        'deskripsi': detail_playlist[3],
        'id_playlist': detail_playlist[6],
        'songs': [
            {
            'judul': song[0],
            'durasi': song[1],
            'nama_artist': song[2],
            'id_song': song[3]
            }
            for song in songs
        ]
    }

    return render(request, "detailPlaylist.html", {'detail': detail})

@csrf_exempt
def show_tambah_lagu(request, playlist_id):
    all_songs = get_all_song()
    songs = [{'judul_lagu': row[0], 'nama_artist': row[1], 'id_song': row[2]} for row in all_songs]
    
    if request.method == 'POST':
        id_song = request.POST.get('song_id')

        rows = get_user_playlist_from_playlist_id(playlist_id)

        if check_lagu_exist_in_playlist(id_song, playlist_id):
            return render(request, "tambah_lagu.html", {'error_message': 'Lagu sudah terdapat dalam playlist!', 'songs': songs})
        else:
            tambah_lagu_ke_playlist(playlist_id, id_song, rows)
            return HttpResponseRedirect(reverse("PlaylistAndSongs:detail_playlist", kwargs={'id_user_playlist': rows[1]}))
            
    return render(request, "tambah_lagu.html", {'songs': songs})    

def show_hapus_lagu(request, playlist_id, id_song):
    rows = delete_lagu_dari_playlist(playlist_id, id_song)
    return HttpResponseRedirect(reverse("PlaylistAndSongs:detail_playlist", kwargs={'id_user_playlist': rows[1]}))

@csrf_exempt
def show_detail_lagu(request, song_id):
    email = request.session.get('email')

    is_premium = check_if_premium(email)
    songs = get_song_detail(song_id)
    genres = get_song_genres(song_id)
    songwriters = get_song_songwriters(song_id)

    detail = {
        'id_song': song_id,
        'judul': songs[0],
        'genres': [
            {
            'genre': genre[0]
            }
            for genre in genres
        ],
        'artist': songs[6],
        'songwriters': [
            {
            'nama': songwriter[0]
            }
            for songwriter in songwriters
        ],
        'durasi': songs[3],
        'tanggal_rilis': songs[1],
        'tahun': songs[2],
        'total_play': songs[4],
        'total_download': songs[5],
        'album': songs[7]
    }

    if request.method == 'POST':
        email = request.session.get('email')
        id_song = request.POST.get('id_song')
        judul_lagu = get_song_detail(id_song)[0]

        if check_downloaded_song(id_song):
            return render(request, "detail_lagu.html", {'detail': detail, 'premium': 'premium', 'gagal': judul_lagu})
        else:
            premium_download_song(id_song, email)
            return render(request, "detail_lagu.html", {'detail': detail, 'premium': 'premium', 'berhasil': judul_lagu})

    if is_premium:
        return render(request, "detail_lagu.html", {'detail': detail, 'premium': 'premium'})
    else:
        return render(request, "detail_lagu.html", {'detail': detail})
    
def download_lagu(request, id_song):
    email = request.session.get('email')
    song_detail = get_song_detail(id_song)[0]

    if check_downloaded_song(id_song):
        return HttpResponseRedirect(reverse("PlaylistAndSongs:detail_lagu", kwargs={'song_id': id_song}))
    else:
        premium_download_song(id_song, email)
        return HttpResponseRedirect(reverse("PlaylistAndSongs:detail_lagu", kwargs={'song_id': id_song}))
    
@csrf_exempt
def slider_play(request, id_song):
    if request.method == "POST":
        email = request.session.get('email')
        slider_value = int(request.POST.get("slider_value", 0))

        if slider_value > 70:
            current_time = timezone.now()
            akun_play_song(email, id_song, current_time)
        
        return HttpResponseRedirect(reverse("PlaylistAndSongs:detail_lagu", kwargs={'song_id': id_song}))
            
@csrf_exempt
def show_tambah_lagu_ke_playlist(request, id_song):
    email = request.session.get('email')

    songs = get_song_detail(id_song)
    playlists = get_user_user_playlist(email)

    song = {
        'id': id_song,
        'judul': songs[0],
        'artist': songs[6],
        'playlists': [
            {
            'id_user_playlist': playlist[0],
            'playlist': playlist[1]
            }
            for playlist in playlists
        ]
    }

    if request.method == 'POST':
        id_user_playlist = request.POST.get('playlist')

        user_playlist_data = get_user_playlist_from_user_playlist_id(id_user_playlist)
        
        if check_lagu_exist_in_playlist(id_song, user_playlist_data[6]):
            return render(request, "tambah_lagu_ke_playlist.html", {'song': song, 'gagal': user_playlist_data[2], 'songs': songs, 'id_user_playlist': id_user_playlist})
        else:
            tambah_lagu_ke_playlist(user_playlist_data[6], id_song, user_playlist_data)
            return render(request, "tambah_lagu_ke_playlist.html", {'song': song, 'berhasil': user_playlist_data[2], 'songs': songs, 'id_user_playlist': id_user_playlist})
            
    return render(request, "tambah_lagu_ke_playlist.html", {'song': song})

def show_play_user_playlist(request,playlist_id):
    detail_playlist = get_user_playlist_from_user_playlist_id(playlist_id)
    songs = get_song_data(playlist_id)

    if detail_playlist[7] < 60:
        total_durasi = f"{detail_playlist[7]} menit"
    else:
        jam = detail_playlist[7] // 60
        menit = detail_playlist[7] % 60
        if menit > 0:
            total_durasi = f"{jam} jam {menit} menit"
        else:
            total_durasi = f"{jam} jam"

    detail = {
        'id_user_playlist': detail_playlist[1],
        'judul': detail_playlist[2],
        'pembuat': detail_playlist[10],
        'jumlah_lagu': detail_playlist[4],
        'total_durasi': total_durasi,
        'tanggal_dibuat': detail_playlist[5],
        'deskripsi': detail_playlist[3],
        'id_playlist': detail_playlist[6],
        'songs': [
            {
            'judul': song[0],
            'durasi': song[1],
            'nama_artist': song[2],
            'id_song': song[3]
            }
            for song in songs
        ]
    }

    return render(request, "play_user_playlist.html", {'detail': detail})

def shuffle_play_playlist(request, playlist_id):
    email = request.session.get('email')

    user_playlist_data = get_user_playlist_from_user_playlist_id(playlist_id)
    songs = get_song_data(playlist_id)
    current_time = timezone.now()

    akun_play_playlist(email, playlist_id, user_playlist_data, current_time)

    for song in songs:
        akun_play_song(email, song[3], current_time)

    return HttpResponseRedirect(reverse("PlaylistAndSongs:play_user_playlist", kwargs={'playlist_id': playlist_id}))

def play_song(request, id_song, playlist_id):
    email = request.session.get('email')
    current_time = timezone.now()

    akun_play_song(email, id_song, current_time)
    
    return HttpResponseRedirect(reverse("PlaylistAndSongs:play_user_playlist", kwargs={'playlist_id': playlist_id}))

def play_song_from_own_playlist(request, id_song, playlist_id):
    email = request.session.get('email')
    current_time = timezone.now()

    akun_play_song(email, id_song, current_time)
    
    return HttpResponseRedirect(reverse("PlaylistAndSongs:detail_playlist", kwargs={'id_user_playlist': playlist_id}))



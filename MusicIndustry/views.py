from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import uuid
from datetime import datetime
from MusicIndustry.query import *

# Create your views here.

def show_royalti(request):
    if 'email' not in request.session:
        return HttpResponseRedirect(reverse("main:login"))
    
    email = request.session.get('email')

    data = []

    if request.session.get('isLabel'):
        data = get_songs_royalti_label(email)
        nama = get_name_label(email)
    else:
        if request.session.get('isArtist'):
            data += get_songs_royalti_artist(email)
        if request.session.get('isSongwriter'):
            data += get_songs_royalti_songwriter(email)
        nama = get_name_akun(email)

    isi_tabel = []
    total_play = 0
    total_download = 0
    total_royalti = 0
    
    for song in data:
        song_dict = {
            'judul_lagu': song[1],
            'judul_album': song[2],
            'total_play': count_total_play(song[0]),
            'total_download': count_total_download(song[0]),
            'total_royalti_didapat': song[3]
        }
        isi_tabel.append(song_dict)
        total_play += count_total_play(song[0])
        total_download += count_total_download(song[0])
        total_royalti += song[3]
        
    context = {
        'nama': nama,
        'email': email,
        'total_keseluruhan_play': total_play,
        'total_keseluruhan_download': total_download,
        'isi_tabel': isi_tabel,
        'total_keseluruhan_royalti': total_royalti
    }
    return render(request, "cek_royalti.html", context)

def kelola_album(request):
    if 'email' not in request.session:
        return HttpResponseRedirect(reverse("main:login"))
    
    email = request.session.get('email')

    if(request.session.get('isLabel')):
        albums = get_albums_label(email)
        data = get_label_data(email)

        isi_tabel = []
        jumlah_lagu = 0

        # Memetakan hasil query ke dalam format dictionary isi_tabel
        for album in albums:
            album_dict = {
                'judul': album[1],  # Nama album
                'jumlah_lagu': album[2],  # Jumlah lagu
                'id': album[0],
                'total_durasi': album[4],  # Total durasi
            }
            isi_tabel.append(album_dict)
            jumlah_lagu += album[2]

        context = {
            'nama': data[1],
            'kontak': data[4],
            'isLabel': True,
            'total_album': len(isi_tabel),
            'total_lagu': jumlah_lagu,
            'isi_tabel' : isi_tabel
        }
    
    else:
        if (request.session.get('isArtist')):
            albums = get_albums_artist(email)
        if (request.session.get('isSongwriter')):
            albums = get_albums_songwriter(email)
        data = get_akun_data(email)

        isi_tabel = []
        jumlah_lagu = 0

        # Memetakan hasil query ke dalam format dictionary isi_tabel
        for album in albums:
            album_dict = {
                'judul': album[1],  # Nama album
                'label': album[2],
                'jumlah_lagu': album[3],  # Jumlah lagu
                'total_durasi': album[4],  # Total durasi
                'id': album[0],
            }
            isi_tabel.append(album_dict)
            jumlah_lagu += album[3]

        context = {
            'nama': data[2],
            'email': data[0],
            'isLabel': False,
            'total_album': len(isi_tabel),
            'total_lagu': jumlah_lagu,
            'isi_tabel' : isi_tabel
        }

    return render(request, "kelola_album.html", context)

def daftar_lagu(request, album_id):
    if 'email' not in request.session:
        return HttpResponseRedirect(reverse("main:login"))
    songs = get_albums_songs(album_id)
    nama = get_album_name(album_id)

    isi_tabel = []
    total_durasi = 0
    for song in songs:
            song_dict = {
                'id': song[0],
                'judul': song[1],  # Nama album
                'durasi': song[4],  # Jumlah lagu
                'total_play': count_total_play(song[0]),
                'total_download': count_total_download(song[0])
            }
            isi_tabel.append(song_dict)
            total_durasi += song[4]
    context = {
        'nama': nama,
        'total_lagu': len(isi_tabel),
        'total_durasi': total_durasi,
        'isi_tabel': isi_tabel
    }
    return render(request, "daftar_lagu.html", context)

def create_album(request):
    labels = get_labels()
    pilihan_label = []
    for label in labels:
        label_dict = {
            'id': label[0],
            'nama': label[1],  # Nama Label
        }
        pilihan_label.append(label_dict)

    artists = get_artists()
    pilihan_artist = []
    for artist in artists:
        artist_dict = {
            'id': artist[0],
            'nama': artist[1],  # Nama artist
        }
        pilihan_artist.append(artist_dict)
    
    songwriters = get_songwriters()
    pilihan_songwriter = []
    for songwriter in songwriters:
        songwriter_dict = {
            'id': songwriter[0],
            'nama': songwriter[1],  # Nama songwriter
        }
        pilihan_songwriter.append(songwriter_dict)

    genres = get_genres()
    pilihan_genre = []
    for genre in genres:
        genre_dict = {
            'nama': genre[0],
        }
        pilihan_genre.append(genre_dict)

    email = request.session.get('email')
    is_artist = request.session.get('isArtist')
    is_songwriter = request.session.get('isSongwriter')
    
    context = {
        'me': get_name_akun(email),
        'labels': pilihan_label,
        'artists': pilihan_artist,
        'genres': pilihan_genre,
        'songwriters': pilihan_songwriter,
        'isArtist': request.session.get('isArtist'),
        'isSongwriter' : request.session.get('isSongwriter')
    }

    if request.method == 'POST':
        album_id = uuid.uuid4()
        judul_album = request.POST.get('judul')
        label = request.POST.get('label')

        lagu_id = uuid.uuid4()
        judul = request.POST.get('judul_lagu')
        if (is_artist):
            artist = get_id_artist(email)
        else:
            artist = request.POST.get('artist')

        songwriters = request.POST.getlist('songwriter')
        genres = request.POST.getlist('genre')
        durasi = request.POST.get('durasi')
        tanggal_rilis = datetime.now()
        tahun = tanggal_rilis.year

        if (is_artist):
            hak_cipta_id = get_pemilik_hak_cipta_artist(email)
        if (is_songwriter):
            hak_cipta_id = get_pemilik_hak_cipta_songwriter(email)
            songwriters.append(get_id_songwriter(email))

        insert_album(album_id, judul_album, label, durasi)
        insert_konten(lagu_id, judul, tanggal_rilis, tahun, durasi)
        insert_song(lagu_id, artist, album_id)

        for songwriter in songwriters:
            insert_songwriter_write_song(songwriter, lagu_id)
        for genre in genres:
            insert_genre(lagu_id, genre)
        
        insert_royalti(hak_cipta_id, lagu_id)
    return render(request, "create_album.html", context)

def create_lagu(request, album_id):

    artists = get_artists()
    pilihan_artist = []
    for artist in artists:
        artist_dict = {
            'id': artist[0],
            'nama': artist[1],  # Nama artist
        }
        pilihan_artist.append(artist_dict)
    
    songwriters = get_songwriters()
    pilihan_songwriter = []
    for songwriter in songwriters:
        songwriter_dict = {
            'id': songwriter[0],
            'nama': songwriter[1],  # Nama songwriter
        }
        pilihan_songwriter.append(songwriter_dict)
    
    genres = get_genres()
    pilihan_genre = []
    for genre in genres:
        genre_dict = {
            'nama': genre[0],
        }
        pilihan_genre.append(genre_dict)

    email = request.session.get('email')
    is_artist = request.session.get('isArtist')
    is_songwriter = request.session.get('isSongwriter')
    
    context = {
        'album_name': get_album_name(album_id),
        'me': get_name_akun(email),
        'artists': pilihan_artist,
        'genres': pilihan_genre,
        'songwriters': pilihan_songwriter,
        'isArtist': is_artist,
        'isSongwriter' : is_songwriter
        
    }

    if request.method == 'POST':
        lagu_id = uuid.uuid4()
        judul = request.POST.get('judul')
        if (is_artist):
            artist = get_id_artist(email)
        else:
            artist = request.POST.get('artist')

        songwriters = request.POST.getlist('songwriter')
        genres = request.POST.getlist('genre')
        durasi = request.POST.get('durasi')
        tanggal_rilis = datetime.now()
        tahun = tanggal_rilis.year

        if (is_artist):
            hak_cipta_id = get_pemilik_hak_cipta_artist(email)
        if (is_songwriter):
            hak_cipta_id = get_pemilik_hak_cipta_songwriter(email)
            songwriters.append(get_id_songwriter(email))

        insert_konten(lagu_id, judul, tanggal_rilis, tahun, durasi)
        insert_song(lagu_id, artist, album_id)

        for songwriter in songwriters:
            insert_songwriter_write_song(songwriter, lagu_id)
        for genre in genres:
            insert_genre(lagu_id, genre)
        
        insert_royalti(hak_cipta_id, lagu_id)
        return HttpResponseRedirect(reverse("MusicIndustry:kelola_album"))

    return render(request, "create_lagu.html", context)

def delete_lagu(request, lagu_id):
    if request.method == 'POST':
        print(f"akan didelete lagu", lagu_id)

        #PANGGIL QUERYNYA TAPI NANTI AJA    
        delete_song_query(lagu_id)

        previous_url = request.META.get('HTTP_REFERER', '/')
        return HttpResponseRedirect(previous_url)

def delete_album(request, album_id):
    if request.method == 'POST':
        print(f"akan didelete album", album_id)

        #PANGGIL QUERYNYA TAPI NANTI AJA    
        delete_album_query(album_id)

        previous_url = request.META.get('HTTP_REFERER', '/')
        return HttpResponseRedirect(previous_url)
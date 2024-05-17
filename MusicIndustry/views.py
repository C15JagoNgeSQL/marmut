from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
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
    
    elif(request.session.get('isArtist')):
        albums = get_albums_artist(email)
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

def create_album(request):
    return render(request, "create_album.html")

def daftar_lagu(request, album_id):
    songs = get_albums_songs(album_id)
    nama = get_album_name(album_id)[0]

    isi_tabel = []
    total_durasi = 0
    for song in songs:
            song_dict = {
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

def create_lagu(request):
    context = {
        'isSongwriter' : False
    }
    return render(request, "create_lagu.html", context)
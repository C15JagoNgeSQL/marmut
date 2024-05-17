from django.shortcuts import render
from django.db import connection as conn
from django.http import HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import uuid
from django.utils import timezone
from PlaylistsAndSongs.query import *

def show_kelola_playlist(request):
    email = request.session.get('email')

    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM user_playlist WHERE email_pembuat = %s", [email])
        rows = cursor.fetchall()
        
        playlists = [
            {
            'id':row[1],
            'judul': row[2],
            'jumlah_lagu': row[4],
            'total_durasi': row[7],
            }
            for row in rows
        ]

    return render(request, "kelolaPlaylist.html", {'playlists': playlists})

@csrf_exempt
def show_tambah_playlist(request):
    if request.method == "POST":
        id = uuid.uuid4()
        id_playlist = uuid.uuid4()
        judul = request.POST.get('judul')
        deskripsi = request.POST.get('deskripsi')
        tanggal_dibuat = timezone.now().date()

        if 'email' not in request.session:
            return HttpResponseRedirect(reverse("main:login"))
    
        email = request.session.get('email')

        tambah_playlist(email,id,judul,deskripsi,tanggal_dibuat,id_playlist)
        return HttpResponseRedirect(reverse("PlaylistAndSongs:kelola_playlist"))

    return render(request, "tambahPlaylist.html")

@csrf_exempt
def show_ubah_playlist(request, playlist_id):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM user_playlist WHERE id_user_playlist = %s", [playlist_id])
        rows = cursor.fetchone()

        playlist = {
            'judul': rows[2],
            'deskripsi': rows[3]
        }

        if request.method == 'POST':
            judul = request.POST.get('judul')
            deskripsi = request.POST.get('deskripsi')
            cursor.execute("""
                    UPDATE user_playlist
                    SET judul = %s, deskripsi = %s
                    WHERE id_user_playlist = %s
                """, [judul, deskripsi, playlist_id])
            return HttpResponseRedirect(reverse("PlaylistAndSongs:kelola_playlist"))

    return render(request, "ubahPlaylist.html", {'playlist': playlist})

def show_hapus_playlist(request, playlist_id):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM user_playlist WHERE id_user_playlist = %s", [playlist_id])
        rows = cursor.fetchone()

        id_playlist = rows[6]

        cursor.execute("""
                DELETE FROM user_playlist
                WHERE id_user_playlist = %s
            """, [playlist_id])
        
        cursor.execute("""
                DELETE FROM playlist
                WHERE id = %s
            """, [id_playlist])
        return HttpResponseRedirect(reverse("PlaylistAndSongs:kelola_playlist"))

def show_detail_playlist(request, playlist_id):
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT * 
            FROM 
                user_playlist 
            JOIN 
                akun ON akun.email = user_playlist.email_pembuat 
            WHERE 
                id_user_playlist = %s;
        """, [playlist_id])
        rows = cursor.fetchone()
        print(rows)
        cursor.execute("""
            SELECT 
                konten.judul,
                konten.durasi,
                akun.nama,
                song.id_konten
            FROM 
                user_playlist
            JOIN 
                playlist ON user_playlist.id_playlist = playlist.id
            JOIN 
                playlist_song ON playlist.id = playlist_song.id_playlist
            JOIN 
                konten ON playlist_song.id_song = konten.id
            JOIN
                song ON playlist_song.id_song = song.id_konten
            JOIN
                artist ON song.id_artist = artist.id
            JOIN 
                akun ON artist.email_akun = akun.email
            WHERE 
                user_playlist.id_user_playlist = %s;
        """, [playlist_id])
        songs = cursor.fetchall()

        detail = {
            'id_user_playlist': rows[1],
            'judul': rows[2],
            'pembuat': rows[10],
            'jumlah_lagu': rows[4],
            'total_durasi': rows[7],
            'tanggal_dibuat': rows[5],
            'deskripsi': rows[3],
            'id_playlist': rows[6],
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
    with conn.cursor() as cursor:
        cursor.execute("""
                SELECT 
                    konten.judul AS judul_lagu, 
                    akun.nama AS nama_artist,
                    song.id_konten AS id_song
                FROM 
                    song
                INNER JOIN 
                    konten ON song.id_konten = konten.id
                INNER JOIN 
                    artist ON song.id_artist = artist.id
                INNER JOIN 
                    akun ON artist.email_akun = akun.email;
            """)
        songs = cursor.fetchall()

        songs = [{'judul_lagu': row[0], 'nama_artist': row[1], 'id_song': row[2]} for row in songs]
        
        if request.method == 'POST':
            id_song = request.POST.get('song_id')
            cursor.execute("SELECT * FROM user_playlist WHERE id_playlist = %s", [playlist_id])
            rows = cursor.fetchone()

            if check_lagu_exist_in_playlist(id_song, playlist_id):
                return render(request, "tambahLagu.html", {'error_message': 'Lagu sudah terdapat dalam playlist!', 'songs': songs})
            else:
                cursor.execute("""
                        INSERT INTO playlist_song (id_playlist, id_song)
                        VALUES (%s,%s)
                    """, [playlist_id, id_song])
                
                cursor.execute("""
                    SELECT COUNT(id_song)
                    FROM playlist_song
                    WHERE id_playlist = %s
                """, [playlist_id])
                jumlah_lagu = cursor.fetchone()

                cursor.execute("""
                    SELECT SUM(konten.durasi)
                    FROM playlist_song
                    JOIN song ON playlist_song.id_song = song.id_konten
                    JOIN konten ON konten.id = song.id_konten
                    WHERE playlist_song.id_playlist = %s
                """, [playlist_id])
                total_durasi = cursor.fetchone()
                
                cursor.execute("""
                    UPDATE user_playlist
                    SET jumlah_lagu = %s, total_durasi = %s
                    WHERE id_user_playlist = %s
                """, [jumlah_lagu[0], total_durasi[0], rows[1]])
                return HttpResponseRedirect(reverse("PlaylistAndSongs:detail_playlist", kwargs={'playlist_id': rows[1]}))
            
    return render(request, "tambahLagu.html", {'songs': songs})    

def show_hapus_lagu(request, playlist_id, id_song):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM user_playlist WHERE id_playlist = %s", [playlist_id])
        rows = cursor.fetchone()
        cursor.execute("""
                DELETE FROM playlist_song
                WHERE id_playlist = %s AND id_song = %s
            """, [playlist_id, id_song])
        
        cursor.execute("""
            SELECT COUNT(id_song)
            FROM playlist_song
            WHERE id_playlist = %s
        """, [playlist_id])
        jumlah_lagu = cursor.fetchone()

        cursor.execute("""
            SELECT SUM(konten.durasi)
            FROM playlist_song
            JOIN song ON playlist_song.id_song = song.id_konten
            JOIN konten ON konten.id = song.id_konten
            WHERE playlist_song.id_playlist = %s
        """, [playlist_id])
        total_durasi = cursor.fetchone()
        if total_durasi[0] is None:
            total_durasi = [0]
        
        cursor.execute("""
            UPDATE user_playlist
            SET jumlah_lagu = %s, total_durasi = %s
            WHERE id_user_playlist = %s
        """, [jumlah_lagu[0], total_durasi[0], rows[1]])
        
        return HttpResponseRedirect(reverse("PlaylistAndSongs:detail_playlist", kwargs={'playlist_id': rows[1]}))
          
def show_detail_lagu(request, song_id):
    with conn.cursor() as cursor:
        email = request.session.get('email')
        cursor.execute("""
            SELECT 
                premium.email
            FROM 
                premium
            WHERE
                premium.email = %s;
        """, [email])
        is_premium = cursor.fetchone()

        
        cursor.execute("""
            SELECT 
                konten.judul,
                konten.tanggal_rilis,
                konten.tahun,
                konten.durasi,
                song.total_play,
                song.total_download,
                akun.nama,
                album.judul
            FROM 
                konten
            JOIN 
                song ON konten.id = song.id_konten
            JOIN
                album ON album.id = song.id_album
            JOIN
                artist ON artist.id = song.id_artist
            JOIN
                akun ON akun.email = artist.email_akun
            WHERE 
                konten.id = %s;
        """, [song_id])
        songs = cursor.fetchone()

        cursor.execute("""
            SELECT 
                genre.genre
            FROM 
                genre
            JOIN 
                konten ON konten.id = genre.id_konten
            WHERE 
                konten.id = %s;
        """, [song_id])
        genres = cursor.fetchall()

        cursor.execute("""
            SELECT 
                akun.nama
            FROM 
                akun
            JOIN 
                songwriter ON songwriter.email_akun = akun.email
            JOIN
                songwriter_write_song ON songwriter_write_song.id_songwriter = songwriter.id
            JOIN
                song ON song.id_konten = songwriter_write_song.id_song
            WHERE 
                song.id_konten = %s;
        """, [song_id])
        songwriters = cursor.fetchall()

        #print(songs)
        #print(genres)
        #print(songwriters)

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
    if is_premium:
        return render(request, "detailLagu.html", {'detail': detail, 'premium': 'premium'})
    else:
        return render(request, "detailLagu.html", {'detail': detail})

def show_tambah_lagu_ke_playlist(request, id_song):
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT 
                konten.judul,
                akun.nama
            FROM 
                konten
            JOIN 
                song ON konten.id = song.id_konten
            JOIN
                artist ON artist.id = song.id_artist
            JOIN
                akun ON akun.email = artist.email_akun
            WHERE 
                konten.id = %s;
        """, [id_song])
        songs = cursor.fetchone()

        email = request.session.get('email')

        cursor.execute("""
            SELECT 
                id,judul
            FROM 
                user_playlist
            WHERE 
                email_pembuat = %s;
        """, [email])
        playlists = cursor.fetchall()

        song = {
            'judul': songs[0],
            'artist': songs[1],
            'playlists': [
                {
                'id': playlist[0],
                'playlist': playlist[1]
                }
                for playlist in playlists
            ]
        }

        if request.method == 'POST':
            playlist_id = request.POST.get('playlist')

            if check_lagu_exist_in_playlist(id_song, playlist_id):
                return render(request, "tambahLagu.html", {'error_message': 'Lagu sudah terdapat dalam playlist!', 'songs': songs})
            else:
                cursor.execute("""
                    INSERT INTO playlist_song (id_playlist, id_song)
                    VALUES (%s,%s)
                """, [playlist_id, id_song])
                
                cursor.execute("""
                    SELECT COUNT(id_song)
                    FROM playlist_song
                    WHERE id_playlist = %s
                """, [playlist_id])
                jumlah_lagu = cursor.fetchone()

                cursor.execute("""
                    SELECT SUM(konten.durasi)
                    FROM playlist_song
                    JOIN song ON playlist_song.id_song = song.id_konten
                    JOIN konten ON konten.id = song.id_konten
                    WHERE playlist_song.id_playlist = %s
                """, [playlist_id])
                total_durasi = cursor.fetchone()
                
                cursor.execute("""
                    UPDATE user_playlist
                    SET jumlah_lagu = %s, total_durasi = %s
                    WHERE id_user_playlist = %s
                """, [jumlah_lagu[0], total_durasi[0], playlist_id])
                return HttpResponseRedirect(reverse("PlaylistAndSongs:detail_playlist", kwargs={'playlist_id': rows[1]}))

        return render(request, "tambah_lagu_ke_playlist.html", {'song': song})

def show_play_user_playlist(request):
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
    return render(request, "play_user_playlist.html", {'detail': detail})


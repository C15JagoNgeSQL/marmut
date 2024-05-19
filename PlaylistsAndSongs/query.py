from django.db import connection as conn

def get_user_playlist_data(email):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")

        cursor.execute("SELECT * FROM user_playlist WHERE email_pembuat = %s", [email])
        user_playlist_data = cursor.fetchall()
        
        playlists = [
            {
            'id':data[1],
            'judul': data[2],
            'jumlah_lagu': data[4],
            'total_durasi': data[7],
            }
            for data in user_playlist_data
        ]

        cursor.execute("set search_path to public;")

        return playlists
    
def tambah_playlist(email, id_user_playlist, judul, deskripsi, tanggal_dibuat, id_playlist):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")

        cursor.execute("""
            INSERT INTO PLAYLIST (id)
            VALUES (%s)
        """, [id_playlist])

        cursor.execute("""
            INSERT INTO USER_PLAYLIST (email_pembuat, id_user_playlist, judul, deskripsi, jumlah_lagu, tanggal_dibuat, id_playlist, total_durasi)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, [email, id_user_playlist, judul, deskripsi, 0, tanggal_dibuat, id_playlist, 0])

        cursor.execute("set search_path to public;")
    
def edit_playlist(judul, deskripsi, user_playlist_id):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")

        cursor.execute("""
            UPDATE user_playlist
            SET judul = %s, deskripsi = %s
            WHERE id_user_playlist = %s
        """, [judul, deskripsi, user_playlist_id])

        cursor.execute("set search_path to public;")

def get_user_playlist_from_user_playlist_id(id_user_playlist):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")

        cursor.execute("""
            SELECT * 
            FROM user_playlist 
            JOIN akun ON akun.email = user_playlist.email_pembuat 
            WHERE id_user_playlist = %s
        """, [id_user_playlist])
        data_user_playlist = cursor.fetchone()

        cursor.execute("set search_path to public;")

        return data_user_playlist
    
def get_user_playlist_from_playlist_id(playlist_id):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")

        cursor.execute("""
            SELECT * 
            FROM user_playlist 
            WHERE id_playlist = %s
        """, [playlist_id])
        data_user_playlist = cursor.fetchone()

        cursor.execute("set search_path to public;")

        return data_user_playlist
    
def delete_user_playlist(id_user_playlist, id_playlist):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")

        cursor.execute("""
            DELETE FROM user_playlist
            WHERE id_user_playlist = %s
        """, [id_user_playlist])
        
        cursor.execute("""
            DELETE FROM playlist_song
            WHERE id_playlist = %s
        """, [id_playlist])

        cursor.execute("set search_path to public;")

def get_song_data(playlist_id):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")

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

        cursor.execute("set search_path to public;")

        return songs
    
def get_all_song():
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")

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

        cursor.execute("set search_path to public;")

        return songs

def check_lagu_exist_in_playlist(id_song, playlist_id):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")

        cursor.execute("""
            SELECT id_song
            FROM playlist_song
            WHERE id_playlist = %s AND id_song = %s
        """, [playlist_id, id_song])
        existing_song = cursor.fetchone()

        cursor.execute("set search_path to public;")

        if existing_song:
            return True
        else:
            return False
        
def tambah_lagu_ke_playlist(playlist_id, id_song, rows):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")
        
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

        cursor.execute("set search_path to public;")

def delete_lagu_dari_playlist(playlist_id, id_song):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")
        
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
        
        cursor.execute("set search_path to public;")

        return rows
    
def check_if_premium(email):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")
        
        cursor.execute("""
            SELECT premium.email
            FROM premium
            WHERE premium.email = %s;
        """, [email])
        is_premium = cursor.fetchone()

        cursor.execute("set search_path to public;")

        return is_premium
    
def get_song_detail(song_id):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")
        
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
        song_detail = cursor.fetchone()

        cursor.execute("set search_path to public;")

        return song_detail
    
def hitung_total_play(song_id):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")

        cursor.execute("""
                SELECT COUNT(id_song)
                FROM akun_play_song
                WHERE id_song = %s
            """, [song_id])
        jumlah_play = cursor.fetchone()

        cursor.execute("set search_path to public;")

        return jumlah_play
    
def hitung_total_download(song_id):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")

        cursor.execute("""
                SELECT COUNT(id_song)
                FROM downloaded_song
                WHERE id_song = %s
            """, [song_id])
        jumlah_download = cursor.fetchone()

        cursor.execute("set search_path to public;")

        return jumlah_download
    
def get_song_genres(song_id):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")
        
        cursor.execute("""
            SELECT genre.genre
            FROM genre
            JOIN konten ON konten.id = genre.id_konten
            WHERE konten.id = %s;
        """, [song_id])
        song_genres = cursor.fetchall()

        cursor.execute("set search_path to public;")

        return song_genres
    
def get_song_songwriters(song_id):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")
        
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

        cursor.execute("set search_path to public;")

        return songwriters
    
def get_user_user_playlist(email):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")
        
        cursor.execute("""
            SELECT id_user_playlist,judul
            FROM user_playlist
            WHERE email_pembuat = %s;
        """, [email])
        user_playlist = cursor.fetchall()

        cursor.execute("set search_path to public;")
        
        return user_playlist
    
def akun_play_song(email, id_song, current_time):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")
        
        cursor.execute("""
            INSERT INTO akun_play_song (email_pemain, id_song, waktu)
            VALUES (%s, %s, %s)
        """, [email, id_song, current_time])

        cursor.execute("set search_path to public;")

def akun_play_playlist(email, playlist_id, user_playlist_data, current_time):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")
        
        cursor.execute("""
            INSERT INTO akun_play_user_playlist (email_pemain, id_user_playlist, email_pembuat, waktu)
            VALUES (%s, %s, %s, %s)
        """, [email, playlist_id, user_playlist_data[0], current_time])

        cursor.execute("set search_path to public;")

def check_downloaded_song(id_song):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")
        
        cursor.execute("SELECT id_song FROM downloaded_song WHERE id_song = %s", [id_song])
        existing_song = cursor.fetchone()

        cursor.execute("set search_path to public;")

        if existing_song:
            return True
        else:
            return False

def premium_download_song(id_song, email):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")
        
        cursor.execute("""
            INSERT INTO downloaded_song (id_song, email_downloader)
            VALUES (%s, %s)
        """, [id_song, email])

        cursor.execute("set search_path to public;")
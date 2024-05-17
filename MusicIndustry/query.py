from django.db import connection as conn

def get_akun_data(email):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")

        cursor.execute(""" 
        SELECT *
        FROM AKUN
        WHERE email = %s;
        """, (email,))

        result = cursor.fetchone()
        cursor.execute("set search_path to public;")
        return result

def get_label_data(email):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")

        cursor.execute(""" 
        SELECT *
        FROM LABEL
        WHERE email = %s;
        """, (email,))

        result = cursor.fetchone()
        cursor.execute("set search_path to public;")
        return result

def get_albums_label(email):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")

        cursor.execute(""" 
        select album.*
        from album, label
        where album.id_label = label.id and email = %s;
        """, (email,))

        result = cursor.fetchall()
        cursor.execute("set search_path to public;")
        return result
    
def get_albums_songs(id):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")

        cursor.execute(""" 
        select konten.*
        from konten, song, album
        where song.id_album = album.id and song.id_konten = konten.id and album.id = %s;
        """, (id,))

        result = cursor.fetchall()
        cursor.execute("set search_path to public;")
        return result
    
def get_songs_royalti_artist(email):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")

        cursor.execute(""" 
        SELECT 
            konten.id, 
            konten.judul AS judul_lagu, 
            album.judul AS judul_album, 
            COALESCE(royalti.jumlah, 0) AS jumlah_royalti
        FROM 
            konten
        JOIN 
            song ON konten.id = song.id_konten
        JOIN 
            album ON song.id_album = album.id
        LEFT JOIN 
            royalti ON song.id_konten = royalti.id_song
        JOIN 
            artist ON song.id_artist = artist.id
        WHERE 
            artist.email_akun = %s;
        """, (email,))

        result = cursor.fetchall()
        cursor.execute("set search_path to public;")
        return result
    
def get_songs_royalti_label(email):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")

        cursor.execute(""" 
        SELECT 
            konten.id, 
            konten.judul AS judul_lagu, 
            album.judul AS judul_album, 
            COALESCE(royalti.jumlah, 0) AS jumlah_royalti
        FROM 
            konten
        JOIN 
            song ON konten.id = song.id_konten
        JOIN 
            album ON song.id_album = album.id
        LEFT JOIN 
            royalti ON song.id_konten = royalti.id_song
        JOIN 
            label ON album.id_label = label.id
        WHERE 
            label.email = %s;
        """, (email,))
        
        result = cursor.fetchall()
        cursor.execute("set search_path to public;")
        return result
    
def get_songs_royalti_songwriter(email):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")

        cursor.execute(""" 
        SELECT 
            konten.id, 
            konten.judul AS judul_lagu, 
            album.judul AS judul_album, 
            COALESCE(royalti.jumlah, 0) AS jumlah_royalti
        FROM 
            konten
        JOIN 
            song ON konten.id = song.id_konten
        JOIN 
            album ON song.id_album = album.id
        LEFT JOIN 
            royalti ON song.id_konten = royalti.id_song
        JOIN 
            songwriter_write_song ON song.id_konten = songwriter_write_song.id_song
        JOIN 
            songwriter ON songwriter.id = songwriter_write_song.id_songwriter
        WHERE 
            songwriter.email_akun = %s;
        """, (email,))

        result = cursor.fetchall()
        cursor.execute("set search_path to public;")
        return result
    
def get_albums_artist(email):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")

        cursor.execute(""" 
        select distinct album.id, album.judul, label.nama, album.jumlah_lagu, album.total_durasi
        from album
        join song on song.id_album = album.id
        join artist on song.id_artist = artist.id
        join label on label.id = album.id_label
        where artist.email_akun = %s;
        """, (email,))

        result = cursor.fetchall()
        cursor.execute("set search_path to public;")
        return result
    
def get_albums_songwriter(email):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")

        cursor.execute(""" 
        select distinct album.id, album.judul, label.nama, album.jumlah_lagu, album.total_durasi
        from album
        join song on song.id_album = album.id
        join songwriter_write_song on song.id_konten = songwriter_write_song.id_song
        join songwriter on songwriter.id = songwriter_write_song.id_songwriter
        join label on label.id = album.id_label
        where songwriter.email_akun = %s;
        """, (email,))

        result = cursor.fetchall()
        cursor.execute("set search_path to public;")
        return result
    
def get_name_akun(email):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")

        cursor.execute(""" 
        select akun.nama
        from akun
        where akun.email = %s;
        """, (email,))

        result = cursor.fetchone()
        cursor.execute("set search_path to public;")
        return result[0]
    
def get_name_label(email):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")

        cursor.execute(""" 
        select label.nama
        from label
        where label.email = %s;
        """, (email,))

        result = cursor.fetchone()
        cursor.execute("set search_path to public;")
        return result[0]
    
def get_album_name(id):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")

        cursor.execute(""" 
        select album.judul
        from album
        where album.id = %s
        """, (id,))

        result = cursor.fetchone()
        cursor.execute("set search_path to public;")
        return result
    
def count_total_play(id_lagu):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")

        cursor.execute(""" 
        select count(akun_play_song) as total_play
        from akun_play_song
        where id_song = %s;
        """, (id_lagu,))

        result = cursor.fetchone()
        cursor.execute("set search_path to public;")
        
        if result:
            return result[0]  # Mengambil elemen pertama dari tuple
        return 0

def count_total_download(id_lagu):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")

        cursor.execute(""" 
        select count(downloaded_song) as total_download
        from downloaded_song
        where id_song = %s;
        """, (id_lagu,))

        result = cursor.fetchone()
        cursor.execute("set search_path to public;")
        
        if result:
            return result[0]  # Mengambil elemen pertama dari tuple
        return 0

def delete_song_query(id_lagu):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")

        cursor.execute(""" 
        delete from konten
        where konten.id = %s
        """, (id_lagu,))

        cursor.execute("set search_path to public;")
    
def delete_album_query(id_album):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")

        cursor.execute(""" 
        delete from album
        where album.id = %s;
        """, (id_album,))

        cursor.execute("set search_path to public;")
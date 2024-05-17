from django.db import connection as conn
import uuid

def get_songs_artist(email):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")

        cursor.execute(""" 
        select konten.judul from konten, song, artist
        where konten.id = song.id_konten and artist.id = song.id_artist and artist.email_akun = %s;
        """, (email,))

        result = cursor.fetchall()
        cursor.execute("set search_path to public;")
        return result
    
def get_songs_songwriter(email):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")

        cursor.execute(""" 
        select konten.judul 
        from konten, songwriter, songwriter_write_song
        where konten.id = songwriter_write_song.id_song and songwriter.id = songwriter_write_song.id_songwriter and songwriter.email_akun = %s;
        """, (email,))

        result = cursor.fetchall()
        cursor.execute("set search_path to public;")
        return result

def get_podcasts(email):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")

        cursor.execute(""" 
        select konten.judul
        from konten, podcast
        where konten.id = podcast.id_konten and email_podcaster = %s;
        """, (email,))

        result = cursor.fetchall()
        cursor.execute("set search_path to public;")
        return result
    
def get_playlist(email):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")

        cursor.execute(""" 
        select judul
        from user_playlist
        where email_pembuat = %s;
        """, (email,))

        result = cursor.fetchall()
        cursor.execute("set search_path to public;")
        return result
    
def get_album(email):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")

        cursor.execute(""" 
        select album.judul
        from album, label
        where album.id_label = label.id and email = %s;
        """, (email,))

        result = cursor.fetchall()
        cursor.execute("set search_path to public;")
        return result

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

def login_akun(email, password):
    with conn.cursor() as cursor:
        # Mengatur schema database
        cursor.execute("set search_path to marmut;")

        cursor.execute(""" 
        SELECT *
        FROM AKUN
        WHERE email = %s AND password = %s;
        """, (email, password))

        result = cursor.fetchone()

        cursor.execute("set search_path to public;")
        return result
    
def login_label(email, password):
    with conn.cursor() as cursor:
        # Mengatur schema database
        cursor.execute("set search_path to marmut;")

        cursor.execute(""" 
        SELECT *
        FROM LABEL
        WHERE email = %s AND password = %s;
        """, (email, password))

        result = cursor.fetchone()

        cursor.execute("set search_path to public;")
        return result
    
def cek_akun(email):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")

        cursor.execute(""" 
        SELECT *
        FROM AKUN
        WHERE email = %s;
        """, (email,))
    
        result = cursor.fetchone()
        cursor.execute("set search_path to public;")
        return result is not None

    
def cek_artist(email):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")

        cursor.execute(""" 
        SELECT *
        FROM ARTIST
        WHERE email_akun = %s;
        """, (email,))

        result = cursor.fetchone()
        cursor.execute("set search_path to public;")
        return result is not None

def cek_songwriter(email):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")

        cursor.execute(""" 
        SELECT *
        FROM SONGWRITER
        WHERE email_akun = %s;
        """, (email,))

        result = cursor.fetchone()
        cursor.execute("set search_path to public;")
        return result is not None

def cek_podcaster(email):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")

        cursor.execute(""" 
        SELECT *
        FROM PODCASTER
        WHERE email = %s;
        """, (email,))

        result = cursor.fetchone()
        cursor.execute("set search_path to public;")
        return result is not None

def cek_label(email):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")

        cursor.execute(""" 
        SELECT *
        FROM LABEL
        WHERE email = %s;
        """, (email,))

        result = cursor.fetchone()
        cursor.execute("set search_path to public;")
        return result is not None

def cek_premium(email):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")

        cursor.execute(""" 
        SELECT *
        FROM PREMIUM
        WHERE email = %s;
        """, (email,))

        result = cursor.fetchone()
        cursor.execute("set search_path to public;")
        return result is not None

def cek_nonpremium(email):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")

        cursor.execute(""" 
        SELECT *
        FROM NONPREMIUM
        WHERE email = %s;
        """, (email,))

        result = cursor.fetchone()
        cursor.execute("set search_path to public;")
        return result is not None
    
def cek_existing_email(email):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")

        cursor.execute("SELECT email FROM AKUN WHERE email = %s", [email])
        existing_email_in_user = cursor.fetchone()

        cursor.execute("SELECT email FROM LABEL WHERE email = %s", [email])
        existing_email_in_label = cursor.fetchone()

        cursor.execute("set search_path to public;")

        if existing_email_in_user or existing_email_in_label:
            return True
        else:
            return False
    
def register_user(email, password, nama, gender, tempat_lahir, tanggal_lahir, is_verified, kota_asal):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")

        cursor.execute("""
            INSERT INTO AKUN (email, password, nama, gender, tempat_lahir, tanggal_lahir, is_verified, kota_asal)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, [email, password, nama, gender, tempat_lahir, tanggal_lahir, is_verified, kota_asal])
        
        cursor.execute("""
            INSERT INTO nonpremium (email)
            VALUES (%s)
        """, [email])

        cursor.execute("set search_path to public;")

def register_podcaster(email):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")

        cursor.execute("""
            INSERT INTO podcaster (email)
            VALUES (%s)
        """, [email])

        cursor.execute("set search_path to public;")
            
def register_artist(id, id_pemilik_hak_cipta, email):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")

        cursor.execute("""
            INSERT INTO pemilik_hak_cipta (id, rate_royalti)
            VALUES (%s, %s)
        """, [id_pemilik_hak_cipta, 10])

        cursor.execute("""
            INSERT INTO artist (id, email_akun, id_pemilik_hak_cipta)
            VALUES (%s, %s, %s)
        """, [id, email, id_pemilik_hak_cipta])

        cursor.execute("set search_path to public;")
            
def register_songwriter(id, id_pemilik_hak_cipta, email):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")

        cursor.execute("""
            INSERT INTO pemilik_hak_cipta (id, rate_royalti)
            VALUES (%s, %s)
        """, [id_pemilik_hak_cipta, 10])

        cursor.execute("""
            INSERT INTO songwriter (id, email_akun, id_pemilik_hak_cipta)
            VALUES (%s, %s, %s)
        """, [id, email, id_pemilik_hak_cipta])

        cursor.execute("set search_path to public;")

def register_label(id,email,password,nama,kontak):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")

        cursor.execute("""
            INSERT INTO LABEL (id, email, password, nama, kontak)
            VALUES (%s,%s,%s,%s,%s)
        """, [id,email,password,nama,kontak])

        cursor.execute("set search_path to public;")
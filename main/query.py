from django.db import connection as conn

def get_songs(email):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")

        cursor.execute(""" 
        select konten.judul from konten, song, artist
        where konten.id = song.id_konten and artist.id = song.id_artist and artist.email_akun = %s;
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
from django.db import connection as conn
    

def get_podcast_data(id):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")

        cursor.execute(""" 
        SELECT k.judul, k.genre, p.email_podcaster, k.tanggal_rilis, k.tahun
        FROM PODCAST p
        JOIN KONTEN k ON p.id_konten = k.id
        WHERE p.id_konten = %s;
        """, (id,))

        result = cursor.fetchone()
        cursor.execute("set search_path to public;")
        return result
    
def get_podcast_episodes(id):
    with conn.cursor() as cursor:
        cursor.execute("set search_path to marmut;")

        cursor.execute(""" 
        SELECT k.judul, k.genre, k.tanggal_rilis, k.tahun, k.durasi, e.id
        FROM EPISODE e
        JOIN KONTEN k ON e.id_konten = k.id
        WHERE e.id_podcast = %s;
        """, (id,))

        result = cursor.fetchall()
        cursor.execute("set search_path to public;")
        return result
    


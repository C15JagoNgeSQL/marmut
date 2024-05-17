from django.db import connection as conn

def tambah_playlist(email,id,judul,deskripsi,tanggal_dibuat,id_playlist):
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO PLAYLIST (id)
            VALUES (%s)
        """, [id_playlist])

        cursor.execute("""
            INSERT INTO USER_PLAYLIST (email_pembuat, id_user_playlist, judul, deskripsi, jumlah_lagu, tanggal_dibuat, id_playlist, total_durasi)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, [email,id,judul,deskripsi,0, tanggal_dibuat,id_playlist,0])

def check_lagu_exist_in_playlist(id_song, playlist_id):
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT id_song
            FROM playlist_song
            WHERE id_playlist = %s AND id_song = %s
        """, [playlist_id, id_song])
        existing_song = cursor.fetchone()

        if existing_song:
            return True
        else:
            return False
        
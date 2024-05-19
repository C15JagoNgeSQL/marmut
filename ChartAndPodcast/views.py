import json
from django.shortcuts import render

from django.db import connections
from django.db import connection
from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

# def chart_detail_view(request):
#     # Data yang akan dimasukkan ke dalam template
#     context = {
#         'chart_type': 'Daily Top 20',
#         'songs': [
#             {'title': 'Song1', 'artist': 'Artist1', 'release_date': '09/03/2024', 'total_plays': 21000},
#             {'title': 'Song2', 'artist': 'Artist2', 'release_date': '02/03/2024', 'total_plays': 19000}
#         ]
#     }
#     return render(request, 'chart_detail.html', context)

def chart_detail_view(request, id_playlist):
    chart_data = {}
    with connections['default'].cursor() as cursor:
        # Mengatur schema database
        cursor.execute("SET search_path TO marmut;")

        # Mengambil tipe chart berdasarkan tipe dan id_playlist
        cursor.execute("""
            SELECT chart.tipe, chart.id_playlist
            FROM chart
            WHERE id_playlist = %s;
        """, [id_playlist])
        chart = cursor.fetchone()
        if chart:
            chart_data['chart_type'] = chart[0]
            chart_data['chart_id'] = chart[1]

            # Mengambil data lagu dari tabel SONG, KONTEN, dan ARTISTS berdasarkan id_playlist
            cursor.execute("""
                           
                    
                SELECT 
                    k.judul, 
                    k.tanggal_rilis, 
                    AKUN.nama, 
                    s.total_play
                FROM 
                    PLAYLIST_SONG ps, 
                    SONG s, 
                    KONTEN k, 
                    ARTIST a,
                    AKUN
                WHERE 
                    ps.id_song = s.id_konten 
                    AND s.id_konten = k.id 
                    AND s.id_artist = a.id 
                    AND a.email_akun = AKUN.email
                    AND ps.id_playlist = %s
                ORDER BY 
                    s.total_play DESC

            """, [id_playlist])
            songs = cursor.fetchall()
            song_list = []
            for song in songs:
                song_data = {
                    'judul': song[0],
                    'tanggal_rilis': song[1].strftime('%d/%m/%Y'),
                    'artist': song[2],
                    'total_play': song[3]
                }
                song_list.append(song_data)

            chart_data['songs'] = song_list

    return render(request, 'chart_detail.html', {'chart_data': chart_data, 'songs': song_list})



def crud_kelola_podcast_view(request):
    # Mendapatkan data email podcaster
    if 'email' not in request.session:
        return HttpResponseRedirect(reverse("main:login"))
    
    email_podcaster = request.session.get('email')

    # Mempersiapkan data untuk konteks
    podcast_data = []

    with connections['default'].cursor() as cursor:
        # Mengatur schema database
        cursor.execute("SET search_path TO marmut;")

        # Mendapatkan daftar podcast milik podcaster
        cursor.execute("""
            SELECT p.id_konten::text, k.judul, k.tanggal_rilis, k.durasi, k.tahun
            FROM PODCAST p, KONTEN k
            WHERE p.id_konten = k.id AND
            p.email_podcaster = %s;
        """, [email_podcaster])
        podcasts = cursor.fetchall()

        # print(podcasts)

        for podcast in podcasts:
            # Mendapatkan daftar episode untuk setiap podcast
            cursor.execute("""
                SELECT e.judul, e.deskripsi, e.durasi, e.tanggal_rilis
                FROM EPISODE e
                WHERE e.id_konten_podcast = %s;
            """, [podcast[0]])
            episodes = cursor.fetchall()

            total_durasi = podcast[3]

            podcast_data.append({
                'id_konten': podcast[0],
                'judul': podcast[1],
                'jumlah_episode': len(episodes),
                'total_durasi': f"{total_durasi // 60} jam {total_durasi % 60} menit",
                'episodes': [
                    {
                        'judul': episode[0],
                        'deskripsi': episode[1],
                        'durasi': f"{episode[2] // 60} menit {episode[2] % 60} detik",
                        'tanggal_rilis': episode[3],
                    }
                    for episode in episodes
                ],
            })

    context = {
        'podcasts': podcast_data,
    }

    # print(context)

    return render(request, 'crud_kelola_podcast.html', context)


def crud_episode_view(request, podcast_data):
    #Mengambil dari crud_kelola_podcast.view
    if 'email' not in request.session:
        return HttpResponseRedirect(reverse("main:login"))

    email_podcaster = request.session.get('email')

    # Mempersiapkan data untuk konteks
    podcast_data = []

    with connections['default'].cursor() as cursor:
        # Mengatur schema database
        cursor.execute("SET search_path TO marmut;")

        # Mendapatkan daftar podcast milik podcaster
        cursor.execute("""
            SELECT p.id_konten::text, k.judul, k.tanggal_rilis, k.durasi, k.tahun
            FROM PODCAST p, KONTEN k
            WHERE p.id_konten = k.id AND
            p.email_podcaster = %s;
        """, [email_podcaster])
        podcasts = cursor.fetchall()

        # print(podcasts)

        for podcast in podcasts:
            # Mendapatkan daftar episode untuk setiap podcast
            cursor.execute("""
                SELECT e.judul, e.deskripsi, e.durasi, e.tanggal_rilis, e.id_episode, e.id_konten_podcast
                FROM EPISODE e
                WHERE e.id_konten_podcast = %s;
            """, [podcast[0]])
            episodes = cursor.fetchall()

            total_durasi = podcast[3]

            podcast_data.append({
                'id_konten': podcast[0],
                'judul': podcast[1],
                'jumlah_episode': len(episodes),
                'total_durasi': f"{total_durasi // 60} jam {total_durasi % 60} menit",
                'episodes': [
                    {
                        'id_konten_podcast': episode[5],
                        'id_episode': episode[4],
                        'judul': episode[0],
                        'deskripsi': episode[1],
                        'durasi': f"{episode[2] // 60} menit {episode[2] % 60} detik",
                        'tanggal_rilis': episode[3],
                    }
                    for episode in episodes
                ],
            })

    # print(podcast_data)
    context = {
        'podcasts': podcast_data,
        'episodes': podcast_data[0]['episodes']
    }

    return render(request, 'crud_episode.html', context)




def lihat_chart_view(request):
    chart_data = []
    with connections['default'].cursor() as cursor:
        # Mengatur schema database
        cursor.execute("SET search_path TO marmut;")

        # Mengambil daftar chart
        cursor.execute("""
            SELECT chart.tipe, chart.id_playlist
            FROM chart;
        """)
        charts = cursor.fetchall()
        for chart in charts:
            chart_data.append({
                "tipe": chart[0],
                "id_playlist": chart[1]
            })

    return render(request, 'lihat_chart.html', {'chart_data': chart_data})

#Done first

#Melihat daftar episode di dalam podcast
def r_podcast_view(request, podcast_id):
    podcast_data = {}

    with connections['default'].cursor() as cursor:
        # Mengatur schema database
        cursor.execute("SET search_path TO marmut;")

        #Data yang perlu diambil
        #1. Judul podcast
        #2. Genre podcast
        #3. Podcaster
        #4. Total durasi
        #5. Tanggal rilis
        #6. Tahun

        # Daftar episode
        #1. Judul episode
        #2. Deskripsi episode
        #3. Durasi episode
        #4. Tanggal rilis episode

        
        # Mengambil data podcast berdasarkan podcast_id
        cursor.execute("""
            SELECT 
                k.judul, 
                k.tanggal_rilis, 
                k.durasi, 
                k.tahun, 
                g.genre, 
                pd.email,
                a.nama
            FROM 
                PODCAST as p, 
                KONTEN as k, 
                GENRE as g, 
                PODCASTER as pd,
                AKUN as a
            WHERE 
                p.id_konten = k.id 
                AND k.id = g.id_konten 
                AND p.email_podcaster = pd.email
                AND pd.email = a.email
                AND k.id = %s;
                       
        """, [podcast_id])
        podcast = cursor.fetchone()

        # print(podcast)

        # Mengambil data podcaster berdasarkan email_podcaster
        if podcast:
            # podcast_data['id_konten'] = podcast[0]
            podcast_data['judul'] = podcast[0]
            podcast_data['tanggal_rilis'] = podcast[1]
            podcast_data['durasi'] = podcast[2]
            podcast_data['genre'] = podcast[4]
            podcast_data['tahun'] = podcast[3]
            podcast_data['podcaster'] = podcast[6]

            # Mengambil data episode yang terkait dengan id_konten
            cursor.execute("""
                SELECT e.judul, e.deskripsi, e.durasi, e.tanggal_rilis
                FROM episode e
                WHERE e.id_konten_podcast = %s;
            """, [podcast_id])
            episodes = cursor.fetchall()

            total_durasi_menit = 0
            episode_list = []

            for episode in episodes:
                judul_episode = episode[0]
                deskripsi = episode[1]
                durasi_menit = episode[2]
                tanggal_rilis = episode[3]

                total_durasi_menit += durasi_menit

                durasi_jam = durasi_menit // 60
                durasi_menit = durasi_menit % 60
                durasi_str = f"{durasi_jam} jam {durasi_menit} menit" if durasi_jam > 0 else f"{durasi_menit} menit"

                episode_data = {
                    'judul_episode': judul_episode,
                    'deskripsi': deskripsi,
                    'durasi': durasi_str,
                    'tanggal': tanggal_rilis.strftime('%d/%m/%Y')
                }
                episode_list.append(episode_data)

            total_jam = total_durasi_menit // 60
            total_menit = total_durasi_menit % 60
            podcast_data['durasi'] = f"{total_jam} jam {total_menit} menit" if total_jam > 0 else f"{total_menit} menit"
            podcast_data['episodes'] = episode_list
            

    return render(request, 'r_podcast.html', {'podcast_data': podcast_data})


def list_podcast_view(request):
    with connection.cursor() as cursor:
        cursor.execute("set search_path to marmut;")
        cursor.execute("""
            SELECT KONTEN.id, KONTEN.judul
            FROM PODCAST
            JOIN KONTEN ON PODCAST.id_konten = KONTEN.id
        """)
        podcasts = cursor.fetchall()
   
    # Cek apakah ada data podcast yang ditemukan
    if podcasts:
        context = {
            'podcasts': [{'id_konten': podcast[0], 'judul': podcast[1]} for podcast in podcasts],
        }
    else:
        context = {
            'podcasts': [],
        }
    return render(request, 'podcast_list.html', context)


@csrf_exempt
def delete_episode_view(request):
    podcast_id = json.loads(request.body)['id_podcast']
    episode_id = json.loads(request.body)['id_episode']

    # Mengambil email dari sesi
    if 'email' not in request.session:
        return HttpResponseRedirect(reverse("main:login"))

    email_podcaster = request.session.get('email')

    with connections['default'].cursor() as cursor:
        # Mengatur schema database
        cursor.execute("SET search_path TO marmut;")

        # Periksa apakah episode terkait dengan podcast yang dimiliki oleh podcaster
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1
                FROM EPISODE e
                JOIN PODCAST p ON e.id_konten_podcast = p.id_konten
                WHERE p.email_podcaster = %s AND e.id_konten_podcast = %s AND e.id_episode = %s
            );
        """, [email_podcaster, podcast_id, episode_id])
        episode_exists = cursor.fetchone()[0]

        if episode_exists:
            # Hapus episode dari database
            cursor.execute("""
                DELETE FROM EPISODE
                WHERE id_episode = %s;
            """, [episode_id])

    # Redirect ke halaman detail podcast atau halaman lain yang sesuai
    return HttpResponse("Success!")

import uuid

@csrf_exempt
def create_episode(request, id_konten_podcast):
    print("tes")
    if request.method == 'POST':
        print("masuk")
        data = json.loads(request.body)
        id_episode = uuid.uuid4()
        judul = data.get('judul')
        deskripsi = data.get('deskripsi')
        durasi = data.get('durasi')
        tanggal_rilis = data.get('tanggal_rilis')

        with connections['default'].cursor() as cursor:
            cursor.execute("SET search_path TO marmut;")
            cursor.execute("""
                INSERT INTO EPISODE (id_episode, id_konten_podcast, judul, deskripsi, durasi, tanggal_rilis)
                VALUES (%s, %s, %s, %s, %s)
            """, [id_episode, id_konten_podcast, judul, deskripsi, durasi, tanggal_rilis])

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)




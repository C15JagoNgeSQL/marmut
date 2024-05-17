from django.shortcuts import render

from django.db import connections
from django.shortcuts import render
from datetime import datetime

# Create your views here.

def chart_detail_view(request):
    # Data yang akan dimasukkan ke dalam template
    context = {
        'chart_type': 'Daily Top 20',
        'songs': [
            {'title': 'Song1', 'artist': 'Artist1', 'release_date': '09/03/2024', 'total_plays': 21000},
            {'title': 'Song2', 'artist': 'Artist2', 'release_date': '02/03/2024', 'total_plays': 19000}
        ]
    }
    return render(request, 'chart_detail.html', context)


def crud_kelola_podcast_view(request):
    context = {
        'judul_playlist': 'Playlist1',
        'pembuat': 'Pembuat1',
        'jumlah_lagu': 12,
        'total_durasi': '8 jam 20 menit',
        'tanggal_dibuat': '18/03/24',
        'deskripsi': 'Lorem Ipsum ...',
        'daftar_lagu': [
            {'judul': 'Song1', 'artis': 'Artist1', 'durasi': '2 menit'},
            {'judul': 'Song2', 'artis': 'Artist2', 'durasi': '3 menit'},
            {'judul': 'Song3', 'artis': 'Artist3', 'durasi': '4 menit'}
        ]
    }
    return render(request, 'crud_kelola_podcast.html', context)

def lihat_chart_view(request):
    chart_data = [
        {"title": "Actions Daily Top 20", "url": "chart_detail.html"},
        {"title": "Weekly Top 20", "url": "chart_detail.html"},
        # Add more chart data as needed
    ]
    return render(request, 'lihat_chart.html', {'chart_data': chart_data})


#Done first
def r_podcast_view(request, podcast_id):
    podcast_data = {}

    with connections['default'].cursor() as cursor:
        # Mengatur schema database
        cursor.execute("SET search_path TO marmut;")
        
        # Mengambil data podcast berdasarkan podcast_id
        cursor.execute("""
            SELECT p.id_konten, u.nama, p.email_podcaster
            FROM podcast p
            JOIN users u ON p.email_podcaster = u.email
            WHERE p.id_konten = %s;
        """, [podcast_id])
        podcast = cursor.fetchone()

        if podcast:
            podcast_data['id_konten'] = podcast[0]
            podcast_data['podcaster'] = podcast[1]
            podcast_data['email_podcaster'] = podcast[2]

            # Mengambil data episode yang terkait dengan id_konten
            cursor.execute("""
                SELECT e.judul, e.deskripsi, e.durasi, e.tanggal_rilis
                FROM episode e
                WHERE e.id_konten_podcast = %s;
            """, [podcast_data['id_konten']])
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

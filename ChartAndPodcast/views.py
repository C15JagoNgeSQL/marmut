from django.shortcuts import render

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


def r_podcast_view(request):
    podcast_data = {
        'judul': 'The Daily',
        'genres': ['Comedy', 'Motivation'],
        'podcaster': 'Jeffrey Mitchell',
        'durasi': '8 jam 20 menit',
        'tanggal_rilis': '18/03/24',
        'tahun': '2024',
        'episodes': [
            {
                'judul_episode': 'The Power of Positive Thinking',
                'deskripsi': 'Join us as we explore the transformative effects of maintaining a positive mindset in our daily lives',
                'durasi': '24 menit',
                'tanggal': '30/06/2021'
            },
            {
                'judul_episode': 'Journey Through Ancient Civilizations',
                'deskripsi': 'Embark on a captivating journey through the ruins and relics of ancient civilizations as we unravel their mysteries',
                'durasi': '1 jam 43 menit',
                'tanggal': '01/10/2019'
            }
        ]
    }
    return render(request, 'r_podcast.html', {'podcast_data': podcast_data})
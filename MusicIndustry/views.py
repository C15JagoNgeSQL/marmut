from django.shortcuts import render

# Create your views here.

def show_royalti(request):
    context = {
        'nama': "Taylor Swift",
        'email': "taylorswift@gmail.com",
        'total_keseluruhan_play': 999999,
        'total_keseluruhan_download': 100000,  # Added comma here
        'isi_tabel': [
            {
                'judul_lagu': "I Can Do It With A Broken Heart",
                'judul_album': "The Tortured Poets Department",
                'total_play': 50000,
                'total_download': 1000,
                'total_royalti_didapat': 1000000
            },
            {
                'judul_lagu': "I Can Do It With A Broken Heart",
                'judul_album': "The Tortured Poets Department",
                'total_play': 50000,
                'total_download': 1000,
                'total_royalti_didapat': 1000000
            },
            {
                'judul_lagu': "I Can Do It With A Broken Heart",
                'judul_album': "The Tortured Poets Department",
                'total_play': 50000,
                'total_download': 1000,
                'total_royalti_didapat': 1000000
            },
            {
                'judul_lagu': "I Can Do It With A Broken Heart",
                'judul_album': "The Tortured Poets Department",
                'total_play': 50000,
                'total_download': 1000,
                'total_royalti_didapat': 1000000
            },
            {
                'judul_lagu': "I Can Do It With A Broken Heart",
                'judul_album': "The Tortured Poets Department",
                'total_play': 50000,
                'total_download': 1000,
                'total_royalti_didapat': 1000000
            }
        ]
    }
    return render(request, "cek_royalti.html", context)
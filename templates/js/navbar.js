// // Mock data for user state and role
// const user = {
//     isLoggedIn: true,
//     role: 'artist', // Can be 'biasa', 'artist', 'songwriter', 'podcaster', 'label', 'premium'
// };

// function setupNavbar() {
//     const navbarGuest = document.getElementById('navbar-guest');
//     const navbarUser = document.getElementById('navbar-user');

//     if (user.isLoggedIn) {
//         navbarGuest.style.display = 'none';
//         navbarUser.style.display = 'flex';

//         const role = user.role;

//         // Show elements based on role
//         if (['biasa', 'artist', 'songwriter', 'podcaster'].includes(role)) {
//             document.querySelectorAll('.chart, .search-bar, .kelola-playlist, .langganan-paket').forEach(el => el.style.display = 'block');
//         }
//         if (role === 'premium') {
//             document.querySelector('.kelola-downloaded-songs').style.display = 'block';
//         }
//         if (role === 'podcaster') {
//             document.querySelector('.kelola-podcast').style.display = 'block';
//         }
//         if (['artist', 'songwriter'].includes(role)) {
//             document.querySelector('.kelola-album-songs').style.display = 'block';
//         }
//         if (role === 'label') {
//             document.querySelector('.kelola-album').style.display = 'block';
//         }
//         if (['artist', 'songwriter', 'label'].includes(role)) {
//             document.querySelector('.cek-royalti').style.display = 'block';
//         }
//     } else {
//         navbarGuest.style.display = 'flex';
//         navbarUser.style.display = 'none';
//     }
// }

// setupNavbar();

// ==========================================
// 1. INITIALIZATION & USER ONBOARDING
// ==========================================

document.addEventListener('DOMContentLoaded', () => {
    const savedName = localStorage.getItem('cinevibe_name');
    const savedMood = localStorage.getItem('cinevibe_mood');

    if (savedName && savedMood) {
        document.getElementById('welcome-screen').style.display = 'none';
        setupUserProfile(savedName, savedMood);
    } else {
        document.body.classList.add('no-scroll');
    }
    renderWishlist();
});

function enterSite() {
    const nameInput = document.getElementById('userNameInput').value.trim();
    const moodInput = document.getElementById('userMoodInput').value;
    const name = nameInput || "Guest";
    
    localStorage.setItem('cinevibe_name', name);
    localStorage.setItem('cinevibe_mood', moodInput);

    const welcomeScreen = document.getElementById('welcome-screen');
    welcomeScreen.classList.add('fade-out-welcome');
    
    setTimeout(() => {
        welcomeScreen.style.display = 'none';
        document.body.classList.remove('no-scroll');
        setupUserProfile(name, moodInput);
    }, 1000);
}

function setupUserProfile(name, mood) {
    // UI Avatars with Emerald Background (#10b981)
    const avatarUrl = `https://ui-avatars.com/api/?name=${encodeURIComponent(name)}&background=10b981&color=fff&bold=true`;
    document.getElementById('userAvatar').src = avatarUrl;
    document.getElementById('sidebarAvatar').src = avatarUrl;
    document.getElementById('sidebarName').innerText = name;
    document.getElementById('sidebarMood').innerText = `Vibe: ${mood}`;
    loadPersonalizedMovies(mood);
}

// ==========================================
// 2. PROFILE SIDEBAR & WISHLIST LOGIC
// ==========================================

function toggleProfile() {
    const sidebar = document.getElementById('profileSidebar');
    sidebar.classList.toggle('translate-x-full');
}

function addToWishlist(title, posterUrl) {
    let wishlist = JSON.parse(localStorage.getItem('cinevibe_wishlist')) || [];
    if (!wishlist.some(m => m.title === title)) {
        wishlist.push({ title, posterUrl });
        localStorage.setItem('cinevibe_wishlist', JSON.stringify(wishlist));
        alert(`❤️ Added "${title}" to your Wishlist!`);
        renderWishlist();
    } else {
        alert(`"${title}" is already in your Wishlist!`);
    }
}

function renderWishlist() {
    const container = document.getElementById('wishlistContainer');
    const wishlist = JSON.parse(localStorage.getItem('cinevibe_wishlist')) || [];
    if (wishlist.length === 0) {
        container.innerHTML = `<p class="text-sm text-gray-500 italic text-center mt-4">No movies added yet.</p>`;
        return;
    }
    container.innerHTML = wishlist.map(movie => `
        <div class="flex items-center bg-slate-800 p-2 rounded-lg border border-slate-700 hover:border-emerald-500 transition cursor-pointer">
            <img src="${movie.posterUrl}" onerror="this.src='https://placehold.co/100x150/1e293b/10b981?text=Movie'" class="w-12 h-16 object-cover rounded shadow">
            <span class="ml-3 font-bold text-white text-sm flex-1">${movie.title}</span>
        </div>
    `).join('');
}

function clearWishlist() {
    localStorage.removeItem('cinevibe_wishlist');
    renderWishlist();
}

// ==========================================
// 3. MOOD AI & PERSONALIZED ROW
// ==========================================

async function loadPersonalizedMovies(mood) {
    const res = await fetch('/api/mood', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mood: mood })
    });
    const data = await res.json();
    const container = document.getElementById('personalizedContainer');
    document.getElementById('personalizedRow').classList.remove('hidden');

    container.innerHTML = data.movies.map(movie => `
        <div class="min-w-[220px] max-w-[220px] bg-slate-900 rounded-xl relative movie-card group">
            <img src="${movie.poster}" onerror="this.src='https://placehold.co/500x750/1e293b/10b981?text=${encodeURIComponent(movie.title)}'" class="w-full h-80 object-cover rounded-xl shadow-lg cursor-pointer" onclick="openTrailer('${movie.trailer}')">
            <div class="absolute top-3 right-3 bg-black/60 backdrop-blur-md px-2 py-1 rounded-md text-xs text-yellow-400 font-bold border border-yellow-500/30">⭐ ${movie.rating}</div>
            <button onclick="addToWishlist('${movie.title}', '${movie.poster}')" class="absolute top-3 left-3 bg-black/60 backdrop-blur-md p-2 rounded-full text-white hover:text-red-500 border border-white/20 opacity-0 group-hover:opacity-100 transition z-30">
                <i class="ph-fill ph-heart text-xl"></i>
            </button>
            <div class="movie-info absolute bottom-0 left-0 right-0 p-4 rounded-b-xl pointer-events-none">
                <h4 class="font-bold text-md text-white drop-shadow-lg">${movie.title}</h4>
                <p class="text-xs text-emerald-300">⭐ ${movie.rating}</p>
            </div>
        </div>
    `).join('');
}

async function getMood(moodStr) {
    const res = await fetch('/api/mood', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mood: moodStr })
    });
    const data = await res.json();
    const container = document.getElementById('moodResults');
    container.innerHTML = data.movies.map(movie => `
        <div class="min-w-[180px] bg-slate-800 rounded-xl relative movie-card" onclick="openTrailer('${movie.trailer}')">
            <img src="${movie.poster}" onerror="this.src='https://placehold.co/500x750/1e293b/10b981?text=${encodeURIComponent(movie.title)}'" class="w-full h-64 object-cover rounded-xl shadow-lg">
            <div class="absolute bottom-0 w-full bg-black/80 p-3 text-center text-sm rounded-b-xl font-bold">${movie.title}</div>
        </div>
    `).join('');
}

// ==========================================
// 4. ML SENTIMENT REVIEW ENGINE
// ==========================================

let currentBaseRating = 4.5;
const reviewMovieDropdown = document.getElementById('reviewMovie');
if (reviewMovieDropdown) {
    reviewMovieDropdown.addEventListener('change', (e) => {
        document.getElementById('simulatedMovieName').innerText = e.target.value;
        currentBaseRating = 4.5;
        document.getElementById('liveRating').innerText = currentBaseRating.toFixed(1);
        document.getElementById('sentimentResult').innerHTML = "Awaiting Review...";
        document.getElementById('liveRating').className = "text-6xl font-black text-yellow-400 mb-2 transition-all duration-700";
    });
}

async function submitReview() {
    const text = document.getElementById('reviewText').value;
    if (!text) return alert("Please write a review first!");
    const res = await fetch('/api/analyze_review', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ review: text, base_rating: currentBaseRating })
    });
    const data = await res.json();
    const ratingElement = document.getElementById('liveRating');
    ratingElement.style.transform = "scale(1.5)";
    setTimeout(() => {
        ratingElement.innerText = data.new_rating.toFixed(1);
        currentBaseRating = data.new_rating;
        ratingElement.style.transform = "scale(1)";
        if (data.sentiment.includes('Positive')) {
            ratingElement.className = "text-6xl font-black text-emerald-400 mb-2 transition-all duration-300";
        } else if (data.sentiment.includes('Negative')) {
            ratingElement.className = "text-6xl font-black text-red-500 mb-2 transition-all duration-300";
        } else {
            ratingElement.className = "text-6xl font-black text-yellow-400 mb-2 transition-all duration-300";
        }
    }, 300);
    const changeText = data.change > 0 ? `+${data.change}` : data.change;
    document.getElementById('sentimentResult').innerHTML = `
        <span class="${data.color.replace('green', 'emerald')} font-bold text-lg">${data.sentiment}</span> <br> 
        <span class="text-xs text-gray-400">(Rating adjusted by ${changeText})</span>`;
    document.getElementById('reviewText').value = '';
}

// ==========================================
// 5. LIVE SEARCH FUNCTIONALITY
// ==========================================

async function searchMovie() {
    const query = document.getElementById('searchInput').value;
    const resultsDiv = document.getElementById('searchResults');
    const sections = document.getElementById('mainSections');
    if (query.length < 2) {
        resultsDiv.classList.add('hidden');
        sections.classList.remove('hidden');
        return;
    }
    const res = await fetch('/api/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: query })
    });
    const data = await res.json();
    sections.classList.add('hidden');
    resultsDiv.classList.remove('hidden');
    if(data.movies.length === 0) {
        resultsDiv.innerHTML = `<h3 class="text-2xl text-gray-400 mt-10 text-center w-full">No movies found 🥺</h3>`;
        return;
    }
    resultsDiv.innerHTML = `
        <h3 class="text-2xl font-bold mb-6 text-emerald-400 border-b border-emerald-900 pb-2">Search Results ✦</h3>
        <div class="grid grid-cols-2 md:grid-cols-5 gap-6">
            ${data.movies.map(movie => `
                <div class="bg-slate-800 rounded-xl relative movie-card" onclick="openTrailer('${movie.trailer}')">
                    <img src="${movie.poster}" onerror="this.src='https://placehold.co/500x750/1e293b/10b981?text=${encodeURIComponent(movie.title)}'" class="w-full h-64 object-cover rounded-xl">
                    <div class="absolute top-2 right-2 bg-black/80 px-2 py-1 rounded text-xs text-yellow-400 font-bold backdrop-blur-sm">⭐ ${movie.rating}</div>
                    <div class="p-3 text-center text-sm font-semibold">${movie.title}</div>
                </div>
            `).join('')}
        </div>
    `;
}

// ==========================================
// 6. AI CHATBOT LOGIC
// ==========================================

function toggleChat() {
    const chat = document.getElementById('chat-window');
    chat.classList.toggle('hidden');
    chat.classList.toggle('flex');
}

function handleChatEnter(e) {
    if (e.key === 'Enter') sendMessage();
}

async function sendMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    if (!message) return;
    const chatBox = document.getElementById('chat-messages');
    chatBox.innerHTML += `
        <div class="flex justify-end mb-3">
            <div class="bg-emerald-600 text-white p-2 rounded-xl rounded-br-none max-w-[80%] text-sm shadow-md">${message}</div>
        </div>
    `;
    input.value = '';
    chatBox.scrollTop = chatBox.scrollHeight;
    const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: message })
    });
    const data = await res.json();
    setTimeout(() => {
        chatBox.innerHTML += `
            <div class="flex justify-start mb-3">
                <div class="bg-slate-700 text-emerald-100 p-3 rounded-xl rounded-bl-none max-w-[85%] text-sm shadow-md border border-slate-600">
                    <span class="text-emerald-400 mr-1">✦</span> ${data.reply}
                </div>
            </div>
        `;
        chatBox.scrollTop = chatBox.scrollHeight;
    }, 400);
}

// ==========================================
// 7. UI CONTROLS
// ==========================================

window.addEventListener('scroll', () => {
    const nav = document.getElementById('navbar');
    if (window.scrollY > 50) {
        nav.classList.add('bg-[#020617]', 'shadow-lg', 'shadow-emerald-900/20');
        nav.classList.remove('bg-transparent');
    } else {
        nav.classList.remove('bg-[#020617]', 'shadow-lg', 'shadow-emerald-900/20');
        nav.classList.add('bg-transparent');
    }
});

function openTrailer(url) {
    const autoPlayUrl = url.includes('?') ? url + '&autoplay=1' : url + '?autoplay=1';
    document.getElementById('trailerFrame').src = autoPlayUrl;
    document.getElementById('trailerModal').classList.remove('hidden');
    document.getElementById('trailerModal').classList.add('flex');
}

function closeTrailer() {
    document.getElementById('trailerModal').classList.add('hidden');
    document.getElementById('trailerModal').classList.remove('flex');
    document.getElementById('trailerFrame').src = "";
}

function logout() {
    if (confirm("Reset profile and start over?")) {
        localStorage.clear();
        window.location.reload();
    }
}
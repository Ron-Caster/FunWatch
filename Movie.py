<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Movie Stream Hub</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #7e22ce 0%, #4c1d95 100%);
            min-height: 100vh;
        }
        
        .movie-card {
            transition: all 0.3s ease;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
        }
        
        .movie-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2);
        }
        
        .movie-poster {
            aspect-ratio: 2/3;
            object-fit: cover;
        }
        
        .search-input:focus {
            box-shadow: 0 0 0 2px rgba(124, 58, 237, 0.5);
        }
        
        .spinner {
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .gradient-text {
            background-clip: text;
            -webkit-background-clip: text;
            color: transparent;
        }
    </style>
</head>
<body class="text-white">
    <div class="min-h-screen p-4 flex flex-col items-center">
        <!-- Header with search -->
        <div class="w-full max-w-4xl bg-white p-6 rounded-xl shadow-2xl mb-8 flex flex-col md:flex-row items-center justify-between gap-4">
            <h1 class="text-3xl md:text-4xl font-extrabold gradient-text bg-gradient-to-r from-purple-600 to-indigo-700">
                <i class="fas fa-film mr-2"></i>Movie Stream Hub
            </h1>
            <div class="flex w-full md:w-auto flex-grow gap-2">
                <input 
                    type="text" 
                    id="searchInput"
                    class="flex-grow p-3 border border-gray-300 rounded-lg focus:outline-none search-input text-gray-800 transition duration-200"
                    placeholder="Search for movies..."
                    aria-label="Search movie title"
                />
                <button 
                    id="searchBtn"
                    class="bg-gradient-to-r from-purple-600 to-indigo-700 text-white font-bold py-3 px-5 rounded-lg shadow-md hover:from-purple-700 hover:to-indigo-800 focus:outline-none focus:ring-2 focus:ring-purple-500 transition-all duration-300"
                >
                    <i class="fas fa-search mr-2"></i>Search
                </button>
            </div>
        </div>
        
        <!-- Message display -->
        <div id="messageContainer" class="hidden text-center p-3 rounded-lg text-sm font-medium w-full max-w-4xl mb-4"></div>
        
        <!-- Loading indicator -->
        <div id="loadingIndicator" class="hidden items-center justify-center py-8">
            <div class="spinner rounded-full h-12 w-12 border-b-4 border-white"></div>
            <p class="ml-4 text-white text-lg">Loading movies...</p>
        </div>
        
        <!-- Movie grid -->
        <div id="movieGrid" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6 w-full max-w-6xl pb-8"></div>
        
        <!-- Pagination -->
        <div id="paginationContainer" class="hidden flex justify-center items-center gap-4 mt-8 pb-8">
            <button id="prevBtn" class="bg-purple-600 text-white py-2 px-4 rounded-lg shadow-md hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200">
                <i class="fas fa-chevron-left mr-2"></i>Previous
            </button>
            <span id="pageInfo" class="text-lg font-bold text-white">
                Page 1 of 1
            </span>
            <button id="nextBtn" class="bg-purple-600 text-white py-2 px-4 rounded-lg shadow-md hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200">
                Next<i class="fas fa-chevron-right ml-2"></i>
            </button>
        </div>
        
        <!-- Footer note -->
        <p class="text-center text-gray-300 text-xs mt-8 pb-4">
            <i class="fas fa-info-circle mr-1"></i>Note: This application opens links from external services. Ensure you have the necessary rights to access content.
        </p>
    </div>

    <script>
        // Configuration
        const TMDB_API_KEY = '7776fd096ce45cbc60f77d02684813df';
        const TMDB_BASE_URL = 'https://api.themoviedb.org/3';
        const TMDB_IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500';
        const OMDB_API_KEY = '8879697a';
        
        // State
        let movies = [];
        let searchQuery = '';
        let currentPage = 1;
        let totalPages = 1;
        let isLoading = false;
        
        // DOM Elements
        const searchInput = document.getElementById('searchInput');
        const searchBtn = document.getElementById('searchBtn');
        const messageContainer = document.getElementById('messageContainer');
        const loadingIndicator = document.getElementById('loadingIndicator');
        const movieGrid = document.getElementById('movieGrid');
        const paginationContainer = document.getElementById('paginationContainer');
        const prevBtn = document.getElementById('prevBtn');
        const nextBtn = document.getElementById('nextBtn');
        const pageInfo = document.getElementById('pageInfo');
        
        // Event Listeners
        searchBtn.addEventListener('click', performSearch);
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') performSearch();
        });
        prevBtn.addEventListener('click', () => {
            currentPage = Math.max(1, currentPage - 1);
            fetchMovies();
        });
        nextBtn.addEventListener('click', () => {
            currentPage = Math.min(totalPages, currentPage + 1);
            fetchMovies();
        });
        
        // Initial load
        fetchMovies();
        
        // Functions
        async function fetchMovies() {
            isLoading = true;
            showLoading();
            clearMessage();
            
            let url;
            if (searchQuery) {
                url = `${TMDB_BASE_URL}/search/movie?api_key=${TMDB_API_KEY}&query=${encodeURIComponent(searchQuery)}&page=${currentPage}`;
            } else {
                url = `${TMDB_BASE_URL}/movie/popular?api_key=${TMDB_API_KEY}&page=${currentPage}`;
            }
            
            try {
                const response = await fetch(url);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();
                
                if (data.results && data.results.length > 0) {
                    movies = data.results;
                    totalPages = data.total_pages;
                    renderMovies();
                    updatePagination();
                } else {
                    showMessage(searchQuery ? `No movies found for "${searchQuery}".` : 'No popular movies found.', 'error');
                    movieGrid.innerHTML = '';
                    paginationContainer.classList.add('hidden');
                }
            } catch (error) {
                console.error('Error fetching movies:', error);
                showMessage('An error occurred while fetching movies. Please check your network connection.', 'error');
                movieGrid.innerHTML = '';
                paginationContainer.classList.add('hidden');
            } finally {
                isLoading = false;
                hideLoading();
            }
        }
        
        function performSearch() {
            searchQuery = searchInput.value.trim();
            currentPage = 1;
            fetchMovies();
        }
        
        async function openMovieLink(movie) {
            showMessage(`Preparing to open link for "${movie.title || movie.name}"...`, 'info');
            showLoading();
            
            let imdbId = movie.imdb_id;
            
            if (!imdbId) {
                try {
                    const omdbUrl = `https://www.omdbapi.com/?t=${encodeURIComponent(movie.title || movie.name)}&apikey=${OMDB_API_KEY}`;
                    const response = await fetch(omdbUrl);
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    const data = await response.json();
                    
                    if (data.Response === 'True' && data.imdbID) {
                        imdbId = data.imdbID;
                    } else {
                        showMessage(`Could not find IMDb ID for "${movie.title || movie.name}". Cannot stream.`, 'error');
                        hideLoading();
                        return;
                    }
                } catch (error) {
                    console.error('Error fetching IMDb ID from OMDb:', error);
                    showMessage('An error occurred while getting movie details for streaming.', 'error');
                    hideLoading();
                    return;
                }
            }
            
            if (imdbId) {
                const streamingLink = `https://vidsrc.net/embed/${imdbId}`;
                window.open(streamingLink, '_blank');
                showMessage(`Opened streaming link for "${movie.title || movie.name}".`, 'success');
            } else {
                showMessage(`Cannot stream "${movie.title || movie.name}" without an IMDb ID.`, 'error');
            }
            hideLoading();
        }
        
        function renderMovies() {
            movieGrid.innerHTML = movies.map(movie => {
                const posterUrl = movie.poster_path 
                    ? `${TMDB_IMAGE_BASE_URL}${movie.poster_path}`
                    : `https://placehold.co/200x300/6A0DAD/ffffff?text=No+Poster`;
                
                const releaseYear = movie.release_date 
                    ? new Date(movie.release_date).getFullYear() 
                    : '';
                
                return `
                    <div class="movie-card bg-white rounded-lg overflow-hidden cursor-pointer" 
                         onclick="openMovieLink(${JSON.stringify(movie).replace(/"/g, '&quot;')})">
                        <img src="${posterUrl}" 
                             alt="${movie.title || movie.name}" 
                             class="w-full movie-poster rounded-t-lg hover:opacity-90 transition-opacity duration-200"
                             onerror="this.onerror=null;this.src='https://placehold.co/200x300/6A0DAD/ffffff?text=Image+Error'">
                        <div class="p-3">
                            <h3 class="text-lg font-semibold text-gray-900 hover:text-purple-700 transition-colors duration-200 text-center">
                                ${movie.title || movie.name}
                            </h3>
                            ${releaseYear ? `<p class="text-gray-600 text-sm text-center mt-1">(${releaseYear})</p>` : ''}
                        </div>
                    </div>
                `;
            }).join('');
        }
        
        function updatePagination() {
            if (totalPages > 1) {
                paginationContainer.classList.remove('hidden');
                pageInfo.textContent = `Page ${currentPage} of ${totalPages}`;
                prevBtn.disabled = currentPage === 1;
                nextBtn.disabled = currentPage === totalPages;
            } else {
                paginationContainer.classList.add('hidden');
            }
        }
        
        function showMessage(message, type) {
            messageContainer.textContent = message;
            messageContainer.className = `text-center p-3 rounded-lg text-sm font-medium w-full max-w-4xl mb-4 ${
                type === 'error' ? 'bg-red-100 text-red-700' : 
                type === 'info' ? 'bg-blue-100 text-blue-700' : 
                'bg-green-100 text-green-700'
            }`;
            messageContainer.classList.remove('hidden');
        }
        
        function clearMessage() {
            messageContainer.classList.add('hidden');
        }
        
        function showLoading() {
            loadingIndicator.classList.remove('hidden');
            searchBtn.disabled = true;
            prevBtn.disabled = true;
            nextBtn.disabled = true;
        }
        
        function hideLoading() {
            loadingIndicator.classList.add('hidden');
            searchBtn.disabled = false;
            prevBtn.disabled = currentPage === 1;
            nextBtn.disabled = currentPage === totalPages;
        }
    </script>
</body>
</html>

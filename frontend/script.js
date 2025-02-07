// Function to toggle between Login and Register form
function toggleAuthForm() {
    const authActionButton = document.getElementById('auth-action');
    const toggleText = document.getElementById('toggle-text');
    
    // If it's showing login, switch to register
    if (authActionButton.innerText === "Login") {
        authActionButton.innerText = "Register";
        toggleText.innerHTML = "Already have an account? <a href='javascript:void(0);' onclick='toggleAuthForm()'>Login</a>";
    } else {
        // If it's showing register, switch to login
        authActionButton.innerText = "Login";
        toggleText.innerHTML = "Don't have an account? <a href='javascript:void(0);' onclick='toggleAuthForm()'>Register</a>";
    }
}

// Function to handle both login and registration based on button text
async function handleAuth() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    // Ensure both fields are filled
    if (!username || !password) {
        alert("Please fill out both username and password fields.");
        return;
    }
    
    // Check if the user is trying to log in or register
    if (document.getElementById('auth-action').innerText === "Login") {
        // Handle Login
        await login(username, password);
    } else {
        // Handle Registration
        await register(username, password);
    }
}

// Function to log in and store session
async function login(username, password) {
    try {
        const response = await axios.post('http://127.0.0.1:5000/login', {
            username: username,
            password: password
        });
        alert(response.data.message);
        localStorage.setItem('loggedIn', true); // Store login status in localStorage
        document.getElementById('main-section').classList.remove('hidden');  // Show the main section
        document.getElementById('auth-section').classList.add('hidden');     // Hide auth section
        get_games();  // Load games after successful login
    } catch (error) {
        console.error('Error logging in:', error);
        alert('Login failed');
    }
}

// Function to handle user registration
async function register(username, password) {
    try {
        const response = await axios.post('http://127.0.0.1:5000/register', {
            username: username,
            password: password
        });

        // Register and automatically log the user in
        alert(response.data.message);
        localStorage.setItem('loggedIn', true);  // Store login status
        document.getElementById('main-section').classList.remove('hidden');  // Show the main section
        document.getElementById('auth-section').classList.add('hidden');     // Hide auth section
        get_games();  // Load games after successful registration
    } catch (error) {
        console.error('Registration failed:', error);
        alert(error.response.data.error);  // Show error message if registration fails
    }
}

// Function to log out and clear session
async function logout() {
    try {
        await axios.post('http://127.0.0.1:5000/logout');
        alert('Logged out successfully');
        localStorage.removeItem('loggedIn'); // Clear login status
        document.getElementById('main-section').classList.add('hidden');  // Hide the main section
        document.getElementById('auth-section').classList.remove('hidden');  // Show auth section
    } catch (error) {
        console.error('Error logging out:', error);
        alert('Logout failed');
    }
}

// Function to get all games from the API (protected route)
async function get_games() {
    if (!localStorage.getItem('loggedIn')) {
        alert('You must log or register in first!');
        return;
    }

    try {
        const response = await axios.get('http://127.0.0.1:5000/games');
        const gamesList = document.getElementById('games-list');
        gamesList.innerHTML = ''; // Clear existing list

        response.data.games.forEach(game => {
            gamesList.innerHTML += `
                <div class="game-card">
                    <h3>${game.title}</h3>
                    <p>Genre: ${game.genre}</p>
                    <p>Price: ${game.price}</p>
                    <p>Quantity: ${game.quantity}</p>
                </div>
            `;
        });
    } catch (error) {
        console.error('Error fetching games:', error);
        alert('Failed to load games');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    if (localStorage.getItem('loggedIn')) {
        document.getElementById('main-section').classList.remove('hidden');
        document.getElementById('auth-section').classList.add('hidden');
        get_games();
    }
});

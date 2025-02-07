// Function to toggle between Login and Register form
function toggleAuthForm() {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const toggleText = document.getElementById('toggle-text');
    
    // Toggle visibility of the forms
    if (loginForm.classList.contains('hidden')) {
        loginForm.classList.remove('hidden');
        registerForm.classList.add('hidden');
        toggleText.innerHTML = "Don't have an account? <a href='javascript:void(0);' onclick='toggleAuthForm()'>Register</a>";
    } else {
        loginForm.classList.add('hidden');
        registerForm.classList.remove('hidden');
        toggleText.innerHTML = "Already have an account? <a href='javascript:void(0);' onclick='toggleAuthForm()'>Login</a>";
    }
}

function toggleToMain() {
    document.getElementById('auth-section').classList.add('hidden');
    document.getElementById('main-section').classList.remove('hidden');
}

// Function to handle both login and registration based on button text
async function handleAuth(action) {
    let username, password;
    if (action === 'login') {
        username = document.getElementById('username').value;
        password = document.getElementById('password').value;
    } else if (action === 'register') {
        username = document.getElementById('reg-username').value;
        password = document.getElementById('reg-password').value;
        const confirmPassword = document.getElementById('reg-password-confirm').value;

        if (password !== confirmPassword) {
            alert("Passwords don't match!");
            return;
        }
    }

    // Ensure both fields are filled
    if (!username || !password) {
        alert("Please fill out both username and password fields.");
        return;
    }

    if (action === 'login') {
        await login(username, password);
    } else {
        await register(username, password);
    }
}

// Function to log in and store session
async function login(username, password) {
    try {
        const response = await axios.post('http://127.0.0.1:5000/login', { username, password });
        alert(response.data.message);
        localStorage.setItem('loggedIn', true); 
        localStorage.setItem('username', username); 
        document.getElementById('main-section').classList.remove('hidden');
        document.getElementById('auth-section').classList.add('hidden');
        get_games();
    } catch (error) {
        console.error('Login failed:', error);
        alert('Login failed');
    }
}

// Function to handle user registration
async function register(username, password) {
    try {
        const response = await axios.post('http://127.0.0.1:5000/register', { username, password });
        alert(response.data.message);
        localStorage.setItem('loggedIn', true); 
        localStorage.setItem('username', username); 
        document.getElementById('main-section').classList.remove('hidden');
        document.getElementById('auth-section').classList.add('hidden');
        get_games();
    } catch (error) {
        console.error('Registration failed:', error);
        alert(error.response.data.error);
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

// Function to add a new game to the database (protected route)
async function add_game() {
    // Ensure that user is logged in
    if (localStorage.getItem('loggedIn') !== 'true') {
        alert('You must log in or register first!');
        return;
    }

    const title = document.getElementById('game-title').value;
    const genre = document.getElementById('game-genre').value;
    const price = document.getElementById('game-price').value;
    const quantity = document.getElementById('game-quantity').value;

    // Ensure all required fields are filled
    if (!title || !genre || !price || !quantity) {
        alert('Please fill out all the fields!');
        return;
    }

    try {
        await axios.post('http://127.0.0.1:5000/games', {
            title: title,
            genre: genre,
            price: price,
            quantity: quantity
        });

        // Clear form fields
        document.getElementById('game-title').value = '';
        document.getElementById('game-genre').value = '';
        document.getElementById('game-price').value = '';
        document.getElementById('game-quantity').value = '';

        // Refresh the games list
        get_games();

        alert('Game added successfully!');
    } catch (error) {
        console.error('Error adding game:', error);
        alert('Failed to add game');
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

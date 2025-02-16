
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
    //document.getElementById('main-section').classList.remove('hidden');
}

// Function to handle both login and registration based on button text
async function handleAuth() {
    //let username, password;
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Ensure both fields are filled
    if (!username || !password) {
        alert("Please fill out both username and password fields.");
        return;
    }

    await login(username, password);
}

// Function to log in and store session
async function login(username, password) {
    // if (document.getElementById('auth-section').classList = 'hidden'){
    //     document.getElementById('auth-section').classList.remove('hidden');
    // document.getElementById('main-section').classList.add('hidden');
    // }
    try {
        // Ensure the request body is correctly formatted
        const response = await axios.post(
            'http://127.0.0.1:5000/login', 
            { "username": username, 
            "password": password
        }
            //{ headers: { 'Content-Type': 'application/json' } } // Ensure the Content-Type is set to application/json
        );
        
        console.log(response);  // Check the response data and status
        alert(response.data.message);
        localStorage.setItem('loggedIn', true);
        toggleToMain();
        get_games();
        get_loaned_games();
    } catch (error) {
        console.error('Login failed:', error.response ? error.response.data : error);  // More detailed error info
        alert('Login failed');
    }
}



// // Function to handle user registration
// async function register(username, password) {
//     try {

//         const response = await axios.post('http://127.0.0.1:5500/register', { username, password });
//         alert('BOOM')
//         alert(response.data.message);
//         localStorage.setItem('loggedIn', true); 
//         localStorage.setItem('username', username); 
//         localStorage.setItem("password", password);
//         toggleToMain();
//         get_games();
//     } catch (error) {
//         console.error('Registration failed:', error);
//         alert(error.response.data.error);
//     }
// }

// Function to log out and clear session
async function logout() {
    try {
        await axios.post('http://127.0.0.1:5000/logout');
        alert('Logged out successfully');
        localStorage.setItem('loggedIn', false); // Clear login status
        document.getElementById('main-section').classList.add('hidden');  // Hide the main section
        document.getElementById('auth-section').classList.remove('hidden');  // Show auth section
    } catch (error) {
        console.error('Error logging out:', error);
        alert('Logout failed');
    }
}

// Function to add a new game to the database (protected route)
async function add_game() {
  //  Ensure that user is logged in
  if (localStorage.getItem('loggedIn') !== 'true') {
    alert('You must login first!');
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
        await axios.post('http://127.0.0.1:5000/add', {
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
        get_loaned_games();
        get_games();
        get_loaned_games();

        alert('Game added successfully!');
    } catch (error) {
        console.error('Error adding game:', error);
        alert('Failed to add game');
    }
}

async function delete_game() {
    if (localStorage.getItem('loggedIn') !== 'true') {
        alert('You must login first!');
        return;
    }

    const title = document.getElementById('delete-game-title').value;
    if (!title) {
        alert('Please write the name of the game!');
        return;
    }

    try {
        await axios.post('http://127.0.0.1:5000/delete', {
            title: title,
        });

        // Clear form fields
        document.getElementById('game-title').value = '';


        // Refresh the games list
        get_loaned_games();
        get_games();

        alert('Game deleted successfully!');
    } catch (error) {
        console.error('Error deleting game:', error);
        alert('Failed to delete game');
    }
}


// Function to get all games from the API (protected route)
async function get_games() {
    //document.getElementById('main-section').classList.remove('hidden');
    if (localStorage.getItem('loggedIn') !== 'true') {
        return;
    }

    try {
        const response = await axios.get('http://127.0.0.1:5000/games');
        const gamesList = document.getElementById('games-list');
        gamesList.innerHTML = ''; // Clear existing list

        response.data.games.forEach(game =>  {
            gamesList.innerHTML += `
                <div class="game-card">
                    <h3>${game.title}</h3>
                    <p>Genre: ${game.genre}</p>
                    <p>Price: ${game.price}</p>
                    <p>Quantity: ${game.quantity}</p>
                </div>
            `;
        });
        console.log(response.data.games);
    } catch (error) {
        console.error('Error fetching games:', error);
        alert('Failed to load games');
    }
}

async function get_loaned_games() {
    if (localStorage.getItem('loggedIn') !== 'true') {
        return;
    }

    try {
        const response = await axios.get('http://127.0.0.1:5000/loaned');
        const loansList = document.getElementById('loaned-games-list');
        loansList.innerHTML = ''; // Clear existing list

        // Filter games where loan_status is 1
        const loanedGames = response.data.games.filter(game => game.loan_status === true);

        loanedGames.forEach(game => {
            loansList.innerHTML += `
                <div class="game-card">
                    <h3>${game.title}</h3>
                    <p>Genre: ${game.genre}</p>
                    <p>Price: ${game.price}</p>
                    <p>Quantity: ${game.quantity}</p>
                </div>
            `;
        });

        console.log('Loaned games list:', loanedGames);
        console.log(loanedGames);
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
        get_loaned_games();
    }
});


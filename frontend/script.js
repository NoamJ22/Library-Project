// function to get all books from the API
async function get_games() {
    try {
        const response = await axios.get('http://127.0.0.1:5000/books');
        const booksList = document.getElementById('books-list');
        booksList.innerHTML = ''; // Clear existing list

        response.data.books.forEach(book => {
            booksList.innerHTML += `
                <div class="game-card">
                    <h3>${game.title}</h3>
                    <p>Author: ${game.genre}</p>
                    <p>Year: ${game.price}</p>
                    <p>Type: ${game.quantity}</p>
                </div>
            `;
        });
    } catch (error) {
        console.error('Error fetching games:', error);
        alert('Failed to load games');
    }
}

// function to add a new book to the database
async function add_game() {
    const title = document.getElementById('game-title').value;
    const genre = document.getElementById('game-genre').value;
    const price = document.getElementById('game-price').value;
    const quantity = document.getElementById('game-quantity').value;

    try {
        await axios.post('http://127.0.0.1:5000/books', {
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

        // Refresh the books list
        get_games();
        
        alert('Game added successfully!');
    } catch (error) {
        console.error('Error adding Game:', error);
        alert('Failed to add Game');
    }
}

// Load all books when page loads
document.addEventListener('DOMContentLoaded', get_games);
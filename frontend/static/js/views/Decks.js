export default class Decks {
    constructor(params) {
        this.params = params;
        document.title = "Decks Menu | SpaceReps";
    }

    async getHTML() {
        return `
            <header class="decks-menu">
            <h1 class="decks-menu-title">Decks Menu</h1>
            <nav class="decks-menu-options">
                <!-- insert decks menu options here -->
                <form>
                    <label for="userInput">Enter new deck name:</label>
                    <input type="text" id="userInput" />
                    <button type="button" id="submit-button">Submit</button>
                </form>
            </nav>
            </header>
        `;
    }
    
    async main() {
        async function load_decks() {
            try {
                const resp = await fetch('/api/decks', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });
                if (!resp.ok) {
                    throw new Error(`Failed to fetch decks: ${resp.status} ${resp.statusText}`);
                }
                return await resp.json();
            } catch (error) {
                return null;
            }
        }
        
        function add_new_deck_button(deck_name, target_nav) {
            let newButton = document.createElement('button');
            newButton.textContent = `${deck_name}`;
            newButton.addEventListener('click', function() {
                window.location.href += `${deck_name}`;
            })
            target_nav.appendChild(newButton);
        }
        
        function add_new_deck(formInputElement, target_nav) {
            let userInputValue = formInputElement.value;
            formInputElement.value = '';
        
            // Hit the POST /decks/{deck_name} endpoint to create a new blank deck
        
            add_new_deck_button(userInputValue, target_nav)
        }

        let decks = await load_decks();

        let decksMenuOptionsNav = document.querySelector(".decks-menu-options");
    
        // a button for each deck, each that routes to /decks/{deck_name}
        decks.decks.forEach(deck => {
            add_new_deck_button(deck.name, decksMenuOptionsNav)
        });
    
        // submit button and form submission use the name to create a new blank deck, then route to /decks/{deck_name}
        let submitButton = document.getElementById("submit-button");
        let userInput = document.getElementById("userInput");
    
        submitButton.addEventListener('click', function() {
            add_new_deck(userInput, decksMenuOptionsNav);
        })
    
        userInput.addEventListener('keydown', function (event) {
            if (event.key === 'Enter') {
                event.preventDefault();
    
                add_new_deck(userInput, decksMenuOptionsNav);
            }
        })
    }
}
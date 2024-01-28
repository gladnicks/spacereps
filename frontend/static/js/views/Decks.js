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

    async load_decks() {
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

    add_new_deck_button(deck_name, target_nav) {
        let newLink = document.createElement('a');
        newLink.href = window.location.href + `/${deck_name}`;

        let newButton = document.createElement('button');
        newButton.textContent = deck_name;

        newLink.appendChild(newButton)
        target_nav.appendChild(newLink);
    }

    add_new_deck_to_decks(deck_name) {
        fetch('/api/decks', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({name: deck_name}),
        });
    }

    handle_new_deck_form_submission(formInputElement, target_nav) {
        let userInputValue = formInputElement.value;
        if (userInputValue !== '') {
            formInputElement.value = '';
            this.add_new_deck_to_decks(userInputValue);
            this.add_new_deck_button(userInputValue, target_nav);
        }
    }
    
    async main() {
        let decks = await this.load_decks();

        let decksMenuOptionsNav = document.querySelector(".decks-menu-options");
    
        for (let deck_name in decks) {
            this.add_new_deck_button(deck_name, decksMenuOptionsNav);
        }
    
        let submitButton = document.getElementById("submit-button");
        let userInput = document.getElementById("userInput");

        submitButton.onclick = () => this.handle_new_deck_form_submission(userInput, decksMenuOptionsNav);
        userInput.onkeydown = (event) => {
            if (event.key === 'Enter') {
                event.preventDefault();
                this.handle_new_deck_form_submission(userInput, decksMenuOptionsNav);
            }
        };
    }
}
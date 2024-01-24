export default class Decks {
    constructor(params) {
        this.params = params;
        document.title = "View Deck | SpaceReps";
    }

    async getHTML() {
        return `
        <header class="deck-display">
        <h1 class="deck-display-title"></h1>

        <a class="study-button-link" href="">
            <button class="study-button">Study</button>
        </a>
        <button class="delete-deck-button"></button>
        </header>
        `;
    }

    async main() {
        const path = window.location.pathname;
        const paths = path.split("/");
        const deck_name = paths[paths.length - 1];
        document.querySelector('.deck-display-title').textContent = deck_name;

        document.querySelector('.study-button-link').href = window.location.pathname + '/study';

        let deleteDeckButton = document.querySelector('.delete-deck-button');
        deleteDeckButton.textContent = `Delete ${deck_name}`;

        deleteDeckButton.onclick = () => {
            if (deleteDeckButton.textContent === `Delete ${deck_name}`) {
                deleteDeckButton.textContent = 'Are you sure?'
            } else {
                fetch(`/api/decks/${deck_name}`, {
                    method: "DELETE",
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });
                let path_arr = window.location.href.split('/');
                window.location.href = path_arr.slice(0, path_arr.length-1).join('/');
            }
        }
    }
}
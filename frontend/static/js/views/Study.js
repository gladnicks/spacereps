export default class Study {
    constructor(params) {
        this.params = params;
        document.title = "Study Deck | SpaceReps";
    }

    async getHTML() {
        return `
        <header class="deck-study">
        <h1 class="deck-study-title"></h1>
        <p>
        This is where decks will be studied
        </p>
        </header>
        `;
    }

    async main() {
        javascript:void(0);
    }
}
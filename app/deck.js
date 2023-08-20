function main() {
    let urlQuery = window.location.search;
    let urlParams = new URLSearchParams(urlQuery);
    let deckName = urlParams.get('deck-name');
    let currentDeck;
    decks.decks.forEach(deck => {
        if (deck.name==deckName) {
            currentDeck = deck;
            return;
        }
    })

    let deckNameHeader = document.querySelector(".deck-name");
    deckNameHeader.textContent = deckName;
    
    let deckOptionsDiv = document.querySelector(".deck-options")
    let addButton = document.createElement('button');
    addButton.textContent = `Add to ${deckName}`;
    let studyButton = document.createElement('button');
    studyButton.textContent = `Study ${deckName}`;
    deckOptionsDiv.appendChild(addButton);
    deckOptionsDiv.appendChild(studyButton);

    let cardsDiv = document.querySelector(".cards");
    currentDeck.cards.forEach(card => {
        let cardParagraph = document.createElement('p');
        cardParagraph.textContent = JSON.stringify(card);
        cardsDiv.appendChild(cardParagraph);
    })
}

import { decks } from './decks.js';
main()

let decksMenuDiv = document.getElementById("decks-menu");

fetch('./decks.json')
.then(response => response.json())
.then(decks => {
    let content = `<button id=new-deck>New Deck</button>`;
    content += `<button id=quit-decks-menu>Quit</button>`;
    decks.decks.forEach(deck => {
        content += `<button id=${deck.name}>${deck.name}</button>`;
    })
    decksMenuDiv.innerHTML = content;
})
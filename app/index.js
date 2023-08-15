async function load_decks() {
    const resp = await fetch('http://localhost:9876/decks', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    }).then(data => data.json());

    return resp;
}

async function main() {
    let decksMenuDiv = document.getElementById("decks-menu");

    let content = `<button id=new-deck>New Deck</button>`;
    content += `<button id=quit-decks-menu>Quit</button>`;

    let decks = await load_decks();
    decks.decks.forEach(deck => {
        content += `<button id=${deck.name}>${deck.name}</button>`;
    });

    decksMenuDiv.innerHTML = content;
}

main();

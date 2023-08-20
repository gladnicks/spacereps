async function load_decks() {
    const resp = await fetch('http://localhost:9876/api/decks', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    }).then(data => data.json());

    return resp;
}

async function main() {
    let decks = await load_decks();

    let decksMenuOptionsNav = document.querySelector(".decks-menu-options");

    let newLink = document.createElement('a');
    newLink.href = 'decks/new-deck';
    newLink.textContent = 'New Deck';
    decksMenuOptionsNav.appendChild(newLink);
    decks.decks.forEach(deck => {
        let newLink = document.createElement('a');
        newLink.href = `decks/${deck.name}`;
        newLink.textContent = `${deck.name}`;
        decksMenuOptionsNav.appendChild(newLink);
    });
}

main();

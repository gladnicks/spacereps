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
    let decksMenuOptionsNav = document.querySelector(".decks-menu-options");

    let newLink = document.createElement('a');
    newLink.href = 'deck?deck-name=new-deck';
    newLink.textContent = 'New Deck';
    decksMenuOptionsNav.appendChild(newLink);
    decks.decks.forEach(deck => {
        let newLink = document.createElement('a');
        newLink.href = `deck?deck-name=${deck.name}`;
        newLink.textContent = `${deck.name}`;
        decksMenuOptionsNav.appendChild(newLink);
    });
}

export const decks = await load_decks();
main();

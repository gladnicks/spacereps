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

// try {
//     fetch('./decks.json')
//     .then(response => response.json())
//     .then(decks => {
//         let content = `<button id=new-deck>New Deck</button>`;
//         content += `<button id=quit-decks-menu>Quit</button>`;
//         decks.decks.forEach(deck => {
//             content += `<button id=${deck.name}>${deck.name}</button>`;
//         });
//         decksMenuDiv.innerHTML = content;
//     });
// } catch (ReferenceError) {
//     let decks = {
//         'decks': []
//     };
//     decks = JSON.stringify(decks);

//     fs.writeFile('./decks.json', decks, 'utf-8');

//     let content = `<button id=new-deck>New Deck</button>`;
//     content += `<button id=quit-decks-menu>Quit</button>`;
//     decksMenuDiv.innerHTML = content;
// }

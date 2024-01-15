async function load_decks() {
    const resp = await fetch('http://localhost:9876/api/decks', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    }).then(data => data.json());

    return resp;
}

function add_new_deck_button(deck_name, target_nav) {
    let newButton = document.createElement('button');
    newButton.textContent = `${deck_name}`;
    newButton.addEventListener('click', function() {
        window.location.href += `${deck_name}`;
    })
    target_nav.appendChild(newButton);
}

function add_new_deck(formInputElement) {
    let userInputValue = formInputElement.value;
    formInputElement.value = '';

    // Hit the POST /decks/{deck_name} endpoint to create a new blank deck

    add_new_deck_button(userInputValue, decksMenuOptionsNav)
}

async function main() {
    let decksMenuOptionsNav = document.querySelector(".decks-menu-options");

    // a button for each deck, each that routes to /decks/{deck_name}
    decks.decks.forEach(deck => {
        add_new_deck_button(deck.name, decksMenuOptionsNav)
    });

    // submit button and form submission use the name to create a new blank deck, then route to /decks/{deck_name}
    let submitButton = document.getElementById("submit-button");
    let userInput = document.getElementById("userInput");

    submitButton.addEventListener('click', function() {
        add_new_deck(userInput);
    })

    userInput.addEventListener('keydown', function (event) {
        if (event.key === 'Enter') {
            event.preventDefault();

            add_new_deck(userInput);
        }
    })

}

let decks = await load_decks();
export { decks };

main();

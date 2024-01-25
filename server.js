const express = require('express');
const path = require('path');
const fs = require('fs');

const app = express();

const DECKS_FILENAME = 'decks.json';

app.use(express.json());
app.use("/static", express.static(path.resolve(__dirname, "frontend", "static")));

app.get('/api/decks', (req, res) => {
    let decks_json;
    if (!fs.existsSync(DECKS_FILENAME)) {
        decks_json = {decks: []};
        fs.writeFileSync(DECKS_FILENAME, JSON.stringify(decks_json, null, 2), 'utf8');
    } else {
        const decks = fs.readFileSync(DECKS_FILENAME);
        decks_json = JSON.parse(decks);
    }
    res.status(200).json(decks_json);
});

app.post('/api/decks', (req, res) => {
    const deck = {name: req.body.name, cards: []};
    if (!fs.existsSync(DECKS_FILENAME)) {
        fs.writeFileSync(DECKS_FILENAME, JSON.stringify({decks: [deck]}, null, 2), 'utf8');
    } else {
        let decks = fs.readFileSync(DECKS_FILENAME);
        let decks_json = JSON.parse(decks);
        decks_json.decks.push(deck);
        fs.writeFileSync(DECKS_FILENAME, JSON.stringify(decks_json, null, 2), 'utf8');
    }
    res.status(200);
});

app.delete('/api/decks/:deck_name', (req, res) => {
    let decks = fs.readFileSync(DECKS_FILENAME);
    let decks_json = JSON.parse(decks);
    decks_json.decks = decks_json.decks.filter(deck => deck.name !== req.params.deck_name);
    fs.writeFileSync(DECKS_FILENAME, JSON.stringify(decks_json, null, 2), 'utf8');
    res.status(200);
});

app.get('/api/decks/:deck_name', (req, res) => {
    let decks = fs.readFileSync(DECKS_FILENAME);
    let decks_json = JSON.parse(decks);
    let myDeck;
    for (const deck of decks_json.decks) {
        if (deck.name === req.params.deck_name) {
            myDeck = deck;
            break;
        }
    }
    res.status(200).json(myDeck);
})

app.get('/*', (req, res) => {
    res.status(200).sendFile(path.resolve(__dirname, "frontend", "index.html"));
});

app.listen(process.env.PORT || 8080, () => console.log('Server running at localhost:8080'));
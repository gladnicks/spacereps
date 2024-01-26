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
        decks_json = {};
        fs.writeFileSync(DECKS_FILENAME, JSON.stringify(decks_json, null, 2), 'utf8');
    } else {
        const decks = fs.readFileSync(DECKS_FILENAME);
        decks_json = JSON.parse(decks);
    }
    res.status(200).json(decks_json);
});

app.post('/api/decks', (req, res) => {
    const deck_name = req.body.name;
    if (!fs.existsSync(DECKS_FILENAME)) {
        fs.writeFileSync(DECKS_FILENAME, JSON.stringify({[deck_name]: {}}, null, 2), 'utf8');
    } else {
        let decks = fs.readFileSync(DECKS_FILENAME);
        let decks_json = JSON.parse(decks);
        decks_json[deck_name] = {};
        fs.writeFileSync(DECKS_FILENAME, JSON.stringify(decks_json, null, 2), 'utf8');
    }
    res.status(200);
});

app.delete('/api/decks/:deck_name', (req, res) => {
    let decks = fs.readFileSync(DECKS_FILENAME);
    let decks_json = JSON.parse(decks);
    delete decks_json[req.params.deck_name];
    fs.writeFileSync(DECKS_FILENAME, JSON.stringify(decks_json, null, 2), 'utf8');
    res.status(200);
});

app.get('/api/decks/:deck_name', (req, res) => {
    const decks = fs.readFileSync(DECKS_FILENAME);
    const decks_json = JSON.parse(decks);
    const myDeck = decks_json[req.params.deck_name];
    res.status(200).json(myDeck);
})

app.get('/*', (req, res) => {
    res.status(200).sendFile(path.resolve(__dirname, "frontend", "index.html"));
});

app.listen(process.env.PORT || 8080, () => console.log('Server running at localhost:8080'));
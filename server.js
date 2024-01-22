const express = require('express');
const path = require('path');
const fs = require('fs');

const app = express();

app.use(express.json());
app.use("/static", express.static(path.resolve(__dirname, "frontend", "static")));

app.get('/api/decks', (req, res) => {
    const decks = fs.readFileSync('decks.json');
    const decks_json = JSON.parse(decks);
    res.status(200).json(decks_json);
})

app.post('/api/decks', (req, res) => {
    let decks = fs.readFileSync('decks.json');
    let decks_json = JSON.parse(decks);
    decks_json.decks.push({name: req.body.name, cards: []});
    fs.writeFileSync('decks.json', JSON.stringify(decks_json, null, 2), 'utf8');
    res.status(200);
})

app.get('/*', (req, res) => {
    res.status(200).sendFile(path.resolve(__dirname, "frontend", "index.html"));
});

app.listen(process.env.PORT || 8080, () => console.log('Server running at localhost:8080'));
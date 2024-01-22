const express = require('express');
const path = require('path');
const fs = require('fs');

const app = express();

app.use("/static", express.static(path.resolve(__dirname, "frontend", "static")));

app.get('/api/decks', (req, res) => {
    const decks = fs.readFileSync('decks.json');
    const decks_json = JSON.parse(decks);
    res.json(decks_json);
})

app.get('/*', (req, res) => {
    res.sendFile(path.resolve(__dirname, "frontend", "index.html"));
});

app.listen(process.env.PORT || 8080, () => console.log('Server running at localhost:8080'));
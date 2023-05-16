import json
from queue import Queue
from time import time

def main():
    # Load the decks from the JSON decks file
    with open("decks.json", "r+") as decks_file:
        decks = json.load(decks_file)
    
    # Ask user which deck they want to study and assign it to a variable
    print("Which deck would you like to study?")
    decks_menu = {}
    for i, (name, deck) in enumerate(decks.items()):
        print(f"{i}: {name}")
        decks_menu[i] = deck
    deck_choice = int(input())
    study_deck = decks_menu[deck_choice]

    # Add each card to the study queue if it's been at least I (spaced repetition interval) days since the last time the card was studied
    to_study = Queue()
    for card in study_deck['cards']:
        if time() >= card['I']*24*60*60 + card['last_studied']:
            to_study.put(card)
    
    # Loop over study queue until all of the cards are recalled with at least a memory score of 4
    while not to_study.empty():
        current = to_study.get()
        print(f"front of card:\n{current['front']}")
        input("[Enter] to show other side")
        print(f"back of card:\n{current['back']}")
        q = int(input("What would you rate your ease of remembering this card (0-5)? "))
        # TODO: update card metadata using SM2 algorithm here
        if q < 4:
            to_study.put(current)
    print("No more cards to study. Come back tomorrow!")

if __name__ == '__main__':
    main()
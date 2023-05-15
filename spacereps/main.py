import os
from queue import Queue
from time import time

def main():
    print("Which deck would you like to study?")
    for i, deck_name in enumerate(os.listdir('decks')):
        print(f"{i}: {deck_name}")
    deck_choice = input()
    with open(deck_choice, "r+") as deck:
        to_study = Queue()
        for card in deck['cards']:
            if time() >= card['I']*24*60*60 + card['last_studied']:
                to_study.put(card)
        while not to_study.empty():
            current = to_study.pop()
            print(f"front of card:\n{current['front']}")
            input("[Enter] to show other side")
            print(f"back of card:\n{current['back']}")
            q = input("What would you rate the difficulty of this card (0-5)? ")
            # update card metadata using SM2 algorithm
            if q < 4:
                to_study.put(current)
    print("No more cards to study. Come back tomorrow!")

if __name__ == '__main__':
    main()
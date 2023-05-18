import json
from queue import Queue
from time import time

def sm2(q: int, n: int, ef: float, i: int):
    """
    input:  q: The user grade for a card from 0-5
                0 - Complete failure to recall the information
                1 - Incorrect response, but upon seeing the correct answer it felt familiar
                2 - Incorrect response, but upon seeing the correct answer it seemed easy to remember
                3 - Correct response, but required significant effort to recall
                4 - Correct response, after some hesitation
                5 - Correct response with perfect recall
            n: Number of times the card has been successfully recalled (q >= 3) in a row since the last time it was not
            ef: A card's easiness factor
            i: Inter-repetition interval in days that the program will wait after the previous review before asking to review again
    output: Updated values of n, ef, and i
    """
    if q >= 3:
        if n == 0:
            mod_i = 1
        elif n == 1:
            mod_i = 6
        else:
            mod_i = round(i * ef)
        mod_n = n + 1
    else:
        mod_n = 0
        mod_i = 1
    
    mod_ef = ef + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
    if mod_ef < 1.3:
        mod_ef = 1.3

    return mod_n, mod_ef, mod_i

def main():
    # Load the decks from the JSON decks file
    with open("decks.json", "r") as decks_file:
        decks = json.load(decks_file)
    
    # Ask user which deck they want to work with and assign it to a variable
    print("Which deck would you like to study or add to?")
    for idx, deck in enumerate(decks['decks']):
        print(f"{idx}: {deck['name']}")
    deck_choice = int(input())
    study_deck = decks['decks'][deck_choice]
    # Ask whether you'd like to add to or study the deck
    mode = input("Would like to (a)dd to or (s)tudy this deck? ")

    # Add mode
    if mode == "a":
        want_to_quit = False
        while not want_to_quit:
            # Ask user to define front and back of new card, then add card to deck
            front = input("What should the front of this new card say?\n")
            back = input("What should the back of this new card say?\n")
            card = {
                "front": front,
                "back": back,
                "n": 0,
                "ef": 2.5,
                "i": 0,
                "last_studied": time()
            }
            decks['decks'][deck_choice]['cards'].append(card)
            want_to_quit = input("Press q to (q)uit, or any other key to add more cards ") == "q"
        # Update the decks json file
        with open("decks.json", "w") as updated_decks_file:
            json.dump(decks, updated_decks_file)
        print(f"{decks['decks'][deck_choice]['name']} has been successfully updated!")
    
    # Study mode
    elif mode == "s":
        # Add each card to the study queue if it's been at least I (spaced repetition interval) days since the last time the card was studied
        to_study = Queue()
        for index, card in enumerate(study_deck['cards']):
            if time() >= card['i']*24*60*60 + card['last_studied']:
                to_study.put((index, card))
        # Loop over study queue until all of the cards are recalled with at least a memory score of 4
        while not to_study.empty():
            current = to_study.get()
            current_idx = current[0]
            print(f"front of card:\n{current[1]['front']}")
            input("[Enter] to show other side")
            print(f"back of card:\n{current[1]['back']}")
            q = int(input("What would you rate your ease of remembering this card (0-5)? "))
            if q < 4:
                to_study.put(current)
            # Update card metadata
            last_studied = time()
            n, ef, i = sm2(q, current[1]['n'], current[1]['ef'], current[1]['i'])
            decks['decks'][deck_choice]['cards'][current_idx]['n'] = n
            decks['decks'][deck_choice]['cards'][current_idx]['ef'] = ef
            decks['decks'][deck_choice]['cards'][current_idx]['i'] = i
            decks['decks'][deck_choice]['cards'][current_idx]['last_studied'] = last_studied
        # Update the decks json file
        with open("decks.json", "w") as updated_decks_file:
            json.dump(decks, updated_decks_file)
        print("No more cards to study. Come back tomorrow!")
    
    # Invalid mode input
    else:
        print("Invalid input. Please enter either 'a' or 's'")

if __name__ == '__main__':
    main()

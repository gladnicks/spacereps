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


def add_to_deck(decks: dict, deck_choice: int):
    mod_decks = decks
    want_to_quit = False
    while not want_to_quit:
        # Ask user to define front and back of new card, then add card to deck
        front = input("\n\nWhat should the front of this new card say?\n")
        back = input("What should the back of this new card say?\n")
        card = {
            "front": front,
            "back": back,
            "n": 0,
            "ef": 2.5,
            "i": 0,
            "last_studied": time()
        }
        mod_decks['decks'][deck_choice]['cards'].append(card)
        want_to_quit = input("Press q to (q)uit, or any other key to add more cards ") == "q"
    print(f"{mod_decks['decks'][deck_choice]['name']} has been updated!")
    return mod_decks


def study_deck(decks: dict, deck_choice: int):
    mod_decks = decks
    # Add each card to the study queue if it's been at least I (spaced repetition interval) days since the last time the card was studied
    study_deck = mod_decks['decks'][deck_choice]
    to_study = Queue()
    for index, card in enumerate(study_deck['cards']):
        if time() >= card['i']*24*60*60 + card['last_studied']:
            to_study.put((index, card))
    # Loop over study queue until all of the cards are recalled with at least a memory score of 4
    while not to_study.empty():
        current = to_study.get()
        current_idx = current[0]
        print(f"\n\nfront of card:\n{current[1]['front']}")
        input("Press any key to show other side")
        print(f"back of card:\n{current[1]['back']}")
        q = int(input("What would you rate your ease of remembering this card (0-5)? "))
        if q < 4:
            to_study.put(current)
        # Update card metadata
        last_studied = time()
        n, ef, i = sm2(q, current[1]['n'], current[1]['ef'], current[1]['i'])
        mod_decks['decks'][deck_choice]['cards'][current_idx]['n'] = n
        mod_decks['decks'][deck_choice]['cards'][current_idx]['ef'] = ef
        mod_decks['decks'][deck_choice]['cards'][current_idx]['i'] = i
        mod_decks['decks'][deck_choice]['cards'][current_idx]['last_studied'] = last_studied
    print("No more cards to study. Come back tomorrow!")
    return mod_decks


def main():
    # Load the decks from the JSON decks file
    try:
        with open("decks.json", "r") as decks_file:
            decks = json.load(decks_file)
    # If it doesn't exist, create it
    except FileNotFoundError:
        with open("decks.json", "w"):
            decks = {
                "decks": []
            }
    
    if len(decks['decks']) == 0:
        print("\nYou have no decks yet! Please add at least one deck.")
        deck_choice = 0
    else:
        # Ask user which deck they want to work with and assign it to a variable
        print("\n-- Decks Menu --")
        for idx, deck in enumerate(decks['decks']):
            print(f"{idx}: {deck['name']}")
        print(f"{len(decks['decks'])}: New deck")
        deck_choice = int(input("Which deck? "))
    mode = None

    # Create a new deck if there aren't any or if the user has indicated they want to
    if deck_choice == len(decks['decks']):
        name = input("\nWhat is the name of your new deck? ")
        new_deck = {
            "name": name,
            "cards": []
        }
        decks['decks'].append(new_deck)
        print(f"Your new deck {name} has been created! Please add at least one card.")
        mode = "a"

    menu = {
        "a": add_to_deck,
        "s": study_deck,
    }

    if mode is None:
            print("\n-- Actions Menu --")
            for key, value in menu.items():
                print(f"{key}: {value.__name__.replace('_', ' ')}")
            print("q: quit")
            mode = input("Which action? ")

    while mode != "q":
        if mode == "q":
            break
        try:
            decks = menu[mode](decks, deck_choice)
        except KeyError:
            print("Invalid input. Please enter either 'a' or 's'")
        
        # Ask what the user would like to do
        print("\n-- Actions Menu --")
        for key, value in menu.items():
            print(f"{key}: {value.__name__.replace('_', ' ')}")
        print("q: quit")
        mode = input("Which action? ")
            
    # Update the decks json file
    with open("decks.json", "w") as updated_decks_file:
        json.dump(decks, updated_decks_file, indent=4)
    print("\nCome back soon!")

if __name__ == '__main__':
    main()

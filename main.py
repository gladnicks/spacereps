import json
from queue import Queue
from time import time


def sm2(q: int, n: int, ef: float, i: int):
    """
    Updates card metadata using the SuperMemo2 algorithm for spaced repitition

    Input:  q: The user grade for a card from 0-5
                0 - Complete failure to recall the information
                1 - Incorrect response, but upon seeing the correct answer it felt familiar
                2 - Incorrect response, but upon seeing the correct answer it seemed easy to remember
                3 - Correct response, but required significant effort to recall
                4 - Correct response, after some hesitation
                5 - Correct response with perfect recall
            n: Number of times the card has been successfully recalled (q >= 3) in a row since the last time it was not
            ef: A card's easiness factor
            i: Inter-repetition interval in days that the program will wait after the previous review before asking to review again

    Output: Updated values of n, ef, and i
    """
    if q >= 3:
        mod_n = n + 1
        mod_i = 1 if n == 0 else (6 if n == 1 else round(i * ef))
    else:
        mod_n = 0
        mod_i = 1
    mod_ef = max(1.3, ef + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02)))
    
    return mod_n, mod_ef, mod_i


def new_deck():
    """
    Returns a new blank deck with a name specified by the user

    Output: new blank deck
    """
    name = input("\nWhat is the name of your new deck? ")
    new_deck = {
        "name": name,
        "cards": []
    }
    print(f"Your new deck {name} has been created! Please add at least one card.")
    new_deck = add_to_deck(new_deck)
    return new_deck


def add_to_deck(deck: dict):
    """
    Allows the user to add cards to a given deck

    Input:  deck: the deck dictionary that the user wants to add to

    Output: the modified deck
    """
    mod_deck = deck
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
        mod_deck['cards'].append(card)
        want_to_quit = input("Press q to (q)uit, or any other key to add more cards ") == "q"
    print(f"{mod_deck['name']} has been updated!")
    return mod_deck


def study_deck(deck: dict):
    """
    Allows the user to study a given deck, updating each card's metadata as it's reviewed

    Input:  deck: the deck dictionary that the user wants to study

    Output: the deck with updated card metadata
    """
    mod_deck = deck
    # Add each card to the study queue if it's been at least I (spaced repetition interval) days since the last time the card was studied
    study_deck = mod_deck
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
        mod_deck['cards'][current_idx]['n'] = n
        mod_deck['cards'][current_idx]['ef'] = ef
        mod_deck['cards'][current_idx]['i'] = i
        mod_deck['cards'][current_idx]['last_studied'] = last_studied
    print("No more cards to study. Come back tomorrow!")
    return mod_deck


ACTIONS_MENU = {
    "a": add_to_deck,
    "s": study_deck,
}


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
    
    # If there are no decks yet, have the user create one
    if len(decks['decks']) == 0:
        print("\nYou have no decks yet! Please add at least one deck.")
        decks['decks'].append(new_deck())
    
    # Menus loop
    while True:
        # Decks menu loop
        while True:
            # Display decks menu
            print("\n-- Decks Menu --")
            for idx, deck in enumerate(decks['decks']):
                print(f"{idx}: {deck['name']}")
            print("n: new deck")
            print("q: quit")
            # Get user input to select a menu option
            decks_menu_selection = input("Which deck would you like to work with? ")
            try:
                decks_menu_selection = int(decks_menu_selection)
                if decks_menu_selection in range(len(decks['decks'])):
                    break
                else:
                    print("Invalid input. Please enter one of the menu options as displayed.")
            except ValueError:
                if decks_menu_selection == "n":
                    decks['decks'].append(new_deck())
                elif decks_menu_selection == "q":
                    break
                else:
                    print("Invalid input. Please enter one of the menu options as displayed.")
        if decks_menu_selection == "q":
            break
        
        # Actions menu loop
        while True:
            # Display actions menu
            print("\n-- Actions Menu --")
            for key, value in ACTIONS_MENU.items():
                print(f"{key}: {value.__name__.replace('_', ' ')}")
            print("r: return to decks menu")
            print("q: quit")
            # Get user input to select a menu option
            actions_menu_selection = input(f"Which action would you like to perform with {decks['decks'][decks_menu_selection]['name']}? ")
            try:
                # Perform the selected action to the selected deck
                decks['decks'][decks_menu_selection] = ACTIONS_MENU[actions_menu_selection](decks['decks'][decks_menu_selection])
            except KeyError:
                if actions_menu_selection == "r" or actions_menu_selection == "q":
                    break
                else:
                    print("Invalid input. Please enter one of the menu options as displayed.")
        if actions_menu_selection == "q":
            break
            
    # Update the decks json file
    with open("decks.json", "w") as updated_decks_file:
        json.dump(decks, updated_decks_file, indent=4)
    print("\nCome back soon!")

if __name__ == '__main__':
    main()

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
        mod_n = n + 1
        mod_i = 1 if n == 0 else (6 if n == 1 else round(i * ef))
    else:
        mod_n = 0
        mod_i = 1
    mod_ef = max(1.3, ef + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02)))
    
    return mod_n, mod_ef, mod_i


### make new_deck work without the deck_choice variable
def new_deck(decks: dict, deck_choice: int):
    mod_decks = decks
    name = input("\nWhat is the name of your new deck? ")
    new_deck = {
        "name": name,
        "cards": []
    }
    mod_decks['decks'].append(new_deck)
    print(f"Your new deck {name} has been created! Please add at least one card.")
    mod_decks = add_to_deck(decks, deck_choice)
    return mod_decks


### make add_to_deck work with a single deck instead of the whole decks variable and remove deck_choice argument
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


### make study_deck work with a single deck and without the deck_choice var
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


actions_menu = {
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
    
    if len(decks['decks']) == 0:
        print("\nYou have no decks yet! Please add at least one deck.")
        decks = new_deck(decks, 0)

    ### instead of doing integer manipulation, make deck_choice be "n" if you want a new deck
    ### set deck_choice to "n" instead here
    deck_choice = len(decks['decks'])
    ### while deck_choice == "n"
    while deck_choice == len(decks['decks']):
        # Ask user which deck they want to work with and assign it to a variable
        print("\n-- Decks Menu --")
        for idx, deck in enumerate(decks['decks']):
            print(f"{idx}: {deck['name']}")
        ### make the menu option "n" instead of the length of decks
        print(f"{len(decks['decks'])}: New deck")
        ### make deck_choice a string here and cast it as an int later
        deck_choice = int(input("Which deck would you like to work with? "))

        # Create a new deck if there aren't any or if the user has indicated they want to
        ### if deck_choice == "n"
        if deck_choice == len(decks['decks']):
            decks = new_deck(decks, deck_choice)
            ### remove line below
            deck_choice += 1
    
    mode = None
    while mode != "q":
        # Ask what the user would like to do
        print("\n-- Actions Menu --")
        for key, value in actions_menu.items():
            print(f"{key}: {value.__name__.replace('_', ' ')}")
        print("q: quit")
        mode = input("Which action? ")
        if mode == "q":
            break
        try:
            ### actions_menu functions should now work with a single deck and without the deck_choice argument
            decks = actions_menu[mode](decks, deck_choice)
        except KeyError:
            print("Invalid input. Please enter either 'a' or 's'")
            
    # Update the decks json file
    with open("decks.json", "w") as updated_decks_file:
        json.dump(decks, updated_decks_file, indent=4)
    print("\nCome back soon!")

if __name__ == '__main__':
    main()

# ask which deck to study
# ask whether question is front or back of card
# list to study = each card in deck if (current timestamp) >= (I + last timestamp the card was studied)
# while there are still cards in list to study:
    # print to terminal: front side of card at front of list to study
    # press enter to flip card
    # prompt for difficulty rating, wait for user to enter it
    # update card metadata using SM2 algorithm
    # if the rating was below 4:
        # pop onto back of list to study
    # else:
        # remove from list to study
# print to terminal: no more cards to study. come back tomorrow!
import random

DECK = []

def shuffle_deck():
    global DECK
    DECK = [2,3,4,5,6,7,8,9, 
            2,3,4,5,6,7,8,9, 
            2,3,4,5,6,7,8,9, 
            2,3,4,5,6,7,8,9,
            10, 10, 10, 10, 11,
            10, 10, 10, 10, 11,
            10, 10, 10, 10, 11,
            10, 10, 10, 10, 11
            ]
    random.shuffle(DECK)

# A simple model for the deck
def deal():
    global DECK
    if not DECK:
        return 0
    card = DECK.pop()      # draw top card
    return card

# Modelling hands

def hand(h):
    return h               # identity function

def new_hand():
    return [deal()]        

def up_card(hand):
    return hand[0]         

def add_card(hand, card):
    return hand + [card]   

def total(hand):
    return sum(hand)       

# We will model a strategy as a procedure of the current hand
# and the dealers 'up card' (which a decent strategy will take into account) 
# that returns true or false if it decides to 'hit'.

# Strategies
def strategy(total, up_card):
    pass

def hard_totals(total,up_card):

    if total < 12:
        action = True
    elif total == 12:
        if up_card in [4, 5, 6]:
            action = False
        else:
            action =  True
    elif total < 17:
        if up_card in [7, 8, 9, 10] or up_card == '11':
            action = False
        else:
            action = True
    else:
        action = False

    return action
    
# Take a look at the play-game procedure: it takes 2 strategies, 
# for the player and dealer then uses play-hand to play the players 
# hand and then (if the player didnt bust), plays the dealers hand. 
# It returns 1 if the player wins and 0 if she loses.

# The play-hand procedure takes a strategy, a hand (list of cards)
# and the visible card of the opponent, it always returns a hand 
# and will stop if either 
# the strategy decides to stop, or the player goes bust
# otherwise it takes a card and recurs

        
def play_hand(strategy, hand, up_card): 
    print('current hand: ', hand)
    print('total: ',total(hand))
    print('up: ',up_card)
    
    if strategy(total(hand), up_card) == True:  
        print('HIT')     
        hand = add_card(hand, deal()) 
        return play_hand(strategy, hand, up_card)
    else:
        print('STAND')
        return hand


def play_game(strategy_p):

    # initialize deck
    shuffle_deck()

    # initialize hands
    p = hand(new_hand())
    d = hand(new_hand())

    # draw other card
    p = add_card(p,deal())
    d = add_card(d,deal())

    # play
    p = play_hand(strategy_p,p,up_card(d))

    print('Player hand:',p)
    print('Dealer hand:',d)

    if total(p) > 21: # bust
        return 0
    else:
        if total(p) > total(d):
            return 1
        else:
            return 0



# simulate games
games = []
n = 500

for i in range(n):
    games.append(play_game(hard_totals))

print(f'Winrate: {sum(games)/n * 100}%')
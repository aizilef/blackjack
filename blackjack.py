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
            10, 10, 10, 10, 11]
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

def hard_totals(total, up_card):
    if total < 12:
        action = True
    elif total == 12:
        if up_card in [4, 5, 6]:
            action = False
        else:
            action =  True
    elif total < 17:
        if up_card in [7, 8, 9, 10] or up_card == 11:
            action = False
        else:
            action = True
    else:
        action = False

    return action

def soft_totals(total,up_card):
    if total <= 17:
        action = True

    elif total == 18:
        if up_card in [9,10] or up_card == 11:
            action = True
        else:
            action = False 
    else: 
        action = False

    return action

def watched(strategy):
# Write a procedure called watched that takes a strategy 
# and returns a strategy that behaves the same way only also prints 
# (as a side-effect) the arguments it was called with (hand and up-card) 
# and the decision to hit or not

# vvv this Stands immediately, idk how to make it run
    # def strategy(total, up_card):
    #     if strategy == True:
    #         print('Watch that hit')
    #         action = True
    #     else:
    #         print('make a stand')
    #         action = False
    #     print(f'total: {total} up_card: {up_card}')
    #     return action
    return strategy

def stop_at_17(total, up_card):
    if total >= 17:
        action = False
    else: 
        action = True
    return action

def stop_at_n(n):
    def stop_n(total, up_card):
        if total >= n:
            action = False
        else: 
            action = True
        return action
    return stop_n
    
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
    # print('current hand: ', hand)
    # print('total: ',total(hand))
    # print('up: ',up_card)
    
    if strategy(total(hand), up_card) == True:  
        print('HIT')     
        hand = add_card(hand, deal()) 
        return play_hand(strategy, hand, up_card)
    else:
        print('STAND')
        return hand


def play_game(strategy_p, strategy_d):
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
    d = play_hand(strategy_d,d,up_card(p))

    print('Player hand:',p,'Total: ',total(p))
    print('Dealer hand:',d,'Total: ',total(d))

    if total(p) > 21: # bust
        print('L')
        return 0
    elif total(d) > 21:
        print('W')
        return 1
    else:
        if total(p) > total(d):
            print('W')
            return 1
        else:
            print('L')
            return 0



# simulate games
games = []
n = 50

for i in range(n):
    print(f'===== Game {i+1} =====')
    games.append(play_game(stop_at_17, stop_at_n(18)))

print(f'Winrate: {sum(games)/n * 100}%')
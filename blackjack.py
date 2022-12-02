import random

DECK = []


def shuffle_deck():
    global DECK
    DECK = [2, 3, 4, 5, 6, 7, 8, 9,
            2, 3, 4, 5, 6, 7, 8, 9,
            2, 3, 4, 5, 6, 7, 8, 9,
            2, 3, 4, 5, 6, 7, 8, 9,
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


def face_val(total):
    if total < 11:
        return 11
    else:
        return 1

# We will model a strategy as a procedure of the current hand
# and the dealers 'up card' (which a decent strategy will take into account)
# that returns true or false if it decides to 'hit'.

# Strategies


def hard_totals(total, up_card):
    if total < 12:
        hit = True
    elif total == 12:
        if up_card in [4, 5, 6]:
            hit = False
        else:
            hit = True
    elif total < 17:
        if up_card in [7, 8, 9, 10] or up_card == 11:
            hit = False
        else:
            hit = True
    else:
        hit = False

    return hit


def soft_totals(total, up_card):
    if total <= 17:
        hit = True

    elif total == 18:
        if up_card in [9, 10] or up_card == 11:
            hit = True
        else:
            hit = False
    else:
        hit = False

    return hit


def stop_at_17(total, up_card):
    if total >= 17:
        hit = False
    else:
        hit = True
    return hit

# Write a procedure called stop-at-n that takes a number
# and returns a strategy that will stop when it gets higher
# than that number (so stop-at-17 should be 'the same' as (stop-at-n 17))


def stop_at_n(n):
    def stop_n(total, up_card):
        if total >= n:
            hit = False
        else:
            hit = True
        return hit
    return stop_n

# Write a procedure called watched that takes a strategy
# and returns a strategy that behaves the same way only also
# prints (as a side-effect) the arguments it was called
# with (hand and up-card) and the decision to hit or not


def watched(strategy):
    def watched_strategy(total, up_card):
        print(f'total: {total}, up_card: {up_card}')
        hit = strategy(total, up_card)

        if hit == True:
            print('hit')
        else:
            print('stand')
        return hit

    return watched_strategy


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
    if strategy(total(hand), up_card) == True:
        hand = add_card(hand, deal())
        return play_hand(strategy, hand, up_card)
    else:
        return hand


def play_game(strategy_p, strategy_d):
    # initialize deck
    shuffle_deck()

    # initialize player & dealer hands
    p = hand(new_hand())
    d = hand(new_hand())

    # draw other card
    p = add_card(p, deal())
    d = add_card(d, deal())

    # play
    p = play_hand(strategy_p, p, up_card(d))
    d = play_hand(strategy_d, d, up_card(d))

    print('Final player hand:', p, 'Total: ', total(p))
    print('Final dealer hand:', d, 'Total: ', total(d))

    if total(d) > 21:  # dealer bust
        print('W')
        return 1

    if total(p) > 21:  # player bust
        print('L')
        return 0
    else:
        if total(p) > total(d):
            print('W')
            return 1
        else:
            print('L')
            return 0


# simulate games
games = []
n = 5

for i in range(n):
    print(f'===== Game {i+1} =====')
    games.append(play_game(watched(stop_at_17), stop_at_n(18)))

print(f'Winrate: {sum(games)/n * 100}%')

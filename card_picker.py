import os
import random

# playing cards from:https://code.google.com/archive/p/vector-playing-cards/
# uno cards from: https://github.com/celsiusnarhwal/uno
# Tarot Cards from: https://luciellaes.itch.io/rider-waite-smith-tarot-cards-cc0

card_decks = {
    'standard-52': {
        'separator': '-of-',
        'suits': ['Hearts', 'Clubs', 'Diamonds', 'Spades'],
        'values': ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    },
    'standard-32': {
        'separator': '-of-',
        'suits': ['Hearts', 'Clubs', 'Diamonds', 'Spades'],
        'values': ['7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    },
    'tarot-major': {
        'names': ['The Fool', 'The Magician', 'The High Priestess', 'The Empress', 'The Emperor', 'The Hierophant', 'The Lovers', 'The Chariot',
                  'Strength', 'The Hermit', 'Wheel Of Fortune', 'Justice', 'The Hanged Man', 'Death', 'Temperance', 'The Devil', 'The Tower', 'The Star',
                  'The Moon', 'The Sun', 'Judgement', 'The World'],
        'values': ['0', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII', 'XIX', 'XX', 'XXI']
    },
    'tarot-minor': {
        'separator': '-of-',
        'suits': ['Wands', 'Cups', 'Swords', 'Diamonds'],
        'values': ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Page', 'Knight', 'Queen', 'King', 'Ace']
    },
    'deck-of-omens': {
        'names': ['The Clever Animal', 'The Duelist', 'The Beloved Friends', 'The Runaway', 'The Avenger', 'The Traveller', 'The Beguiler', 'The Phantom',
                  'The Brute', 'The Dragon', 'The Angel', 'The Mind-Bender', 'Time', 'New Beginnings', 'The Hunt', 'War', 'The Moon', 'The Sea',
                  'The Truth', 'The Seasons', 'The Campions', 'The Dead'],
        'values': ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII', 'XIX', 'XX', 'XXI', 'XXII']
    },
    'uno': {
        'separator': '-',
        'suits': ['Red', 'Yellow', 'Green', 'Blue'],
        'values': ['0', '0', '0', '0', '1', '1', '1', '1', '1', '1', '1', '1', '2', '2', '2', '2', '2', '2', '2', '2', '3', '3', '3', '3', '3', '3', '3', '3',
                   '4', '4', '4', '4', '4', '4', '4', '4', '5', '5', '5', '5', '5', '5', '5', '5', '6', '6', '6', '6', '6', '6', '6', '6', '7', '7', '7', '7', '7', '7', '7', '7',
                   '8', '8', '8', '8', '8', '8', '8', '8', '9', '9', '9', '9', '9', '9', '9', '9', 'block', 'block', 'block', 'block', 'block', 'block', 'block', 'block',
                   'reverse', 'reverse', 'reverse', 'reverse', 'reverse', 'reverse', 'reverse', 'reverse', '+2', '+2', '+2', '+2', '+2', '+2', '+2', '+2'],
        'wildcards': ['wildcard', 'wildcard', 'wildcard', 'wildcard', 'wildcard', 'wildcard+4', 'wildcard+4', 'wildcard+4', 'wildcard+4']
    }

}


def pick_card(deck):
    card = deck[0]
    deck.pop(0)
    return card


def shuffle_deck(deck, add_orientation=False):
    if add_orientation:
        for i in range(len(deck)):
            if random.choice([True, False]):
                deck[i] = deck[i]+' (U)'
            else:
                deck[i] = deck[i]+' (R)'
    random.shuffle(deck)
    return deck


def create_deck(deck_type, add_names=True):
    deck = []

    if deck_type in ['standard-52', 'standard-32', 'tarot-minor', 'tarot', 'uno']:
        deck_key = deck_type
        if deck_key == 'tarot':
            deck_key = 'tarot-minor'

        suits = card_decks[deck_key]['suits']
        values = card_decks[deck_key]['values']
        separator = card_decks[deck_key]['separator']

        for suit in suits:
            for value in values:
                deck.append(value+separator+suit)

    if deck_type in ['tarot-major', 'tarot', 'deck-of-omens']:
        deck_key = deck_type
        if deck_key == 'tarot':
            deck_key = 'tarot-major'

        names = card_decks[deck_key]['names']
        values = card_decks[deck_key]['values']

        for i in range(len(values)):
            if add_names:
                deck.append(values[i]+'-'+names[i])
            else:
                deck.append(values[i])
    if deck_type == 'uno':
        deck.extend(card_decks['uno']['wildcards'])
    return deck


def draw_cards(card_count, deck_type, added_jokers=0, add_names=True, add_orientation=False):
    if deck_type not in ['tarot-major', 'tarot', 'deck-of-omens', 'standard-52', 'standard-32', 'tarot-minor', 'uno']:
        return[]

    deck = create_deck(deck_type, add_names)

    if 'standard' in deck_type:
        for i in range(added_jokers):
            deck.append('Joker')
    deck = shuffle_deck(deck, add_orientation)

    new_deck = []
    for i in range(card_count):
        new_deck.append(pick_card(deck))

    return new_deck


if __name__ == '__main__':
    print(draw_cards(1, "uno"))

# -*- coding: utf-8 -*-

from json import loads
from urllib.parse import quote

_CATEGORIES_TRANSLATE_TABLE = [
    ('number', 'number'),
    ('rarity', 'rarity'),
    ('name', 'name'),
    ('type', 'type'),
    ('manaCost', 'mana_cost'),
    ('power', 'power'),
    ('toughness', 'toughness'),
]

_COST_TRANSLATE_TABLE = {
    '0': 'u0',
    '1': 'u1',
    '2': 'u2',
    '3': 'u3',
    '4': 'u4',
    '5': 'u5',
    '6': 'u6',
    '7': 'u7',
    '8': 'u8',
    '9': 'u9',
    '10': 'u10',
    '11': 'u11',
    '12': 'u12',
    '13': 'u13',
    '14': 'u14',
    '15': 'u15',
    '16': 'u16',
    '17': 'u17',
    '18': 'u18',
    '19': 'u19',
    '20': 'u20',
    'X': 'x',
    'Y': 'y',
    'Z': 'z',
    'W': 'white',
    'U': 'blue',
    'B': 'black',
    'R': 'red',
    'G': 'green',
    'W/U': 'white-blue',
    'W/B': 'white-black',
    'U/B': 'blue-black',
    'U/R': 'blue-red',
    'B/R': 'black-red',
    'B/G': 'black-green',
    'R/W': 'red-white',
    'R/G': 'red-green',
    'G/W': 'green-white',
    'G/B': 'green-blue',
    '2/W': 'white-2',
    '2/U': 'blue-2',
    '2/B': 'black-2',
    '2/R': 'red-2',
    '2/G': 'green-2',
    'W/P': 'white-phyrexian',
    'U/P': 'blue-phyrexian',
    'B/P': 'black-phyrexian',
    'R/P': 'red-phyrexian',
    'G/P': 'green-phyrexian',
    '1000000': 'u1000000',
    'hw': 'half-white',
}

_RARITY_TABLE = {
    'm': 'Mythic',
    'r': 'Rare',
    'u': 'Uncommon',
    'c': 'Common',
}


def get_mtgjson(file_='mtgjson/AllSets.json'):
    with open(file_, 'r') as file_data:
        mtgjson = loads(file_data.read())

    return mtgjson


def get_rarity(query_parameter):
    if query_parameter == 'all':
        return set(['Mythic', 'Rare', 'Uncommon', 'Common'])

    rarity = set()
    for r in query_parameter.split(','):
        if r in _RARITY_TABLE:
            rarity.add(_RARITY_TABLE[r])

    if not rarity:
        return set(['Mythic', 'Rare', 'Uncommon', 'Common'])

    return rarity


def strip_rarity(cards, rarity=[]):
    for card in cards[:]:
        if card['rarity'] not in rarity:
            cards.remove(card)


def purify_cards(cards, translate=[]):
    purified_cards = []

    for card in cards:
        current_purified = {}
        for key1, key2 in translate:
            if key1 in card:
                current_purified[key2] = card[key1]
        purified_cards.append(current_purified.copy())

    return purified_cards


def tokenize_cost(card):
    try:
        cost = card['mana_cost']
    except KeyError:
        return []

    return cost[1:-1].split('}{')


def translate_mana_cost(set_):
    for card in set_['cards']:
        mana_cost = []
        for cost_token in tokenize_cost(card):
            try:
                css_class = _COST_TRANSLATE_TABLE[cost_token]
            except KeyError:
                mana_cost.append('{[{0}}}'.format(cost_token))
            else:
                mana_cost.append(css_class)
        card['mana_cost'] = mana_cost


def add_image_name(set_):
    for card in set_['cards']:
        card['image_name'] = quote(card['name'])


def get_purified_set(mtgjson=None, set_name=None, rarity=[]):
    if set_name is None:
        return {}

    try:
        whole_set = mtgjson[set_name]
    except KeyError:
        return {}

    if rarity:
        strip_rarity(whole_set['cards'], rarity=rarity)

    set_ = {}
    for key, value in whole_set.items():
        if key != 'cards':
            set_[key] = value

    set_['cards'] = purify_cards(whole_set['cards'],
                                 translate=_CATEGORIES_TRANSLATE_TABLE)
    add_image_name(set_)
    translate_mana_cost(set_)

    return set_


def get_available_sets(mtgjson=[]):
    return mtgjson.keys()

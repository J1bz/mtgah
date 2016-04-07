#!/usr/bin/env python

from os.path import join
from bottle import get, route, run, template, static_file, request

from mtgtools import (
    get_mtgjson, get_purified_set, get_rarity, get_available_sets)


@route('/static/css/<filename>')
def css(filename):
    return static_file(filename, root='static/css')


@route('/static/js/<filename>')
def js(filename):
    return static_file(filename, root='static/js')


@route('/static/img/<filename>')
def img(filename):
    return static_file(filename, root='static/img')


@route('/static/img/<extension>/<card_name>')
def card_img(extension, card_name):
    root = join('static/img', extension)
    return static_file(card_name, root=root)


def get_rarity_label(rarity):
    label = "Rarity : "
    for r in rarity:
        label += '{}, '.format(r)

    return label[:-2]


@get('/')
@get('/<set_name>')
def list_cards(set_name=None):
    # Default rarities taken in account are Rare and Mythic
    r = request.query.get("r", "m,r")
    rarity = get_rarity(r)

    mtgjson = get_mtgjson(file_='mtgjson/AllSets.json')

    available_sets = get_available_sets(mtgjson=mtgjson)
    set_ = get_purified_set(mtgjson=mtgjson, set_name=set_name, rarity=rarity)

    response = template(
        'cards',
        set_=set_,
        rarity=get_rarity_label(rarity),
        available_sets=available_sets
    )
    return response

run(host='0.0.0.0', port=8080, debug=True)

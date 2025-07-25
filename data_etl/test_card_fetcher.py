import json
import unittest
from unittest.mock import MagicMock
from data_etl.card_fetcher import transform_card_data

import logging

logging.basicConfig(level=logging.INFO)


class TestTransformCardData(unittest.TestCase):
    def test_transform_card_data_s3(self):
        # Sample input data
        data = r"""[
  {
    "object": "card",
    "id": "0000419b-0bba-4488-8f7a-6194544ce91e",
    "oracle_id": "b34bb2dc-c1af-4d77-b0b3-a0fb342a5fc6",
    "multiverse_ids": [
      668564
    ],
    "mtgo_id": 129825,
    "arena_id": 91829,
    "tcgplayer_id": 558404,
    "cardmarket_id": 777725,
    "name": "Forest",
    "lang": "en",
    "released_at": "2024-08-02",
    "uri": "https://api.scryfall.com/cards/0000419b-0bba-4488-8f7a-6194544ce91e",
    "scryfall_uri": "https://scryfall.com/card/blb/280/forest?utm_source=api",
    "layout": "normal",
    "highres_image": true,
    "image_status": "highres_scan",
    "image_uris": {
      "small": "https://cards.scryfall.io/small/front/0/0/0000419b-0bba-4488-8f7a-6194544ce91e.jpg?1721427487",
      "normal": "https://cards.scryfall.io/normal/front/0/0/0000419b-0bba-4488-8f7a-6194544ce91e.jpg?1721427487",
      "large": "https://cards.scryfall.io/large/front/0/0/0000419b-0bba-4488-8f7a-6194544ce91e.jpg?1721427487",
      "png": "https://cards.scryfall.io/png/front/0/0/0000419b-0bba-4488-8f7a-6194544ce91e.png?1721427487",
      "art_crop": "https://cards.scryfall.io/art_crop/front/0/0/0000419b-0bba-4488-8f7a-6194544ce91e.jpg?1721427487",
      "border_crop": "https://cards.scryfall.io/border_crop/front/0/0/0000419b-0bba-4488-8f7a-6194544ce91e.jpg?1721427487"
    },
    "mana_cost": "",
    "cmc": 0.0,
    "type_line": "Basic Land \u2014 Forest",
    "oracle_text": "({T}: Add {G}.)",
    "colors": [],
    "color_identity": [
      "G"
    ],
    "keywords": [],
    "produced_mana": [
      "G"
    ],
    "legalities": {
      "standard": "legal",
      "future": "legal",
      "historic": "legal",
      "timeless": "legal",
      "gladiator": "legal",
      "pioneer": "legal",
      "modern": "legal",
      "legacy": "legal",
      "pauper": "legal",
      "vintage": "legal",
      "penny": "legal",
      "commander": "legal",
      "oathbreaker": "legal",
      "standardbrawl": "legal",
      "brawl": "legal",
      "alchemy": "legal",
      "paupercommander": "legal",
      "duel": "legal",
      "oldschool": "not_legal",
      "premodern": "legal",
      "predh": "legal"
    },
    "games": [
      "paper",
      "mtgo",
      "arena"
    ],
    "reserved": false,
    "game_changer": false,
    "foil": true,
    "nonfoil": true,
    "finishes": [
      "nonfoil",
      "foil"
    ],
    "oversized": false,
    "promo": false,
    "reprint": true,
    "variation": false,
    "set_id": "a2f58272-bba6-439d-871e-7a46686ac018",
    "set": "blb",
    "set_name": "Bloomburrow",
    "set_type": "expansion",
    "set_uri": "https://api.scryfall.com/sets/a2f58272-bba6-439d-871e-7a46686ac018",
    "set_search_uri": "https://api.scryfall.com/cards/search?order=set&q=e%3Ablb&unique=prints",
    "scryfall_set_uri": "https://scryfall.com/sets/blb?utm_source=api",
    "rulings_uri": "https://api.scryfall.com/cards/0000419b-0bba-4488-8f7a-6194544ce91e/rulings",
    "prints_search_uri": "https://api.scryfall.com/cards/search?order=released&q=oracleid%3Ab34bb2dc-c1af-4d77-b0b3-a0fb342a5fc6&unique=prints",
    "collector_number": "280",
    "digital": false,
    "rarity": "common",
    "card_back_id": "0aeebaf5-8c7d-4636-9e82-8c27447861f7",
    "artist": "David Robert Hovey",
    "artist_ids": [
      "22ab27e3-6476-48f1-a9f7-9a9e86339030"
    ],
    "illustration_id": "fb2b1ca2-7440-48c2-81c8-84da0a45a626",
    "border_color": "black",
    "frame": "2015",
    "full_art": true,
    "textless": false,
    "booster": true,
    "story_spotlight": false,
    "prices": {
      "usd": "0.26",
      "usd_foil": "0.45",
      "usd_etched": null,
      "eur": "0.28",
      "eur_foil": "0.40",
      "tix": "0.03"
    },
    "related_uris": {
      "gatherer": "https://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=668564&printed=false",
      "tcgplayer_infinite_articles": "https://partner.tcgplayer.com/c/4931599/1830156/21018?subId1=api&trafcat=tcgplayer.com%2Fsearch%2Farticles&u=https%3A%2F%2Fwww.tcgplayer.com%2Fsearch%2Farticles%3FproductLineName%3Dmagic%26q%3DForest",
      "tcgplayer_infinite_decks": "https://partner.tcgplayer.com/c/4931599/1830156/21018?subId1=api&trafcat=tcgplayer.com%2Fsearch%2Fdecks&u=https%3A%2F%2Fwww.tcgplayer.com%2Fsearch%2Fdecks%3FproductLineName%3Dmagic%26q%3DForest",
      "edhrec": "https://edhrec.com/route/?cc=Forest"
    },
    "purchase_uris": {
      "tcgplayer": "https://partner.tcgplayer.com/c/4931599/1830156/21018?subId1=api&u=https%3A%2F%2Fwww.tcgplayer.com%2Fproduct%2F558404%3Fpage%3D1",
      "cardmarket": "https://www.cardmarket.com/en/Magic/Products?idProduct=777725&referrer=scryfall&utm_campaign=card_prices&utm_medium=text&utm_source=scryfall",
      "cardhoarder": "https://www.cardhoarder.com/cards/129825?affiliate_id=scryfall&ref=card-profile&utm_campaign=affiliate&utm_medium=card&utm_source=scryfall"
    }
  },
  {
    "object": "card",
    "id": "0000579f-7b35-4ed3-b44c-db2a538066fe",
    "oracle_id": "44623693-51d6-49ad-8cd7-140505caf02f",
    "multiverse_ids": [
      109722
    ],
    "mtgo_id": 25527,
    "mtgo_foil_id": 25528,
    "tcgplayer_id": 14240,
    "cardmarket_id": 13850,
    "name": "Fury Sliver",
    "lang": "en",
    "released_at": "2006-10-06",
    "uri": "https://api.scryfall.com/cards/0000579f-7b35-4ed3-b44c-db2a538066fe",
    "scryfall_uri": "https://scryfall.com/card/tsp/157/fury-sliver?utm_source=api",
    "layout": "normal",
    "highres_image": true,
    "image_status": "highres_scan",
    "image_uris": {
      "small": "https://cards.scryfall.io/small/front/0/0/0000579f-7b35-4ed3-b44c-db2a538066fe.jpg?1562894979",
      "normal": "https://cards.scryfall.io/normal/front/0/0/0000579f-7b35-4ed3-b44c-db2a538066fe.jpg?1562894979",
      "large": "https://cards.scryfall.io/large/front/0/0/0000579f-7b35-4ed3-b44c-db2a538066fe.jpg?1562894979",
      "png": "https://cards.scryfall.io/png/front/0/0/0000579f-7b35-4ed3-b44c-db2a538066fe.png?1562894979",
      "art_crop": "https://cards.scryfall.io/art_crop/front/0/0/0000579f-7b35-4ed3-b44c-db2a538066fe.jpg?1562894979",
      "border_crop": "https://cards.scryfall.io/border_crop/front/0/0/0000579f-7b35-4ed3-b44c-db2a538066fe.jpg?1562894979"
    },
    "mana_cost": "{5}{R}",
    "cmc": 6.0,
    "type_line": "Creature \u2014 Sliver",
    "oracle_text": "All Sliver creatures have double strike.",
    "power": "3",
    "toughness": "3",
    "colors": [
      "R"
    ],
    "color_identity": [
      "R"
    ],
    "keywords": [],
    "legalities": {
      "standard": "not_legal",
      "future": "not_legal",
      "historic": "not_legal",
      "timeless": "not_legal",
      "gladiator": "not_legal",
      "pioneer": "not_legal",
      "modern": "legal",
      "legacy": "legal",
      "pauper": "not_legal",
      "vintage": "legal",
      "penny": "not_legal",
      "commander": "legal",
      "oathbreaker": "legal",
      "standardbrawl": "not_legal",
      "brawl": "not_legal",
      "alchemy": "not_legal",
      "paupercommander": "not_legal",
      "duel": "legal",
      "oldschool": "not_legal",
      "premodern": "not_legal",
      "predh": "legal"
    },
    "games": [
      "paper",
      "mtgo"
    ],
    "reserved": false,
    "game_changer": false,
    "foil": true,
    "nonfoil": true,
    "finishes": [
      "nonfoil",
      "foil"
    ],
    "oversized": false,
    "promo": false,
    "reprint": false,
    "variation": false,
    "set_id": "c1d109bc-ffd8-428f-8d7d-3f8d7e648046",
    "set": "tsp",
    "set_name": "Time Spiral",
    "set_type": "expansion",
    "set_uri": "https://api.scryfall.com/sets/c1d109bc-ffd8-428f-8d7d-3f8d7e648046",
    "set_search_uri": "https://api.scryfall.com/cards/search?order=set&q=e%3Atsp&unique=prints",
    "scryfall_set_uri": "https://scryfall.com/sets/tsp?utm_source=api",
    "rulings_uri": "https://api.scryfall.com/cards/0000579f-7b35-4ed3-b44c-db2a538066fe/rulings",
    "prints_search_uri": "https://api.scryfall.com/cards/search?order=released&q=oracleid%3A44623693-51d6-49ad-8cd7-140505caf02f&unique=prints",
    "collector_number": "157",
    "digital": false,
    "rarity": "uncommon",
    "flavor_text": "\"A rift opened, and our arrows were abruptly stilled. To move was to push the world. But the sliver's claw still twitched, red wounds appeared in Thed's chest, and ribbons of blood hung in the air.\"\n\u2014Adom Capashen, Benalish hero",
    "card_back_id": "0aeebaf5-8c7d-4636-9e82-8c27447861f7",
    "artist": "Paolo Parente",
    "artist_ids": [
      "d48dd097-720d-476a-8722-6a02854ae28b"
    ],
    "illustration_id": "2fcca987-364c-4738-a75b-099d8a26d614",
    "border_color": "black",
    "frame": "2003",
    "full_art": false,
    "textless": false,
    "booster": true,
    "story_spotlight": false,
    "edhrec_rank": 9396,
    "penny_rank": 11333,
    "prices": {
      "usd": "0.31",
      "usd_foil": "3.79",
      "usd_etched": null,
      "eur": "0.22",
      "eur_foil": "1.25",
      "tix": "0.03"
    },
    "related_uris": {
      "gatherer": "https://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=109722&printed=false",
      "tcgplayer_infinite_articles": "https://partner.tcgplayer.com/c/4931599/1830156/21018?subId1=api&trafcat=tcgplayer.com%2Fsearch%2Farticles&u=https%3A%2F%2Fwww.tcgplayer.com%2Fsearch%2Farticles%3FproductLineName%3Dmagic%26q%3DFury%2BSliver",
      "tcgplayer_infinite_decks": "https://partner.tcgplayer.com/c/4931599/1830156/21018?subId1=api&trafcat=tcgplayer.com%2Fsearch%2Fdecks&u=https%3A%2F%2Fwww.tcgplayer.com%2Fsearch%2Fdecks%3FproductLineName%3Dmagic%26q%3DFury%2BSliver",
      "edhrec": "https://edhrec.com/route/?cc=Fury+Sliver"
    },
    "purchase_uris": {
      "tcgplayer": "https://partner.tcgplayer.com/c/4931599/1830156/21018?subId1=api&u=https%3A%2F%2Fwww.tcgplayer.com%2Fproduct%2F14240%3Fpage%3D1",
      "cardmarket": "https://www.cardmarket.com/en/Magic/Products?idProduct=13850&referrer=scryfall&utm_campaign=card_prices&utm_medium=text&utm_source=scryfall",
      "cardhoarder": "https://www.cardhoarder.com/cards/25527?affiliate_id=scryfall&ref=card-profile&utm_campaign=affiliate&utm_medium=card&utm_source=scryfall"
    }
  },
  {
    "object": "card",
    "id": "00006596-1166-4a79-8443-ca9f82e6db4e",
    "oracle_id": "8ae3562f-28b7-4462-96ed-be0cf7052ccc",
    "multiverse_ids": [
      189637
    ],
    "mtgo_id": 34586,
    "mtgo_foil_id": 34587,
    "tcgplayer_id": 33347,
    "cardmarket_id": 21851,
    "name": "Kor Outfitter",
    "lang": "en",
    "released_at": "2009-10-02",
    "uri": "https://api.scryfall.com/cards/00006596-1166-4a79-8443-ca9f82e6db4e",
    "scryfall_uri": "https://scryfall.com/card/zen/21/kor-outfitter?utm_source=api",
    "layout": "normal",
    "highres_image": true,
    "image_status": "highres_scan",
    "image_uris": {
      "small": "https://cards.scryfall.io/small/front/0/0/00006596-1166-4a79-8443-ca9f82e6db4e.jpg?1562609251",
      "normal": "https://cards.scryfall.io/normal/front/0/0/00006596-1166-4a79-8443-ca9f82e6db4e.jpg?1562609251",
      "large": "https://cards.scryfall.io/large/front/0/0/00006596-1166-4a79-8443-ca9f82e6db4e.jpg?1562609251",
      "png": "https://cards.scryfall.io/png/front/0/0/00006596-1166-4a79-8443-ca9f82e6db4e.png?1562609251",
      "art_crop": "https://cards.scryfall.io/art_crop/front/0/0/00006596-1166-4a79-8443-ca9f82e6db4e.jpg?1562609251",
      "border_crop": "https://cards.scryfall.io/border_crop/front/0/0/00006596-1166-4a79-8443-ca9f82e6db4e.jpg?1562609251"
    },
    "mana_cost": "{W}{W}",
    "cmc": 2.0,
    "type_line": "Creature \u2014 Kor Soldier",
    "oracle_text": "When this creature enters, you may attach target Equipment you control to target creature you control.",
    "power": "2",
    "toughness": "2",
    "colors": [
      "W"
    ],
    "color_identity": [
      "W"
    ],
    "keywords": [],
    "legalities": {
      "standard": "not_legal",
      "future": "not_legal",
      "historic": "not_legal",
      "timeless": "not_legal",
      "gladiator": "not_legal",
      "pioneer": "not_legal",
      "modern": "legal",
      "legacy": "legal",
      "pauper": "legal",
      "vintage": "legal",
      "penny": "legal",
      "commander": "legal",
      "oathbreaker": "legal",
      "standardbrawl": "not_legal",
      "brawl": "not_legal",
      "alchemy": "not_legal",
      "paupercommander": "legal",
      "duel": "legal",
      "oldschool": "not_legal",
      "premodern": "not_legal",
      "predh": "legal"
    },
    "games": [
      "paper",
      "mtgo"
    ],
    "reserved": false,
    "game_changer": false,
    "foil": true,
    "nonfoil": true,
    "finishes": [
      "nonfoil",
      "foil"
    ],
    "oversized": false,
    "promo": false,
    "reprint": false,
    "variation": false,
    "set_id": "eb16a2bd-a218-4e4e-8339-4aa1afc0c8d2",
    "set": "zen",
    "set_name": "Zendikar",
    "set_type": "expansion",
    "set_uri": "https://api.scryfall.com/sets/eb16a2bd-a218-4e4e-8339-4aa1afc0c8d2",
    "set_search_uri": "https://api.scryfall.com/cards/search?order=set&q=e%3Azen&unique=prints",
    "scryfall_set_uri": "https://scryfall.com/sets/zen?utm_source=api",
    "rulings_uri": "https://api.scryfall.com/cards/00006596-1166-4a79-8443-ca9f82e6db4e/rulings",
    "prints_search_uri": "https://api.scryfall.com/cards/search?order=released&q=oracleid%3A8ae3562f-28b7-4462-96ed-be0cf7052ccc&unique=prints",
    "collector_number": "21",
    "digital": false,
    "rarity": "common",
    "flavor_text": "\"We take only what we need to survive. Believe me, you will need this.\"",
    "card_back_id": "0aeebaf5-8c7d-4636-9e82-8c27447861f7",
    "artist": "Kieran Yanner",
    "artist_ids": [
      "aa7e89ed-d294-4633-9057-ce04dacfcfa4"
    ],
    "illustration_id": "de0310d1-e97f-46e0-bc16-c980c2adedee",
    "border_color": "black",
    "frame": "2003",
    "full_art": false,
    "textless": false,
    "booster": true,
    "story_spotlight": false,
    "edhrec_rank": 18979,
    "penny_rank": 5921,
    "prices": {
      "usd": "0.15",
      "usd_foil": "1.70",
      "usd_etched": null,
      "eur": "0.31",
      "eur_foil": "1.86",
      "tix": "0.03"
    },
    "related_uris": {
      "gatherer": "https://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=189637&printed=false",
      "tcgplayer_infinite_articles": "https://partner.tcgplayer.com/c/4931599/1830156/21018?subId1=api&trafcat=tcgplayer.com%2Fsearch%2Farticles&u=https%3A%2F%2Fwww.tcgplayer.com%2Fsearch%2Farticles%3FproductLineName%3Dmagic%26q%3DKor%2BOutfitter",
      "tcgplayer_infinite_decks": "https://partner.tcgplayer.com/c/4931599/1830156/21018?subId1=api&trafcat=tcgplayer.com%2Fsearch%2Fdecks&u=https%3A%2F%2Fwww.tcgplayer.com%2Fsearch%2Fdecks%3FproductLineName%3Dmagic%26q%3DKor%2BOutfitter",
      "edhrec": "https://edhrec.com/route/?cc=Kor+Outfitter"
    },
    "purchase_uris": {
      "tcgplayer": "https://partner.tcgplayer.com/c/4931599/1830156/21018?subId1=api&u=https%3A%2F%2Fwww.tcgplayer.com%2Fproduct%2F33347%3Fpage%3D1",
      "cardmarket": "https://www.cardmarket.com/en/Magic/Products?idProduct=21851&referrer=scryfall&utm_campaign=card_prices&utm_medium=text&utm_source=scryfall",
      "cardhoarder": "https://www.cardhoarder.com/cards/34586?affiliate_id=scryfall&ref=card-profile&utm_campaign=affiliate&utm_medium=card&utm_source=scryfall"
    }
  },
  {
    "object": "card",
    "id": "0000a54c-a511-4925-92dc-01b937f9afad",
    "oracle_id": "dc4e2134-f0c2-49aa-9ea3-ebf83af1445c",
    "multiverse_ids": [],
    "tcgplayer_id": 98659,
    "name": "Spirit",
    "lang": "en",
    "released_at": "2015-05-22",
    "uri": "https://api.scryfall.com/cards/0000a54c-a511-4925-92dc-01b937f9afad",
    "scryfall_uri": "https://scryfall.com/card/tmm2/5/spirit?utm_source=api",
    "layout": "token",
    "highres_image": true,
    "image_status": "highres_scan",
    "image_uris": {
      "small": "https://cards.scryfall.io/small/front/0/0/0000a54c-a511-4925-92dc-01b937f9afad.jpg?1562701869",
      "normal": "https://cards.scryfall.io/normal/front/0/0/0000a54c-a511-4925-92dc-01b937f9afad.jpg?1562701869",
      "large": "https://cards.scryfall.io/large/front/0/0/0000a54c-a511-4925-92dc-01b937f9afad.jpg?1562701869",
      "png": "https://cards.scryfall.io/png/front/0/0/0000a54c-a511-4925-92dc-01b937f9afad.png?1562701869",
      "art_crop": "https://cards.scryfall.io/art_crop/front/0/0/0000a54c-a511-4925-92dc-01b937f9afad.jpg?1562701869",
      "border_crop": "https://cards.scryfall.io/border_crop/front/0/0/0000a54c-a511-4925-92dc-01b937f9afad.jpg?1562701869"
    },
    "mana_cost": "",
    "cmc": 0.0,
    "type_line": "Token Creature \u2014 Spirit",
    "oracle_text": "Flying",
    "power": "1",
    "toughness": "1",
    "colors": [
      "W"
    ],
    "color_identity": [
      "W"
    ],
    "keywords": [
      "Flying"
    ],
    "all_parts": [
      {
        "object": "related_card",
        "id": "9e371a29-bb06-402d-8ea3-f2a0b982a310",
        "component": "combo_piece",
        "name": "Kykar, Zephyr Awakener",
        "type_line": "Legendary Creature \u2014 Bird Wizard",
        "uri": "https://api.scryfall.com/cards/9e371a29-bb06-402d-8ea3-f2a0b982a310"
      },
      {
        "object": "related_card",
        "id": "4d8542f6-ee34-42c6-acd5-07b0c7cc2f63",
        "component": "combo_piece",
        "name": "Funeral Pyre",
        "type_line": "Instant",
        "uri": "https://api.scryfall.com/cards/4d8542f6-ee34-42c6-acd5-07b0c7cc2f63"
      },
      {
        "object": "related_card",
        "id": "db15f7e6-a4fa-4dd5-b072-37fc213c99d0",
        "component": "combo_piece",
        "name": "Haunted Dead",
        "type_line": "Creature \u2014 Zombie",
        "uri": "https://api.scryfall.com/cards/db15f7e6-a4fa-4dd5-b072-37fc213c99d0"
      },
      {
        "object": "related_card",
        "id": "184e5208-edbe-417f-8ff8-1950d08071ab",
        "component": "combo_piece",
        "name": "Blessed Defiance",
        "type_line": "Instant",
        "uri": "https://api.scryfall.com/cards/184e5208-edbe-417f-8ff8-1950d08071ab"
      },
      {
        "object": "related_card",
        "id": "f0ad0796-0357-4e74-9d65-c7761a3f223c",
        "component": "combo_piece",
        "name": "Slayer's Plate",
        "type_line": "Artifact \u2014 Equipment",
        "uri": "https://api.scryfall.com/cards/f0ad0796-0357-4e74-9d65-c7761a3f223c"
      },
      {
        "object": "related_card",
        "id": "e464408d-3e50-4a9e-beca-b91e15baacaf",
        "component": "combo_piece",
        "name": "Lingering Souls",
        "type_line": "Sorcery",
        "uri": "https://api.scryfall.com/cards/e464408d-3e50-4a9e-beca-b91e15baacaf"
      },
      {
        "object": "related_card",
        "id": "6f4ad71f-14e6-4b1e-9558-1400a36f27a9",
        "component": "combo_piece",
        "name": "Staff of the Storyteller",
        "type_line": "Artifact",
        "uri": "https://api.scryfall.com/cards/6f4ad71f-14e6-4b1e-9558-1400a36f27a9"
      },
      {
        "object": "related_card",
        "id": "8a840ee7-5728-4b1b-92ac-54612e5397b3",
        "component": "combo_piece",
        "name": "Gallows at Willow Hill",
        "type_line": "Artifact",
        "uri": "https://api.scryfall.com/cards/8a840ee7-5728-4b1b-92ac-54612e5397b3"
      },
      {
        "object": "related_card",
        "id": "dd4287fc-3e16-473f-818c-9f4d57d03125",
        "component": "combo_piece",
        "name": "Kaya the Inexorable",
        "type_line": "Legendary Planeswalker \u2014 Kaya",
        "uri": "https://api.scryfall.com/cards/dd4287fc-3e16-473f-818c-9f4d57d03125"
      },
      {
        "object": "related_card",
        "id": "a4861c8d-5e4a-4c4b-854c-410aad2d49cb",
        "component": "combo_piece",
        "name": "Nearheath Chaplain",
        "type_line": "Creature \u2014 Human Cleric",
        "uri": "https://api.scryfall.com/cards/a4861c8d-5e4a-4c4b-854c-410aad2d49cb"
      },
      {
        "object": "related_card",
        "id": "d2709d91-4235-482c-b9b3-ac5d61cb5bcb",
        "component": "combo_piece",
        "name": "Oath of the Grey Host",
        "type_line": "Enchantment \u2014 Saga",
        "uri": "https://api.scryfall.com/cards/d2709d91-4235-482c-b9b3-ac5d61cb5bcb"
      },
      {
        "object": "related_card",
        "id": "d7953153-e7da-4e3d-a962-eb57b726aaf0",
        "component": "combo_piece",
        "name": "Ethereal Investigator",
        "type_line": "Creature \u2014 Spirit",
        "uri": "https://api.scryfall.com/cards/d7953153-e7da-4e3d-a962-eb57b726aaf0"
      },
      {
        "object": "related_card",
        "id": "a3f29cbb-d802-4085-a236-86775764bc9e",
        "component": "combo_piece",
        "name": "Whispering Wizard",
        "type_line": "Creature \u2014 Human Wizard",
        "uri": "https://api.scryfall.com/cards/a3f29cbb-d802-4085-a236-86775764bc9e"
      },
      {
        "object": "related_card",
        "id": "9964629e-d79e-46e4-b3fd-e7d1759cbc60",
        "component": "combo_piece",
        "name": "Spectral Procession",
        "type_line": "Sorcery",
        "uri": "https://api.scryfall.com/cards/9964629e-d79e-46e4-b3fd-e7d1759cbc60"
      },
      {
        "object": "related_card",
        "id": "0df01c9a-5d2c-4391-99a3-f10e404b7133",
        "component": "combo_piece",
        "name": "Abzan Ascendancy",
        "type_line": "Enchantment",
        "uri": "https://api.scryfall.com/cards/0df01c9a-5d2c-4391-99a3-f10e404b7133"
      },
      {
        "object": "related_card",
        "id": "d080c35d-f2c6-4f4e-8f7c-305b319d4cde",
        "component": "combo_piece",
        "name": "Benevolent Offering",
        "type_line": "Instant",
        "uri": "https://api.scryfall.com/cards/d080c35d-f2c6-4f4e-8f7c-305b319d4cde"
      },
      {
        "object": "related_card",
        "id": "c630a2ba-9009-4463-91f8-a0eb4af3c1b0",
        "component": "combo_piece",
        "name": "King of the Oathbreakers",
        "type_line": "Legendary Creature \u2014 Spirit Noble",
        "uri": "https://api.scryfall.com/cards/c630a2ba-9009-4463-91f8-a0eb4af3c1b0"
      },
      {
        "object": "related_card",
        "id": "1b302947-5d66-425d-b67e-bf1d5846d490",
        "component": "combo_piece",
        "name": "Nurturing Presence",
        "type_line": "Enchantment \u2014 Aura",
        "uri": "https://api.scryfall.com/cards/1b302947-5d66-425d-b67e-bf1d5846d490"
      },
      {
        "object": "related_card",
        "id": "c539c201-64c2-475c-b934-8a738d071b02",
        "component": "combo_piece",
        "name": "Summoner's Sending",
        "type_line": "Enchantment",
        "uri": "https://api.scryfall.com/cards/c539c201-64c2-475c-b934-8a738d071b02"
      },
      {
        "object": "related_card",
        "id": "05c90b56-6e4b-43d1-886d-a6d78da7a586",
        "component": "combo_piece",
        "name": "Triplicate Spirits",
        "type_line": "Sorcery",
        "uri": "https://api.scryfall.com/cards/05c90b56-6e4b-43d1-886d-a6d78da7a586"
      },
      {
        "object": "related_card",
        "id": "f18f726e-3bf2-436c-95cb-f7b4a10f18f6",
        "component": "combo_piece",
        "name": "Afterlife",
        "type_line": "Instant",
        "uri": "https://api.scryfall.com/cards/f18f726e-3bf2-436c-95cb-f7b4a10f18f6"
      },
      {
        "object": "related_card",
        "id": "a264d5f2-9e27-4c41-a76e-0dc944c6dc74",
        "component": "combo_piece",
        "name": "Field of Souls",
        "type_line": "Enchantment",
        "uri": "https://api.scryfall.com/cards/a264d5f2-9e27-4c41-a76e-0dc944c6dc74"
      },
      {
        "object": "related_card",
        "id": "fbbbbbf7-eaae-462e-a8eb-7f6a97703600",
        "component": "combo_piece",
        "name": "Kirtar's Wrath",
        "type_line": "Sorcery",
        "uri": "https://api.scryfall.com/cards/fbbbbbf7-eaae-462e-a8eb-7f6a97703600"
      },
      {
        "object": "related_card",
        "id": "df8bbd04-981e-45ec-a835-7237350630cf",
        "component": "combo_piece",
        "name": "Moorland Haunt",
        "type_line": "Land",
        "uri": "https://api.scryfall.com/cards/df8bbd04-981e-45ec-a835-7237350630cf"
      },
      {
        "object": "related_card",
        "id": "dc8037d5-79fa-47e3-9d3b-eb29643ecae7",
        "component": "combo_piece",
        "name": "Hallowed Spiritkeeper",
        "type_line": "Creature \u2014 Avatar",
        "uri": "https://api.scryfall.com/cards/dc8037d5-79fa-47e3-9d3b-eb29643ecae7"
      },
      {
        "object": "related_card",
        "id": "ddcb90f4-82c0-412c-9e90-9fffc8c5df10",
        "component": "combo_piece",
        "name": "Requiem Angel",
        "type_line": "Creature \u2014 Angel",
        "uri": "https://api.scryfall.com/cards/ddcb90f4-82c0-412c-9e90-9fffc8c5df10"
      },
      {
        "object": "related_card",
        "id": "7618aa2d-d5b3-41e6-978f-2c8292f7f896",
        "component": "combo_piece",
        "name": "Spectral Reserves",
        "type_line": "Sorcery",
        "uri": "https://api.scryfall.com/cards/7618aa2d-d5b3-41e6-978f-2c8292f7f896"
      },
      {
        "object": "related_card",
        "id": "849bea7e-74e5-4310-be5a-d517d7b19be6",
        "component": "combo_piece",
        "name": "Mausoleum Guard",
        "type_line": "Creature \u2014 Human Scout",
        "uri": "https://api.scryfall.com/cards/849bea7e-74e5-4310-be5a-d517d7b19be6"
      },
      {
        "object": "related_card",
        "id": "add661e7-b337-44e4-9614-ca958e20e86f",
        "component": "combo_piece",
        "name": "Occult Epiphany",
        "type_line": "Instant",
        "uri": "https://api.scryfall.com/cards/add661e7-b337-44e4-9614-ca958e20e86f"
      },
      {
        "object": "related_card",
        "id": "2791a28a-30fa-4f1a-9f05-f3db155b6f06",
        "component": "combo_piece",
        "name": "Hanged Executioner",
        "type_line": "Creature \u2014 Spirit",
        "uri": "https://api.scryfall.com/cards/2791a28a-30fa-4f1a-9f05-f3db155b6f06"
      },
      {
        "object": "related_card",
        "id": "5345d199-79e5-466b-85f3-365f6e39457d",
        "component": "combo_piece",
        "name": "Millicent, Restless Revenant",
        "type_line": "Legendary Creature \u2014 Spirit Soldier",
        "uri": "https://api.scryfall.com/cards/5345d199-79e5-466b-85f3-365f6e39457d"
      },
      {
        "object": "related_card",
        "id": "013fdf2d-8fa5-4d84-9a4d-e39dbed1c31b",
        "component": "combo_piece",
        "name": "Kykar, Wind's Fury",
        "type_line": "Legendary Creature \u2014 Bird Wizard",
        "uri": "https://api.scryfall.com/cards/013fdf2d-8fa5-4d84-9a4d-e39dbed1c31b"
      },
      {
        "object": "related_card",
        "id": "6fbc9abd-8719-4cea-8bf4-1a3d78e3f00b",
        "component": "combo_piece",
        "name": "Priest of the Blessed Graf",
        "type_line": "Creature \u2014 Human Cleric",
        "uri": "https://api.scryfall.com/cards/6fbc9abd-8719-4cea-8bf4-1a3d78e3f00b"
      },
      {
        "object": "related_card",
        "id": "f8cd8b55-2927-4e53-be1e-cc33c35f85b7",
        "component": "combo_piece",
        "name": "Thalisse, Reverent Medium",
        "type_line": "Legendary Creature \u2014 Human Cleric",
        "uri": "https://api.scryfall.com/cards/f8cd8b55-2927-4e53-be1e-cc33c35f85b7"
      },
      {
        "object": "related_card",
        "id": "c9786c13-b57a-46be-bbbe-e17333defbd4",
        "component": "combo_piece",
        "name": "Sanctifier of Souls",
        "type_line": "Creature \u2014 Human Cleric",
        "uri": "https://api.scryfall.com/cards/c9786c13-b57a-46be-bbbe-e17333defbd4"
      },
      {
        "object": "related_card",
        "id": "783a4c53-c006-46d7-bca6-cd9e12f0da13",
        "component": "combo_piece",
        "name": "Teysa, Orzhov Scion",
        "type_line": "Legendary Creature \u2014 Human Advisor",
        "uri": "https://api.scryfall.com/cards/783a4c53-c006-46d7-bca6-cd9e12f0da13"
      },
      {
        "object": "related_card",
        "id": "219dd7c5-0d8f-46a2-9181-3ed30d489397",
        "component": "combo_piece",
        "name": "Avacyn's Collar",
        "type_line": "Artifact \u2014 Equipment",
        "uri": "https://api.scryfall.com/cards/219dd7c5-0d8f-46a2-9181-3ed30d489397"
      },
      {
        "object": "related_card",
        "id": "83632e73-be3f-43fc-932f-45cb1af4f8fb",
        "component": "combo_piece",
        "name": "Valor of the Worthy",
        "type_line": "Enchantment \u2014 Aura",
        "uri": "https://api.scryfall.com/cards/83632e73-be3f-43fc-932f-45cb1af4f8fb"
      },
      {
        "object": "related_card",
        "id": "4205f8f8-7b18-4999-ac51-860fab376d79",
        "component": "combo_piece",
        "name": "Brine Comber // Brinebound Gift",
        "type_line": "Creature \u2014 Spirit // Enchantment \u2014 Aura",
        "uri": "https://api.scryfall.com/cards/4205f8f8-7b18-4999-ac51-860fab376d79"
      },
      {
        "object": "related_card",
        "id": "c3ac419f-7630-48c7-9039-88ce28898b6d",
        "component": "combo_piece",
        "name": "Luminous Angel",
        "type_line": "Creature \u2014 Angel",
        "uri": "https://api.scryfall.com/cards/c3ac419f-7630-48c7-9039-88ce28898b6d"
      },
      {
        "object": "related_card",
        "id": "29bf245f-e8e0-4d32-8cd7-06d832609910",
        "component": "combo_piece",
        "name": "Seize the Soul",
        "type_line": "Instant",
        "uri": "https://api.scryfall.com/cards/29bf245f-e8e0-4d32-8cd7-06d832609910"
      },
      {
        "object": "related_card",
        "id": "3a79a435-9b58-4bcd-8544-79d9a71d85a2",
        "component": "combo_piece",
        "name": "Heron-Blessed Geist",
        "type_line": "Creature \u2014 Spirit",
        "uri": "https://api.scryfall.com/cards/3a79a435-9b58-4bcd-8544-79d9a71d85a2"
      },
      {
        "object": "related_card",
        "id": "8a03d414-bff9-4aba-8b0a-0ed57982251e",
        "component": "combo_piece",
        "name": "Doomed Traveler",
        "type_line": "Creature \u2014 Human Soldier",
        "uri": "https://api.scryfall.com/cards/8a03d414-bff9-4aba-8b0a-0ed57982251e"
      },
      {
        "object": "related_card",
        "id": "eddc09d1-63de-4791-b654-31b354032c54",
        "component": "combo_piece",
        "name": "Midnight Haunting",
        "type_line": "Instant",
        "uri": "https://api.scryfall.com/cards/eddc09d1-63de-4791-b654-31b354032c54"
      },
      {
        "object": "related_card",
        "id": "a36ab7fa-7b90-4ccc-8fe9-93453f10a237",
        "component": "combo_piece",
        "name": "Drogskol Cavalry",
        "type_line": "Creature \u2014 Spirit Knight",
        "uri": "https://api.scryfall.com/cards/a36ab7fa-7b90-4ccc-8fe9-93453f10a237"
      },
      {
        "object": "related_card",
        "id": "9b0f860c-029c-4856-a999-05b3306c7d46",
        "component": "combo_piece",
        "name": "Spirit Cairn",
        "type_line": "Enchantment",
        "uri": "https://api.scryfall.com/cards/9b0f860c-029c-4856-a999-05b3306c7d46"
      },
      {
        "object": "related_card",
        "id": "c369d381-b48e-43cf-a032-8bcb120f443e",
        "component": "combo_piece",
        "name": "Bishop of Wings",
        "type_line": "Creature \u2014 Human Cleric",
        "uri": "https://api.scryfall.com/cards/c369d381-b48e-43cf-a032-8bcb120f443e"
      },
      {
        "object": "related_card",
        "id": "481b1eb5-9fbb-4e27-8d0a-5ca6c34179b6",
        "component": "combo_piece",
        "name": "Twilight Drover",
        "type_line": "Creature \u2014 Spirit",
        "uri": "https://api.scryfall.com/cards/481b1eb5-9fbb-4e27-8d0a-5ca6c34179b6"
      },
      {
        "object": "related_card",
        "id": "97c4288f-7d22-4a5f-9b2e-d67734d9a6e7",
        "component": "combo_piece",
        "name": "Path of the Ghosthunter",
        "type_line": "Sorcery",
        "uri": "https://api.scryfall.com/cards/97c4288f-7d22-4a5f-9b2e-d67734d9a6e7"
      },
      {
        "object": "related_card",
        "id": "71398076-a0ff-4bc5-b141-25dfaebe0d53",
        "component": "combo_piece",
        "name": "Shadow Summoning",
        "type_line": "Sorcery",
        "uri": "https://api.scryfall.com/cards/71398076-a0ff-4bc5-b141-25dfaebe0d53"
      },
      {
        "object": "related_card",
        "id": "f07dd0f1-b80b-4af0-ae76-907ec55ec7d5",
        "component": "combo_piece",
        "name": "March of Souls",
        "type_line": "Sorcery",
        "uri": "https://api.scryfall.com/cards/f07dd0f1-b80b-4af0-ae76-907ec55ec7d5"
      },
      {
        "object": "related_card",
        "id": "87673b63-cacb-43b3-8723-924a7d5aed0c",
        "component": "combo_piece",
        "name": "Confront the Assault",
        "type_line": "Instant",
        "uri": "https://api.scryfall.com/cards/87673b63-cacb-43b3-8723-924a7d5aed0c"
      },
      {
        "object": "related_card",
        "id": "f4051020-688c-473a-9a08-b62f0fd75675",
        "component": "combo_piece",
        "name": "Vessel of Ephemera",
        "type_line": "Enchantment",
        "uri": "https://api.scryfall.com/cards/f4051020-688c-473a-9a08-b62f0fd75675"
      },
      {
        "object": "related_card",
        "id": "35f8d43a-a62a-433a-afd3-a3b16ba7cb10",
        "component": "combo_piece",
        "name": "Dauntless Cathar",
        "type_line": "Creature \u2014 Human Soldier",
        "uri": "https://api.scryfall.com/cards/35f8d43a-a62a-433a-afd3-a3b16ba7cb10"
      },
      {
        "object": "related_card",
        "id": "1c8c41dd-8551-4ce8-a9be-9b9f65718852",
        "component": "combo_piece",
        "name": "Ranar the Ever-Watchful",
        "type_line": "Legendary Creature \u2014 Spirit Warrior",
        "uri": "https://api.scryfall.com/cards/1c8c41dd-8551-4ce8-a9be-9b9f65718852"
      },
      {
        "object": "related_card",
        "id": "6a0dd7ba-673e-4f69-8cd3-806784501dc2",
        "component": "combo_piece",
        "name": "Custodi Soulbinders",
        "type_line": "Creature \u2014 Human Cleric",
        "uri": "https://api.scryfall.com/cards/6a0dd7ba-673e-4f69-8cd3-806784501dc2"
      },
      {
        "object": "related_card",
        "id": "f699f8d9-8708-44ca-8d14-1ca93aa68c9e",
        "component": "combo_piece",
        "name": "Alharu, Solemn Ritualist",
        "type_line": "Legendary Creature \u2014 Human Monk",
        "uri": "https://api.scryfall.com/cards/f699f8d9-8708-44ca-8d14-1ca93aa68c9e"
      },
      {
        "object": "related_card",
        "id": "0000a54c-a511-4925-92dc-01b937f9afad",
        "component": "token",
        "name": "Spirit",
        "type_line": "Token Creature \u2014 Spirit",
        "uri": "https://api.scryfall.com/cards/0000a54c-a511-4925-92dc-01b937f9afad"
      },
      {
        "object": "related_card",
        "id": "55882138-83a2-4a0a-96b0-6d5150edc4e3",
        "component": "combo_piece",
        "name": "Clarion Spirit",
        "type_line": "Creature \u2014 Spirit",
        "uri": "https://api.scryfall.com/cards/55882138-83a2-4a0a-96b0-6d5150edc4e3"
      },
      {
        "object": "related_card",
        "id": "52faa78e-252e-465b-91b5-6f64d828da81",
        "component": "combo_piece",
        "name": "Kaya, Geist Hunter",
        "type_line": "Legendary Planeswalker \u2014 Kaya",
        "uri": "https://api.scryfall.com/cards/52faa78e-252e-465b-91b5-6f64d828da81"
      },
      {
        "object": "related_card",
        "id": "05860b72-fb1b-44d8-9275-12863724a9ef",
        "component": "combo_piece",
        "name": "Not Forgotten",
        "type_line": "Sorcery",
        "uri": "https://api.scryfall.com/cards/05860b72-fb1b-44d8-9275-12863724a9ef"
      },
      {
        "object": "related_card",
        "id": "4d09ef1d-3552-43a3-91c7-0d14c0f06780",
        "component": "combo_piece",
        "name": "Geist-Honored Monk",
        "type_line": "Creature \u2014 Human Monk",
        "uri": "https://api.scryfall.com/cards/4d09ef1d-3552-43a3-91c7-0d14c0f06780"
      },
      {
        "object": "related_card",
        "id": "1b7a47cc-9311-4f92-b19c-8956db5f2b5f",
        "component": "combo_piece",
        "name": "Rousing of Souls",
        "type_line": "Sorcery",
        "uri": "https://api.scryfall.com/cards/1b7a47cc-9311-4f92-b19c-8956db5f2b5f"
      },
      {
        "object": "related_card",
        "id": "7ebd275e-f097-448c-aba3-eab8ee8c9a8c",
        "component": "combo_piece",
        "name": "And\u00faril, Flame of the West",
        "type_line": "Legendary Artifact \u2014 Equipment",
        "uri": "https://api.scryfall.com/cards/7ebd275e-f097-448c-aba3-eab8ee8c9a8c"
      },
      {
        "object": "related_card",
        "id": "b3e98964-e1ce-40ba-be0d-27e39e724074",
        "component": "combo_piece",
        "name": "Haunted Library",
        "type_line": "Enchantment",
        "uri": "https://api.scryfall.com/cards/b3e98964-e1ce-40ba-be0d-27e39e724074"
      },
      {
        "object": "related_card",
        "id": "c342e1da-7ab9-4e29-96e6-77d820a45ede",
        "component": "combo_piece",
        "name": "Elgaud Inquisitor",
        "type_line": "Creature \u2014 Human Cleric",
        "uri": "https://api.scryfall.com/cards/c342e1da-7ab9-4e29-96e6-77d820a45ede"
      },
      {
        "object": "related_card",
        "id": "4531482d-9238-40de-957e-61beb5700330",
        "component": "combo_piece",
        "name": "Thalia's Geistcaller",
        "type_line": "Creature \u2014 Human Cleric",
        "uri": "https://api.scryfall.com/cards/4531482d-9238-40de-957e-61beb5700330"
      },
      {
        "object": "related_card",
        "id": "a37510bb-245c-47bc-bbf3-2b202b67d383",
        "component": "combo_piece",
        "name": "Muster the Departed",
        "type_line": "Enchantment",
        "uri": "https://api.scryfall.com/cards/a37510bb-245c-47bc-bbf3-2b202b67d383"
      },
      {
        "object": "related_card",
        "id": "cc5fa496-a830-4031-a19a-d6467d074ad1",
        "component": "combo_piece",
        "name": "Emissary of the Sleepless",
        "type_line": "Creature \u2014 Spirit",
        "uri": "https://api.scryfall.com/cards/cc5fa496-a830-4031-a19a-d6467d074ad1"
      },
      {
        "object": "related_card",
        "id": "aa2a3aaa-e78a-48cc-b7d3-7f65e467054c",
        "component": "combo_piece",
        "name": "Spirit Bonds",
        "type_line": "Enchantment",
        "uri": "https://api.scryfall.com/cards/aa2a3aaa-e78a-48cc-b7d3-7f65e467054c"
      },
      {
        "object": "related_card",
        "id": "2f28187b-2c99-4502-99d5-3a53ff3fa008",
        "component": "combo_piece",
        "name": "Transluminant",
        "type_line": "Creature \u2014 Dryad Shaman",
        "uri": "https://api.scryfall.com/cards/2f28187b-2c99-4502-99d5-3a53ff3fa008"
      },
      {
        "object": "related_card",
        "id": "dc098d5b-0cdb-422f-8bd2-7afd81a7b7c3",
        "component": "combo_piece",
        "name": "Court of Grace",
        "type_line": "Enchantment",
        "uri": "https://api.scryfall.com/cards/dc098d5b-0cdb-422f-8bd2-7afd81a7b7c3"
      },
      {
        "object": "related_card",
        "id": "3e2137fe-5e92-442e-b22a-473c5a669308",
        "component": "combo_piece",
        "name": "Sandsteppe Outcast",
        "type_line": "Creature \u2014 Human Warrior",
        "uri": "https://api.scryfall.com/cards/3e2137fe-5e92-442e-b22a-473c5a669308"
      }
    ],
    "legalities": {
      "standard": "not_legal",
      "future": "not_legal",
      "historic": "not_legal",
      "timeless": "not_legal",
      "gladiator": "not_legal",
      "pioneer": "not_legal",
      "modern": "not_legal",
      "legacy": "not_legal",
      "pauper": "not_legal",
      "vintage": "not_legal",
      "penny": "not_legal",
      "commander": "not_legal",
      "oathbreaker": "not_legal",
      "standardbrawl": "not_legal",
      "brawl": "not_legal",
      "alchemy": "not_legal",
      "paupercommander": "not_legal",
      "duel": "not_legal",
      "oldschool": "not_legal",
      "premodern": "not_legal",
      "predh": "not_legal"
    },
    "games": [
      "paper"
    ],
    "reserved": false,
    "game_changer": false,
    "foil": false,
    "nonfoil": true,
    "finishes": [
      "nonfoil"
    ],
    "oversized": false,
    "promo": false,
    "reprint": true,
    "variation": false,
    "set_id": "f7aa47c6-c1e2-4de5-9a68-4406d84bd6bb",
    "set": "tmm2",
    "set_name": "Modern Masters 2015 Tokens",
    "set_type": "token",
    "set_uri": "https://api.scryfall.com/sets/f7aa47c6-c1e2-4de5-9a68-4406d84bd6bb",
    "set_search_uri": "https://api.scryfall.com/cards/search?order=set&q=e%3Atmm2&unique=prints",
    "scryfall_set_uri": "https://scryfall.com/sets/tmm2?utm_source=api",
    "rulings_uri": "https://api.scryfall.com/cards/0000a54c-a511-4925-92dc-01b937f9afad/rulings",
    "prints_search_uri": "https://api.scryfall.com/cards/search?order=released&q=oracleid%3Adc4e2134-f0c2-49aa-9ea3-ebf83af1445c&unique=prints",
    "collector_number": "5",
    "digital": false,
    "rarity": "common",
    "card_back_id": "0aeebaf5-8c7d-4636-9e82-8c27447861f7",
    "artist": "Mike Sass",
    "artist_ids": [
      "155bc2cb-038d-4b1f-9990-6178db1d1a21"
    ],
    "illustration_id": "1dbe0618-dd47-442c-acf6-ac5e4b136e5a",
    "border_color": "black",
    "frame": "2015",
    "full_art": false,
    "textless": false,
    "booster": true,
    "story_spotlight": false,
    "promo_types": [
      "setpromo"
    ],
    "prices": {
      "usd": "0.10",
      "usd_foil": null,
      "usd_etched": null,
      "eur": null,
      "eur_foil": null,
      "tix": null
    },
    "related_uris": {
      "tcgplayer_infinite_articles": "https://partner.tcgplayer.com/c/4931599/1830156/21018?subId1=api&trafcat=tcgplayer.com%2Fsearch%2Farticles&u=https%3A%2F%2Fwww.tcgplayer.com%2Fsearch%2Farticles%3FproductLineName%3Dmagic%26q%3DSpirit",
      "tcgplayer_infinite_decks": "https://partner.tcgplayer.com/c/4931599/1830156/21018?subId1=api&trafcat=tcgplayer.com%2Fsearch%2Fdecks&u=https%3A%2F%2Fwww.tcgplayer.com%2Fsearch%2Fdecks%3FproductLineName%3Dmagic%26q%3DSpirit",
      "edhrec": "https://edhrec.com/route/?cc=Spirit"
    },
    "purchase_uris": {
      "tcgplayer": "https://partner.tcgplayer.com/c/4931599/1830156/21018?subId1=api&u=https%3A%2F%2Fwww.tcgplayer.com%2Fproduct%2F98659%3Fpage%3D1",
      "cardmarket": "https://www.cardmarket.com/en/Magic/Products/Search?referrer=scryfall&searchString=Spirit&utm_campaign=card_prices&utm_medium=text&utm_source=scryfall",
      "cardhoarder": "https://www.cardhoarder.com/cards?affiliate_id=scryfall&data%5Bsearch%5D=Spirit&ref=card-profile&utm_campaign=affiliate&utm_medium=card&utm_source=scryfall"
    }
  },
  {
    "object": "card",
    "id": "0000cd57-91fe-411f-b798-646e965eec37",
    "oracle_id": "9f0d82ae-38bf-45d8-8cda-982b6ead1d72",
    "multiverse_ids": [
      435231
    ],
    "mtgo_id": 65170,
    "mtgo_foil_id": 65171,
    "arena_id": 66119,
    "tcgplayer_id": 145764,
    "cardmarket_id": 301766,
    "name": "Siren Lookout",
    "lang": "en",
    "released_at": "2017-09-29",
    "uri": "https://api.scryfall.com/cards/0000cd57-91fe-411f-b798-646e965eec37",
    "scryfall_uri": "https://scryfall.com/card/xln/78/siren-lookout?utm_source=api",
    "layout": "normal",
    "highres_image": true,
    "image_status": "highres_scan",
    "image_uris": {
      "small": "https://cards.scryfall.io/small/front/0/0/0000cd57-91fe-411f-b798-646e965eec37.jpg?1562549609",
      "normal": "https://cards.scryfall.io/normal/front/0/0/0000cd57-91fe-411f-b798-646e965eec37.jpg?1562549609",
      "large": "https://cards.scryfall.io/large/front/0/0/0000cd57-91fe-411f-b798-646e965eec37.jpg?1562549609",
      "png": "https://cards.scryfall.io/png/front/0/0/0000cd57-91fe-411f-b798-646e965eec37.png?1562549609",
      "art_crop": "https://cards.scryfall.io/art_crop/front/0/0/0000cd57-91fe-411f-b798-646e965eec37.jpg?1562549609",
      "border_crop": "https://cards.scryfall.io/border_crop/front/0/0/0000cd57-91fe-411f-b798-646e965eec37.jpg?1562549609"
    },
    "mana_cost": "{2}{U}",
    "cmc": 3.0,
    "type_line": "Creature \u2014 Siren Pirate",
    "oracle_text": "Flying\nWhen this creature enters, it explores. (Reveal the top card of your library. Put that card into your hand if it's a land. Otherwise, put a +1/+1 counter on this creature, then put the card back or put it into your graveyard.)",
    "power": "1",
    "toughness": "2",
    "colors": [
      "U"
    ],
    "color_identity": [
      "U"
    ],
    "keywords": [
      "Flying",
      "Explore"
    ],
    "legalities": {
      "standard": "not_legal",
      "future": "not_legal",
      "historic": "legal",
      "timeless": "legal",
      "gladiator": "legal",
      "pioneer": "legal",
      "modern": "legal",
      "legacy": "legal",
      "pauper": "legal",
      "vintage": "legal",
      "penny": "legal",
      "commander": "legal",
      "oathbreaker": "legal",
      "standardbrawl": "not_legal",
      "brawl": "legal",
      "alchemy": "not_legal",
      "paupercommander": "legal",
      "duel": "legal",
      "oldschool": "not_legal",
      "premodern": "not_legal",
      "predh": "not_legal"
    },
    "games": [
      "arena",
      "paper",
      "mtgo"
    ],
    "reserved": false,
    "game_changer": false,
    "foil": true,
    "nonfoil": true,
    "finishes": [
      "nonfoil",
      "foil"
    ],
    "oversized": false,
    "promo": false,
    "reprint": false,
    "variation": false,
    "set_id": "fe0dad85-54bc-4151-9200-d68da84dd0f2",
    "set": "xln",
    "set_name": "Ixalan",
    "set_type": "expansion",
    "set_uri": "https://api.scryfall.com/sets/fe0dad85-54bc-4151-9200-d68da84dd0f2",
    "set_search_uri": "https://api.scryfall.com/cards/search?order=set&q=e%3Axln&unique=prints",
    "scryfall_set_uri": "https://scryfall.com/sets/xln?utm_source=api",
    "rulings_uri": "https://api.scryfall.com/cards/0000cd57-91fe-411f-b798-646e965eec37/rulings",
    "prints_search_uri": "https://api.scryfall.com/cards/search?order=released&q=oracleid%3A9f0d82ae-38bf-45d8-8cda-982b6ead1d72&unique=prints",
    "collector_number": "78",
    "digital": false,
    "rarity": "common",
    "card_back_id": "0aeebaf5-8c7d-4636-9e82-8c27447861f7",
    "artist": "Chris Rallis",
    "artist_ids": [
      "a8e7b854-b15a-421a-b66d-6e68187ae285"
    ],
    "illustration_id": "e0a40a54-9216-4c86-b9e3-daed04abc310",
    "border_color": "black",
    "frame": "2015",
    "full_art": false,
    "textless": false,
    "booster": true,
    "story_spotlight": false,
    "edhrec_rank": 17493,
    "penny_rank": 13352,
    "prices": {
      "usd": "0.04",
      "usd_foil": "0.30",
      "usd_etched": null,
      "eur": "0.02",
      "eur_foil": "0.17",
      "tix": "0.03"
    },
    "related_uris": {
      "gatherer": "https://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=435231&printed=false",
      "tcgplayer_infinite_articles": "https://partner.tcgplayer.com/c/4931599/1830156/21018?subId1=api&trafcat=tcgplayer.com%2Fsearch%2Farticles&u=https%3A%2F%2Fwww.tcgplayer.com%2Fsearch%2Farticles%3FproductLineName%3Dmagic%26q%3DSiren%2BLookout",
      "tcgplayer_infinite_decks": "https://partner.tcgplayer.com/c/4931599/1830156/21018?subId1=api&trafcat=tcgplayer.com%2Fsearch%2Fdecks&u=https%3A%2F%2Fwww.tcgplayer.com%2Fsearch%2Fdecks%3FproductLineName%3Dmagic%26q%3DSiren%2BLookout",
      "edhrec": "https://edhrec.com/route/?cc=Siren+Lookout"
    },
    "purchase_uris": {
      "tcgplayer": "https://partner.tcgplayer.com/c/4931599/1830156/21018?subId1=api&u=https%3A%2F%2Fwww.tcgplayer.com%2Fproduct%2F145764%3Fpage%3D1",
      "cardmarket": "https://www.cardmarket.com/en/Magic/Products?idProduct=301766&referrer=scryfall&utm_campaign=card_prices&utm_medium=text&utm_source=scryfall",
      "cardhoarder": "https://www.cardhoarder.com/cards/65170?affiliate_id=scryfall&ref=card-profile&utm_campaign=affiliate&utm_medium=card&utm_source=scryfall"
    }
  },
  {
    "object": "card",
    "id": "00012bd8-ed68-4978-a22d-f450c8a6e048",
    "oracle_id": "5aa12aff-db3c-4be5-822b-3afdf536b33e",
    "multiverse_ids": [
      1278
    ],
    "tcgplayer_id": 1623,
    "cardmarket_id": 5664,
    "name": "Web",
    "lang": "en",
    "released_at": "1994-04-11",
    "uri": "https://api.scryfall.com/cards/00012bd8-ed68-4978-a22d-f450c8a6e048",
    "scryfall_uri": "https://scryfall.com/card/3ed/229/web?utm_source=api",
    "layout": "normal",
    "highres_image": true,
    "image_status": "highres_scan",
    "image_uris": {
      "small": "https://cards.scryfall.io/small/front/0/0/00012bd8-ed68-4978-a22d-f450c8a6e048.jpg?1559596693",
      "normal": "https://cards.scryfall.io/normal/front/0/0/00012bd8-ed68-4978-a22d-f450c8a6e048.jpg?1559596693",
      "large": "https://cards.scryfall.io/large/front/0/0/00012bd8-ed68-4978-a22d-f450c8a6e048.jpg?1559596693",
      "png": "https://cards.scryfall.io/png/front/0/0/00012bd8-ed68-4978-a22d-f450c8a6e048.png?1559596693",
      "art_crop": "https://cards.scryfall.io/art_crop/front/0/0/00012bd8-ed68-4978-a22d-f450c8a6e048.jpg?1559596693",
      "border_crop": "https://cards.scryfall.io/border_crop/front/0/0/00012bd8-ed68-4978-a22d-f450c8a6e048.jpg?1559596693"
    },
    "mana_cost": "{G}",
    "cmc": 1.0,
    "type_line": "Enchantment \u2014 Aura",
    "oracle_text": "Enchant creature (Target a creature as you cast this. This card enters attached to that creature.)\nEnchanted creature gets +0/+2 and has reach. (It can block creatures with flying.)",
    "colors": [
      "G"
    ],
    "color_identity": [
      "G"
    ],
    "keywords": [
      "Enchant"
    ],
    "legalities": {
      "standard": "not_legal",
      "future": "not_legal",
      "historic": "not_legal",
      "timeless": "not_legal",
      "gladiator": "not_legal",
      "pioneer": "not_legal",
      "modern": "legal",
      "legacy": "legal",
      "pauper": "not_legal",
      "vintage": "legal",
      "penny": "legal",
      "commander": "legal",
      "oathbreaker": "legal",
      "standardbrawl": "not_legal",
      "brawl": "not_legal",
      "alchemy": "not_legal",
      "paupercommander": "not_legal",
      "duel": "legal",
      "oldschool": "legal",
      "premodern": "legal",
      "predh": "legal"
    },
    "games": [
      "paper"
    ],
    "reserved": false,
    "game_changer": false,
    "foil": false,
    "nonfoil": true,
    "finishes": [
      "nonfoil"
    ],
    "oversized": false,
    "promo": false,
    "reprint": true,
    "variation": false,
    "set_id": "45a69797-8adf-468e-a4e1-ba81fd9d66ac",
    "set": "3ed",
    "set_name": "Revised Edition",
    "set_type": "core",
    "set_uri": "https://api.scryfall.com/sets/45a69797-8adf-468e-a4e1-ba81fd9d66ac",
    "set_search_uri": "https://api.scryfall.com/cards/search?order=set&q=e%3A3ed&unique=prints",
    "scryfall_set_uri": "https://scryfall.com/sets/3ed?utm_source=api",
    "rulings_uri": "https://api.scryfall.com/cards/00012bd8-ed68-4978-a22d-f450c8a6e048/rulings",
    "prints_search_uri": "https://api.scryfall.com/cards/search?order=released&q=oracleid%3A5aa12aff-db3c-4be5-822b-3afdf536b33e&unique=prints",
    "collector_number": "229",
    "digital": false,
    "rarity": "rare",
    "card_back_id": "0aeebaf5-8c7d-4636-9e82-8c27447861f7",
    "artist": "Rob Alexander",
    "artist_ids": [
      "35906871-6c78-4ab2-9ed1-e6792c8efb74"
    ],
    "illustration_id": "1eac4d23-2b24-4f4a-b73f-25607c13b806",
    "border_color": "white",
    "frame": "1993",
    "full_art": false,
    "textless": false,
    "booster": true,
    "story_spotlight": false,
    "edhrec_rank": 25071,
    "prices": {
      "usd": "0.77",
      "usd_foil": null,
      "usd_etched": null,
      "eur": "1.02",
      "eur_foil": null,
      "tix": null
    },
    "related_uris": {
      "gatherer": "https://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=1278&printed=false",
      "tcgplayer_infinite_articles": "https://partner.tcgplayer.com/c/4931599/1830156/21018?subId1=api&trafcat=tcgplayer.com%2Fsearch%2Farticles&u=https%3A%2F%2Fwww.tcgplayer.com%2Fsearch%2Farticles%3FproductLineName%3Dmagic%26q%3DWeb",
      "tcgplayer_infinite_decks": "https://partner.tcgplayer.com/c/4931599/1830156/21018?subId1=api&trafcat=tcgplayer.com%2Fsearch%2Fdecks&u=https%3A%2F%2Fwww.tcgplayer.com%2Fsearch%2Fdecks%3FproductLineName%3Dmagic%26q%3DWeb",
      "edhrec": "https://edhrec.com/route/?cc=Web"
    },
    "purchase_uris": {
      "tcgplayer": "https://partner.tcgplayer.com/c/4931599/1830156/21018?subId1=api&u=https%3A%2F%2Fwww.tcgplayer.com%2Fproduct%2F1623%3Fpage%3D1",
      "cardmarket": "https://www.cardmarket.com/en/Magic/Products?idProduct=5664&referrer=scryfall&utm_campaign=card_prices&utm_medium=text&utm_source=scryfall",
      "cardhoarder": "https://www.cardhoarder.com/cards?affiliate_id=scryfall&data%5Bsearch%5D=Web&ref=card-profile&utm_campaign=affiliate&utm_medium=card&utm_source=scryfall"
    }
  }
]"""
        s3_client = MagicMock()
        file_name = "prices-202507180900.json"
        # Call the function
        transform_card_data(json.loads(data), s3_client, file_name)
        # Assert put_object was called
        s3_client.put_object.assert_called()


if __name__ == "__main__":
    unittest.main()

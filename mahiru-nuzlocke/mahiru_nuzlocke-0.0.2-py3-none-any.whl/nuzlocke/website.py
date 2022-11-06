import json
import os.path
from typing import Dict

import aiohttp_jinja2
from aiohttp import web

import jinja2

from .badges import BadgeData
from .state import NuzlockeState


class Website:
    def __init__(self, rules: Dict[str, str], state: NuzlockeState, secret: str):
        self.rules = rules
        self.state = state
        self.secret = secret
        with open('pokemon_images.json') as imagesfile:
            self.pokemon_images = json.load(imagesfile)
        self.loader = jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates"))
        self.routes = [
            web.get('/nuzlocke/rules', lambda r: self.get_rules(r)),
            web.get('/nuzlocke/display/static', lambda r: self.get_display(r)),
            web.get('/nuzlocke/display', lambda r: self.get_display_smooth(r)),
            web.put('/nuzlocke/display/game', lambda r: self.put_game(r)),
            web.put('/nuzlocke/display/pokemon', lambda r: self.put_pokemon(r)),
            web.delete('/nuzlocke/display/pokemon', lambda r: self.delete_pokemon(r)),
            web.post('/nuzlocke/display/badge', lambda r: self.post_badge(r)),
        ]

    @aiohttp_jinja2.template('rules.html')
    def get_rules(self, request: web.Request):
        return {'rules': self.rules}

    @aiohttp_jinja2.template('smooth.html')
    def get_display_smooth(self, request: web.Request):
        try:
            return {'timeout': int(request.query['timeout'])}
        except ValueError:
            pass
        except KeyError:
            pass
        return {'timeout': 5000}

    @aiohttp_jinja2.template('display.html')
    def get_display(self, request: web.Request):
        if self.state.game is None:
            return {'running': False}
        pokemons = []
        for pokemon in self.state.pokemon:
            if pokemon is None:
                pokemons.append(None)
            else:
                pokemons.append({
                    'name': pokemon,
                    'image': self.pokemon_images[pokemon]
                })
        return {
            'running': True,
            'pokemons': pokemons,
            'badges': BadgeData[self.state.game],
            'badge_progress': self.state.progress,
        }

    async def put_game(self, request: web.Request):
        secret = request.headers['X-Nuzlocke-Secret']
        if secret != self.secret:
            raise web.HTTPForbidden
        data = await request.json()
        self.state.game = data['game']
        return web.Response()

    async def put_pokemon(self, request: web.Request):
        secret = request.headers['X-Nuzlocke-Secret']
        if secret != self.secret:
            raise web.HTTPForbidden
        data = await request.json()
        slot = data['slot'] - 1
        name = data['name']
        self.state.pokemon[slot] = name
        return web.Response()

    async def delete_pokemon(self, request: web.Request):
        secret = request.headers['X-Nuzlocke-Secret']
        if secret != self.secret:
            raise web.HTTPForbidden
        data = await request.json()
        slot = data['slot'] - 1
        self.state.pokemon[slot] = None
        return web.Response()

    async def post_badge(self, request: web.Request):
        secret = request.headers['X-Nuzlocke-Secret']
        if secret != self.secret:
            raise web.HTTPForbidden
        self.state.progress += 1
        return web.Response()

import folium
from .models import Pokemon, PokemonEntity
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils import timezone

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    time_fixed = timezone.localtime()
    pokemon_entities = PokemonEntity.objects.filter(appeared_at__lt=time_fixed, disappeared_at__gt=time_fixed)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            f'media/{pokemon_entity.pokemon.image}'
        )

    pokemons = Pokemon.objects.all()
    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon.image.url,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemons = Pokemon.objects.all()
    for pokemon in pokemons:
        if pokemon.id == int(pokemon_id):
            requested_pokemon = pokemon
            next_evolution_pokemon = pokemon.next_evolutions.all()
            pokemon = {
                'title_ru': requested_pokemon.title,
                'title_en': requested_pokemon.title_en,
                'title_jp': requested_pokemon.title_jp,
                'img_url': requested_pokemon.image.url,
                'description': requested_pokemon.description,
            }
            if requested_pokemon.previous_evolution is not None:
                pokemon['previous_evolution'] = {
                    'title_ru': requested_pokemon.previous_evolution.title,
                    'pokemon_id': requested_pokemon.previous_evolution.id,
                    'img_url': requested_pokemon.previous_evolution.image.url
                }
            if next_evolution_pokemon.exists():
                next_evolution_pokemon = next_evolution_pokemon[0]
                pokemon['next_evolution'] = {
                    'title_ru': next_evolution_pokemon.title,
                    'pokemon_id': next_evolution_pokemon.id,
                    'img_url': next_evolution_pokemon.image.url
                }
            break
    else:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    time_fixed = timezone.localtime()
    pokemon_entities = PokemonEntity.objects.filter(appeared_at__lt=time_fixed, disappeared_at__gt=time_fixed)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities.filter(pokemon=requested_pokemon):
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            f'media/{pokemon_entity.pokemon.image}'
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })

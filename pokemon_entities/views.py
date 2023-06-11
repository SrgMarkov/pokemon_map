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
    pokemons = Pokemon.objects.all()
    pokemon_entities = PokemonEntity.objects.filter(appeared_at__lt=timezone.localtime(),
                                                    disappeared_at__gt=timezone.localtime())
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.Lat,
            pokemon_entity.Lon,
            f'media/{pokemon_entity.Pokemon.image}'
        )

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
    pokemon_entities = PokemonEntity.objects.filter(appeared_at__lt=timezone.localtime(),
                                                    disappeared_at__gt=timezone.localtime())

    for pokemon in pokemons:
        if pokemon.id == int(pokemon_id):
            requested_pokemon = pokemon
            pokemon = {
                'title_ru': requested_pokemon.title,
                'title_en': requested_pokemon.title_en,
                'title_jp': requested_pokemon.title_jp,
                'img_url': requested_pokemon.image.url,
                'description': requested_pokemon.description,
                }
            if requested_pokemon.parent is not None:
                pokemon['previous_evolution'] = {
                    'title_ru': requested_pokemon.parent.title,
                    'pokemon_id': requested_pokemon.parent.id,
                    'img_url': requested_pokemon.parent.image.url}
            break
    else:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')



    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities.filter(Pokemon=requested_pokemon):
        add_pokemon(
            folium_map, pokemon_entity.Lat,
            pokemon_entity.Lon,
            f'media/{pokemon_entity.Pokemon.image}'
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })

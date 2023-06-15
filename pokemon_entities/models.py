from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название (Рус)', null=True)
    title_en = models.CharField(max_length=200, verbose_name='Название (Англ)', null=True, blank=True)
    title_jp = models.CharField(max_length=200, verbose_name='Название (Яп)', null=True, blank=True)
    description = models.TextField(verbose_name='Описание', blank=True)
    image = models.ImageField(verbose_name='Изображение', blank=True)
    previous_evolution = models.ForeignKey('self',
                                           verbose_name='Из кого эволюционирует',
                                           null=True,
                                           blank=True,
                                           related_name='next_evolutions',
                                           on_delete=models.SET_NULL)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, verbose_name='Покемон', on_delete=models.CASCADE)
    lat = models.FloatField(verbose_name='широта точки появления')
    lon = models.FloatField(verbose_name='долгота точки появления')
    appeared_at = models.DateTimeField(verbose_name='Время появления', blank=True, null=True)
    disappeared_at = models.DateTimeField(verbose_name='Время исчезания', blank=True, null=True)
    level = models.IntegerField(verbose_name='Уровень', blank=True, null=True)
    health = models.IntegerField(verbose_name='Здоровье', blank=True, null=True)
    strength = models.IntegerField(verbose_name='Сила', blank=True, null=True)
    defence = models.IntegerField(verbose_name='Урон', blank=True, null=True)
    stamina = models.IntegerField(verbose_name='Выносливость', blank=True, null=True)

    def __str__(self):
        return self.pokemon.title

from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200, null=True)
    image = models.ImageField(blank=True)

    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    Lat = models.FloatField()
    Lon = models.FloatField()

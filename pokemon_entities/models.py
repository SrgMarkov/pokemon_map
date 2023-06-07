from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200, null=True)
    image = models.ImageField(blank=True)

    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    Pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    Lat = models.FloatField()
    Lon = models.FloatField()
    appeared_at = models.DateTimeField(default='')
    disappeared_at = models.DateTimeField(default='')
    Level = models.IntegerField(null=True)
    Health = models.IntegerField(null=True)
    Strength = models.IntegerField(null=True)
    Defence = models.IntegerField(null=True)
    Stamina = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.Pokemon}'

from peewee import Model, CharField, IntegerField, ForeignKeyField
from database import db
from models.country import Country


class City(Model):
    """Model representing a city."""

    name = CharField()  # Name of the city
    population = IntegerField()  # Population of the city
    country = ForeignKeyField(Country, backref="cities")  # Relationship with the Country model

    class Meta:
        """Additional configuration for the model."""
        database = db  # Database to be used

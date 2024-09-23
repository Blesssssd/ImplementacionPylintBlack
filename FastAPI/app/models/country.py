from peewee import Model, CharField
from database import db


class Country(Model):
    """Model representing a country."""

    name = CharField(unique=True)  # Name of the country, must be unique
    continent = CharField()  # Continent where the country is located

    class Meta:
        """Meta class for additional model configuration."""
        database = db  # Database to be used for this model

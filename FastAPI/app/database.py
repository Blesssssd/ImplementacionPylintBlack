from peewee import *
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Configure the database connection
db = MySQLDatabase(
    os.getenv("DB_NAME"),  # Name of the database
    user=os.getenv("DB_USER"),  # MySQL username
    password=os.getenv("DB_PASSWORD"),  # MySQL password
    host=os.getenv("DB_HOST"),  # Database host
    port=int(os.getenv("DB_PORT", 3308)),  # MySQL port (default is 3306)
)


class BaseModel(Model):
    """Base model class to define the database connection."""
    class Meta:
        database = db  # Use the configured database


class Country(BaseModel):
    """Model representing a country."""
    id = AutoField()  # Auto-incrementing ID
    name = CharField(unique=True)  # Name of the country (must be unique)
    code = CharField(max_length=3, unique=True)  # Country code (ISO 3166-1 alpha-3)
    population = IntegerField(null=True)  # Population (optional)
    area = FloatField(null=True)  # Area in square kilometers (optional)


class City(BaseModel):
    """Model representing a city."""
    id = AutoField()  # Auto-incrementing ID
    name = CharField()  # Name of the city
    country = ForeignKeyField(Country, backref="cities")  # Relationship with Country
    population = IntegerField(null=True)  # Population (optional)
    area = FloatField(null=True)  # Area in square kilometers (optional)


def connect_db():
    """Connect to the database and create it if it doesn't exist."""
    db.connect()
    # Create the database if it does not exist
    db.execute_sql(f"CREATE DATABASE IF NOT EXISTS `{db.database}`;")
    db.close()
    # Reinitialize the database connection
    db.init(db.database, user=db.user, password=db.password, host=db.host, port=db.port)
    db.connect()


def close_db():
    """Close the database connection if it is open."""
    if not db.is_closed():
        db.close()


def create_tables():
    """Create tables for the Country and City models if they do not exist."""
    with db:
        db.create_tables([Country, City], safe=True)  # Create tables safely

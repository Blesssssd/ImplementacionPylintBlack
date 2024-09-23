from fastapi import APIRouter, HTTPException
from models.city import City
from models.country import Country
from pydantic import BaseModel

router = APIRouter()


class CitySchema(BaseModel):
    """Schema for city data validation and serialization."""
    name: str  # Name of the city
    population: int  # Population of the city
    country_id: int  # ID of the associated country


@router.post("/cities/", response_model=CitySchema)
async def create_city(city: CitySchema):
    """Create a new city in the database."""
    try:
        # Retrieve the country based on the provided country_id
        country = Country.get(Country.id == city.country_id)
        # Create a new city object
        city_obj = City.create(
            name=city.name, population=city.population, country=country
        )
        return CitySchema.from_orm(city_obj)
    except Country.DoesNotExist:
        raise HTTPException(status_code=404, detail="Country not found")


@router.get("/cities/", response_model=list[CitySchema])
async def get_cities():
    """Retrieve a list of all cities."""
    cities = City.select()  # Select all city records
    return [CitySchema.from_orm(city) for city in cities]


@router.get("/cities/{city_id}", response_model=CitySchema)
async def get_city(city_id: int):
    """Retrieve a specific city by its ID."""
    try:
        city = City.get(City.id == city_id)  # Get the city by ID
        return CitySchema.from_orm(city)
    except City.DoesNotExist:
        raise HTTPException(status_code=404, detail="City not found")


@router.put("/cities/{city_id}", response_model=CitySchema)
async def update_city(city_id: int, city: CitySchema):
    """Update an existing city by its ID."""
    try:
        city_obj = City.get(City.id == city_id)  # Get the city by ID
        # Update city attributes
        city_obj.name = city.name
        city_obj.population = city.population
        city_obj.country = city.country_id
        city_obj.save()  # Save changes to the database
        return CitySchema.from_orm(city_obj)
    except City.DoesNotExist:
        raise HTTPException(status_code=404, detail="City not found")


@router.delete("/cities/{city_id}")
async def delete_city(city_id: int):
    """Delete a specific city by its ID."""
    try:
        city = City.get(City.id == city_id)  # Get the city by ID
        city.delete_instance()  # Delete the city from the database
        return {"detail": "City deleted"}
    except City.DoesNotExist:
        raise HTTPException(status_code=404, detail="City not found")

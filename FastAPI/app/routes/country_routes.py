from fastapi import APIRouter, HTTPException
from models.country import Country
from pydantic import BaseModel

router = APIRouter()


class CountrySchema(BaseModel):
    name: str
    continent: str


@router.post("/countries/", response_model=CountrySchema)
async def create_country(country: CountrySchema):
    country_obj = Country.create(name=country.name, continent=country.continent)
    return CountrySchema.from_orm(country_obj)


@router.get("/countries/", response_model=list[CountrySchema])
async def get_countries():
    countries = Country.select()
    return [CountrySchema.from_orm(country) for country in countries]


@router.get("/countries/{country_id}", response_model=CountrySchema)
async def get_country(country_id: int):
    try:
        country = Country.get(Country.id == country_id)
        return CountrySchema.from_orm(country)
    except Country.DoesNotExist:
        raise HTTPException(status_code=404, detail="Country not found")


@router.put("/countries/{country_id}", response_model=CountrySchema)
async def update_country(country_id: int, country: CountrySchema):
    try:
        country_obj = Country.get(Country.id == country_id)
        country_obj.name = country.name
        country_obj.continent = country.continent
        country_obj.save()
        return CountrySchema.from_orm(country_obj)
    except Country.DoesNotExist:
        raise HTTPException(status_code=404, detail="Country not found")


@router.delete("/countries/{country_id}")
async def delete_country(country_id: int):
    try:
        country = Country.get(Country.id == country_id)
        country.delete_instance()
        return {"detail": "Country deleted"}
    except Country.DoesNotExist:
        raise HTTPException(status_code=404, detail="Country not found")

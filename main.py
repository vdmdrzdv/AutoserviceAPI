from uuid import UUID, uuid4
from typing import Annotated

from fastapi import FastAPI, Path, Query, status
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse


class Car(BaseModel):
    id: UUID | None = None
    brand: str
    model: str
    year: int = Field(ge=1885, description="The year must be greater than 1885")
    mileage: int = Field(gt=0, description="The mileage must be greater than 0")


app = FastAPI(title='AutoServiceAPI', description='API designed to work with car service vehicles', version='1.0')
cars = [
    {
        "id": "a5759deb-480b-4224-a4a7-e35fbb8d2915",
        "brand": "Audi",
        "model": "Q3",
        "year": 2012,
        "mileage": 185000
    },
    {
        "id": "4c16fc7c-d92c-44ed-8397-083cc94e7b0f",
        "brand": "Ford",
        "model": "Maverick",
        "year": 2004,
        "mileage": 192000
    },
    {
        "id": "6c4067b2-efef-474e-a72f-1ac74a5c6c51",
        "brand": "Chevrolet",
        "model": "Tahoe",
        "year": 2015,
        "mileage": 228100
    }
]


@app.get("/cars", tags=['Cars'], summary='Get all cars from the database',
         description='Getting all information (brand, model, year, mileage) about cars from the database.')
async def get_cars():
    return cars


@app.get("/cars/{car_id}", tags=['Cars'], summary='Get a car from the database by ID',
         description='Getting all information (brand, model, year, mileage) about one car from the database by ID.')
async def get_car(car_id: Annotated[
        UUID, Path(description='Car ID in the uuid4 format', example='6c4067b2-efef-474e-a72f-1ac74a5c6c51')]):
    for car in cars:
        if car['id'] == str(car_id):
            return car
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": "The car with this ID was not found"}
    )


@app.post("/cars/add", tags=['Cars'], status_code=201, summary='Adding a new car to the database',
          description='Adding all information (brand, model, year, mileage) about one car to the database.')
async def add_car(car: Car):
    if car.id is None:
        car.id = uuid4()
    cars.append(car)
    return cars[-1]


@app.put("/cars/{car_id}", tags=['Cars'], summary='Changing car information',
         description='Changing car information (brand, model, year, mileage).')
async def change_car(car_id: Annotated[
    UUID, Path(description='Car ID in the uuid4 format', example='a5759deb-480b-4224-a4a7-e35fbb8d2915')],
                     brand: Annotated[str | None, Query(example='Audi')] = None,
                     model: Annotated[str | None, Query(example='Q3')] = None,
                     year: Annotated[int | None, Query(example='2012')] = None,
                     mileage: Annotated[
                         int | None, Query(description='Car mileage in kilometers', example='185000')] = None):
    for car in cars:
        if car['id'] == str(car_id):
            if brand is not None:
                car['brand'] = brand
            if model is not None:
                car['model'] = model
            if year is not None:
                car['year'] = year
            if mileage is not None:
                car['mileage'] = mileage
            return car
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": "The car with this ID was not found"}
    )


@app.delete("/cars/{car_id}", tags=['Cars'], summary='Delete a car from the database by ID',
            description='Deleting all information (brand, model, year, mileage) about one car from the database by ID.')
async def delete_car(car_id: Annotated[
        UUID, Path(description='Car ID in the uuid4 format', example='6c4067b2-efef-474e-a72f-1ac74a5c6c51')]):
    for car in cars:
        if car['id'] == str(car_id):
            cars.remove(car)
            return car
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": "The car with this ID was not found"}
    )

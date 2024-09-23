from fastapi import FastAPI
from routes.country_routes import router as country_router
from routes.city_routes import router as city_router
from database import connect_db, close_db, create_tables
from peewee import OperationalError

app = FastAPI()


async def lifespan(app: FastAPI):
    """Manage the lifespan of the FastAPI application."""
    try:
        connect_db()  # Connect to the database
        create_tables()  # Create necessary tables
        yield  # This allows the application to run
    except OperationalError as e:
        print(f"Error connecting to the database: {e}")  # Log the connection error
        # Here you could add additional logic to handle the error
        raise e  # Raise the error for FastAPI to handle
    finally:
        close_db()  # Ensure the database connection is closed


# Replace the app creation with the lifespan management
app = FastAPI(lifespan=lifespan)

# Include the routes for countries and cities
app.include_router(country_router, tags=["Countries"])  # Add country routes
app.include_router(city_router, tags=["Cities"])  # Add city routes


@app.get("/", tags=["Home"])
async def read_root():
    """Root endpoint that returns a welcome message."""
    return {"message": "Welcome to the Countries and Cities API"}

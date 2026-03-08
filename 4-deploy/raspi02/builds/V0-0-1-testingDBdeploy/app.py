"""
Test script to put a databast and api onto my raspberry pi. This is a test to see if I can get the database working on the pi, and if I can connect to it from my local machine. This is not the final version of the app, just a test to see if I can get the database working on the pi.
"""

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    Date
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

from datetime import date


# 1. Create SQLite database file / engine
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)

# 2. Base class for models
Base = declarative_base()

# 3. Define tables
class Recipe(Base):
    __tablename__ = "recipes"
    recipe_id = Column(Integer, primary_key=True) # PK makes it auto-incrementing, so no need to define it in the constructor
    name = Column(String, nullable=False)
    description = Column(String)
    instructions = Column(String)
    servings = Column(Integer)
    vegetarian = Column(Integer)  # 0 (False) or 1 (True)
    vegan = Column(Integer)  # 0 (False) or 1 (True)

    # "a recipe can have multiple meal_plan entries"
    # meal_plans = relationship("MealPlan", back_populates="recipe") 


# 4. Create tables in database from all tables inheriting from Base
Base.metadata.create_all(bind=engine)


# 5. Insert initial data
Session = sessionmaker(bind=engine)
session = Session()

recipe1 = Recipe(
    name="Fajitas",
    description="Fried chicken, onion, peppers and spices in a tortilla.",
    instructions="ez",
    servings=4,
    vegetarian=0,
    vegan=0
)

recipe2 = Recipe(
    name="Sausages",
    description="sausages and sweet potato",
    instructions="ez2",
    servings=2,
    vegetarian=0,
    vegan=0
)

recipe3 = Recipe(
    name="Halloumi",
    servings=2,
    vegetarian=1,
    vegan=0
)

session.add_all([recipe1, recipe2, recipe3])
session.commit()

print("Database setup complete.")


from fastapi import FastAPI

app = FastAPI()

db = session # renaming the same session to db for clarity

@app.get("/recipes")
def get_recipes():
    
    recipe_sql_return = session.query(Recipe).all()
    
    recipe_json = {}
    for r in recipe_sql_return:
        recipe_json[r.recipe_id] = {
            "name": r.name,
            "description": r.description,
            "instructions": r.instructions,
            "servings": r.servings,
            "vegetarian": r.vegetarian,
            "vegan": r.vegan
        }
    
    db.close() # close the session after use

    return recipe_json


# starting uvicorn for testing. threading to not block the notebook
import uvicorn
import threading

def run():
    uvicorn.run(app, host="0.0.0.0", port=8000)

threading.Thread(target=run).start()

# then go to http://127.0.0.1:8000/recipes, 
# as long as above host is 127.0.0.1
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from iris import run_model
from iris.database import PLANT_DF, find_similar_plants

app = FastAPI()

# Setup for templates
templates = Jinja2Templates(directory="templates")

# Static files for images
app.mount("/static", StaticFiles(directory="static"), name="static")

# List of 50 plants with images and details
plants = PLANT_DF.rename(columns={
    "Plant name": "name",
    "Description": "description",
    "Price (eur)": "price",
})
plants["image"] = (plants["name"] + ".webp")
plants = plants.to_dict('records')

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # Affiche toutes les plantes par défaut
    return templates.TemplateResponse("index.html", {"request": request, "plants": plants, "query": ""})

@app.post("/", response_class=HTMLResponse)
async def search_plants(request: Request, plant_name: str = Form(...)):
    # Filtrer les plantes en fonction du nom saisi
    filtered_plants = [
        plant for plant in plants if plant_name.lower() in plant["name"].lower()
    ]
    return templates.TemplateResponse("index.html", {"request": request, "plants": filtered_plants, "query": plant_name})

@app.get("/plant_details/{plant_name}", response_class=HTMLResponse)
async def plant_details(request: Request, plant_name: str):
    # Rechercher la plante correspondante
    plant = next((plant for plant in plants if plant["name"] == plant_name), None)
    if not plant:
        return templates.TemplateResponse(
            "404.html", {"request": request, "message": f"Plant '{plant_name}' not found."}
        )
    similar = find_similar_plants(plant["name"])
    # TODO: show similar plants below plant details
    return templates.TemplateResponse("plant_details.html", {"request": request, "plant": plant})

@app.post("/ask", response_class=HTMLResponse)
async def ask_question(request: Request, question: str = Form(...)):
    response = run_model(question)
    answer = response.content
    recommended_plants = [
        plant
        for plant in plants
        if plant["name"].lower() in answer.lower()
    ]
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "plants": recommended_plants,
            "query": "",
            "question": question,
            "answer": answer,
        },
    )

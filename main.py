from fastapi import FastAPI, File, UploadFile, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image
from app.model.model import classify_image  # Assurez-vous que ce chemin est correct
import os

app = FastAPI()

# Configurer Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

# Monter le dossier static pour servir les fichiers CSS et autres fichiers statiques
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/favicon.ico")
async def favicon():
    file_path = os.path.join(os.path.dirname(__file__), "static", "favicon.ico")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        return {"error": "Favicon not found"}

@app.post("/predict")
async def predict_image(request: Request, image: UploadFile = File(...)):
    img = Image.open(image.file)
    prediction = classify_image(img)
    return templates.TemplateResponse("predict.html", {"request": request, "prediction": prediction})



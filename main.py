from fastapi import FastAPI, File, UploadFile, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image, UnidentifiedImageError
# Assurez-vous que ce chemin est correct
from app.model.model import classify_image
import os

app = FastAPI(
    docs_url=None,       # Désactive Swagger UI
    redoc_url=None       # Désactive Redoc
)

# Configurer Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

# Monter le dossier static pour servir les fichiers CSS et autres fichiers statiques
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/favicon.ico")
async def favicon():
    file_path = os.path.join(os.path.dirname(
        __file__), "static", "favicon.ico")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        return {"error": "Favicon not found"}


@app.post("/predict")
async def predict_image(request: Request, image: UploadFile = File(...)):
    # Vérification du type MIME pour s'assurer que c'est bien une image
    if not image.content_type.startswith("image/"):
        # Redirige vers la page d'erreur avec un message
        return RedirectResponse(url="/error?message=This isn't a image, try again", status_code=303)

    try:
        # Tenter d'ouvrir l'image
        img = Image.open(image.file)
        prediction = classify_image(img)
        return templates.TemplateResponse("predict.html", {"request": request, "prediction": prediction})
    except UnidentifiedImageError:
        # Redirige vers la page d'erreur avec un message
        return RedirectResponse(url="/error?message=Corrupted.", status_code=303)


@app.get("/error")
def error_page(request: Request, message: str):
    return templates.TemplateResponse("error.html", {"request": request, "error_message": message})

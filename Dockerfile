# Utiliser une image de base Python
FROM python:3.12

# Définir le répertoire de travail dans le conteneur
WORKDIR /code

# Copier les fichiers de l'application dans le répertoire de travail
COPY . /app

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port sur lequel l'application écoute (par exemple 8000)
EXPOSE 8000

# Lancer l'application FastAPI avec Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

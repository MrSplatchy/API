FROM python:3.12

# Définir le répertoire de travail dans le conteneur
WORKDIR /

# Copier seulement requirements.txt à la racine
COPY requirements.txt /requirements.txt

# Installer les dépendances
RUN pip install --no-cache-dir -r /requirements.txt

# Copier tous les fichiers dans la racine du conteneur
COPY . /

# Exposer le port sur lequel l'application écoute (par exemple 8000)
EXPOSE 8000

# Lancer l'application FastAPI avec Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python:3.12

# Définir le répertoire de travail
WORKDIR /app

# Copier seulement le fichier requirements.txt
COPY requirements.txt .

# Lister les fichiers dans le conteneur pour vérifier si requirements.txt est bien là
RUN ls -la /app

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste des fichiers de l'application
COPY . .

# Exposer le port de l'application
EXPOSE 8000

# Lancer l'application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

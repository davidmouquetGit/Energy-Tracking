# Image de base Python
FROM python:3.11-slim

# Créer le répertoire de travail
WORKDIR /app

# Copier requirements et installer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le projet
COPY . .

# Exposer le port Streamlit
EXPOSE 8501

# Commande pour lancer Streamlit
CMD ["streamlit", "run", "Accueil.py", "--server.port=8501", "--server.address=0.0.0.0"]

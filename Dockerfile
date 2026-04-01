FROM python:3.10-slim

# Évite que Python ne génère des fichiers .pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Installation des dépendances système (git est requis pour certaines opérations dbt/dagster si besoin)
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Copie et installation des requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du projet entier
COPY . .

# Configuration Dagster
ENV DAGSTER_HOME=/app/dagster_home
RUN mkdir -p $DAGSTER_HOME

# Expose les ports par défaut pour Dagster (3000) et Streamlit (8501)
EXPOSE 3000 8501

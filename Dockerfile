# 1. Pobieramy oficjalny system Linux z lekkim Pythonem 3.11
FROM python:3.11-slim

# 2. Ustawiamy /app jako nasz folder roboczy w kontenerze
WORKDIR /app

# 3. Zabezpieczenia: zapobiegają plikom .pyc i opóźnieniom logów
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 4. Kopiujemy najpierw listę zależności (żeby użyć cache Dockera)
COPY requirements.txt .

# 5. Instalujemy biblioteki
RUN pip install --no-cache-dir -r requirements.txt

# 6. Kopiujemy cały nasz kod (main.py, models.py, crud.py itd.)
COPY . .

# 7. Odblokowujemy port 8000
EXPOSE 8000

# 8. Komenda uruchamiająca serwer
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
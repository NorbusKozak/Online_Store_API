# downloading python 3.11
FROM python:3.11-slim

# setting app as working directory
WORKDIR /app

# securities
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# copying requirements for docker to know on what libraries it has to work
COPY requirements.txt .

# installing these libraries
RUN pip install --no-cache-dir -r requirements.txt

# copying the whole code
COPY . .

# unlocking port 8000
EXPOSE 8000

# server running command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
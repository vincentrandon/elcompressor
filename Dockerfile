#Python image
FROM python:3.10.12
LABEL authors="vincent"

#Working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app
RUN pip install -r requirements.txt

# Copy source code
COPY . /app


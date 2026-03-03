# Stage 1: Build the Vite frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend

COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install

COPY frontend/ ./
RUN npm run build

# Stage 2: Build the FastAPI backend with Playwright
# Using the official Playwright python image which includes browser dependencies
FROM mcr.microsoft.com/playwright/python:v1.41.0-jammy
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PORT=8080

# Install Python dependencies
COPY backend/requirements.txt ./
# Make sure uvicorn is in requirements or installed
RUN pip install --no-cache-dir -r requirements.txt

# Install playwright browsers (Just in case the image doesn't match the exact version of the python package)
RUN playwright install chromium

# Copy the built frontend static files from the previous stage
COPY --from=frontend-builder /app/frontend/dist /app/frontend/dist

# Copy the backend code
COPY backend/ /app/backend/

# Expose port
EXPOSE $PORT

# Start Uvicorn from the backend directory
WORKDIR /app/backend
CMD sh -c "uvicorn main:app --host 0.0.0.0 --port ${PORT}"

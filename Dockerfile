FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV SYSMLV2_URL=http://localhost:8080
ENV READ_ONLY=true
ENV MCPPATH=/mcp

# Set the working directory inside the container
WORKDIR /app

# Copy and install dependencies first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY ./*.py .

EXPOSE 8000

# Command to run the FastAPI application with Uvicorn
CMD ["python", "server.py"]
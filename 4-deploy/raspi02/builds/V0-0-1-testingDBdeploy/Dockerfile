# Use an official Python runtime as a parent image
FROM python:3.14.3-slim-trixie

# Set working directory
WORKDIR /app

# Copy only the contents of the current folder (V0-0-1-testingDBdeploy)
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000
EXPOSE 8000

# Run the application
CMD ["python", "app.py"]
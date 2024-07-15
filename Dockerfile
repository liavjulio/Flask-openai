# Use the official Python image from the Docker Hub
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /backend-developer-assignment

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set environment variables
ENV FLASK_APP=app:create_app()
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080
ENV PYTHONPATH=os.getenv("PYTHONPATH")

# Expose the port the app runs on
EXPOSE 8080

# Run the application
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]

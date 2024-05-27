# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /RestaurantSystem

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project code into the container
COPY . .

# Expose the port on which the Django server will run
EXPOSE 8000

# Set the command to run Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "RestaurantSystem.wsgi:application"]
# # Use the official Python image as the base image
# FROM python:3.8

# # Set environment variables
# ENV PYTHONUNBUFFERED 1

# # Set the working directory in the container
# WORKDIR /app

# # Copy the requirements file into the container at /app
# COPY requirements.txt /app/

# COPY . /app/

# RUN python manage.py collectstatic --noinput

# # Install dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the current directory contents into the container at /app
# COPY . /app/

# # Expose the port the app runs on
# EXPOSE 8000

# # Command to run the application
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# Use the official Python image as the base image
FROM python:3.8

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Run collectstatic to collect static files
RUN python manage.py collectstatic --noinput

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Use an official Python runtime as a base image
FROM python:3.8-slim

# Set the working directory to /app in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the CSV file into the container
COPY ./data/ /app/data/

# Make port 80 available to the world outside this container (optional)
EXPOSE 80

# Define environment variable (optional)
ENV NAME WebScraper

# Run script.py when the container launches
CMD ["python", "script.py"]

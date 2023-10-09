# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the install script and Python script into the container
COPY install.sh .
COPY RunAll.py .

# Make the install script executable
RUN chmod +x install.sh

# Install any needed dependencies specified in requirements.txt (if you have one)
# COPY requirements.txt .
# RUN pip install -r requirements.txt

# Run the install script to install prerequisites
RUN ./install.sh

# Run the Python script
CMD ["python3", "RunAll.py"]

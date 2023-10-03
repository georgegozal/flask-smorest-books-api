# Use an official Python runtime as a parent image
FROM python:3.10-alpine3.18

# Set environment variables
ENV FLASK_APP main.py
ENV FLASK_ENV=production
ENV FLASK_DEBUG=False
ENV FLASK_RUN_HOST 0.0.0.0

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["gunicorn", "main:app", "-w", "4", "--threads", "2", "-b", "0.0.0.0:5000"]

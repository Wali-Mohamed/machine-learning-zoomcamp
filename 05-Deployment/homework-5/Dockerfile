# Start from the base image
FROM svizor/zoomcamp-model:3.11.5-slim

# Set the working directory in the container
WORKDIR /app

# Copy the Pipfile and Pipfile.lock into the container
COPY Pipfile Pipfile.lock /app/

# Install Pipenv and dependencies
RUN pip install --no-cache-dir pipenv && \
    pipenv install --deploy --system

# Install Gunicorn
RUN pip install gunicorn

# Copy the Flask application code into the container
COPY . /app

# Expose the port that the Flask app will run on
EXPOSE 5000

# Define the command to run your Flask app with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "churn-pred-app:app"]

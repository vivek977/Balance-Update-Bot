# Use an appropriate base image for Python
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the Python scripts and any required files (e.g., .env, requirements.txt)
COPY . /app

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose any necessary ports (if required)
EXPOSE 8080

# Command to run the bot.py script as the main process
CMD ["python", "bot.py"]


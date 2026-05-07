# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /code

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variables
ENV PORT=7860
EXPOSE 7860

# Run the application
CMD ["python", "app.py"]

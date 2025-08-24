# Use official python image
FROM python:3.9

# Set working directory
WORKDIR /code

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Expose port
EXPOSE 7860

# Run FastAPI with uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]

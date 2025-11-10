# 1. Use a stable Python base image (3.11 is better than 3.10 for newer PyTorch)
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# 2. Copy requirement files first to leverage Docker layer caching
COPY requirements.txt .

# 3. Install CPU-ONLY PyTorch and then the rest of the dependencies
# Installing torch first, using the special index URL, is the fix for your build errors.
RUN pip install torch==2.3.1+cpu -f https://download.pytorch.org/whl/torch_stable.html && \
    pip install -r requirements.txt

# 4. Copy the entire project code and data
COPY . .

# 5. Set the entry point to run the FastAPI server on port 8000 (Railway's default)
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
# Install Python dependencies
RUN pip install -r requirements.txt

# Expose the default Hugging Face port
EXPOSE 7860

# Run Streamlit
CMD ["streamlit", "run", "ui/app.py", "--server.port=7860", "--server.address=0.0.0.0"]

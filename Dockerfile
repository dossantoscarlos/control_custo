# 1. Base Image
FROM python:3.13-slim

# 2. Set working directory
WORKDIR /app

# 3. Install poetry
RUN pip install uv

# 4. Copy dependency files
COPY pyproject.toml uv.lock README.md /app/

# 5. Install dependencies
RUN uv sync 

# 6. Copy application code
COPY . .

# 8. Expose the port the app runs on
EXPOSE 8000

# 9. Command to run the application
CMD ["python", "wait_for_keycloak.py", "uv", "run", "task", "run"]


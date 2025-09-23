# 1. Base Image
FROM python:3.13-slim

# 2. Set working directory
WORKDIR /app

# 3. Install poetry
RUN pip install poetry

# 4. Copy dependency files
COPY pyproject.toml poetry.lock /app/

# 5. Install dependencies
RUN poetry install --without dev --no-root

# 6. Copy application code
COPY . .

# 7. Copy wait script
COPY wait_for_keycloak.py ./

# 8. Expose the port the app runs on
EXPOSE 8000


# 9. Command to run the application
CMD ["python", "wait_for_keycloak.py", "poetry", "run", "task", "run"]
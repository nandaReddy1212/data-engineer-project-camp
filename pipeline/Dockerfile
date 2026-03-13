# # base Docker image that we will build on
# FROM python:3.13.11-slim

# # install PostgreSQL client library and compiler needed by psycopg
# RUN apt-get update && \
#     apt-get install -y libpq-dev gcc && \
#     rm -rf /var/lib/apt/lists/*

# # Copy uv binary from official uv image (multi-stage build pattern)
# COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# # set up the working directory 
# WORKDIR /app

# # Add virtual environment to PATH so we can use installed packages
# ENV PATH="/app/.venv/bin:$PATH"

# # Copy dependency files first (better layer caching)
# COPY pyproject.toml uv.lock .python-version ./
# # Install dependencies from lock file (ensures reproducible builds)
# RUN uv sync --locked

# # copy the script to the container. 1st name is source file, 2nd is destination
# COPY *.py ./

# # Set entry point
# ENTRYPOINT ["python", "ingest_data.py"]



FROM python:3.13.11-slim

RUN apt-get update && \
    apt-get install -y libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /code

COPY pyproject.toml uv.lock .python-version ./

# create venv + install deps
RUN uv sync --locked

# add venv to path
ENV PATH="/code/.venv/bin:$PATH"

# copy project files
COPY . .

ENTRYPOINT ["python"]
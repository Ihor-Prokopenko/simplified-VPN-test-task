FROM python:3.11-slim

# env variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWEITEBYTECODE 1

ARG PROJECT_DIR
ENV PROJECT_DIR ${PROJECT_DIR}
# setting work directory
WORKDIR ${PROJECT_DIR}

# Copy the project's dependency files
COPY pyproject.toml poetry.lock ${PROJECT_DIR}/

# Install Poetry and project dependencies
RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

RUN mkdir ${PROJECT_DIR}/static && mkdir ${PROJECT_DIR}/media

COPY src $PROJECT_DIR
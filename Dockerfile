# ── Railway Dockerfile for Manim Animation Studio ────────────────────────────
# This Dockerfile is placed at the repo root so Railway auto-detects it
# instead of using Nixpacks (which lacks the pangocairo system libraries).

# ── Stage 1: builder ─────────────────────────────────────────────────────────
FROM python:3.11-slim AS builder

# Install ALL build-time system dependencies including pangocairo
RUN apt-get update -qq \
    && apt-get install --no-install-recommends -y \
        build-essential \
        gcc \
        cmake \
        make \
        pkg-config \
        wget \
        libcairo2-dev \
        libffi-dev \
        libpango1.0-dev \
        libegl-dev \
        ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install manim into an isolated virtualenv
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy only requirements first for better caching
COPY requirements.txt /opt/manim/requirements.txt
WORKDIR /opt/manim
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . /opt/manim

# ── Stage 2: runtime ─────────────────────────────────────────────────────────
FROM python:3.11-slim

# Runtime system libraries
RUN apt-get update -qq \
    && apt-get install --no-install-recommends -y \
        libcairo2 \
        libpango-1.0-0 \
        libpangocairo-1.0-0 \
        libpangoft2-1.0-0 \
        libffi8 \
        libegl1 \
        libgl1 \
        ffmpeg \
        fonts-noto-core \
        fontconfig \
    && rm -rf /var/lib/apt/lists/*

RUN fc-cache -fv

# Copy the pre-built virtualenv from builder
ENV VIRTUAL_ENV=/opt/venv
COPY --from=builder /opt/venv /opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy project files
COPY --from=builder /opt/manim /opt/manim
WORKDIR /opt/manim

# Create required directories
RUN mkdir -p /opt/manim/media /opt/manim/temp

# Railway provides $PORT, default to 10000
ENV PORT=10000

# Use the server module as entrypoint
CMD uvicorn server.server:app --host 0.0.0.0 --port $PORT

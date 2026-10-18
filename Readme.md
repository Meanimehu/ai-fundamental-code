 Let's continue with Step 2: configure Docker to run Python and `uv`. We'll keep your existing Mac setup unchanged and run the course environment inside the container.

## Step 2A — Add the `Dockerfile`

In VS Code, open `Dockerfile` and paste:

```
FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /workspace

CMD ["sleep", "infinity"]
```

What this does:

- `python:3.12-slim` provides Python inside the container.
- The `COPY` line adds `uv`.
- `WORKDIR` sets the working directory inside the container.
- `sleep infinity` keeps the container running so we can execute commands in it.

## Step 2B — Configure `compose.yaml`

Open `compose.yaml` and paste:

```
services:
  app:
    build: .
    working_dir: /workspace
    volumes:
      - .:/workspace
      - uv-cache:/root/.cache/uv
    env_file:
      - .env
    stdin_open: true
    tty: true

volumes:
  uv-cache:
```

This tells Docker Compose how to build and run our container. Your project folder stays on your Mac, and the container can access the files through the mounted `/workspace` directory.

## Step 2C — Protect your files and API keys

In `.dockerignore`, add:

```
.env
.git
.DS_Store
__pycache__
.venv
```

In `.gitignore`, add:

```
.env
.venv/
__pycache__/
```

The `.dockerignore` file prevents these items from being sent as part of the Docker build context. The `.gitignore` file prevents Git from tracking them.

Keep your API keys private. We don't need to put them in the Dockerfile.

## Step 2D — Build and start the container

Open the VS Code terminal using Terminal → New Terminal. Make sure you're in your `ai-learning` directory, then run:

```
docker compose up -d --build
```

Wait for the build to finish. Then check Python:

```
docker compose exec app python --version
```

Check `uv`:

```
docker compose exec app uv --version
```

Check the container status:

```
docker compose ps
```

You should see Python 3.12.x, a `uv` version, and an app container with a running status.

## Step 2E — Initialize the Python project

Once those checks pass, run:

```
docker compose exec app uv init --bare
```

This initializes a Python project in your mounted folder. Then add the libraries we'll need:

```
docker compose exec app uv add openai qdrant-client python-dotenv
```

This creates project dependency files on your Mac, so the project configuration persists even if you remove and recreate the container.

One note: we're intentionally not configuring Grok or Qdrant credentials yet. First, let's confirm the environment works.

## Your checkpoint

Run the commands through Step 2D and tell me the result. If everything works, we can continue to Step 2E and then test a Python script.
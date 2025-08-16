#!/bin/bash
PROJECT_NAME="EduAgent"
VENV_DIR=".venv"
WEAVIATE_CONTAINER_NAME="eduagent-weaviate"
RAG_DOCKER_FILEPATH="docker/docker-compose.rag.yml"
OLLAMA_PID_FILE="scripts/data/ollama.pid"
OLLAMA_LOG_FILE="scripts/data/ollama.log"

setup_venv() {
    if [ -d "$VENV_DIR" ]; then
        # venv directory exists, just enter environment and sync
        source "$VENV_DIR/bin/activate"
        uv sync
    else
        # venv doesn't exist, create one, enter it and sync
        uv venv "$VENV_DIR" || { echo "Failed to create venv"; exit 1; }
        source "$VENV_DIR/bin/activate"
        uv sync
    fi
    echo "Virtual environment set up successful.\n"
}

setup_docker() {
    RUNNING_DOCKER_ID=$(docker ps -q -f name="$WEAVIATE_CONTAINER_NAME")
    if [ -n "$RUNNING_DOCKER_ID" ]; then
        # Container is already spun up
        echo "RAG Docker container already running"
    else 
        # Container needs to be composed up
        docker compose -f "$RAG_DOCKER_FILEPATH" up -d
    fi
}

is_ollama_running() {
    # Returns 0 if running, 1 if not
    if curl -s http://localhost:11434/ >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

setup_ollama() {
    if is_ollama_running; then
        # Server already running
        echo "Ollama server already running..."
    else 
        # Start up ollama server
        echo "Starting up Ollama server..."
        nohup ollama serve > "$OLLAMA_LOG_FILE" 2>&1 &
        OLLAMA_PID=$!
        echo $OLLAMA_PID > "$OLLAMA_PID_FILE"
        echo "Ollama started with PID: $OLLAMA_PID"
    fi
}

setup_venv
setup_docker
setup_ollama

echo "$PROJECT_NAME development environment ready.\n"
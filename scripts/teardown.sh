#!/bin/bash
PROJECT_NAME="EduAgent"
VENV_DIR=".venv"
WEAVIATE_CONTAINER_NAME="eduagent-weaviate"
RAG_DOCKER_FILEPATH="docker/docker-compose.rag.yml"
OLLAMA_PID_FILE="scripts/data/ollama.pid"
OLLAMA_LOG_FILE="scripts/data/ollama.log"

teardown_venv() {
    if [ -n "$VIRTUAL_ENV" ]; then
        deactivate
    elif [ -n "$CONDA_DEFAULT_ENV" ]; then
        conda deactivate
    else
        # Already not inside of a venv
    fi
    echo "Virtual environment tear down successful."
}

teardown_docker() {
    RUNNING_DOCKER_ID=$(docker ps -q -f name="$WEAVIATE_CONTAINER_NAME")
    if [ -n "$RUNNING_DOCKER_ID" ]; then
        # Container is actively running
        docker compose -f "$RAG_DOCKER_FILEPATH" down
        echo "RAG Docker container spun down"
    else 
        # Container already composed down
        echo "RAG Docker container is already spun down"
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

teardown_ollama() {
    if [ -f "$OLLAMA_PID_FILE" ]; then
        OLLAMA_PID=$(cat "$OLLAMA_PID_FILE")
        if kill -0 $OLLAMA_PID 2>/dev/null; then
            echo "Stopping Ollama server with PID $OLLAMA_PID..."
            kill $OLLAMA_PID
            rm "$OLLAMA_PID_FILE"
            rm "$OLLAMA_LOG_FILE"
            echo "Ollama server stopped."
        else
            echo "PID $OLLAMA_PID not running. Removing stale PID file."
            rm "$OLLAMA_PID_FILE"
            rm "$OLLAMA_LOG_FILE"
        fi
    else 
        # Server already spun down
        echo "Ollama server already stopped"
    fi
    if is_ollama_running; then
        echo "Ollama server couldn't be killed, PID file not found. Try manually"
    fi
}

teardown_venv
teardown_docker
teardown_ollama

echo "$PROJECT_NAME development environment torn down."
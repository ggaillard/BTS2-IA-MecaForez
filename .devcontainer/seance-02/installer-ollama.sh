#!/usr/bin/env bash
# Installe Ollama et le modèle de la séance 2 dans le Codespace, puis démarre
# le serveur. Rejouable : ce qui est déjà là n'est pas refait.
#   bash .devcontainer/seance-02/installer-ollama.sh            # tout
#   bash .devcontainer/seance-02/installer-ollama.sh --demarrer # serveur seul
set -euo pipefail
MODELE="${MODELE:-qwen2.5:1.5b}"

demarrer() {
  if curl -fsS http://localhost:11434/api/version >/dev/null 2>&1; then return; fi
  nohup ollama serve >/tmp/ollama.log 2>&1 &
  for _ in $(seq 1 30); do
    curl -fsS http://localhost:11434/api/version >/dev/null 2>&1 && return
    sleep 1
  done
  echo "❌ Ollama ne démarre pas : voir /tmp/ollama.log" >&2
  exit 1
}

if [ "${1:-}" != "--demarrer" ]; then
  if ! command -v ollama >/dev/null; then
    echo "📦 Installation d'Ollama…"
    sudo apt-get update -qq && sudo apt-get install -y -qq zstd >/dev/null
    curl -fsSL https://ollama.com/install.sh | sh
  fi
fi

demarrer

if ! ollama list | grep -q "^${MODELE}"; then
  echo "⬇️  Téléchargement de ${MODELE} (1 Go)…"
  ollama pull "$MODELE"
fi
echo "✅ Ollama répond sur http://localhost:11434 avec ${MODELE}."

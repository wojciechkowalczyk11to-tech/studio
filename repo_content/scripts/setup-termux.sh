#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

if ! command -v pkg >/dev/null 2>&1; then
  echo "Ten skrypt musi być uruchomiony w Termux." >&2
  exit 1
fi

REPO_URL="${1:-https://github.com/wojciechkowalczyk11to-tech/N.0.C.git}"
TARGET_DIR="${2:-$HOME/N.O.C}"

echo "[1/11] Aktualizacja pakietów"
pkg update -y
pkg upgrade -y

echo "[2/11] Instalacja zależności systemowych"
pkg install -y \
  python \
  python-pip \
  nodejs-lts \
  git \
  openssh \
  curl \
  wget \
  unzip \
  jq \
  clang \
  make \
  libjpeg-turbo \
  libpng \
  redis \
  postgresql

echo "[3/11] Instalacja cloudflared"
pkg install -y cloudflared || true

echo "[4/11] Klonowanie repozytorium"
if [[ -d "${TARGET_DIR}/.git" ]]; then
  echo "Repozytorium już istnieje w ${TARGET_DIR}, wykonuję git pull"
  git -C "${TARGET_DIR}" pull --ff-only
else
  git clone "${REPO_URL}" "${TARGET_DIR}"
fi

echo "[5/11] Tworzenie virtualenv i instalacja zależności Python"
python -m venv "$HOME/.venvs/nexus"
# shellcheck disable=SC1091
source "$HOME/.venvs/nexus/bin/activate"
pip install --upgrade pip wheel setuptools
if [[ -f "${TARGET_DIR}/requirements.txt" ]]; then
  pip install -r "${TARGET_DIR}/requirements.txt"
fi
if [[ -f "${TARGET_DIR}/nexus_cli/requirements.txt" ]]; then
  pip install -r "${TARGET_DIR}/nexus_cli/requirements.txt"
fi

echo "[6/11] Instalacja aliasów nexus-cli"
if [[ -f "${TARGET_DIR}/nexus_cli/aliases/install_aliases.sh" ]]; then
  bash "${TARGET_DIR}/nexus_cli/aliases/install_aliases.sh"
fi

echo "[7/11] Konfiguracja Gemini CLI i Claude Code"
npm install -g @google/gemini-cli @anthropic-ai/claude-code || true

echo "[8/11] Tworzenie katalogu ~/.nexus"
mkdir -p "$HOME/.nexus"

echo "[9/11] Interaktywne tworzenie pliku .env"
ENV_FILE="${TARGET_DIR}/.env"
if [[ ! -f "${ENV_FILE}" ]]; then
  cp "${TARGET_DIR}/.env.example" "${ENV_FILE}" 2>/dev/null || touch "${ENV_FILE}"
fi

prompt_env() {
  local key="$1"
  local description="$2"
  local value
  read -r -p "${description}: " value
  if grep -qE "^${key}=" "${ENV_FILE}"; then
    sed -i "s#^${key}=.*#${key}=${value}#" "${ENV_FILE}"
  else
    echo "${key}=${value}" >> "${ENV_FILE}"
  fi
}

prompt_env "TELEGRAM_BOT_TOKEN" "Podaj TELEGRAM_BOT_TOKEN"
prompt_env "OPENAI_API_KEY" "Podaj OPENAI_API_KEY"
prompt_env "GOOGLE_API_KEY" "Podaj GOOGLE_API_KEY"
prompt_env "ANTHROPIC_API_KEY" "Podaj ANTHROPIC_API_KEY"
prompt_env "CF_API_TOKEN" "Podaj CF_API_TOKEN"

echo "[10/11] Instalacja rclone"
pkg install -y rclone || true
if command -v rclone >/dev/null 2>&1; then
  echo "Uruchamiam 'rclone config' (opcjonalnie)"
  rclone config || true
fi

echo "[11/11] Instalacja Google Cloud CLI (gcloud)"
pip install google-cloud-cli || true
if command -v gcloud >/dev/null 2>&1; then
  gcloud auth login --no-launch-browser || true
  gcloud auth application-default login --no-launch-browser || true
fi

echo "Konfiguracja Termux zakończona."

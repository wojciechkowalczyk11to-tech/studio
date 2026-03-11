#!/data/data/com.termux/files/usr/bin/bash
#
# Termux AI Agent - Automatyczna Instalacja (PRODUCTION AGGRESSIVE MODE)
# Budget: $4,300 ($800 Gemini + $3,500 Vertex AI)
#
# Usage:
#   bash setup_termux.sh
#

set -e  # Exit on error

# Kolory
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funkcje pomocnicze
print_header() {
    echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  🤖 TERMUX AI AGENT - PRODUCTION AGGRESSIVE SETUP            ║${NC}"
    echo -e "${BLUE}║  Budget: \$4,300 | Mode: MAX QUALITY                          ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

print_step() {
    echo -e "${GREEN}▶ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

# Sprawdzenie wymagań
check_requirements() {
    print_step "Sprawdzanie wymagań systemowych..."
    
    # Sprawdź czy to Termux
    if [ ! -d "/data/data/com.termux" ]; then
        print_warning "To nie wygląda na Termux. Kontynuować? (y/n)"
        read -r response
        if [ "$response" != "y" ]; then
            exit 1
        fi
    fi
    
    # Sprawdź Android version
    if command -v getprop &> /dev/null; then
        ANDROID_VER=$(getprop ro.build.version.release)
        print_success "Android: $ANDROID_VER"
    fi
    
    # Sprawdź dostępną przestrzeń
    AVAILABLE_SPACE=$(df -h $HOME | awk 'NR==2 {print $4}')
    print_success "Wolna przestrzeń: $AVAILABLE_SPACE"
    
    # Sprawdź RAM
    if command -v free &> /dev/null; then
        TOTAL_RAM=$(free -h | awk '/^Mem:/ {print $2}')
        print_success "Całkowity RAM: $TOTAL_RAM"
    fi
    
    echo ""
}

# Instalacja pakietów Termux
install_termux_packages() {
    print_step "Instalacja pakietów Termux..."
    
    # Aktualizacja repozytoriów
    pkg update -y
    pkg upgrade -y
    
    # Podstawowe pakiety
    pkg install -y \
        python \
        python-pip \
        git \
        curl \
        wget \
        openssl \
        libxml2 \
        libxslt \
        libjpeg-turbo \
        libpng \
        freetype
    
    print_success "Pakiety Termux zainstalowane"
    echo ""
}

# Weryfikacja Python
verify_python() {
    print_step "Weryfikacja Python..."
    
    PYTHON_VER=$(python --version 2>&1 | awk '{print $2}')
    REQUIRED_VER="3.11.0"
    
    if [ "$(printf '%s\n' "$REQUIRED_VER" "$PYTHON_VER" | sort -V | head -n1)" = "$REQUIRED_VER" ]; then
        print_success "Python $PYTHON_VER (OK)"
    else
        print_error "Python $PYTHON_VER < wymagana wersja $REQUIRED_VER"
        exit 1
    fi
    
    # Aktualizacja pip
    python -m pip install --upgrade pip setuptools wheel
    
    print_success "pip zaktualizowany"
    echo ""
}

# Klonowanie projektu
clone_project() {
    print_step "Klonowanie projektu..."
    
    if [ -d "$HOME/termux-ai-agent" ]; then
        print_warning "Katalog termux-ai-agent już istnieje. Usunąć? (y/n)"
        read -r response
        if [ "$response" = "y" ]; then
            rm -rf "$HOME/termux-ai-agent"
        else
            print_error "Instalacja przerwana"
            exit 1
        fi
    fi
    
    # PLACEHOLDER: Zamień na swoje repo
    # git clone https://github.com/YOUR_USERNAME/termux-ai-agent.git $HOME/termux-ai-agent
    
    # Alternatywnie: rozpakuj ZIP
    print_warning "Upewnij się, że projekt jest w $HOME/termux-ai-agent"
    
    cd "$HOME/termux-ai-agent" || exit 1
    print_success "Projekt gotowy w: $HOME/termux-ai-agent"
    echo ""
}

# Instalacja zależności Python
install_python_deps() {
    print_step "Instalacja zależności Python (to może zająć 10-20 minut)..."
    
    cd "$HOME/termux-ai-agent" || exit 1
    
    # Instalacja z requirements.txt
    print_step "pip install -r requirements.txt..."
    python -m pip install -r requirements.txt --no-cache-dir
    
    print_success "Wszystkie zależności zainstalowane"
    echo ""
}

# Konfiguracja
setup_config() {
    print_step "Konfiguracja..."
    
    cd "$HOME/termux-ai-agent" || exit 1
    
    # Tworzenie katalogów
    mkdir -p config memory logs
    
    # Kopiowanie przykładowej konfiguracji
    if [ ! -f "config/agent_config.yaml" ]; then
        if [ -f "agent_config.yaml" ]; then
            cp agent_config.yaml config/agent_config.yaml
        else
            print_error "Brak pliku konfiguracji agent_config.yaml"
            exit 1
        fi
    fi
    
    # Tworzenie .env z template
    if [ ! -f ".env" ]; then
        cat > .env << 'EOF'
# Termux AI Agent - Environment Variables
# CRITICAL: Fill in your credentials!

# Google Cloud Project
GCP_PROJECT_ID="your-project-id-here"
VERTEX_DATASTORE_ID="your-datastore-id-here"

# Gemini API Key (get from https://makersuite.google.com/app/apikey)
GEMINI_API_KEY="your-gemini-api-key-here"

# Optional: Additional datastores
VERTEX_DATASTORE_DOCS=""
VERTEX_DATASTORE_CODE=""

# Service Account (path to JSON key file)
GOOGLE_APPLICATION_CREDENTIALS="config/service-account-key.json"
EOF
        print_warning "Utworzono .env - WYPEŁNIJ swoje dane!"
    fi
    
    print_success "Konfiguracja gotowa"
    echo ""
}

# Weryfikacja Google Cloud
verify_google_cloud() {
    print_step "Weryfikacja Google Cloud credentials..."
    
    cd "$HOME/termux-ai-agent" || exit 1
    
    # Sprawdź czy .env ma dane
    if grep -q "your-project-id-here" .env 2>/dev/null; then
        print_warning ".env zawiera placeholdery - uzupełnij przed uruchomieniem!"
        return
    fi
    
    # Test połączenia (jeśli credentials są)
    print_step "Testowanie połączenia..."
    python3 -c "
import os
from dotenv import load_dotenv
load_dotenv()

project_id = os.getenv('GCP_PROJECT_ID')
api_key = os.getenv('GEMINI_API_KEY')

if not project_id or project_id == 'your-project-id-here':
    print('❌ GCP_PROJECT_ID nie jest ustawiony')
    exit(1)

if not api_key or api_key == 'your-gemini-api-key-here':
    print('❌ GEMINI_API_KEY nie jest ustawiony')
    exit(1)

print('✅ Credentials configuration OK')
" 2>&1 || print_warning "Uzupełnij credentials w .env"
    
    echo ""
}

# Instalacja aliasów
install_aliases() {
    print_step "Instalacja aliasów CLI..."
    
    cd "$HOME/termux-ai-agent" || exit 1
    
    if [ -f "install_aliases.sh" ]; then
        bash install_aliases.sh
        print_success "Aliasy zainstalowane"
    else
        print_warning "Brak pliku install_aliases.sh - pomiń"
    fi
    
    echo ""
}

# Test instalacji
test_installation() {
    print_step "Test instalacji..."
    
    cd "$HOME/termux-ai-agent" || exit 1
    
    # Test importów
    print_step "Testowanie importów Python..."
    python3 -c "
import asyncio
import yaml
import numpy
import google.generativeai as genai
from google.cloud import discoveryengine_v1
from sqlalchemy import create_engine
from sentence_transformers import SentenceTransformer
print('✅ Wszystkie importy OK')
" 2>&1 && print_success "Importy OK" || print_error "Błąd importów"
    
    # Test agenta (podstawowy)
    if [ -f "run_agent.py" ]; then
        print_step "Testowanie agenta..."
        python3 run_agent.py --status 2>&1 && print_success "Agent działa" || print_warning "Agent wymaga konfiguracji"
    fi
    
    echo ""
}

# Podsumowanie
print_summary() {
    echo ""
    echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║                    INSTALACJA ZAKOŃCZONA                      ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${GREEN}✓ Pakiety Termux${NC}"
    echo -e "${GREEN}✓ Python $(python --version 2>&1 | awk '{print $2}')${NC}"
    echo -e "${GREEN}✓ Zależności Python${NC}"
    echo -e "${GREEN}✓ Konfiguracja${NC}"
    echo ""
    echo -e "${YELLOW}NASTĘPNE KROKI:${NC}"
    echo ""
    echo "1. Uzupełnij credentials w .env:"
    echo "   nano ~/.env"
    echo ""
    echo "2. Pobierz Service Account key z GCP i zapisz jako:"
    echo "   config/service-account-key.json"
    echo ""
    echo "3. Załaduj aliasy:"
    echo "   source ~/.bashrc"
    echo ""
    echo "4. Sprawdź status agenta:"
    echo "   agent-status"
    echo ""
    echo "5. Wykonaj pierwsze zadanie:"
    echo "   agent-task \"Sprawdź status systemu\""
    echo ""
    echo -e "${BLUE}📚 Dokumentacja: cat README.md${NC}"
    echo -e "${BLUE}🆘 Pomoc: agent-help${NC}"
    echo ""
}

# ===== MAIN =====
main() {
    print_header
    
    check_requirements
    install_termux_packages
    verify_python
    # clone_project  # Uncomment when repo is ready
    install_python_deps
    setup_config
    verify_google_cloud
    install_aliases
    test_installation
    print_summary
}

# Uruchomienie
main "$@"

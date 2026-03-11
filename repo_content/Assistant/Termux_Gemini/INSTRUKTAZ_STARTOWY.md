# 🚀 TERMUX AI AGENT - INSTRUKTAŻ STARTOWY

## 📦 Wersja: PRODUCTION AGGRESSIVE MODE v1.0
**Budżet: $4,300** ($800 Gemini + $3,500 Vertex AI)
**Tryb: MAX QUALITY** - Pełne wykorzystanie budżetu dla maksymalnej jakości

---

## ⚡ SZYBKI START (5 MINUT)

### 1️⃣ POBRANIE I ROZPAKOWANIE (Termux)

```bash
# Pobierz ZIP (zastąp URL swoim)
cd $HOME
curl -L -O https://your-link/termux-ai-agent-PRODUCTION-v1.0.zip

# Rozpakuj
unzip termux-ai-agent-PRODUCTION-v1.0.zip

# Przejdź do katalogu
cd termux-ai-agent
```

---

### 2️⃣ AUTOMATYCZNA INSTALACJA

```bash
# Uruchom installer (10-20 minut)
bash setup_termux.sh
```

**Installer automatycznie:**
- ✅ Aktualizuje pakiety Termux
- ✅ Instaluje Python 3.11+
- ✅ Instaluje wszystkie zależności (90+ pakietów)
- ✅ Tworzy strukturę katalogów
- ✅ Konfiguruje environment

---

### 3️⃣ KONFIGURACJA CREDENTIALS (KRYTYCZNE!)

#### A. Edytuj plik `.env`:

```bash
nano .env
```

Uzupełnij:

```bash
# Google Cloud Project
GCP_PROJECT_ID="twoj-projekt-id"              # Z GCP Console
VERTEX_DATASTORE_ID="twoj-datastore-id"       # Z Vertex AI Search

# Gemini API Key (z https://makersuite.google.com/app/apikey)
GEMINI_API_KEY="AIza..."

# Service Account (ścieżka do pliku JSON)
GOOGLE_APPLICATION_CREDENTIALS="config/service-account-key.json"
```

**Zapisz:** `Ctrl+O`, `Enter`, `Ctrl+X`

---

#### B. Pobierz Service Account Key z GCP:

**W przeglądarce:**

1. Idź do: https://console.cloud.google.com
2. **IAM & Admin** → **Service Accounts**
3. Wybierz/stwórz Service Account z rolami:
   - `Vertex AI User`
   - `Discovery Engine Admin`
4. **Keys** → **Add Key** → **Create new key** → **JSON**
5. Pobierz plik JSON

**W Termux:**

```bash
# Przenieś pobrany plik do Termux
# (użyj Termux:API lub scp/ftp)

# Lub skopiuj zawartość:
nano config/service-account-key.json
# Wklej JSON, zapisz (Ctrl+O, Enter, Ctrl+X)

# Ustaw uprawnienia
chmod 600 config/service-account-key.json
```

---

### 4️⃣ WERYFIKACJA INSTALACJI

```bash
# Test 1: Sprawdź importy Python
python3 -c "
import google.generativeai as genai
from google.cloud import discoveryengine_v1
from sentence_transformers import SentenceTransformer
print('✅ Wszystkie biblioteki załadowane!')
"

# Test 2: Sprawdź credentials
python3 -c "
from dotenv import load_dotenv
import os
load_dotenv()
assert os.getenv('GCP_PROJECT_ID') != 'your-project-id-here'
assert os.getenv('GEMINI_API_KEY') != 'your-gemini-api-key-here'
print('✅ Credentials skonfigurowane!')
"

# Test 3: Sprawdź agenta (opcjonalnie - wymaga aktywnych API)
python3 run_agent.py --status
```

---

### 5️⃣ PIERWSZE ZADANIE

```bash
# Sprawdź status systemu
python3 run_agent.py --task "Sprawdź status systemu Termux"

# Wykonaj prosty task
python3 run_agent.py --task "Wylistuj pliki w bieżącym katalogu i podaj ich rozmiary"

# Z rozumowaniem (tryb AGGRESSIVE - 7 kroków)
python3 run_agent.py --task "Jak mogę zoptymalizować ten projekt?" --reasoning-depth 7
```

---

## 🔧 ZAAWANSOWANE OPCJE

### Aliasy CLI (opcjonalne)

Po instalacji możesz użyć skrótów:

```bash
# Załaduj aliasy
source ~/.bashrc

# Dostępne komendy:
agent-task "Twoje zadanie"           # Wykonaj zadanie
agent-status                        # Status agenta
agent-budget                        # Budżet API
agent-help                          # Pomoc
agent-memory                        # Statystyki pamięci
```

---

### Konfiguracja AGGRESSIVE MODE (już aktywna!)

Plik `config/agent_config.yaml` jest już skonfigurowany w trybie agresywnym:

```yaml
vertex_ai_search:
  enabled: true              # ✅ Domyślnie włączone
  aggressive_mode: true      # ✅ Bez throttlingu
  queries_per_task: 5        # ✅ Wysokiej jakości kontekst

api:
  max_tokens: 8192          # ✅ Pełny kontekst
  reasoning_depth: 7        # ✅ Głębokie rozumowanie

learning:
  experience_replay_size: 500  # ✅ Duży bufor
  improvement_frequency: 5     # ✅ Częste cykle
```

**Nie musisz niczego zmieniać** - wszystko jest już zoptymalizowane pod maksymalną jakość!

---

## 📊 MONITOROWANIE BUDŻETU

### Sprawdź aktualne wydatki:

```bash
# Ręcznie
cat config/budget.json | python3 -m json.tool

# Lub przez skrypt (jeśli stworzyłeś)
python3 -c "
from monitoring.cost_tracker import CostTracker
tracker = CostTracker()
stats = tracker.get_stats()
print(f\"Vertex AI: \${stats['vertex']['spent']:.2f} / \${stats['vertex']['budget']:.2f}\")
print(f\"Gemini: \${stats['gemini']['spent']:.2f} / \${stats['gemini']['budget']:.2f}\")
print(f\"TOTAL: \${stats['total']['spent']:.2f} / \${stats['total']['budget']:.2f}\")
"
```

**Alerty:**
- ⚠️  75% budżetu: Ostrzeżenie w logach
- 🚨 90% budżetu: Krytyczne ostrzeżenie

**Ale NIE BLOKUJE requestów** - agent działa zawsze!

---

## 🐛 TROUBLESHOOTING

### Problem 1: "ImportError: No module named 'google.cloud'"

```bash
pip install google-cloud-discoveryengine google-generativeai
```

### Problem 2: "ValueError: GCP_PROJECT_ID not set"

```bash
# Upewnij się że wypełniłeś .env
nano .env
# Sprawdź czy plik .env jest w katalogu termux-ai-agent/
ls -la .env
```

### Problem 3: "Failed to initialize Vertex Search"

```bash
# Sprawdź Service Account key
cat config/service-account-key.json | head -3
# Powinien być poprawny JSON zaczynający się od:
# {
#   "type": "service_account",
#   "project_id": "...",

# Sprawdź uprawnienia
chmod 600 config/service-account-key.json
```

### Problem 4: "Vertex AI Search returns 404"

**Musisz utworzyć Datastore w GCP:**

1. Idź do: https://console.cloud.google.com/gen-app-builder
2. **Create App** → **Search**
3. **Data Store** → **Create New**
   - Type: **Unstructured**
   - Name: `termux-agent-knowledge`
   - Location: `global`
4. Dodaj źródła (opcjonalnie):
   - Python docs: https://docs.python.org/3/
   - Termux wiki: https://wiki.termux.com/
5. Skopiuj **Data Store ID** do `.env` jako `VERTEX_DATASTORE_ID`

---

## 📚 STRUKTURA PROJEKTU

```
termux-ai-agent/
├── config/
│   ├── agent_config.yaml           # ✅ AGGRESSIVE MODE (już skonfigurowany)
│   └── service-account-key.json    # ⚠️  Musisz dodać!
├── integrations/
│   ├── vertex_search.py            # ✅ Real Vertex AI (NO SIMULATION)
│   └── gemini_client.py            # ✅ Native google-generativeai
├── learning/
│   ├── experience_replay.py        # ✅ SQLite persistence
│   └── knowledge_graph.py          # ✅ Embeddings + SQLite
├── monitoring/
│   └── cost_tracker.py             # ✅ Budget monitoring (non-blocking)
├── memory/                         # SQLite databases (auto-created)
├── logs/                           # Logi agenta
├── run_agent.py                    # Main entry point
├── setup_termux.sh                 # Installer
├── requirements.txt                # Wszystkie zależności
└── .env                            # ⚠️  Credentials (wypełnij!)
```

---

## 🎯 CO DALEJ?

1. **Eksperymentuj** - agent uczy się z każdego zadania!
2. **Monitoruj** budżet regularnie
3. **Czytaj logi** w `logs/agent.log`
4. **Sprawdzaj pamięć** - bazy SQLite w `memory/`
5. **Dodaj więcej datastores** w Vertex AI dla lepszej wiedzy

---

## 📞 WSPARCIE

**Dokumentacja:**
- README.md - Przegląd projektu
- INSTALL.md - Szczegółowa instalacja
- USER_GUIDE.md - Przewodnik użytkownika
- ARCHITECTURE.md - Architektura systemu

**Problemy:**
- Sprawdź logi: `tail -f logs/agent.log`
- Debug mode: `python3 run_agent.py --task "test" --verbose`

---

## ✅ CHECKLIST

Przed pierwszym użyciem upewnij się że:

- [ ] Zainstalowałeś pakiety przez `setup_termux.sh`
- [ ] Wypełniłeś `.env` (GCP_PROJECT_ID, GEMINI_API_KEY, VERTEX_DATASTORE_ID)
- [ ] Pobrałeś Service Account JSON z GCP
- [ ] Skopiowałeś JSON do `config/service-account-key.json`
- [ ] Utworzyłeś Vertex AI Datastore w GCP
- [ ] Przetestowałeś importy Python (test #1 wyżej)
- [ ] Przetestowałeś credentials (test #2 wyżej)

**Gdy wszystko gotowe:**

```bash
python3 run_agent.py --task "Hello World - sprawdź czy wszystko działa"
```

---

## 🚀 MIŁEJ ZABAWY Z AGENTEM AI!

**PRODUCTION AGGRESSIVE MODE** - Najlepsza jakość, pełne wykorzystanie budżetu.

Twój agent jest gotowy do autonomicznej pracy na Termux! 🎉

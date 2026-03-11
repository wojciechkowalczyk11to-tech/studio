# Termux Gemini Agent Kit

Zestaw narzędzi do uruchomienia bezpiecznego agenta Gemini CLI w środowisku Termux (Android). Domyślnie skonfigurowany pod logowanie Google (zero-config), z możliwością łatwego przejścia na Vertex AI.

## Szybka Instalacja (60 sekund)

### Instalacja przez Git (Zalecana)
1. Otwórz Termux.
2. Sklonuj repozytorium i uruchom instalator:

```bash
git clone https://github.com/USERNAME/termux-gemini-agent-kit.git
cd termux-gemini-agent-kit
./install.sh
```

### Instalacja z pliku ZIP (Alternatywna)
Jeśli nie masz Gita lub wolisz ręczne pobranie:
1. Pobierz plik ZIP z repozytorium.
2. Rozpakuj go w katalogu domowym.
3. Wejdź do katalogu i uruchom instalator:

```bash
cd ~
# (Użyj unzip lub innej metody rozpakowania, np. poprzez menedżer plików Termux)
cd termux-gemini-agent-kit-main  # nazwa katalogu może się różnić zależnie od zipa
bash install.sh
```

### Po instalacji
1. Zrestartuj Termux lub uruchom `source ~/.bashrc`.
2. Zaloguj się (jeśli używasz domyślnego trybu Google):
   *Uwaga: Instalator automatycznie ustawia `selectedAuthType=oauth-personal` w `settings.json`, co jest wymagane do działania autoryzacji na Termux.*
   ```bash
   gemini auth login
   ```
3. Sprawdź status:
   ```bash
   ./scripts/doctor.sh
   ```
4. Przetestuj komendy:
   ```bash
   gemini run battery
   gemini run wifi
   ```

## Użycie

### Komendy
Zestaw dodaje aliasy i konfiguracje do Gemini CLI.

- **Status**: `gstat` (lub `gmode status`) - pokazuje obecny tryb, projekt i lokalizację.
- **Planowanie**: Użyj `gemini run plan "Opis zadania"`.
- **Diagnostyka**: `./scripts/doctor.sh` - sprawdza poprawność instalacji.

### Tryby Pracy

#### Tryb Google (Domyślny)
Wykorzystuje darmową warstwę lub płatną subskrypcję Gemini Advanced połączoną z Twoim kontem Google. Nie wymaga konfiguracji chmury. Idealny na start.

Aby wrócić do tego trybu:
```bash
gmode google
```

#### Tryb Vertex AI (Zaawansowany)
Dla użytkowników Google Cloud. Wymagane, jeśli potrzebujesz większych limitów lub specyficznych ustawień korporacyjnych.

**Jak przejść na Vertex AI?**
1. Utwórz projekt w Google Cloud Platform.
2. Włącz API Vertex AI.
3. Przełącz się w terminalu:

```bash
# Użyj domyślnej lokalizacji (us-central1)
gmode vertex TWOJ_PROJECT_ID

# Lub określ lokalizację (np. europe-west4)
gmode vertex TWOJ_PROJECT_ID europe-west4
```

Możesz też ustawić lokalizację ręcznie zmienną środowiskową:
```bash
export GOOGLE_CLOUD_LOCATION=europe-west1
```

*Uwaga: Zmiana `gmode` jest tymczasowa dla obecnej sesji.*

## Zaawansowane

### Wersja CLI
Instalator instaluje przypiętą, przetestowaną wersję `gemini-cli` (obecnie 0.26.0).
Jeśli chcesz zainstalować inną wersję, ustaw zmienną przed instalacją/aktualizacją:

```bash
export GEMINI_CLI_VERSION=0.27.0
./install.sh
```

## Aktualizacja

Aby zaktualizować CLI i odświeżyć konfigurację (z kopią zapasową starej):
```bash
./scripts/update.sh
```
*Uwaga: Jeśli zainstalowałeś zestaw z pliku ZIP, skrypt aktualizacji nie pobierze automatycznie najnowszego kodu repozytorium (brak Gita). Musisz pobrać nowy plik ZIP ręcznie. Skrypt nadal zaktualizuje jednak CLI i odświeży pliki konfiguracyjne, jeśli je nadpisałeś.*

## Rozwiązywanie Problemów

Jeśli masz problemy, uruchom:
```bash
./scripts/doctor.sh
```
Skrypt ten wskaże brakujące zależności lub problemy z konfiguracją.

## Odinstalowanie

Aby usunąć zmiany w `.bashrc` i przywrócić kopię zapasową:
```bash
./uninstall.sh
```

#!/usr/bin/env bash
set -euo pipefail

if [[ "$(id -u)" -ne 0 ]]; then
  echo "Uruchom skrypt jako root (sudo)." >&2
  exit 1
fi

USERNAME="${SUDO_USER:-${USER}}"
HOME_DIR="$(getent passwd "${USERNAME}" | cut -d: -f6)"

echo "[1/8] Aktualizacja systemu"
apt update
apt upgrade -y

echo "[2/8] Instalacja Docker + Docker Compose"
apt install -y ca-certificates curl gnupg lsb-release ufw fail2ban git
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | tee /etc/apt/sources.list.d/docker.list >/dev/null
apt update
apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
usermod -aG docker "${USERNAME}"

echo "[3/8] Instalacja cloudflared"
curl -fsSL https://pkg.cloudflare.com/cloudflare-main.gpg | gpg --dearmor -o /usr/share/keyrings/cloudflare-main.gpg
echo "deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] https://pkg.cloudflare.com/cloudflared bookworm main" > /etc/apt/sources.list.d/cloudflared.list
apt update
apt install -y cloudflared

echo "[4/8] Instalacja code-server"
curl -fsSL https://code-server.dev/install.sh | sh
systemctl enable --now code-server@"${USERNAME}"

echo "[5/8] Instalacja Node.js 20 LTS"
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt install -y nodejs

echo "[6/8] Konfiguracja usług systemd"
systemctl enable --now docker
systemctl enable --now cloudflared || true
systemctl enable --now code-server@"${USERNAME}"

echo "[7/8] Konfiguracja zapory UFW"
ufw default deny incoming
ufw default allow outgoing
ufw allow OpenSSH
ufw allow 8080/tcp comment 'code-server'
ufw --force enable

echo "[8/8] Harden SSH"
SSHD_CONFIG="/etc/ssh/sshd_config"
sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin no/' "${SSHD_CONFIG}"
sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication no/' "${SSHD_CONFIG}"
sed -i 's/^#\?PubkeyAuthentication.*/PubkeyAuthentication yes/' "${SSHD_CONFIG}"
systemctl restart ssh

echo "Konfiguracja Debian zakończona. Użytkownik: ${USERNAME}, katalog domowy: ${HOME_DIR}."

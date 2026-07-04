#!/bin/bash
set -e

# ============================================
# Скрипт настройки EC2 для Etno_Practic
# Запускать от пользователя ubuntu на сервере
# ============================================

# --- Вставьте свой EC2 public IP и репозиторий ---
EC2_IP=""        # например: 54.123.45.67
REPO_URL=""      # например: https://github.com/user/Etno_Practic.git
# -------------------------------------------------

if [ -z "$EC2_IP" ] || [ -z "$REPO_URL" ]; then
    echo "ОШИБКА: Отредактируйте EC2_IP и REPO_URL в начале скрипта!"
    exit 1
fi

echo "=== 1/8 Обновление системы ==="
sudo apt update && sudo apt upgrade -y

echo "=== 2/8 Установка Python 3.12, pip, venv ==="
sudo apt install -y python3.12 python3.12-venv python3-pip

echo "=== 3/8 Установка Node.js 20 ==="
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

echo "=== 4/8 Установка nginx ==="
sudo apt install -y nginx

echo "=== 5/8 Клонирование проекта ==="
cd /home/ubuntu
if [ ! -d "Etno_Practic" ]; then
    git clone "$REPO_URL" Etno_Practic
fi
cd Etno_Practic

echo "=== 6/8 Настройка Python окружения ==="
python3.12 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "=== 7/8 Настройка .env для продакшена ==="
# Генерируем новый SECRET_KEY
NEW_SECRET=$(python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")

cat > movie/.env << EOF
SECRET_KEY=${NEW_SECRET}
DEBUG=False
ALLOWED_HOSTS=${EC2_IP},localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://${EC2_IP}
EOF

echo "=== 8/8 Сборка фронтенда ==="
cd frontend
npm install
cat > .env << EOF
VITE_API_BASE_URL=http://${EC2_IP}
VITE_API_LANG=ru
EOF
npm run build
cd ..

echo "=== Миграции и статика ==="
cd movie
python manage.py migrate
python manage.py collectstatic --noinput
cd ..

echo "=== Настройка nginx ==="
sudo cp deploy/nginx.conf /etc/nginx/sites-available/etno
sudo ln -sf /etc/nginx/sites-available/etno /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

echo "=== Настройка gunicorn ==="
sudo cp deploy/gunicorn.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable gunicorn
sudo systemctl restart gunicorn

echo ""
echo "============================================"
echo "  ДЕПЛОЙ ЗАВЕРШЁН!"
echo "  Откройте: http://${EC2_IP}"
echo "  Админка:  http://${EC2_IP}/admin/"
echo "  API:      http://${EC2_IP}/ru/film/"
echo "============================================"
echo ""
echo "Создайте суперпользователя:"
echo "  cd /home/ubuntu/Etno_Practic/movie"
echo "  source ../venv/bin/activate"
echo "  python manage.py createsuperuser"

# 🏢 RealEstate Telegram Bot

Telegram бот для управления документооборотом в сфере недвижимости с интеграцией Google Drive и Google Sheets.

## 📋 Описание

Бот предназначен для структурированного хранения документов по объектам недвижимости, управления доступом пользователей и предоставления доступа к учетным данным вендоров. Все файлы автоматически организуются в папки на Google Drive по схеме `клиент/объект/этап`.

## 🚀 Возможности

- **📤 Загрузка документов** - структурированное сохранение файлов с автоматическим именованием
- **📁 Просмотр файлов** - навигация по загруженным документам с получением ссылок
- **🔐 Управление доступом** - получение логинов и паролей вендоров
- **👥 Контроль доступа** - ограничение доступа пользователей к конкретным клиентам/объектам

## 🏗️ Архитектура

```
realestate-tgbot1/
├── bot.py                 # Главный файл запуска с меню
├── handlers/              # Обработчики команд
│   ├── upload.py         # Загрузка файлов
│   ├── credentials.py    # Управление учетными данными
│   └── view_files.py     # Просмотр файлов
├── google/               # Интеграция с Google сервисами
│   ├── drive.py         # Работа с Google Drive
│   └── sheet.py         # Работа с Google Sheets
├── core/                # Основные утилиты
│   ├── auth.py         # Авторизация (пустой)
│   └── file_utils.py   # Утилиты для файлов
└── data/               # Данные
    └── clients.json    # Клиенты (пустой)
```

## 🔧 Установка и настройка

### 1. Клонирование репозитория
```bash
git clone <repository_url>
cd realestate-tgbot1
```

### 2. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 3. Настройка Google API

#### Создание Service Account:
1. Перейдите в [Google Cloud Console](https://console.cloud.google.com/)
2. Создайте новый проект или выберите существующий
3. Включите Google Drive API и Google Sheets API
4. Создайте Service Account в разделе "Учетные данные"
5. Скачайте JSON ключ и сохраните как `google/service_account.json`

#### Создание Google Sheets для управления:
Создайте таблицу с листами:

**AccessControl:**
| telegram_id | client   | object    |
|-------------|----------|-----------|
| 123456789   | Client A | Object 1  |
| 123456789   | Client A | Object 2  |

**VendorCredentials:**
| client   | object    | vendor_name | url                | login    | password |
|----------|-----------|-------------|--------------------|---------  |----------|
| Client A | Object 1  | Portal 1    | https://portal1.com| user123  | pass123  |

### 4. Переменные окружения

Создайте файл `.env`:
```env
BOT_TOKEN=ваш_telegram_bot_token
ROOT_FOLDER_ID=id_корневой_папки_google_drive
SPREADSHEET_NAME=название_google_таблицы
```

### 5. Запуск
```bash
python bot.py
```

## 📱 Использование

### Основное меню:
- **📤 Загрузить файл** (`/upload`) - пошаговая загрузка документов
- **📁 Посмотреть файлы** (`/view`) - просмотр загруженных файлов
- **🔐 Логины и пароли** (`/credentials`) - доступ к учетным данным
- **⚙️ Настройки** - в разработке

### Процесс загрузки файла:
1. Выбор клиента
2. Выбор объекта  
3. Выбор этапа (Purchase/Operation)
4. Указание типа документа
5. Указание контрагента
6. Загрузка файла

Файл автоматически переименовывается в формат: `YYYY-MM-DD_тип_контрагент.pdf`

### Структура папок на Google Drive:
```
Root Folder/
└── Client A/
    └── Object 1/
        ├── Purchase/
        │   ├── 2024-01-15_contract_vendor1.pdf
        │   └── 2024-01-16_invoice_vendor2.pdf
        └── Operation/
            └── 2024-01-20_report_manager.pdf
```

## 🔐 Система доступа

Доступ пользователей контролируется через Google Sheets:
- Пользователи привязываются к клиентам/объектам по `telegram_id`
- Только авторизованные пользователи могут загружать/просматривать файлы
- Учетные данные вендоров доступны только для соответствующих объектов

## 📦 Зависимости

- `python-telegram-bot==20.7` - Telegram Bot API
- `google-api-python-client==2.126.0` - Google API клиент
- `google-auth==2.29.0` - Google авторизация
- `google-auth-oauthlib==1.2.0` - OAuth для Google
- `gspread==6.0.2` - Работа с Google Sheets
- `python-dotenv==1.0.1` - Загрузка переменных окружения

## 🔄 Развертывание

### Heroku:
1. Создайте приложение на Heroku
2. Добавьте переменные окружения
3. Загрузите `service_account.json` через Heroku CLI или переменные
4. Деплой через Git

### Docker:
```dockerfile
FROM python:3.10.13
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "bot.py"]
```

## 🤝 Участие в разработке

1. Fork репозитория
2. Создайте feature ветку
3. Сделайте изменения
4. Создайте Pull Request

## 📄 Лицензия

MIT License

## 📞 Поддержка

Для вопросов и предложений создавайте Issues в репозитории.

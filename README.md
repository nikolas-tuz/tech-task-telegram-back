# Telegram Web App Setup Instructions

Привіт, Neuro Track! Хочу висловити вам подяку за таке цікаве технічне завдання) Мені дуже сподобалось! Це було весело, цікаво) Одне з найкращих тестових, яке мені давали виконувати, без перебільшень)
Нижче вже на англійській розписав, як запустити цей застосунок. Створив інструкції й нотатки по запуску. Застосунок написаний використовуючи MongoDB, FastAPI, NextJS. Прошу оцінити якість коду, враховуючи
скільки часу було дано на виконання. Я старався писати чистий, реюзабельний код як і на фронті, так і на бекі.

## Prerequisites

* Node.js and npm installed
* Docker installed
* Git installed
* A Telegram account AND obtained TELEGRAM_API_ID & TELEGRAM_API_HASH keys.

# Technical Task

# Система перегляду повідомлень у соціальних мережах

**Опис:** Розробити додаток, за допомогою якого можна підключити телеграм аккаунт, з можливістю переглядати список чатів аккаунта та повідомлень.

## Функціонал додатку:

1.  Логін/реєстрація у системі.
2.  Функціонал підключення телеграм аккаунту.
3.  Перегляд усіх чатів підключеного телеграм аккаунту.
4.  Перегляд усіх повідомлень обраного чату.
5.  Функціонал виходу з підключеного телеграм аккаунту.
6.  Функціонал виходу із системи.

## Вимоги:

* Клієнтська частина: React або Next.js.
* Серверна частина: FastAPI.
* Публікація додатку у відкритому репозиторії GitHub.

# Нотатки перед запуском:

- При перевірці еррор хендла(який є :D) саме при підтвердженні телеграм акаунту, telethon який я використав блокує на невизначений час повторну авторизацію. Для того щоб не чекати, треба зупинити FASTAPI сервер
й видалити файл `session_name.session`. Після цього можна без затримки повторити авторизацію.

- Я докеризував бек, де запускаю його разом з базою даних Mongodb. Саме цю базу даних я використав для збереження даних юзера й перевірки при авторизації в системі. Також при успішній авторизації телеграм
акаунту, я зберігаю telegram_session в базу даних. При відключенні телеграма з системи, цей філд видаляється з бд й логаут телгерам застосунку відбувається з самого телеграма також. 

- я не встигаю зробити нормальну пагінацію;  - фетчу перших 140 чатів й до 80 повідомлень кожного чату. Для збереження часу було зроблено саме так, ще й дедлайни по роботі зараз. Я вже й
створив Intersection Observer клас з потрібною логікою для тригеру, який працює, але не встигаю доробити. А telethon не має "skip" параметру
а має offset_id або offset_date. Яке рішення цієї проблеми? - На мою думку можна було зробити пагінацію саме по датах, якщо типового "skip" філда не має telethon.

- також не встиг зробити адаптивну верстку 😪, але запарився зробити гарний інтерфейс). 


## Installation

1.  **Clone the repositories:**

    Open your terminal and execute the following commands to clone the frontend and backend repositories:

    ```bash
    git clone https://github.com/nikolas-tuz/tech-task-telegram-front.git
    git clone https://github.com/nikolas-tuz/tech-task-telegram-back.git
    ```

2.  **Configure the backend:**

    * Navigate to the backend directory:

        ```bash
        cd tech-task-telegram-back
        ```

    * Open the `docker-compose.yaml` file.

    * Add your Telegram API credentials to the `environment` section:

        ```yaml
        version: "3.9"
        services:
          fastapi:
            build:
              context: .
              dockerfile: Dockerfile
            container_name: fastapi
            restart: always
            ports:
              - "8000:8000"
            environment:
              - JWT_SECRET=534bf7011708742cd135692578a45ee725ff738d1eed6a36bcaa0caaf2cbbefe
              - TELEGRAM_API_ID=<YOUR_TELEGRAM_API_ID>
              - TELEGRAM_API_HASH=<YOUR_TELEGRAM_API_HASH>
              - ALLOWED_HOST=http://localhost:3000
            depends_on:
              - mongo
            volumes:
              - .:/app
          mongo:
            image: mongo
        ```

        Replace `<YOUR_TELEGRAM_API_ID>` and `<YOUR_TELEGRAM_API_HASH>` with your actual Telegram API ID and hash.  You can obtain these from [https://my.telegram.org/apps](https://my.telegram.org/apps).

3.  **Run the backend:**

    * Start the Docker containers:

        ```bash
        docker-compose up -d
        ```

        This will start the MongoDB database and the FastAPI backend.

4.  **Configure the frontend:**

    * Navigate to the frontend directory:

        ```bash
        cd tech-task-telegram-front
        ```

    * Create a `.env.local` file in the root of the frontend directory.

    * Add the following environment variables to `.env.local`:

        ```
        JWT_SECRET=534bf7011708742cd135692578a45ee725ff738d1eed6a36bcaa0caaf2cbbefe
        NEXT_PUBLIC_BACKEND_URL=http://127.0.0.1:8000
        ```

5.  **Run the frontend:**

    * Install the dependencies:

        ```bash
        npm i
        ```

    * Build the application:

        ```bash
        npm run build
        ```

    * Start the application:

        ```bash
        npm run start
        ```

6.  **Access the application:**

    Open your web browser and go to `http://localhost:3000/`.

## Testing the application

1.  **Register:** Create a new account on the system.
2.  **Connect to Telegram:**
    * Enter your valid Telegram phone number.
    * Enter the verification code sent to your Telegram account.
    * If you have 2FA enabled, enter your 2FA password.  Authentication will fail without the correct 2FA password.
3.  **Browse:** Browse the first 140 chats and up to 80 messages in each chat.
4.  **Logout from Telegram:** Log out of your Telegram account within the application.
5.  **Logout from System:** Log out of your account on the web application.

# Atom Hackathon - Infinity_zarplata

## Запуск проекта

### На Linux:

```bash
make env  # создание .env файла
make run  # запуск проекта
```

### На Windows с Docker:

```bash
docker compose up
```

## Запуск проекта
Для тестирования системы необходимо создать аккаунт и привзяать в личном кабинете api-key с сайта https://www.segmind.com/

## Участники команды:

- Вячеслав Кирпиченко
- Кирилл Ларионов
- Роман Лящук

## Тизер решения:

Мы рады представить прототип системы для автоматической проверки соответствия требованиям сертификации автомобилей. Это приложение станет незаменимым инструментом для автопроизводителей, позволяя быстро и точно выявлять несоответствия на ранних этапах разработки, что существенно сократит временные и ресурсные затраты.

Одной из ключевых особенностей нашего приложения является его удобный интерфейс, разработанный с учетом мобильной верстки и современного дизайна. Пользователи смогут легко вводить новые требования или загружать их в формате Word. Благодаря использованию нейронных сетей и алгоритмов автоматической обработки текста, приложение быстро анализирует данные и предоставляет краткие отчеты о соответствии, рекомендации по исправлению и детализированные результаты в формате PDF.

## Стек решения:

- Python (FastAPI)
- Vue (Nuxt)
- Claude-3-Haiku

## Уникальность нашего решения:

Наше приложение не только способно обрабатывать большие объемы данных и минимизировать влияние человеческого фактора, но и делает процесс сертификации более доступным и комфортным для пользователей. Наш сайт позволяет вам прямо с телефона загрузить требование и, попивая вкусный чай, наблюдать, как искусственный интеллект анализирует на ошибки ваши требования. Мы уверены, что наше приложение значительно повысит качество проверки и ускорит процесс сертификации, делая его более эффективным и удобным.

# Описание endpoint-ов:

Вот описание всех ручек (эндпоинтов) проекта Atom, основанное на предоставленном OpenAPI спецификации:

### 1. Health Check

- **GET /api/v1/health_check/ping**
  - **Описание**: Проверка состояния сервиса.
  - **Ответ**:
    - 200: Успешный ответ.

### 2. Пользователь

- **POST /api/v1/user/register**

  - **Описание**: Регистрация нового пользователя.
  - **Запрос**: `RegistrationForm`
  - **Ответ**:
    - 201: Успешный ответ с `RegistrationSuccess`.
    - 400: Имя пользователя уже существует.
    - 422: Ошибка валидации.

- **POST /api/v1/user/register/admin**

  - **Описание**: Регистрация администратора.
  - **Запрос**: `RegistrationAdmin`
  - **Ответ**:
    - 201: Успешный ответ с `RegistrationSuccess`.
    - 400: Имя пользователя уже существует.
    - 422: Ошибка валидации.
  - **Безопасность**: Требуется OAuth2.

- **POST /api/v1/user/token**

  - **Описание**: Вход для получения токена доступа.
  - **Запрос**: `Body_login_for_access_token_api_v1_user_token_post`
  - **Ответ**:
    - 200: Успешный ответ с `Token`.
    - 401: Неверное имя пользователя или пароль.
    - 422: Ошибка валидации.

- **POST /api/v1/user/auth**

  - **Описание**: Аутентификация для получения токена доступа.
  - **Запрос**: `AuthSchema`
  - **Ответ**:
    - 200: Успешный ответ с `Token`.
    - 401: Неверное имя пользователя или пароль.
    - 422: Ошибка валидации.

- **GET /api/v1/user/me**

  - **Описание**: Получение информации о текущем пользователе.
  - **Ответ**:
    - 200: Успешный ответ с `UserSchema`.
    - 401: Неверное имя пользователя или пароль.
  - **Безопасность**: Требуется OAuth2.

- **PUT /api/v1/user/me_update**
  - **Описание**: Обновление информации о пользователе.
  - **Запрос**: Параметры (username, old_password, password, api_key).
  - **Ответ**:
    - 200: Успешный ответ с `UserSchema`.
    - 401: Неавторизованный.
    - 404: Пользователь не найден.
    - 422: Ошибка валидации.
  - **Безопасность**: Требуется OAuth2.

### 3. Папки (Folders)

- **POST /api/v1/folders/**

  - **Описание**: Создание новой папки.
  - **Параметры**:
    - `folder_name` (query, обязательный): Имя папки.
  - **Ответ**:
    - 201: Успешный ответ.
    - 422: Ошибка валидации.
  - **Безопасность**: Требуется OAuth2.

- **GET /api/v1/folders/**

  - **Описание**: Получение всех папок.
  - **Ответ**:
    - 200: Успешный ответ с массивом объектов `FoldersTable`.

- **DELETE /api/v1/folders/{folder_id}**
  - **Описание**: Удаление папки.
  - **Параметры**:
    - `folder_id` (path, обязательный): Идентификатор папки (UUID).
  - **Ответ**:
    - 204: Успешный ответ (папка успешно удалена).
    - 422: Ошибка валидации.
  - **Безопасность**: Требуется OAuth2.

### 4. Файлы (Files)

- **GET /api/v1/files/**

  - **Описание**: Получение файлов в указанной папке.
  - **Параметры**:
    - `folder_id` (query, обязательный): Идентификатор папки (UUID).
  - **Ответ**:
    - 200: Успешный ответ с массивом объектов `FilesTable`.
    - 422: Ошибка валидации.

- **POST /api/v1/files/**

  - **Описание**: Создание нового файла в указанной папке.
  - **Параметры**:
    - `folder_id` (query, обязательный): Идентификатор папки (UUID).
  - **Запрос**:
    - `Body_create_file_item_api_v1_files__post` (содержит файл).
  - **Ответ**:
    - 201: Успешный ответ с объектом `FilesTable`.
    - 422: Ошибка валидации.
  - **Безопасность**: Требуется OAuth2.

- **DELETE /api/v1/files/{file_id}**

  - **Описание**: Удаление файла.
  - **Параметры**:
    - `file_id` (path, обязательный): Идентификатор файла (UUID).
  - **Ответ**:
    - 204: Успешный ответ (файл успешно удален).
    - 422: Ошибка валидации.
  - **Безопасность**: Требуется OAuth2.

- **GET /api/v1/files/{file_id}**
  - **Описание**: Получение информации о конкретном файле.
  - **Параметры**:
    - `file_id` (path, обязательный): Идентификатор файла (UUID).
  - **Ответ**:
    - 200: Успешный ответ с объектом `FilesTable`.
    - 422: Ошибка валидации.

### 5. GPT

- **POST /api/v1/gpt/analyze**

  - **Описание**: Анализ текста с использованием GPT.
  - **Запрос**: `AnalizeText`
  - **Ответ**:
    - 200: Успешный ответ.
    - 422: Ошибка валидации.
  - **Безопасность**: Требуется OAuth2.

- **POST /api/v1/gpt/analyze_list**

  - **Описание**: Анализ списка текстов с использованием GPT.
  - **Запрос**: `AnalizeListText`
  - **Ответ**:
    - 200: Успешный ответ.
    - 422: Ошибка валидации.
  - **Безопасность**: Требуется OAuth2.

- **POST /api/v1/gpt/normalize**

  - **Описание**: Форматирование текста.
  - **Параметры**: `text`.
  - **Ответ**:
    - 200: Успешный ответ.
    - 422: Ошибка валидации.
  - **Безопасность**: Требуется OAuth2.

- **POST /api/v1/gpt/shortly**
  - **Описание**: Сжатие текста.
  - **Запрос**: `ShortlyModel`
  - **Ответ**:
    - 200: Успешный ответ.
    - 422: Ошибка валидации.

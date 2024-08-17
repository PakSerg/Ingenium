# Ingenium

## О проекте

Ingenium — это веб-приложение, которое позволяет пользователям задавать вопросы, отвечать на них и взаимодействовать с контентом через лайки и дизлайки. Основные возможности платформы включают регистрацию, создание и поиск вопросов с тегами и категориями, систему голосования, систему уведомлений и кэширование.

## Основные функции

- **Регистрация и авторизация:** При регистрации пользователи должны пройти верификацию email, получив письмо с уникальным URL-адресом. Подобным образом также реализована возможность восстановления пароля.
- **Создание вопросов и ответов:** Зарегистрированные пользователи могут создавать вопросы и отвечать на них. Незарегистрированные пользователи могут только просматривать контент.
- **Теги:** Каждый вопрос может иметь один или несколько тегов для удобного поиска и фильтрации.
- **Голосование:** Пользователи могут ставить лайки и дизлайки на вопросы, влияя на их приоритет выдачи (реализовано с использованием AJAX-запросов).
- **Полнотекстовый поиск:** Триграммный индекс обеспечивает быстрый и точный поиск контента на сайте.
- **Профили пользователей:** Каждый пользователь имеет личный профиль с отображением статистики (число заданных вопросов, ответов и т.д.).
- **Система нотификаций:** Авторы вопросов получают уведомления на электронную почту при появлении новых ответов (используется Redis и Celery).
- **Рекомендательная система:**  Система предлагает пользователям вопросы, которые могут быть для них интересны, основываясь на текущем вопросе.
- **Обработка неактивных пользователей:** Периодическая обработка неактивных аккаунтов, не прошедших верификацию (Redis и Celery Beat).
- **Кэширование:** Лента самых обсуждаемых вопросов и другие часто посещаемые страницы хранятся в кэше (Redis).

## Приложения

- **Users:** Управление пользователями и их профилями.
- **Questions:** Создание и управление вопросами и ответами.
- **Votes:** Система голосования за вопросы.

## Дорожная карта

Предстоящие улучшения и задачи:

- **Подсчёт статистики пользователей:** Отображение полной статистики пользователя в профиле.
- **Отображение аватаров:** Добавление возможности отображения аватаров пользователей.
- **Выбор лучшего ответа:** Введение функции выбора лучшего ответа из предложенных.
- **Счётчик просмотров:** Добавление счётчика просмотров страниц с вопросами.
- **Хранение медиафайлов:** Организация хранения медиафайлов в облачном хранилище (S3).

## Установка и запуск

1. **Клонируйте репозиторий:**

    ```bash
    git clone https://github.com/PakSerg/Ingenium.git
    cd Ingenium
    ```

2. **Настройте переменные окружения:**

    Создайте файл `.env` и добавьте необходимые переменные (настройки для Postgres и SMTP-сервера).
    
3. **Настройте Nginx**

    Настройте nginx.conf для локальной работы проекта.
    
4. **Запустите проект:**

    Запустите контейнеры Docker. При запуске создадутся 4 контейнера: Django, PostgreSQL, Redis и Nginx.
    ```bash
    docker-compose up --build
    ```


## Контакты

- Telegram: https://t.me/PakSergeiDev
- Телефон: +7 (913) 795-65-56
- Email: sergey.pak.dev@gmail.com

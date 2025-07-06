# Instagram Predictive Analytics Dashboard

## 🚨 КРИТИЧЕСКОЕ ПРЕДУПРЕЖДЕНИЕ

**Instagram Basic Display API был полностью отключен 4 декабря 2024 года.**

Текущий проект использует устаревший API, который больше не работает. Instagram функциональность ограничена:
- ❌ Новые подключения Instagram невозможны
- ❌ Синхронизация данных отключена  
- ✅ Доступны только исторические данные из базы
- ✅ Остальная функциональность работает нормально

**Для миграции см. `INSTAGRAM_API_MIGRATION.md`**

---

Дашборд для анализа и предсказания активности в Instagram с использованием машинного обучения.

## Структура проекта

```
predictive_analytics_dashboard/
├── backend/                     # FastAPI backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py             # Точка входа FastAPI приложения
│   │   ├── core/               # Основные настройки и конфигурация
│   │   │   ├── __init__.py
│   │   │   └── config.py       # Настройки приложения
│   │   └── api/                # API endpoints
│   │       ├── __init__.py
│   │       ├── routes.py       # Основной роутер
│   │       └── endpoints/      # Модули с endpoints
│   │           ├── __init__.py
│   │           ├── auth.py     # Аутентификация
│   │           ├── instagram.py # Instagram API
│   │           ├── analytics.py # Аналитика
│   │           └── predictions.py # Предсказания
│   ├── pyproject.toml          # Зависимости Python (uv)
│   └── .env.example            # Пример переменных окружения
├── frontend/                   # React frontend
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   └── Layout/
│   │   │       └── Header.tsx  # Заголовок навигации
│   │   │   ├── pages/              # Страницы приложения
│   │   │   │   ├── Dashboard.tsx   # Главная страница
│   │   │   │   ├── Analytics.tsx   # Аналитика
│   │   │   │   ├── Predictions.tsx # Предсказания
│   │   │   │   └── Profile.tsx     # Профиль
│   │   │   ├── routes/
│   │   │   │   └── AppRoutes.tsx   # Роутинг
│   │   │   ├── App.tsx             # Главный компонент
│   │   │   ├── App.css
│   │   │   ├── index.tsx           # Точка входа React
│   │   │   └── index.css
│   │   └── package.json            # Зависимости Node.js
├── LICENSE                     # MIT лицензия
├── .gitignore                  # Исключения Git
└── README.md                   # Документация проекта
```

## Технологии

### Backend
- **FastAPI** - современный веб-фреймворк для Python
- **uv** - менеджер пакетов Python
- **SQLAlchemy** - ORM для работы с базой данных
- **PostgreSQL** - основная база данных
- **Redis** - кеширование и очереди задач
- **Celery** - асинхронные задачи
- **Pydantic** - валидация данных
- **scikit-learn** - машинное обучение
- **pandas, numpy** - анализ данных

### Frontend
- **React** - UI библиотека
- **TypeScript** - типизированный JavaScript
- **Material-UI** - компоненты интерфейса
- **React Router** - маршрутизация
- **Chart.js / Recharts** - графики и диаграммы
- **Axios** - HTTP клиент

## Установка и запуск

### Backend

1. Убедитесь, что у вас установлен Python 3.11+ и uv:
```bash
# Установка uv (если не установлен)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Перейдите в папку backend и установите зависимости:
```bash
cd backend
uv sync
```

3. Создайте файл .env на основе .env.example:
```bash
cp .env.example .env
# Отредактируйте .env файл с вашими настройками
```

4. Запустите приложение:
```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

1. Убедитесь, что у вас установлен Node.js 18+
2. Перейдите в папку frontend и установите зависимости:
```bash
cd frontend
npm install
```

3. Запустите приложение:
```bash
npm start
```

Приложение будет доступно по адресу http://localhost:3000

## API Documentation

После запуска backend API документация будет доступна по адресам:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Функциональность

### Основные возможности
- 📊 **Аналитика Instagram** - подробная статистика профиля и постов
- 🔮 **Предсказания** - прогнозы engagement, оптимальное время публикации
- 📈 **Визуализация данных** - интерактивные графики и диаграммы
- 🎯 **Рекомендации контента** - предложения на основе ML анализа
- 👤 **Управление профилем** - настройки и подключение Instagram аккаунта

### Планируемые функции
- Анализ конкурентов
- A/B тестирование контента
- Автоматические отчеты
- Интеграция с Instagram Business API

## Разработка

### Требования к коду
- Следуйте принципам SOLID
- Покрытие тестами > 80%
- Используйте type hints в Python
- Следуйте ESLint правилам в TypeScript

### Вклад в проект
1. Создайте форк репозитория
2. Создайте ветку для новой функции
3. Внесите изменения с тестами
4. Создайте Pull Request

## Лицензия

Этот проект лицензирован под MIT License - см. файл [LICENSE](LICENSE) для деталей.
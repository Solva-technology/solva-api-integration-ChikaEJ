[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=20250935&assignment_repo_type=AssignmentRepo)
# Telegram Bot (aiogram)

## 📌 Цель

Собрать Telegram-бота на **aiogram (v3+)** с **inline-клавиатурой из двух кнопок**, все действия должны работать **только через callback\_data**:

1. «Погода» — асинхронный запрос к **OpenWeatherMap**.
2. «Камень-Ножницы-Бумага» — мини-игра с ботом.

---

## ⚙️ Требования

### Технические

* Python **3.11+**, aiogram **3.x**, aiohttp **3.x**.
* Запуск в Docker, docker-compose для локальной разработки.
* Конфигурация через `.env` (не коммитить).
* Логи: structured (JSON) на stdout, уровень задаётся `LOG_LEVEL`.
* Тесты: pytest.
* Запись всех запросов погоды (город + результат) в MongoDB.
* Для просмотра данных подключить **MongoWeiver**.

### Функциональные

* Команда `/start` выводит inline-клавиатуру:

  * Кнопка 1: «Погода» (`cb: weather:ask_city`).
  * Кнопка 2: «КНБ» (`cb: rps:menu`).
* Все кнопки работают через **CallbackQuery**.
* **Погода**:

  * Используется OpenWeatherMap Current Weather Data API.
  * Единицы измерения: `metric`, язык: `ru`.
  * Обработка ошибок API (4xx/5xx/таймаут).
  * Каждый успешный запрос записывается в MongoDB (город, погода, дата/время).
* **Игра КНБ**:

  * Пользователь выбирает жест через inline-кнопки.
  * Бот случайным образом выбирает свой жест.
  * Ответ с результатом и предложением «Сыграть ещё».

### Контроль нагрузки

* Используется файл `sessions.json` для хранения активности пользователей.
* Файл очищается каждые **2 минуты**.
* Если пользователь сделал > 3 запросов за 2 минуты — доступ к функциям блокируется до очистки файла.

---

## 🔑 Переменные окружения (.env.example)

```env
BOT_TOKEN=000000000:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
OPENWEATHER_API_KEY=your_owm_api_key
OPENWEATHER_BASE_URL=https://api.openweathermap.org/data/2.5
MONGO_URI=mongodb://mongo:27017
MONGO_DB=weather_bot
LOG_LEVEL=INFO
```
---

## 📂 Архитектура проекта

```
app/
  main.py                 # точка входа
  keyboards/
    inline.py             # inline-клавиатуры
  services/
    weather_client.py     # aiohttp-клиент OpenWeatherMap
    mongo_client.py       # запись запросов в MongoDB
    rps.py                # логика игры
    sessions.py           # работа с sessions.json
  handlers/
    start.py           
    weather.py
    rps.py
  utils/
    logging.py

sessions.json             # аналог сессий (автоочистка)
tests/
  test_weather_client.py
  test_rps.py
  test_callbacks.py

Dockerfile
docker-compose.yml
requirements.txt
README.md
```

---

## 🔄 Сценарии работы

### Погода
1. `/start` → inline-кнопки \[«Погода», «КНБ»].
2. `cb=weather:ask_city` → бот просит ввести город.
3. Пользователь вводит текст города.
4. `cb=weather:get:<city>` → бот запрашивает погоду и выводит данные.
5. Результат сохраняется в MongoDB.
6. Ошибки API → дружелюбное сообщение и «Попробовать снова».
7. Если пользователь сделал > 3 запросов за 2 минуты → блокировка до очистки `sessions.json`.

### Камень-Ножницы-Бумага

1. `cb=rps:menu` → бот показывает кнопки: «Камень», «Ножницы», «Бумага».
2. Пользователь выбирает жест.
3. Бот выбирает случайный жест.
4. Результат + кнопка «Сыграть ещё».
---

## 📜 Формат callback\_data

* `weather:ask_city`
* `weather:get:<city>`
* `rps:menu`
* `rps:pick:<move>` (`rock|paper|scissors`)

---

## ✅ Тесты

* `test_rps.py`: проверка исходов при фиксированном рандоме.
* `test_weather_client.py`: мок `aiohttp` → ответы 200/404/500/таймаут.
* `test_callbacks.py`: проверка callback\_data.

---

## 📌 Критерии приёмки

* `/start` выводит inline-клавиатуру с 2 кнопками.
* Все взаимодействия через `CallbackQuery`.
* Погода: корректные данные или сообщение об ошибке.
* Все запросы к погоде сохраняются в MongoDB.
* Mongoweiver подключен и позволяет просматривать сохранённые данные.
* Пользователь ограничен 3 запросами за 2 минуты (контроль через `sessions.json`).
* КНБ: игра работает, можно «Сыграть ещё».
* Проект собирается в Docker, переменные читаются из `.env`.
* Логи JSON, линтеры проходят, тесты зелёные.

---

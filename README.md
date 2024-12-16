# Massa-k API

API для получения массы с весов МАССА-К через интерфейс RS-232/USB.

## Установка

1. Клонируйте репозиторий:
    ```sh
    git clone https://github.com/taubusu/massa-k-api.git
    cd mass-api
    ```

2. Создайте виртуальное окружение и активируйте его:
    ```sh
    python -m venv venv
    source venv/bin/activate  # для Windows: venv\Scripts\activate
    ```

3. Установите зависимости:
    ```sh
    pip install -r requirements.txt
    ```

## Запуск

1. Запустите Flask-сервер:
    ```sh
    python app.py
    ```

2. Сервер будет доступен по адресу `http://127.0.0.1:3333`.

## Использование

Запрос массы:
```sh
curl http://127.0.0.1:3333/mass?port=<COM-порт весов> (Например: http://127.0.0.1:3333/mass?port=СOM3)
```

Приложение может быть упаковано в .exe приложение для простоты запуска с помощью pyinstaller
```
pyinstaller --onefile app.py
```



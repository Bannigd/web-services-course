# Подготовка веб-сервиса к запуску
---
Все пункты, кроме настройки ключей для FusionBrain API, можно сделать, выполнив скрипт `setup.sh`.

1. Создать виртуальное окружение и установить необходимые зависимости:
```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

2. Дальше необходимо добавить API ключи для FusionBrain API (через него осуществляется доступ к Кандинскому). Создадим `.env` файл и сохраним эти ключи там:

```
KAND_API=<API ключ>
KAND_SECRET=<Секретный ключ>
```

3. Создадим секретный ключ для Flask и запишем в файл `.flask_env`: 

```bash
python -c 'import secrets; print(f"SECRET_KEY={secrets.token_hex()}")' > .flask_env
```

4. Создадим директорию `static`, где будут храниться изображения:
```bash
mkdir static
```

5. Теперь все готово к запуску:

```bash
python app.py
```


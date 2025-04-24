# Подготовка веб-сервиса к запуску
---

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
python -c 'import secrets; print(secrets.token_hex())' > .flask_env
```

4. Теперь все готово к запуску:

```bash
python app.py
```



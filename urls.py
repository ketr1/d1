SOURCE_DB = BASE_DIR / 'db.sqlite3'

if os.environ.get('VERCEL') == '1':
    TMP_DB = Path('/tmp/db.sqlite3')

    if SOURCE_DB.exists() and not TMP_DB.exists():
        shutil.copyfile(SOURCE_DB, TMP_DB)

    DB_NAME = TMP_DB
else:
    DB_NAME = SOURCE_DB

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DB_NAME,
    }
}
import locale
import os

encoding = locale.getpreferredencoding()


def loadEnv():
    try:
        with open(".env", "r", encoding=encoding) as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and comments
                if not line or line.startswith("#"):
                    continue
                # Split into key and value (handle optional quotes)
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()
                # Remove surrounding quotes if present
                if value.startswith(('"', "'")) and value[0] == value[-1]:
                    value = value[1:-1]
                os.environ[key] = value
    except FileNotFoundError:
        print("Warning: Not found. Using system environment variables.")

from loguru import logger

# Konfigurasi logger menggunakan satu file untuk semua level log
log_config = {
    "handlers": [
        {
            "sink": "logs/app.log",
            "rotation": "2 weeks",
            "retention": "2 weeks",
            "level": "INFO",
            "serialize": True
        }
    ]
}

# Tambahkan konfigurasi ke logger
for handler in log_config["handlers"]:
    logger.add(**handler)

# Ekspor logger
__all__ = ["logger"]
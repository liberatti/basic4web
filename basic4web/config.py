import pytz

_config = {
    'DATETIME_FMT': "%Y-%m-%dT%H:%M:%S.%fZ",
    'TZ': pytz.timezone("UTC"),
    'SECURITY_ENABLED': True,
    'JWT_AUD': 'app',
    'JWT_SECRET_KEY': 'dev',
    'JWT_EXPIRE': 1800,
    'LOG_LEVEL': 'INFO',
    'CORE_VERSION': 'v0.0.2'
}


def init(overrides: dict = None):
    if overrides:
        _config.update(overrides)


def get(key, default=None):
    return _config.get(key, default)


def has(keys):
    hasattr(_config, keys)

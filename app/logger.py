import logging
import logging.config

from environs import Env


def setup_logger():
    Env.read_env()
    env = Env()

    log_level = env.str("LOG_LEVEL", default="INFO").upper()
    root_log_level = env.str("ROOT_LOG_LEVEL", default="WARNING").upper()

    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "detailed": {
                "class": "logging.Formatter",
                "format": (
                    "[%(asctime)s] [%(process)d] [%(levelname)s] "
                    "[%(name)s] %(message)s"
                ),
                "datefmt": "%Y-%m-%d %H:%M:%S %z",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": log_level,
                "formatter": "detailed",
                "filters": ["healthcheck_filter"],
            },
        },
        "filters": {
            "healthcheck_filter": {"()": "app.logger.HealthCheckFilter"},
        },
        "loggers": {
            "": {
                "level": root_log_level,
                "handlers": ["console"],
                "propagate": False,
            },
            "app": {
                "handlers": ["console"],
                "level": log_level,
                "propagate": False,
            },
            "__main__": {
                "handlers": ["console"],
                "level": log_level,
                "propagate": False,
            },
            "uvicorn": {
                "handlers": ["console"],
                "level": log_level,
                "propagate": False,
            },
        },
    }

    logging.config.dictConfig(log_config)


class HealthCheckFilter(logging.Filter):
    def filter(self, record):
        msg = record.getMessage()
        return all(
            (
                "/healthz" not in msg,
                "/readiness" not in msg,
                "/metrics" not in msg,
            )
        )

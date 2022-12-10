""" Utils for IoC """
from typing import Callable

from dependency_injector.wiring import Provide
from fastapi.params import Depends


def toggleable(cls) -> Callable:
    """
    Позволяет отключать сервис
    """

    def _inner(toggle: bool, *args, **kwargs):
        if toggle:
            return cls(*args, **kwargs)
        else:
            return None

    return _inner


def already_initialized(instance) -> Callable:
    def _inner():
        return instance

    return _inner


def async_closeable(cls) -> Callable:
    """
    Позволяет инициализировать асинхронный ресурс

    https://python-dependency-injector.ets-labs.org/providers/resource.html#asynchronous-initializers
    """

    async def _inner(*args, **kwargs):
        instance = cls(*args, **kwargs)
        yield instance

        if instance is not None:
            if hasattr(instance, "aclose"):
                await instance.aclose()

            if hasattr(instance, "close"):
                await instance.close()

            elif hasattr(instance, "shutdown"):
                await instance.shutdown()

    return _inner


class ProvideDependency(Provide, Depends):
    """
    Связующий слой между механизмами инъекции зависимостей
    FastAPI и Dependency Injector (библиотека).
    """

    def __init__(self, *args, **kwargs):
        Depends.__init__(self, dependency=self, use_cache=False)
        Provide.__init__(self, *args, **kwargs)


def get_dependency(dependency_name: str):
    """
    Вспомогательная функция позволяющая инжектить зависимости объявленные
    в контейнере.

    >>> from dependency_injector.wiring import inject
    >>>
    >>> @inject
    >>> def some_func(service = autowire("some_service")):
    >>>     service.some_method()
    """
    return ProvideDependency[dependency_name]  # type:ignore

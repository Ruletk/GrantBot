import logging

logger = logging.getLogger(__name__)


class Injector:
    def __init__(self):
        logger.debug("Initializing injector")
        self._dependencies = {}

    def register(self, dependency, dependency_name=None):
        if dependency_name is None:
            dependency_name = dependency.__name__
        logger.debug(f"Registering {dependency_name} as {dependency}")
        self._dependencies[dependency_name] = dependency

    def get(self, dependency_name):
        logger.debug(f"Getting {dependency_name}")
        return self._dependencies.get(dependency_name)

    def inject(self, dependency_name):
        def decorator(func):
            def wrapper(*args, **kwargs):
                logger.debug(f"Injecting {dependency_name} into {func}")
                dependencies = {}
                for dependency in dependency_name:
                    dependencies[dependency] = self.get(dependency)
                kwargs.update(dependencies)
                return func(*args, **kwargs)

            return wrapper

        return decorator


injector = Injector()

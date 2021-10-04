from abc import (
    ABCMeta,
    abstractmethod
)


# =============================================================================
# CLASS IDENTITY GENERATOR
# =============================================================================
class IdentityGenerator(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def next(self) -> str:
        pass

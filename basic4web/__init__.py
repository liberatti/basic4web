"""basic4web - Biblioteca interna para uso em projetos privados."""

__version__ = "0.0.2"

from gevent import monkey

monkey.patch_all(thread=False)

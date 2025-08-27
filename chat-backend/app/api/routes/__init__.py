# app/api/routes/__init__.py
from .auth import router as auth_router
from .document import router as document_router
from .query import router as query_router

__all__ = ['auth_router', 'document_router', 'query_router']
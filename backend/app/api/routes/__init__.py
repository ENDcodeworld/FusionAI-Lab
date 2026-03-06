"""
Routes package
"""

from app.api.routes import (
    companies,
    funding,
    papers,
    experiments,
    reports,
    users,
    auth
)

__all__ = [
    "companies",
    "funding",
    "papers",
    "experiments",
    "reports",
    "users",
    "auth"
]

from fastapi import FastAPI
from app.settings import settings
from app.logging import configure_logging
from app.middlewares import CorrelationIdMiddleware
from app.routes.health import router as health_router
from app.routes.customize import router as customize_router


def create_app() -> FastAPI:
    configure_logging(settings.log_level)

    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
    )

    app.add_middleware(CorrelationIdMiddleware)

    app.include_router(health_router)
    app.include_router(customize_router)

    return app


app = create_app()

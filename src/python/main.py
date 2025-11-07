import asyncio
import platform
import uvicorn
from fastapi import FastAPI
from importlib.metadata import version, PackageNotFoundError

try:
    package_version = version("backend")
except PackageNotFoundError:
    package_version = "0.0.0-dev"

app = FastAPI(
    version=package_version
)


@app.get("/")
async def root():
    return {"message": "Hello from FastAPI!"}


async def main() -> None:
    """
    Основная корутина приложения.
    Запускает uvicorn сервер.
    """
    config = uvicorn.Config(
        app=app,
        host="0.0.0.0",
        port=8000,
        reload=True,  # Можно включить True для dev-режима
        log_level="info",
    )
    server = uvicorn.Server(config)
    await server.serve()


def entrypoint() -> None:
    """
    Точка входа в приложение.
    Настраивает event loop policy для Windows и запускает main().
    """
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nApplication stopped by user (KeyboardInterrupt)")
    except Exception as e:
        print(f"FATAL ERROR: Application crashed: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    entrypoint()

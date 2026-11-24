from fastapi import FastAPI

app = FastAPI(
    title="PayLink API",
    description="Bill-payment and digital wallet backend service",
    version="0.1.0",
)


@app.get("/health", tags=["System"])
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "paylink-backend"}
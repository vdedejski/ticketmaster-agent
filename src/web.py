import uvicorn
from fastapi import FastAPI, status

from src.models.health import HealthCheck

from chainlit.utils import mount_chainlit

app = FastAPI()

@app.get(
    "/health",
    tags=["healthcheck"],
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck,
)
def health_check():
    return HealthCheck(status="200 OK")

mount_chainlit(app=app, target="./src/services/chainlit_service.py", path="/chainlit")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

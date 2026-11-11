import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.endpoints.ws import listen_to_redis

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(listen_to_redis())
    yield
    task.cancel()

app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/health")
def health_check():
    return {"status": "ok", "app": settings.APP_NAME}

from app.api.v1.endpoints import nodes, vms, network, lb, ws
app.include_router(nodes.router, prefix=f"{settings.API_V1_PREFIX}/nodes", tags=["Nodes"])
app.include_router(vms.router, prefix=f"{settings.API_V1_PREFIX}/vms", tags=["Virtual Machines"])
app.include_router(network.router, prefix=f"{settings.API_V1_PREFIX}/network", tags=["Network"])
app.include_router(lb.router, prefix=f"{settings.API_V1_PREFIX}/load-balancer", tags=["Load Balancer"])
app.include_router(ws.router, prefix="/ws", tags=["WebSockets"])
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .helio_config import Settings
from .routers import helio_document_router
from .routers import helio_qa_service
from .routers import helio_query_service
from .routers import helio_question_service

# =================== Settings ===================

# Load application settings
settings = Settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=settings.app_description,
    contact={
        "name": settings.contact_name,
        "url": settings.contact_url,
        "email": settings.contact_email,
    },
    license_info={
        "name": settings.license_name,
        "url": settings.license_url,
    },
)

# CORS Settings
origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------- Include Routers -------------------------- #

# Register sub modules
app.include_router(helio_qa_service.router, tags=["Answer Generation"])
app.include_router(helio_query_service.router, tags=["Query Expansion"])
app.include_router(
    helio_question_service.router,
    tags=["Hypothetical Question Generation"],
)
app.include_router(helio_document_router.router, tags=["Document Management"])

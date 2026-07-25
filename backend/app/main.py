from fastapi import FastAPI, HTTPException

from app.models import AuditRequest, AuditResponse

from app.services.fetcher import (
    FetchError,
    NonHTMLResponseError,
    RequestTimeoutError,
    fetch_page,
)

from app.services.parser import parse_html

from app.utils.validators import (
    UnsafeURLError,
    validate_public_url,
)
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Page Pulse API",
    description=(
        "A lightweight API for auditing basic "
        "technical and on-page webpage information."
    ),
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "name": "Page Pulse API",
        "version": "1.0.0",
        "status": "running",
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }


@app.post(
    "/api/audit",
    response_model=AuditResponse,
)
async def audit_page(request: AuditRequest):

    try:
        # Convert Pydantic's HttpUrl object into a normal string
        url = str(request.url)

        # Make sure the URL does not point to localhost/private networks
        validate_public_url(url)

        # Download the webpage
        page = await fetch_page(url)

        # Analyze the downloaded HTML
        analysis = parse_html(
            page["html"]
        )

        # Combine HTTP information + HTML analysis
        return AuditResponse(
            url=page["final_url"],
            http_status=page["status_code"],
            response_time_ms=page["response_time_ms"],
            title=analysis["title"],
            meta_description=analysis["meta_description"],
            h1_count=analysis["h1_count"],
            images_missing_alt=analysis["images_missing_alt"],
            word_count=analysis["word_count"],
        )

    except UnsafeURLError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except RequestTimeoutError as exc:
        raise HTTPException(
            status_code=504,
            detail=str(exc),
        ) from exc

    except NonHTMLResponseError as exc:
        raise HTTPException(
            status_code=415,
            detail=str(exc),
        ) from exc

    except FetchError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                "An unexpected error occurred "
                "while auditing the page."
            ),
        ) from exc
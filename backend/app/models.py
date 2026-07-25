from typing import Optional

from pydantic import BaseModel, HttpUrl

class AuditRequest(BaseModel):
    url: HttpUrl

class AuditResponse(BaseModel):
    url: str
    http_status: int
    response_time_ms: int
    title: Optional[str] = None
    meta_description: Optional[str] = None
    h1_count: int
    images_missing_alt: int
    word_count: int
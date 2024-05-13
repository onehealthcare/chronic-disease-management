from typing import List, Optional

from pydantic import BaseModel


class Span(BaseModel):
    offset: int
    length: int


class Word(BaseModel):
    content: str
    boundingBox: List[int]
    confidence: Optional[float] = None
    span: Optional[Span] = None
    spans: Optional[List[Span]] = None


class Page(BaseModel):
    height: int
    width: int
    angle: int
    pageNumber: int
    words: List[Word]


class Style(BaseModel):
    isHandwritten: bool
    spans: List[Span]
    confidence: float


class ReadResult(BaseModel):
    stringIndexType: str
    content: str
    pages: List[Page]
    styles: List[Style]
    modelVersion: str


class Metadata(BaseModel):
    width: int
    height: int


class Result(BaseModel):
    readResult: ReadResult
    modelVersion: str
    metadata: Metadata


class Innererror(BaseModel):
    code: str
    message: str


class Error(BaseModel):
    code: str
    message: str
    innererror: Innererror


class ResultError(BaseModel):
    error: Error

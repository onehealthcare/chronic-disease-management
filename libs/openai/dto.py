from typing import List

from pydantic import BaseModel


class Hate(BaseModel):
    filtered: bool
    severity: str


class SelfHarm(BaseModel):
    filtered: bool
    severity: str


class Sexual(BaseModel):
    filtered: bool
    severity: str


class Violence(BaseModel):
    filtered: bool
    severity: str


class ContentFilterResults(BaseModel):
    hate: Hate
    self_harm: SelfHarm
    sexual: Sexual
    violence: Violence


class PromptFilterResult(BaseModel):
    prompt_index: int
    content_filter_results: ContentFilterResults


class Message(BaseModel):
    role: str
    content: str


class Choice(BaseModel):
    finish_reason: str
    index: int
    message: Message
    content_filter_results: ContentFilterResults


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class Result(BaseModel):
    id: str
    object: str
    created: int
    model: str
    prompt_filter_results: List[PromptFilterResult]
    choices: List[Choice]
    usage: Usage

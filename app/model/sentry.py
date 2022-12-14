import uuid
from typing import Any, List, Literal, Optional, Union

from pydantic import BaseModel, Extra

SENTRY_RESOURCE = Literal[
    "installation", "event_alert", "issue", "metric_alert", "error", "comment"
]


class SentryActor(BaseModel):
    type: str
    id: str
    name: str


class SentryError(BaseModel):
    url: str
    web_url: str
    issue_url: str
    issue_id: str

    class Config:
        extra = Extra.allow


class SentryInstallation(BaseModel):
    status: str
    code: str
    uuid: uuid.UUID

    class Config:
        extra = Extra.allow


class SentryAlertEvent(BaseModel):
    url: str
    issue_url: str
    issue_id: Optional[str]
    event_id: str
    web_url: Optional[str]
    level: Optional[str]
    logger: Optional[str]
    message: Optional[str]

    class Config:
        extra = Extra.allow


class SentryIssueAlert(BaseModel):
    title: str
    settings: Optional[List[dict]]

    class Config:
        extra = Extra.allow


class SentryMetricAlertRule(BaseModel):
    id: str
    name: str
    triggers: Optional[List]

    class Config:
        extra = Extra.allow


class SentryIssue(BaseModel):
    url: str
    web_url: Optional[str]
    project_url: Optional[str]
    id: str
    type: Optional[str]
    event_id: Optional[str]
    culprit: Optional[str]

    class Config:
        extra = Extra.allow


class CommentData(BaseModel):
    comment: str
    project_slug: str
    comment_id: int
    issue_id: int
    timestamp: str


class ErrorData(BaseModel):
    error: SentryError


class InstallationData(BaseModel):
    installation: SentryInstallation


class AlertData(BaseModel):
    event: SentryAlertEvent
    triggered_rule: str
    issue_alert: Optional[SentryIssueAlert]

    class Config:
        extra = Extra.allow


class MetricAlertData(BaseModel):
    metric_alert: SentryMetricAlertRule
    description_text: str
    description_title: str
    web_url: str

    class Config:
        extra = Extra.allow


class IssueData(BaseModel):
    event: SentryIssue


class BasicInstallation(BaseModel):
    uuid: uuid.UUID


class SentryWebhook(BaseModel):
    action: str
    installation: Optional[BasicInstallation]
    data: Union[
        IssueData,
        MetricAlertData,
        AlertData,
        InstallationData,
        CommentData,
        ErrorData,
    ]
    actor: Optional[SentryActor]


class SentryLogEntry(BaseModel):
    formatted: str
    params: Optional[List[Any]]


class SentryGenericEvent(BaseModel):
    event_id: str
    logger: Optional[str]
    level: Optional[str]
    type: str
    culprit: Optional[str]
    transaction: Optional[str]
    environment: str
    metadata: Optional[dict]
    sdk: Optional[dict]
    extra: Optional[dict]
    tags: Optional[List[dict]]
    modules: Optional[dict]
    platform: str
    contexts: Optional[dict]
    logentry: Optional[SentryLogEntry]


class SentryWebhookEvent(BaseModel):
    id: str
    project: str
    project_name: str
    project_slug: str
    logger: Optional[str]
    level: Optional[str]
    url: Optional[str]
    triggering_rules: Optional[List[str]]
    event: SentryGenericEvent

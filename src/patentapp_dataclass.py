from dataclasses import dataclass, field
from datetime import date

@dataclass
class PatentApp:
    app_number: str
    title: str
    applicant: str
    filing_date: date
    status: str = field(default='pending')
    registration_date: date = field(default=None)
    ipc_classes: list[str] = field(default_factory=list)
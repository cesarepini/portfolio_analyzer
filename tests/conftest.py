import pytest

from src.patentapp_dataclass import PatentApp

from datetime import date

@pytest.fixture
def application_data_dict():
    return {
        'app_number': '26001001',
        'title': 'Acme Application',
        'applicant': 'ACME',
        'filing_date': date(2026, 1, 1),
        'registration_date': None,
        'status': 'pending',
        'ipc_classes': ['F25/D']
    }
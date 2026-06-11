import pytest

from src.patentapp_dataclass import PatentApp

from datetime import date

@pytest.fixture
def validate_dataclass():
    return PatentApp(
        app_number='26001001',
        title='An application',
        applicant='ACME',
        filing_date='20260101',
        ipc_classes=['F25/D']
    )

@pytest.fixture
def application_data_dict():
    return {
        'app_number': '26001001',
        'title': 'Acme Application',
        'applicant': 'ACME',
        'filing_date': '20220212',
        'status': 'pending',
        'ipc_classes': ['F25/D']
    }

@pytest.fixture
def application_data_dict_no_ipc():
    return {
        'app_number': '26001001',
        'title': 'Acme Application',
        'applicant': 'ACME',
        'filing_date': '20220212',
        'status': 'pending',
        'ipc_classes': ['']
    }
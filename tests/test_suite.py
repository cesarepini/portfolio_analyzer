from datetime import date, timedelta

import pytest

from src.validation import validate_application, ApplicationDataError

def test_missing_app_number(application_data_dict):
    del application_data_dict['app_number']
    with pytest.raises(ApplicationDataError):
        validate_application(application_data_dict)

def test_missing_title(application_data_dict):
    del application_data_dict['title']
    with pytest.raises(ApplicationDataError):
        validate_application(application_data_dict)

def test_missing_applicant(application_data_dict):
    del application_data_dict['applicant']
    with pytest.raises(ApplicationDataError):
        validate_application(application_data_dict)

def test_missing_filing_date(application_data_dict):
    del application_data_dict['filing_date']
    with pytest.raises(ApplicationDataError):
        validate_application(application_data_dict)

def test_multiple_missing_fields_reports_all(application_data_dict):
    del application_data_dict['app_number']
    del application_data_dict['title']
    with pytest.raises(ApplicationDataError, match='Missing application number'):
        validate_application(application_data_dict)

def test_filing_date_future(application_data_dict):
    application_data_dict['filing_date'] = date.today() + timedelta(days=1)
    with pytest.raises(ValueError):
        validate_application(application_data_dict)

@pytest.mark.parametrize('filing_date',[date.today(), date.today() - timedelta(days=1)])
def test_filing_date_valid(application_data_dict, filing_date):
    application_data_dict['filing_date'] = filing_date
    app = validate_application(application_data_dict)
    assert app.filing_date == filing_date

@pytest.mark.parametrize('registration_date', [date.today(), date(2026, 1, 1)])
def test_registration_date_valid(application_data_dict, registration_date):
    application_data_dict['registration_date'] = registration_date
    app = validate_application(application_data_dict)
    assert app.registration_date == registration_date

@pytest.mark.parametrize('registration_date', [date(2025, 12, 31), date.today() + timedelta(days=1)])
def test_registration_date_invalid(application_data_dict, registration_date):
    application_data_dict['registration_date'] = registration_date
    with pytest.raises(ValueError):
        validate_application(application_data_dict)

@pytest.mark.parametrize('status', ['pending', 'granted', 'dead'])
def test_status(application_data_dict, status):
    application_data_dict['status'] = status
    app = validate_application(application_data_dict)
    assert app.status == status

@pytest.mark.parametrize('status', ['unknown', None])
def test_invalid_status(application_data_dict, status):
    application_data_dict['status'] = status
    with pytest.raises(ValueError):
        validate_application(application_data_dict)
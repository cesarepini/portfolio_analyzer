from src.validation import validate_application


def test_dataclass_patent_application(validate_dataclass):
    assert validate_dataclass.app_number == '26001001'
    assert validate_dataclass.applicant == 'ACME'
    assert validate_dataclass.filing_date == '20260101'
    assert validate_dataclass.title == 'An application'
    assert validate_dataclass.ipc_classes == ['F25/D']

def test_data_validation(application_data_dict):
    application = validate_application(application_data_dict)
    assert application.app_number == '26001001'
    assert application.applicant == 'ACME'
    assert application.filing_date == '20220212'
    assert application.title == 'Acme Application'
    assert application.ipc_classes == ['F25/D']

def test_data_validation_no_ipc(application_data_dict_no_ipc):
    application = validate_application(application_data_dict_no_ipc)
    assert application.app_number == '26001001'
    assert application.applicant == 'ACME'
    assert application.filing_date == '20220212'
    assert application.title == 'Acme Application'
    assert application.ipc_classes == []
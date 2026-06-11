from src.application_serializer import portfolio_extraction_from_csv

def portfolio_analyzer() -> None:
    portfolio_extraction_from_csv()

if __name__ == '__main__':
    portfolio_analyzer()
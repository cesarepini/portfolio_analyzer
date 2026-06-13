from dataclasses import asdict
import json
from pathlib import Path

import dotenv

from src.application_serializer import data_extractrion_from_csv, application_extraction

def portfolio_analyzer() -> None:
    config = dotenv.dotenv_values('.env')
    input_file = input('Digit the name of the file containing the portfolio:>')
    if not input_file.endswith('.csv'):
        raise ValueError('The patent portfolio must be a .csv file.')
    file_path = Path(config['DATA_LOCATION_FOLDER']) / input_file
    try:
        raw_data = data_extractrion_from_csv(file_path)
        applications = application_extraction(raw_data)
    except FileNotFoundError:
        raise FileNotFoundError(f'File {file_path.name} not found.')
    output_file = input('Digit the name of the output file:>')
    if not output_file.endswith('.json'):
        raise ValueError('The output fule must be a .json file.')
    file_path = Path(config['DATA_LOCATION_FOLDER']) / output_file
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump([asdict(app) for app in applications], f, default=str, indent=2, ensure_ascii=False)
    except Exception as e:
        raise e

if __name__ == '__main__':
    portfolio_analyzer()
import os

import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from google.cloud import dataplex_v1

PROJECT = os.environ.get('PROJECT')
LOCATION = os.environ.get('LOCATION')
DATA_SCAN = os.environ.get('DATA_SCAN')


def get_data_scan(project, location, data_scan):
    def parse_condition_expectation(condition_name, condition_expectation, column, dimension, threshold):
        return {
            condition_name: {
                'sqlExpression': condition_expectation.sql_expression
            },
            'column': column,
            'dimension': dimension,
            'threshold': threshold
        }

    output_rules = []
    client = dataplex_v1.DataScanServiceClient()

    scan_request = dataplex_v1.GetDataScanRequest(
        name=f"projects/{project}/locations/{location}/dataScans/{data_scan}",
        view="FULL"
    )

    response = client.get_data_scan(request=scan_request)

    for rule in response.data_quality_spec.rules:
        if rule.row_condition_expectation:
            output_rules.append(parse_condition_expectation(condition_name='rowConditionExpectation',
                                                            condition_expectation=rule.row_condition_expectation,
                                                            column=rule.column,
                                                            dimension=rule.dimension,
                                                            threshold=rule.threshold))
        elif rule.table_condition_expectation:
            output_rules.append(parse_condition_expectation(condition_name='tableConditionExpectation',
                                                            condition_expectation=rule.table_condition_expectation,
                                                            column=rule.column,
                                                            dimension=rule.dimension,
                                                            threshold=rule.threshold))

        elif rule.set_expectation:
            output_rules.append({
                'setExpectation': {
                    'values': list(rule.set_expectation.values)
                },
                'column': rule.column,
                'dimension': rule.dimension,
                'ignoreNull': rule.ignore_null,
                'threshold': rule.threshold
            })
        elif rule.regex_expectation:
            output_rules.append({
                'regexExpectation': {
                    'regex': rule.regex_expectation.regex
                },
                'column': rule.column,
                'dimension': rule.dimension,
                'threshold': rule.threshold
            })
        elif rule.dimension == 'UNIQUENESS':
            output_rules.append({
                'uniquenessExpectation': {},
                'column': rule.column,
                'dimension': rule.dimension,
                'threshold': rule.threshold
            })
        elif rule.dimension == 'COMPLETENESS':
            output_rules.append({
                'nonNullExpectation': {},
                'column': rule.column,
                'dimension': rule.dimension,
                'threshold': rule.threshold
            })

    output = {
        'rules': output_rules,
        'samplingPercent': response.data_quality_spec.sampling_percent
    }
    return yaml.dump(output, Dumper=Dumper)


if __name__ == '__main__':
    output_yaml = get_data_scan(PROJECT, LOCATION, DATA_SCAN)
    print(output_yaml)

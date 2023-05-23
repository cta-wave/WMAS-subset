'''
file utility module, contains read wirte functions to a file
'''
import json
import csv

def read_json_file(file_name: str) -> dict:
    '''Read date from a json file'''
    with open(file_name, 'rt') as file:
        data = json.load(file)
    return data


def write_json_to_file(file_name: str, data: dict):
    '''Write JSON date to a file'''
    with open(file_name, 'w') as outfile:
        json.dump(data, outfile, indent=4, separators=(',', ': '), default=str)


def write_report_to_file(file_name: str, header: list, data: dict):
    '''Write subsetting report to a csv file'''
    with open(file_name, 'w', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)
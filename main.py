import csv
import os
import argparse


def csv_check(file_path: str, key: str, value: str, operator: str) -> bool:
    with open(file_path, encoding='utf-8-sig', errors='ignore', newline='') as f:
        csv_f = csv.DictReader(f)
        for row in csv_f:
            if eval('row[key]' + operator + 'value'):
                return True
            else:
                return False


def csv_read(file_path: str) -> dict:
    with open(file_path, encoding='utf-8-sig', errors='ignore', newline='') as f:
        return list(csv.DictReader(f))[0]


def csv_writer(file_path: str, row: dict):
    with open(file_path, 'w', encoding='utf-8-sig', newline='') as f:
        csv_f = csv.DictWriter(f, fieldnames=[*row])
        csv_f.writeheader()
        csv_f.writerow(row)


def list_of_files(place: str, extension: str) -> list:
    filelist = []
    for file in os.listdir(os.getcwd() if place == '' else place):
        if file.lower().endswith('.' + extension.lower()):
            filelist.append(place + file)
    return filelist


my_parser = argparse.ArgumentParser(
    description='Przykladowe wejscie: python .\edit-csv.py Dane/ csv "wartość depozytu" '
                '2321 "waluta nabycia" == USD \nlista operatorów:\n==\n>\n<\n!=\n>=\n<'
                '=\n Domyślne kodowanie UTF-8 BOM')
my_parser.add_argument('Path', metavar='path', type=str, help='miejsce np. Dane/')
my_parser.add_argument('Extension', metavar='extension', type=str, help='rozszerzenie np. csv')
my_parser.add_argument('ChangeKey', metavar='change value', type=str, help='warunek np. "wartość depozytu"')
my_parser.add_argument('ChangeValue', metavar='change value', type=str, help='wartosc np. 2321')
my_parser.add_argument('ConditionKey', metavar='condition key', type=str, help='warunek zmiany np. "waluta nabycia"')
my_parser.add_argument('ConditionOperator', metavar='condition operator', type=str,
                       choices=['=', '!=', '>', '<', '<=', '>='], help='operator zmiany np. ==')
my_parser.add_argument('ConditionValue', metavar='condition value', type=str, help='wartosc zmiany np. USD')
args = my_parser.parse_args()


def main():
    print(args)
    for file in list_of_files(args.Path, args.Extension):
        if csv_check(file, args.ConditionKey, args.ConditionValue, args.ConditionOperator):
            dictionary = csv_read(file)
            print(dictionary)
            dictionary.update({args.ChangeKey: args.ChangeValue})
            csv_writer(file, dictionary)


if __name__ == '__main__':
    main()

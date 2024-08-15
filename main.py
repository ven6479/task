from typing import Optional
from datetime import datetime

import re

date_pattern = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}"
pattern = f"FROM:(?P<start>{date_pattern}) TO:(?P<end>{date_pattern})"

date_format = "%Y-%m-%d %H:%M"


def str_to_date(date_string: str) -> Optional[datetime]:
    try:
        return datetime.strptime(date_string, date_format)
    except re.error:
        return


def search(text: str) -> tuple[Optional[datetime], Optional[datetime]]:
    match = re.search(pattern, text.strip())

    if match:
        date_start = match.group("start")
        date_end = match.group("end")
        return str_to_date(date_start), str_to_date(date_end)

    return None, None


def read_generator_files(file_path: str) -> str:
    with open(file_path) as file:
        for line in file:
            yield line


def main(file_path: str) -> int:
    operators = []

    for line in read_generator_files(file_path):
        start, end = search(line)

        if not (start and end):
            continue

        for i in range(len(operators)):
            if operators[i] <= start:
                operators[i] = end
                break
        else:
            operators.append(end)

    return len(operators)


if __name__ == '__main__':
    print(main('./test.log'))

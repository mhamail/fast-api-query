from datetime import datetime
from typing import List, Optional


def extractTupleArray(data: List):  # [["first_name", "string"], ["id", 1]]
    return [tuple(sublist) for sublist in data]


date_formats = [
    "dd-MM-yyyy",
    "dd/MM/yyyy",
    "d/M/yyyy",
    "dd/M/yyyy",
    "d/MM/yyyy",
    "dd-M-yyyy",
    "d-MM-yyyy",
    "d-M-yyyy",
    "d-MMM-yy",
    "dd-MMM-yy",
    "d-MMM-yyyy",
    "yyyy-MM-ddTHH:mm:ss.SSSZ",
    "yyyy-MM-ddTHH:mm:ss.SSS",
    "yyyy-MM-ddTHH:mm:ss",
    "yyyy-MM-dd",
]


def parse_date(
    date_string: str, formats: Optional[list[str]] = date_formats
) -> Optional[datetime]:
    for fmt in formats:
        try:
            # Convert the format to Python's strftime format
            fmt = (
                fmt.replace("dd", "%d")
                .replace("d", "%d")
                .replace("MM", "%m")
                .replace("M", "%m")
                .replace("yyyy", "%Y")
                .replace("yy", "%y")
                .replace("HH", "%H")
                .replace("mm", "%M")
                .replace("ss", "%S")
                .replace("SSS", "%f")
            )
            return datetime.strptime(date_string, fmt)
        except ValueError:
            continue
    return None

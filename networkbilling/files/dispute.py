from typing import List
import dateutil.parser as du
import datetime as dt

from pydantic.dataclasses import dataclass
from pydantic import constr, condecimal

import io
import csv
import pathlib as pl

import networkbill.files as files


@dataclass(frozen=True)
class Header:
    dnsp_code: constr(max_length=10)
    retailer_code: constr(max_length=10)
    timestamp: str
    start_period: dt.date
    end_period: dt.date

    @staticmethod
    def record_type() -> int:
        return 913

    @staticmethod
    def from_row(row: List[str]) -> "Header":
        return Header(
            dnsp_code=row[1],
            retailer_code=row[2],
            # this is a workaround as some dnsp put the header
            # using scientific notation....
            timestamp=row[3],
            start_period=du.parse(row[4]).date(),
            end_period=du.parse(row[5]).date(),
        )


@dataclass(frozen=True)
class Detail:
    unique_number: constr(max_length=20)
    line_id: constr(max_length=17)

    nmi: constr(max_length=10)
    nmi_checksum: constr(min_length=1, max_length=1)

    new_status_code: constr(max_length=4)
    status_change_comments: constr(max_length=240)

    @staticmethod
    def record_type() -> int:
        return 914

    @staticmethod
    def from_row(row: List[str]) -> "Detail":
        return Detail(
            unique_number=row[1],
            line_id=row[2],
            nmi=row[3],
            nmi_checksum=row[4],
            new_status_code=row[5],
            status_change_comments=row[6]
        )


@dataclass(frozen=True)
class Footer:
    record_count: condecimal(max_digits=10, decimal_places=0)

    @staticmethod
    def record_type() -> int:
        return 915

    @staticmethod
    def from_row(row: List[str]) -> "Footer":
        return Footer(
            record_count=row[1],
        )



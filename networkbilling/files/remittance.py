from typing import List, Iterable
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

    @staticmethod
    def record_type() -> int:
        return 800

    @staticmethod
    def from_row(row: List[str]) -> "Header":
        return Header(
            dnsp_code=row[1],
            retailer_code=row[2],
            # this is a workaround as some dnsp put the header
            # using scientific notation....
            timestamp=row[3],
        )


@dataclass(frozen=True)
class Detail:
    unique_number: constr(max_length=20)

    nmi: constr(max_length=10)
    nmi_checksum: constr(min_length=1, max_length=1)

    amount_paid: condecimal(max_digits=15, decimal_places=2)
    paid_date: dt.date
    payment_reference: constr(max_length=60)

    @staticmethod
    def record_type() -> int:
        return 810

    @staticmethod
    def from_row(row: List[str]) -> "Detail":
        return Detail(
            unique_number=row[1],
            nmi=row[2],
            nmi_checksum=row[3],
            amount_paid=row[4],
            paid_date=du.parse(row[5]).date(),
            payment_reference=row[6],
        )


@dataclass(frozen=True)
class Footer:
    record_count: condecimal(max_digits=10, decimal_places=0)

    @staticmethod
    def record_type() -> int:
        return 820

    @staticmethod
    def from_row(row: List[str]) -> "Footer":
        return Footer(
            record_count=row[1],
        )


@dataclass(frozen=True)
class Remittance:
    header: Header
    footer: Footer

    @staticmethod
    def from_filesystem(path: pl.Path) -> "Remittance":
        with open(path, 'r') as f:
            return Remittance(csv.reader(f))

    @staticmethod
    def from_str(f: str) -> "Remittance":
        return Remittance(csv.reader(io.StringIO(f)))

    def __init__(self, csv_reader: Iterable[List[str]]) -> None:
        self._files = dict()
        rows = len(csv_reader)
        for row in csv_reader:
            record_type = row[0]
            if record_type == Header.record_type():
                self.header = Header.from_row(row)
            elif record_type == Footer.record_type():
                self.footer = Footer.from_row(row)
            elif record_type == Detail.record_type():
                self.detail.append(Detail.from_row(row))
            else: 
                raise files.UnexpectedRecordType(
                    "got {got} when parsing remittance file row {row}"
                    .format(got=record_type, row=row))
        if self.header is None:
            raise files.MissingHeader()
        if self.footer is None:
            raise files.MissingFooter()
        if self.footer.record_count != rows:
            raise files.UnexpectedNumberOfRows(
                    "got {got} but expected {exp}"
                    .format(got=rows, exp=self.footer.record_count)
                    )

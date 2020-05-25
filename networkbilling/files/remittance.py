from typing import List
import dateutil.parser as du
import datetime as dt

from pydantic.dataclasses import dataclass
from pydantic import constr, condecimal


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



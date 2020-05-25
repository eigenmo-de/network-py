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
    start_period: dt.date
    end_period: dt.date

    @staticmethod
    def record_type() -> int:
        return 930

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

    nmi: constr(max_length=10)
    nmi_checksum: constr(min_length=1, max_length=1)

    issue_date: dt.date
    due_date: dt.date

    total_amount: condecimal(max_digits=15, decimal_places=2)

    dispute_recieved_indicator: constr(max_length=1)
    comments: constr(max_length=240)

    @staticmethod
    def record_type() -> int:
        return 931

    @staticmethod
    def from_row(row: List[str]) -> "Detail":
        return Detail(
            unique_number=row[1],
            nmi=row[2],
            nmi_checksum=row[3],
            issue_date=du.parse(row[4]).date(),
            due_date=du.parse(row[5]).date(),
            total_amount=row[6],
            dispute_recieved_indicator=row[7],
            comments=row[8],
        )


@dataclass(frozen=True)
class Footer:
    record_count: condecimal(max_digits=10, decimal_places=0)
    total_amount: condecimal(max_digits=15, decimal_places=2)

    @staticmethod
    def record_type() -> int:
        return 932

    @staticmethod
    def from_row(row: List[str]) -> "Footer":
        return Footer(
            record_count=row[1],
            total_amount=row[2],
        )

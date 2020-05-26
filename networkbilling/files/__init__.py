import networkbill.files.bill as bill
import networkbill.files.dispute as dispute
import networkbill.files.outstanding as outstanding
import networkbill.files.balance as balance
import networkbill.files.remittance as remittance

from typing import Callable, List, Any, Iterable, Dict

import abc
import io
import csv
import pathlib as pl


class UnexpectedRecordType(Exception):
    pass


class UnexpectedNumberOfRows(Exception):
    pass


class MissingHeader(Exception):
    pass


class MissingFooter(Exception):
    pass


class NetworkRow(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def from_row(row: List[str]):
        ...

    @staticmethod
    @abc.abstractmethod
    def record_type() -> int:
        ...

    def is_header(self) -> bool:
        return False

    def is_footer(self) -> bool:
        return False


class HeaderRow(NetworkRow):
    def is_header(self) -> bool:
        return True


class FooterRow(NetworkRow):
    @abc.abstractmethod
    def record_count(self) -> int:
        ...

    def is_footer(self) -> bool:
        return True


class NetworkFile(abc.ABC):
    header: HeaderRow
    footer: FooterRow
    details: Dict[int, NetworkRow] = {}

    @staticmethod
    def from_filesystem(path: pl.Path) -> "NetworkFile":
        with open(path, 'r') as f:
            return NetworkFile(csv.reader(f))

    @staticmethod
    def from_str(f: str) -> "NetworkFile":
        return NetworkFile(csv.reader(io.StringIO(f)))

    # this should index into a dict and throw a key error if record_type
    # is unexpected
    @staticmethod
    @abc.abstractmethod
    def record_mapping(record_type: int) -> Callable[[List[str], NetworkRow]]:
        ...

    @staticmethod
    @abc.abstractmethod
    def filename() -> str:
        ...

    def __init__(self, csv_reader: Iterable[List[str]]) -> None:
        self._files = dict()
        rows = len(csv_reader)
        for row in csv_reader:
            record_type = int(row[0])
            try:
                parsed = self.record_mapping(record_type)(row)
                if self.is_header(record_type):
                    self.header = parsed
                elif self.is_footer(record_type):
                    self.footer = parsed
                else:
                    self.details.insert(record_type, parsed)
            except KeyError:
                raise UnexpectedRecordType(
                    "got {got} when parsing {filename} file row {row}"
                    .format(got=record_type, filename=self.filename(), row=row)
                    )
        if self.header is None:
            raise MissingHeader()
        if self.footer is None:
            raise MissingFooter()
        if self.footer.record_count != rows:
            raise UnexpectedNumberOfRows(
                    "got {got} but expected {exp}"
                    .format(got=rows, exp=self.footer.record_count)
                    )


# can throw ValueError due to date parsing
def mapping(key: int) -> Callable[[List[str]], Any]:
    to_fn = {
        bill.Header.record_type(): bill.Header.from_row,
        bill.Footer.record_type(): bill.Footer.from_row,
        bill.Summary.record_type(): bill.Summary.from_row,
        bill.NuosCharge.record_type(): bill.NuosCharge.from_row,
        bill.EventCharge.record_type(): bill.EventCharge.from_row,
        dispute.Header.record_type(): dispute.Header.from_row,
        dispute.Detail.record_type(): dispute.Detail.from_row,
        dispute.Footer.record_type(): dispute.Footer.from_row,
        outstanding.Header.record_type(): outstanding.Header.from_row,
        outstanding.Detail.record_type(): outstanding.Detail.from_row,
        outstanding.Footer.record_type(): outstanding.Footer.from_row,
        balance.Header.record_type(): balance.Header.from_row,
        balance.Detail.record_type(): balance.Detail.from_row,
        balance.Footer.record_type(): balance.Footer.from_row,
        remittance.Header.record_type(): remittance.Header.from_row,
        remittance.Detail.record_type(): remittance.Detail.from_row,
        remittance.Footer.record_type(): remittance.Footer.from_row,
    }
    return to_fn[key]



import networkbilling.vic as vic
import networkbilling.nsw as nsw
import networkbilling.qld as qld
import networkbilling.sa as sa
import networkbilling.base as base

from typing import Any, Callable


# can throw ValueError due to date parsing

import csv
import io
import pathlib
from dataclasses import dataclass


@dataclass(frozen=True)
class State:

    def __init__(self, name: str):
        if name in ['nsw', 'qld', 'vic', 'sa']:
            State(name=name)
        else:
            raise base.UnsupportedState

    @property
    def name(self) -> str:
        return self.name

    def get_header_mapping(self) -> Callable[[int], Any]:
        if self.name == 'nsw':
            return nsw.header_mapping
        elif self.name == 'qld':
            return qld.header_mapping
        elif self.name == 'vic':
            return vic.header_mapping
        elif self.name == 'sa':
            return sa.header_mapping
        else:
            raise base.UnsupportedState


def from_filesystem(state: State, path: pathlib.Path) -> Any:
    with open(path, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
        header_record_type = int(data[0][0])
        return state.get_header_mapping()(header_record_type)(data)


def from_str(state: State, f: str) -> Any:
    reader = csv.reader(io.StringIO(f))
    data = list(reader)
    header_record_type = int(data[0][0])
    return state.get_header_mapping()(header_record_type)(data)

import networkbill.files.bill as bill
import networkbill.files.dispute as dispute
import networkbill.files.outstanding as outstanding
import networkbill.files.balance as balance
import networkbill.files.remittance as remittance

from typing import Callable, List, Any


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


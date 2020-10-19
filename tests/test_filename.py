from context import networkbilling
import datetime

def test_filename_one():
    name = "NEM#NBCHARGES#ENERGYAP#TESTPARTICIPANT#20200301012212V1.zip"
    parsed = networkbilling.FileName.parse(name)
    assert parsed.distributor == "ENERGYAP"
    assert parsed.retailer == "TESTPARTICIPANT"
    assert parsed.timestamp == datetime.datetime(2020, 3, 1, 1, 22, 12)
    assert parsed.version == 1
    assert parsed.state == "nsw"

def test_filename_two():
    name = "NEM#NBCHARGES#ENERGEXP#TESTPARTICIPANT#20201101012212V2053 - extrastuff #?*@.zip"
    parsed = networkbilling.FileName.parse(name)
    assert parsed.distributor == "ENERGEXP"
    assert parsed.retailer == "TESTPARTICIPANT"
    assert parsed.timestamp == datetime.datetime(2020, 11, 1, 1, 22, 12)
    assert parsed.version == 2053
    assert parsed.state == "qld"

def test_filename_three():
    name = "NEM_NBCHARGES_SOLARISP_TESTPARTICIPANT_20201022121210V1.zip"
    parsed = networkbilling.FileName.parse(name)
    assert parsed.distributor == "SOLARISP"
    assert parsed.retailer == "TESTPARTICIPANT"
    assert parsed.timestamp == datetime.datetime(2020, 10, 22, 12, 12, 10)
    assert parsed.version == 1
    assert parsed.state == "vic"

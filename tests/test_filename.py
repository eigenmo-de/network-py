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


def test_filename_four():
    name = "nem_nbcharges_solarisp_abcde_20201212222139v1.zip"
    parsed = networkbilling.FileName.parse(name)
    assert parsed.distributor == "SOLARISP"
    assert parsed.retailer == "ABCDE"
    assert parsed.timestamp == datetime.datetime(2020, 12, 12, 22, 21, 39)
    assert parsed.version == 1
    assert parsed.state == "vic"


def test_filename_five():
    name = "nem_nbcharges_solarisp_abcde_20201212201229v1.zip"
    parsed = networkbilling.FileName.parse(name)
    assert parsed.distributor == "SOLARISP"
    assert parsed.retailer == "ABCDE"
    assert parsed.timestamp == datetime.datetime(2020, 12, 12, 20, 12, 29)
    assert parsed.version == 1
    assert parsed.state == "vic"


def test_filename_six():
    name = "NEM#NBCHARGES#ENERGEXP#TESTPARTICIPANT#20201101012212- extrastuff #?*@.zip"
    parsed = networkbilling.FileName.parse(name)
    assert parsed.distributor == "ENERGEXP"
    assert parsed.retailer == "TESTPARTICIPANT"
    assert parsed.timestamp == datetime.datetime(2020, 11, 1, 1, 22, 12)
    assert parsed.version == None
    assert parsed.state == "qld"

def test_filename_seven():
    name = "NEM_NBCHARGES_SOLARISP_TESTPARTICIPANT_20201022121210.zip"
    parsed = networkbilling.FileName.parse(name)
    assert parsed.distributor == "SOLARISP"
    assert parsed.retailer == "TESTPARTICIPANT"
    assert parsed.timestamp == datetime.datetime(2020, 10, 22, 12, 12, 10)
    assert parsed.version == None
    assert parsed.state == "vic"


def test_filename_eight():
    name = "nem_nbcharges_solarisp_abcde_20201212222139.zip"
    parsed = networkbilling.FileName.parse(name)
    assert parsed.distributor == "SOLARISP"
    assert parsed.retailer == "ABCDE"
    assert parsed.timestamp == datetime.datetime(2020, 12, 12, 22, 21, 39)
    assert parsed.version == None
    assert parsed.state == "vic"


def test_filename_nine():
    name = "nem_nbcharges_solarisp_abcde_20201212201229.zip"
    parsed = networkbilling.FileName.parse(name)
    assert parsed.distributor == "SOLARISP"
    assert parsed.retailer == "ABCDE"
    assert parsed.timestamp == datetime.datetime(2020, 12, 12, 20, 12, 29)
    assert parsed.version == None
    assert parsed.state == "vic"


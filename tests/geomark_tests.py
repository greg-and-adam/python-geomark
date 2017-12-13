import unittest
from qq_tools.qq_tools import QQData


class QQTest(object):
    def setUp(self):
        self.filename = ''
        self.header = ''
        self.format = ''
        self.qq = None

    def test_header(self):
        self.assertEqual(self.header, ",".join(self.qqdata.header))

    def test_format_name(self):
        self.assertEqual(self.format, self.qqdata.format['format'])


class QQTestAutoSalt(QQTest, unittest.TestCase):
    def setUp(self):
        self.filename = 'tests/data/AQ05_029.CSV'
        self.header = 'DT,VCnt,TCnt,RTCTmp,RawV,EC,PrbTmp,EC.T'
        self.format = 'autosalt_generic_0'

        with open(self.filename, 'r') as f:
            self.qqdata = QQData(f)


class QQTestAutoSalt_1(QQTest, unittest.TestCase):
    def setUp(self):
        self.filename = 'tests/data/AQ05_unknown.CSV'
        self.header = 'DT,RTCTmp,RawV,EC,PrbTmp,EC.T'
        self.format = 'autosalt_generic_1'

        with open(self.filename, 'r') as f:
            self.qqdata = QQData(f)


class QQTestQQ_1(QQTest, unittest.TestCase):
    def setUp(self):
        self.filename = 'tests/data/SDIQ_CH0_20170605_083410.csv'
        self.header = 'DateTime,EC(uS/cm),Temp(oC),EC.T(uS/cm),Mass(kg),CF.T,BGEC.T(uS/cm),Q(cms),S_BGEC.T(uS/cm),2sUnc_Q(%),SNR,dt(s),Area(s*uS/cm),Ins.Res(uS/cm)'
        self.format = 'qq_generic_0'

        with open(self.filename, 'r') as f:
            self.qqdata = QQData(f)


class QQTestQQ_2(QQTest, unittest.TestCase):
    def setUp(self):
        self.filename = 'tests/data/SDIQ_CH0_20171110_093640.csv'
        self.header = 'DateTime,EC(uS/cm),Temp(oC),EC.T(uS/cm),Mass(kg),CF.T,BGEC.T(uS/cm),Q(cms),S_BGEC.T(uS/cm),2sUnc_Q(%),SNR,dt(s),Area(s*uS/cm),Ins.Res(uS/cm)'
        self.format = 'qq_generic_0'

        with open(self.filename, 'r') as f:
            self.qqdata = QQData(f)

import datetime
import unittest

from intervals import SingleInterval
from intervals.infinity import Infinity
from intervals.endpoint import Endpoint
from intervals.comparable import Comparable


class TestSingleInterval(unittest.TestCase):
    def test_cmp(self):
        test_interval_boundary(self, 3, 4)
        self.assertTrue(SingleInterval(3, 4) < 5)
        self.assertTrue(-1 < SingleInterval(3, 4))
        self.assertTrue(3 <= SingleInterval(3, 4))
        self.assertTrue(SingleInterval(3, 4) <= 4)
        self.assertTrue(SingleInterval(datetime.date(2018, 5, 10), datetime.date(2018, 5, 15)) <= datetime.date(2018, 5, 15))
        self.assertTrue(SingleInterval(datetime.date(2018, 5, 10), datetime.date(2018, 5, 15)) < datetime.date(2018, 5, 16))
        self.assertFalse(SingleInterval(datetime.date(2018, 5, 10), datetime.date(2018, 5, 15)) > datetime.date(2018, 5, 14))
        test_interval_boundary(self, Infinity.Negative, Infinity.Positive)
        test_interval_boundary(self, 3, Infinity.Positive)
        test_interval_boundary(self, Infinity.Negative, 3)

    def test_contains(self):
        self.assertTrue(4 in SingleInterval(3, 5))
        self.assertTrue(3 in SingleInterval(3, 5))
        self.assertTrue(5 in SingleInterval(3, 5))
        self.assertFalse(2 in SingleInterval(3, 5))
        self.assertFalse(7 in SingleInterval(3, 5))
        self.assertFalse(3 in SingleInterval(Endpoint(3, open=True), 5))
        self.assertFalse(5 in SingleInterval(3, Endpoint(5, open=True)))
        self.assertTrue(-1 in SingleInterval(Infinity.Negative, 5))
        self.assertTrue(5 in SingleInterval(3, Infinity.Positive))
        self.assertTrue(Infinity.Positive in SingleInterval(3, Endpoint(Infinity.Positive, open=False)))
        self.assertTrue(Infinity.Negative in SingleInterval(Endpoint(Infinity.Negative, open=False), 3))
        self.assertFalse(Infinity.Positive in SingleInterval(3, Endpoint(Infinity.Positive, open=True)))
        self.assertFalse(Infinity.Negative in SingleInterval(Endpoint(Infinity.Negative, open=True), 3))

    def test_or(self):
        union1 = SingleInterval(3, 5) | SingleInterval(5, 6)
        union2 = SingleInterval(3, Endpoint(5, open=True)) | SingleInterval(5, 6)
        union3 = SingleInterval(3, 5) | SingleInterval(Endpoint(5, open=True), 6)
        for union in (union1, union2):
            self.assertFalse(2 in union)
            self.assertTrue(3 in union)
            self.assertTrue(4 in union)
            self.assertTrue(5 in union)
            self.assertTrue(6 in union)
            self.assertFalse(7 in union)
            self.assertEqual(union, SingleInterval(3, 6))
        union4 = SingleInterval(3, Endpoint(5, open=True)) | SingleInterval(Endpoint(5, open=True), 6)
        self.assertFalse(2 in union4)
        self.assertTrue(3 in union4)
        self.assertTrue(4 in union4)
        self.assertFalse(5 in union4)
        self.assertTrue(6 in union4)
        self.assertFalse(7 in union4)

    def test_and(self):
        union = SingleInterval(3, 5) & SingleInterval(4, 7)
        self.assertFalse(2 in union)
        self.assertFalse(3 in union)
        self.assertTrue(4 in union)
        self.assertTrue(5 in union)
        self.assertFalse(6 in union)
        self.assertFalse(7 in union)
        self.assertEqual(union, SingleInterval(4, 5))


class TestEndpoint(unittest.TestCase):
    def test_basics(self):
        self.assertTrue(Endpoint(3), Endpoint(10))  # 3 < 10

    def test_inf(self):
        NegInf = Endpoint(Infinity.Negative)
        PosInf = Endpoint(Infinity.Positive)
        SomeNumber = Endpoint(100)
        SomeDatetime = datetime.datetime.now()
        SomeDay = datetime.date.today()
        SomeTime = datetime.time(0, 0)
        targets = (SomeNumber, SomeDatetime, SomeDay, SomeTime)
        test_cmp_helper(self, NegInf, PosInf)  # -∞ < +∞
        for target in targets:
            test_cmp_helper(self, target, PosInf)   # x < ∞
        for target in targets:
            test_cmp_helper(self, NegInf, target)   # -∞ < x


class TestInfinity(unittest.TestCase):

    def test_cmp(self):
        test_cmp_helper(self, Infinity.Negative, Infinity.Positive)


class TestComparable(unittest.TestCase):

    def test_type_example(self):
        dt: Comparable = datetime.datetime.now()
        d: Comparable = datetime.date.today()
        t: Comparable = datetime.time(0, 0)
        x: Comparable = 1
        y: Comparable = 1.1


def test_cmp_helper(case, value1, value2):
    # value1 <= value2
    case.assertTrue(value1 < value2)
    case.assertTrue(value2 > value1)
    case.assertFalse(value1 > value2)
    case.assertFalse(value2 < value1)

    case.assertTrue(value1 <= value2)
    case.assertTrue(value2 >= value1)
    case.assertFalse(value1 >= value2)
    case.assertFalse(value2 <= value1)
    test_helper_equality(case, value1, value2)


def test_cmp_close_interval(case, value1, value2):
    # value1 <= value2
    case.assertTrue(value1 <= value2)
    case.assertTrue(value2 >= value1)
    test_helper_equality(case, value1, value2)


def test_cmp_open_interval(case, value1, value2):
    # value1 < value2
    case.assertTrue(value1 < value2)
    case.assertFalse(value1 > value2)
    case.assertTrue(value2 > value1)
    case.assertFalse(value2 < value1)
    test_helper_equality(case, value1, value2)


def test_helper_equality(case, value1, value2):
    case.assertTrue(value1 == value1)
    case.assertTrue(value2 == value2)

    case.assertTrue(value2 <= value2)
    case.assertTrue(value2 >= value2)
    case.assertFalse(value2 < value2)
    case.assertFalse(value2 > value2)

    case.assertTrue(value1 <= value1)
    case.assertTrue(value1 >= value1)
    case.assertFalse(value1 < value1)
    case.assertFalse(value1 > value1)


def test_interval_boundary(case, value1, value2):
    case.assertFalse(value1 == SingleInterval(value1, value2))
    case.assertFalse(SingleInterval(value1, value2) == value2)
    test_cmp_close_interval(case, value1, SingleInterval(Endpoint(value1, open=False), value2))
    test_cmp_close_interval(case, SingleInterval(value1, Endpoint(value2, open=False)), value2)
    test_cmp_open_interval(case, value1, SingleInterval(Endpoint(value1, open=True), value2))
    test_cmp_open_interval(case, SingleInterval(value1, Endpoint(value2, open=True)), value2)

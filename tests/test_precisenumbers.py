import pytest

import precisenumbers


def test_PreciseNumber_init():
    # String
    # - without 'precision' kwarg
    # -- with decimal
    pc1 = precisenumbers.PreciseNumber('180.010')
    assert pc1.multiplier == 1
    assert pc1.integer == 180
    assert pc1.fractional == 10
    assert pc1.precision == 3

    assert float(pc1) == 180.01
    assert str(pc1) == '180.010'

    pc1a = precisenumbers.PreciseNumber('-0.010')
    assert pc1a.multiplier == -1
    assert pc1a.integer == 0
    assert pc1a.fractional == 10
    assert pc1a.precision == 3

    assert float(pc1a) == -0.01
    assert str(pc1a) == '-0.010'

    # -- without decimal
    pc2 = precisenumbers.PreciseNumber('180')
    assert pc2.integer == 180
    assert pc2.fractional == 0
    assert pc2.precision == 0

    assert float(pc2) == 180
    assert str(pc2) == '180'

    # - with 'precision' kwarg
    # -- with decimal
    pc3 = precisenumbers.PreciseNumber('180.210', precision=4)
    assert pc3.integer == 180
    assert pc3.fractional == 2100
    assert pc3.precision == 4

    assert float(pc3) == 180.21
    assert str(pc3) == '180.2100'

    pc4 = precisenumbers.PreciseNumber('180.210', precision=2)
    assert pc4.integer == 180
    assert pc4.fractional == 21
    assert pc4.precision == 2

    assert float(pc4) == 180.21
    assert str(pc4) == '180.21'

    pc4_1 = precisenumbers.PreciseNumber('180.210', precision=0)
    assert pc4_1.integer == 180
    assert pc4_1.fractional == 0
    assert pc4_1.precision == 0

    assert float(pc4_1) == 180
    assert str(pc4_1) == '180'

    # -- without decimal
    pc5 = precisenumbers.PreciseNumber('180', precision=3)
    assert pc5.integer == 180
    assert pc5.fractional == 0
    assert pc5.precision == 3

    assert float(pc5) == 180
    assert str(pc5) == '180.000'

    # Floats
    # - without 'precision' kwarg
    # -- with decimal
    pc6 = precisenumbers.PreciseNumber(180.011)
    assert pc6.integer == 180
    assert pc6.fractional == 11
    assert pc6.precision == 3

    assert float(pc6) == 180.011
    assert str(pc6) == '180.011'

    pc6a = precisenumbers.PreciseNumber(-0.011)
    assert pc6a.multiplier == -1
    assert pc6a.integer == 0
    assert pc6a.fractional == 11
    assert pc6a.precision == 3

    assert float(pc6a) == -0.011
    assert str(pc6a) == '-0.011'

    # -- without decimal
    pc7 = precisenumbers.PreciseNumber(180)
    assert pc7.integer == 180
    assert pc7.fractional == 0
    assert pc7.precision == 0

    assert float(pc7) == 180
    assert str(pc7) == '180'

    # - with 'precision' kwarg
    # -- with decimal
    pc8 = precisenumbers.PreciseNumber(180.010, precision=4)
    assert pc8.integer == 180
    assert pc8.fractional == 100
    assert pc8.precision == 4

    assert float(pc8) == 180.01
    assert str(pc8) == '180.0100'

    pc9 = precisenumbers.PreciseNumber(180.210, precision=2)
    assert pc9.integer == 180
    assert pc9.fractional == 21
    assert pc9.precision == 2

    assert float(pc9) == 180.21
    assert str(pc9) == '180.21'

    # -- without decimal
    pc10 = precisenumbers.PreciseNumber(180, precision=4)
    assert pc10.integer == 180
    assert pc10.fractional == 0
    assert pc10.precision == 4

    assert float(pc10) == 180
    assert str(pc10) == '180.0000'

    with pytest.raises(ValueError):
        precisenumbers.PreciseNumber(1.0, precision=-5)


def test_PreciseNumber_equality():
    # Same number -> True
    assert precisenumbers.PreciseNumber(180.21) == precisenumbers.PreciseNumber(
        180.21
    )

    # Different precision -> True
    assert precisenumbers.PreciseNumber(180.2) == precisenumbers.PreciseNumber(
        180.21
    )
    assert precisenumbers.PreciseNumber(180.21) == precisenumbers.PreciseNumber(
        180.2
    )

    # Different numbers -> False
    assert precisenumbers.PreciseNumber(180.3) != precisenumbers.PreciseNumber(
        180.21
    )

    # Something that is not a PreciseNumber
    assert precisenumbers.PreciseNumber(180.3) != 'hi jess'


def test_precisenumber_repr():
    assert precisenumbers.PreciseNumber(1.0, precision=5).__repr__() == 'PreciseNumber(multiplier=1, integer=1, fractional=0, precision=5)'


def test_parse_number():
    with pytest.raises(NotImplementedError):
        precisenumbers.parse_number([1, 2])


def test_add():
    num = precisenumbers.PreciseNumber('1.0')
    assert num + precisenumbers.PreciseNumber('1.0') == precisenumbers.PreciseNumber('2.0')
    assert num + 1.0 == precisenumbers.PreciseNumber('2.0')
    assert num + 1 == precisenumbers.PreciseNumber('2')

    num = precisenumbers.PreciseNumber('1.00001')
    assert num + 2.005 == precisenumbers.PreciseNumber('3.005')


def test_subtract():
    num = precisenumbers.PreciseNumber('1.0')
    assert num - precisenumbers.PreciseNumber('1.0') == precisenumbers.PreciseNumber('0.0')
    assert num - 1.0 == precisenumbers.PreciseNumber('0.0')
    assert num - 1 == precisenumbers.PreciseNumber('0')

    num = precisenumbers.PreciseNumber('1.00001')
    assert num - 2.005 == precisenumbers.PreciseNumber('-1.004')


def test_float_to_str():
    assert precisenumbers._float_to_str(1.0) == '1.0'
    assert precisenumbers._float_to_str(1) == '1'
    assert precisenumbers._float_to_str(1e-07) == '0.0000001'
    assert precisenumbers._float_to_str(1e+16) == '1000000000000000'

    assert precisenumbers._float_to_str(-1.0) == '-1.0'
    assert precisenumbers._float_to_str(-1) == '-1'
    assert precisenumbers._float_to_str(-1e-07) == '-0.0000001'
    assert precisenumbers._float_to_str(-1e+16) == '-1000000000000000'

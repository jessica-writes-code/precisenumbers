import logging
import math
from typing import Optional, Tuple, Union

logger = logging.getLogger(__name__)


def parse_number(number: Union[float, int, str]) -> Tuple[int, int, int, int]:
    """Segment a number into the boolean negative indicator (which will be used to create
    the multiplier), integer, fractional, and precision

    Args:
        number: the number to be parsed
            e.g., '-85.1420'

    Returns:
        bool: whether or not the number is negative
            e.g., True
        int: the integer portion of the number
            e.g., 85
        int: the fractional portion of the number
            e.g., 1420
        int: the precision of the number (i.e., amount of values after the decimal)
            e.g., 4
    """
    if not isinstance(number, (float, int, str)):
        raise NotImplementedError('number must be float, int, or str')

    negative = math.copysign(1, float(number)) < 0

    if isinstance(number, int):
        return negative, abs(number), 0, 0

    number = str(number)

    if '.' in number:
        integer_str, fractional_str = number.split('.')
        return (
            negative,
            abs(int(integer_str)),
            int(fractional_str),
            len(fractional_str),
        )

    return negative, int(number), 0, 0


class PreciseNumber:
    """Representation of a number that has a value and a precision, i.e., the number of valid
    digits after the decimal."""

    PRECISION_WARNING: bool = True
    MAXIMUM_PRECISION: Optional[int] = None
    MAXIMUM: Optional[Union[float, int]] = None
    MINIMUM: Optional[Union[float, int]] = None

    def __init__(self, number: Union[float, int, str], precision: Optional[int] = None):
        if precision and precision < 0:
            raise ValueError('precision must be >= 0')

        # Parse input number
        (
            self.negative,
            self.integer,
            inferred_fractional,
            inferred_precision,
        ) = parse_number(number)

        # Handle optional precision kwarg
        if precision is None or precision == inferred_precision:
            self.fractional, self.precision = inferred_fractional, inferred_precision
        else:
            if precision < inferred_precision:
                logger.warning(
                    f'inferred precision value is {inferred_precision}; using specified '
                    + f'precision value of {precision}, '
                    + 'which may result in data loss'
                )
            self.fractional = self._change_power_of_ten(
                inferred_fractional, inferred_precision, precision
            )

            self.precision = precision

        # Ensure validity vs. MAXIMUM_PRECISION, MINIMUM, MAXIMUM
        if (
            self.MAXIMUM_PRECISION is not None
            and self.precision > self.MAXIMUM_PRECISION
        ):
            if self.PRECISION_WARNING:
                logger.warning(
                    'precision exceeds maximum allowable value, which may indicate errors in data; '
                    'this warning will not repeat'
                )
                self.set_precision_warning_false()

        if (self.MINIMUM is not None and float(self) < self.MINIMUM) or (
            self.MAXIMUM is not None and float(self) > self.MAXIMUM
        ):
            raise ValueError(
                f'number outside of valid range of ({self.MINIMUM}, {self.MAXIMUM})'
            )

    @classmethod
    def set_precision_warning_false(cls):
        cls.PRECISION_WARNING = False

    @property
    def multiplier(self) -> int:
        """Converts the is_negative property to the relevant multiplier"""
        return -1 if self.negative else 1

    @staticmethod
    def _change_power_of_ten(
        fractional: int, current_precision: int, new_precision: int
    ):
        """Change a fractional using one precision to a fractional using another precision"""
        return int(fractional * (10 ** (new_precision - current_precision)))

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, PreciseNumber):
            return False
        min_precision = min(self.precision, __o.precision)
        if self.integer == __o.integer and (
            self._change_power_of_ten(self.fractional, self.precision, min_precision)
            == self._change_power_of_ten(__o.fractional, __o.precision, min_precision)
        ):
            if self.precision != __o.precision:
                logger.warning(
                    'precision values differ; this may lead to unexpected equality results'
                )
            return True
        return False

    def __float__(self) -> float:
        """Provides the float representation of the PreciseNumber"""
        return self.multiplier * (self.integer + self.fractional / 10**self.precision)

    def __repr__(self) -> str:
        m = f'multiplier={self.multiplier}'
        i = f'integer={self.integer}'
        f = f'fractional={self.fractional}'
        p = f'precision={self.precision}'

        return f'PreciseNumber({m}, {i}, {f}, {p})'

    def __str__(self) -> str:
        """Provides the string representation of the PreciseNumber"""
        negative_indicator = '-' if self.multiplier == -1 else ''
        num_zeros = (self.precision - len(str(self.fractional)))

        if self.precision == 0:
            return negative_indicator + str(self.integer)

        before_decimal = f'{negative_indicator}{self.integer}'
        after_decimal = f'{"0" * num_zeros + str(self.fractional)}'

        return f'{before_decimal}.{after_decimal}'

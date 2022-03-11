# hehe not here :p
import math
from datetime import datetime, date, timedelta
import random

from owlready2 import Thing

from utils.context import ExtensionContext
from utils.utils import ValueGenerationException, DataTypeIssueException


def extend_core(context: ExtensionContext):
    _core = context.core

    class Date(Thing):
        namespace = _core
        # date_time_obj = datetime.strptime(date_time_str, '%d/%m/%Y %H:%M:%S')

        def __init__(self, name=None, namespace=None, has_date_format="%Y-%m-%d", **kwargs):
            super().__init__(name=name, namespace=namespace, **kwargs)
            self.has_date_format = has_date_format
            self._parse_date_format_to_find_precision_of_minimal_increment()

        def _get_timestamp_if_boundary_is_string(self, value):
            constraint_column_type = self._get_constrained_data_type()
            if constraint_column_type is not None \
                    and isinstance(constraint_column_type, _core.Date) \
                    and isinstance(value, str):
                value = datetime.strptime(value, constraint_column_type.has_date_format)
                return value.timestamp()
            return value

        def is_value_valid(self, proposed_value):
            try:
                return self.parse_if_needed(proposed_value) is not None
            except ValueError:
                return False

        def parse_if_needed(self, proposed_value):
            if isinstance(proposed_value, datetime):
                return proposed_value
            if isinstance(proposed_value, str):
                return datetime.strptime(proposed_value, self.has_date_format)
            raise ValueError(f"ERROR: Cannot convert {proposed_value} to datetime.")
            # except ValueError:
            #     return None

        def get_minimum_value(self):
            return datetime(1900, 1, 1, 0, 0, 0)

        def get_maximum_value(self):
            return datetime(2200, 12, 31, 23, 59, 59)

        def convert_to_string(self, value):
            if isinstance(value, datetime):
                return value.strftime(self.has_date_format)
            return value

        def _parse_date_format_to_find_precision_of_minimal_increment(self):
            # %y	Year without century as a zero-padded decimal number.
            # %Y	Year with century as a decimal number.
            # %d	Day of the month as a zero-padded decimal number.
            # %H	Hour (24-hour clock) as a zero-padded decimal number.
            # %I	Hour (12-hour clock) as a zero-padded decimal number.
            # %M	Minute as a zero-padded decimal number.
            # %S	Second as a zero-padded decimal number.
            # %f	Microsecond as a decimal number, zero-padded to 6 digits.

            if "%y" in self.has_date_format or "%Y" in self.has_date_format:
                self.has_datetime_precision = {"days": 365}
            if "%d" in self.has_date_format:
                self.has_datetime_precision = {"days": 1}

            if "%H" in self.has_date_format:
                self.has_datetime_precision = {"hours": 1}
            if "%I" in self.has_date_format:
                self.has_datetime_precision = {"hours": 1}
            if "%M" in self.has_date_format:
                self.has_datetime_precision = {"minutes": 1}
            if "%S" in self.has_date_format:
                self.has_datetime_precision = {"seconds": 1}
            if "%f" in self.has_date_format:
                self.has_datetime_precision = {"microseconds": 1}

        def get_minimal_increment_value(self):
            self._parse_date_format_to_find_precision_of_minimal_increment()
            return timedelta(**self.has_datetime_precision)

        def generate_for_closed_range(self, left: datetime, right: datetime):
            if right < left:
                raise ValueGenerationException(f"ERROR: Left date is greater then right.")

            boundary_delta: timedelta = right - left
            new_random_days = random.randint(0, boundary_delta.days)
            new_random_seconds = random.randint(0, boundary_delta.seconds)

            return left + timedelta(days=new_random_days, seconds=new_random_seconds)

    class Varchar(Thing):
        namespace = _core

        # def __init__(self, name=None, namespace=None, **kwargs):
        #     pass

        def generate_for_closed_range(self, left, right):
            raise ValueGenerationException(f"ERROR: No range for Varchar")

        def is_value_valid(self, proposed_value):
            return True

        def parse_if_needed(self, proposed_value):
            return proposed_value

        def convert_to_string(self, value):
            return str(value)

    class Decimal(Thing):
        namespace = _core

        def is_value_valid(self, value):
            if isinstance(value, datetime):
                raise DataTypeIssueException(f"ERROR: Datetime {value} cannot be converted to decimal.")

            if isinstance(value, str) or isinstance(value, int):
                try:
                    value = float(value)
                except ValueError as error:
                    return False
            return (value * math.pow(10, self.has_scale) - int(value * math.pow(10, self.has_scale))) == 0

        def parse_if_needed(self, proposed_value):
            if isinstance(proposed_value, str):
                return float(proposed_value)
            elif isinstance(proposed_value, int):
                return float(proposed_value)
            elif isinstance(proposed_value, float):
                return proposed_value
            else:
                raise DataTypeIssueException(
                    f"ERROR: Cannot convert {proposed_value} to numeric value for {self.name} datatype.")

        def get_minimum_value(self):
            return sum(math.pow(10, d) * 9 for d in range(0, self.has_precision)) * -1 / math.pow(10, self.has_scale)

        def get_maximum_value(self):
            return sum(math.pow(10, d) * 9 for d in range(0, self.has_precision)) / math.pow(10, self.has_scale)

        def get_minimal_increment_value(self):
            return 1 / math.pow(10, self.has_scale)

        def generate_for_closed_range(self, left, right):
            scaleless_min_viable_value = int(left * math.pow(10, self.has_scale))
            scaleless_max_viable_value = int(right * math.pow(10, self.has_scale))

            chosen_number = random.randint(scaleless_min_viable_value, scaleless_max_viable_value)
            return chosen_number / math.pow(10, self.has_scale)

        def convert_to_string(self, value):
            return str(value)

    class Boolean(Thing):
        namespace = _core

        def generate_for_closed_range(self, left, right):
            raise ValueGenerationException(f"ERROR: No range for Boolean")

        def convert_to_string(self, value):
            """Maybe here you can have some setting how do you represent bool: 1, True, true"""
            return str(value)

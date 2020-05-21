"""A `dowel.logger.LogOutput` for CSV files."""
import csv
import warnings

from dowel import TabularInput
from dowel.simple_outputs import FileOutput
from dowel.utils import colorize


class CsvOutput(FileOutput):
    """CSV file output for logger.

    :param file_name: The file this output should log to.
    """

    def __init__(self, file_name):
        super().__init__(file_name)
        self._writer = None
        self._fieldnames = None
        self._warned_once = set()
        self._disable_warnings = False

    @property
    def types_accepted(self):
        """Accept TabularInput objects only."""
        return (TabularInput, )

    def record(self, data, prefix=''):
        """Log tabular data to CSV."""
        if isinstance(data, TabularInput):
            to_csv = data.as_primitive_dict

            if not to_csv.keys() and not self._writer:
                return

            if not self._writer:
                self._fieldnames = set(to_csv.keys())
                self._writer = csv.DictWriter(
                    self._log_file,
                    fieldnames=self._fieldnames,
                    extrasaction='ignore')
                self._writer.writeheader()

            if to_csv.keys() != self._fieldnames:
                                
                # update new field name
                new_field = set(to_csv.keys())
                self._fieldnames.update(new_field)

                # read existing file and write back with new fieldname
                # self._log_file contains: name, mode, encoding
                # <_io.TextIOWrapper name='out.csv' mode='w' encoding='cp1252'>
                with open(self._log_file.name, "r") as csvfileog:
                    original_data = csv.DictReader(csvfileog)

                    self._writer = csv.DictWriter(
                    self._log_file,
                    fieldnames=self._fieldnames,
                    extrasaction='raise')
                    self._log_file.seek(0)
                    self._writer = self.csvwriter(self._log_file, self._fieldnames, 'ignore', True)

                    # overwrite the file from beginning
                    
                    for row in original_data:
                        self._writer.writerow(row)

            self._writer.writerow(to_csv)

            for k in to_csv.keys():
                data.mark(k)
        else:
            raise ValueError('Unacceptable type.')

    def csvwriter (self, filename, fieldnames,extrasaction,writeheader):
        writer = csv.DictWriter(
            filename,
            fieldnames = fieldnames,
            extrasaction = extrasaction)
        if writeheader:
            self._writer.writeheader()
        return writer

    def _warn(self, msg):
        """Warns the user using warnings.warn.

        The stacklevel parameter needs to be 3 to ensure the call to logger.log
        is the one printed.
        """
        if not self._disable_warnings and msg not in self._warned_once:
            warnings.warn(
                colorize(msg, 'yellow'), CsvOutputWarning, stacklevel=3)
        self._warned_once.add(msg)
        return msg

    def disable_warnings(self):
        """Disable logger warnings for testing."""
        self._disable_warnings = True


class CsvOutputWarning(UserWarning):
    """Warning class for CsvOutput."""

    pass

#fileparse.py
import csv

def extract_val(string):
    return string.strip('\xef\xbb\xbf').strip()

def parse_csv(filename, select=None, types=None, has_headers=True,
              delimiter=',', ignore_errors=False, headers=None, max_entries=0,
              stop_on_blank_lines=False):
    '''Parse a CSV file into a list of records with type conversion.

    filename: The name of the csv file to parse.  The file name can be relative
            or an absolute path
    select: A list of headers to select.  If the list is empty, which is the
            default, all headers are returned.
    types: A list of functions used for type conversion.  Each function must
            except a string as a parameter and return the appropriate converted
            type. The order of this list must match the order of the 'headers'
            parameter.
    has_headers: a bool indicating whether the csv file has headers - default
            is True
    delimiter: Specifies a one-character string to use as the field separator.
            It defaults to ','.
    ignore_errors: A bool indicating whether to ignore errors.  If False, and
            an error occurrs a debug break will be issued.
    headers: A list containing the names of the headers in the case has_headers
            is False. The order of this list must match the order contained in
            the csv file. Note, this is a special case and is only valid when
            has_headers is False and select is None.
    max_entries: an integer indicating the maximum number of enteries can be
            returned. If this parameter is less than or equal to zero, all
            enteries are returned. Default is 0.
    stop_on_blank_lines: A bool indicating whether to stop when a blank row is
            detected.  Default is False.

    returns: If the file contains headers, or headers are specified, a list of
            dictionaries is returned, where the key is the header name as a
            string.  If the file contains no headers, a list of tuples is
            returned.
    '''
    if select and not has_headers:
        raise RuntimeError(
            "'select' parameter is only allowed when has_headers is True.")

    if select is not None and headers:
        raise RuntimeError(
            "'select' and 'headers' parameters cannot be combine."
            "  Please specify one or the other.")

    if headers and has_headers:
        raise RuntimeError(
            "'headers' parameter can only be specified when has_headers=False")

    try:
        with open(filename, 'r') as f:
            # Open a csv reader
            f_csv = csv.reader(f, delimiter=delimiter, dialect='excel')

            # Read the first line of the csv file, which should contain the headers, if headers are present.

            first_line = -1
            raw_headers = []
            if has_headers:
                for first_line, row in enumerate(f_csv):
                    if row:
                        raw_headers = row
                        break
            first_line += 1

            if not headers:
                headers = []

            # We cannot just read the headers, we need to first strip out junk characters
            for header in raw_headers:
                headers.append(extract_val(header))

            # PUT A COMMENT HERE
            indices = [headers.index(colname) for colname in select] if select else []
            columns = select if select else headers

            # if select:
                # indices = [headers.index(colname) for colname in select]
                # columns = select
            # else:
                # indices = []
                # columns = headers
            records = []

            # Enumerate the csv file, starting at the first line
            # following the headers
            for rowno, row in enumerate(f_csv, first_line):
                # If the row is blank, continue to the next row.
                # If stop_on_blank_lines, stop altogether.
                if not row and stop_on_blank_lines:
                    break
                elif not row:
                    continue

                # Filter row if specific columns are selected
                if indices:
                    row = [row[idx] for idx in indices]

                # Apply type conversion if types are specified
                if types:
                    try:
                        row = [func(extract_val(val)) for func, val in zip(types, row)]
                    except ValueError as e:
                        if not ignore_errors:
                            print("Row {}: Couldn't convert {}".format(rowno, row))
                            print("Row {}: Reason {}".format(rowno, e))
                            if __debug__:
                                import pdb; pdb.set_trace()
                        continue

                # Make a dictionary if the file contains headers,
                # otherwise create a tuple
                record = dict(zip(columns, row)) if columns else tuple(row)
                records.append(record)

                if max_entries > 0 and len(records) == max_entries:
                    break
    except Exception as ex:
        print('Failed to parse {}'.format(filename))
        raise
    return records
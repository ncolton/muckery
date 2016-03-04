#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path
import csv
import codecs
import pprint
import argparse

def build_parser():
    parser = argparse.ArgumentParser(description='')
    input_group = parser.add_argument_group(title='input options')
    output_group = parser.add_argument_group(title='output options')

    input_group.add_argument('-i', '--input-file', help='File to read from', required=True)
    input_group.add_argument('-ie', '--input-encoding', help='Input file encoding', default='UTF-16')
    input_group.add_argument('-is', '--input-separator', help='character used to separate values in input file', default='|')

    output_group.add_argument('-o', '--output-file', help='File to write to', required=True)
    output_group.add_argument('-oe', '--output-encoding', help='Output file encoding', default='UTF-8')
    output_group.add_argument('-os', '--output-separator', help='character used to separate values in output file', default=',')

    return parser

RESTKEY = 'extra_crap_column'

OUTPUT_SUMMARY = """lines:
    read      : {read}
    malformed : {bad}
    converted : {written}
"""

INPUT_INFO = """input
    file      : {filename} ({encoding})
    separator : {field_separator}
"""

OUTPUT_INFO = """output
    file      : {filename} ({encoding})
    separator : {field_separator}
"""

def normalize_filepath(filepath):
    """Expand variables and ~-paths to ensure the `filepath` will work with open."""
    return os.path.abspath(os.path.expandvars(os.path.expanduser(filepath)))

if __name__ == '__main__':
    parser = build_parser()
    args = parser.parse_args()

    READING_MSG = "Reading from {file} ({encoding}).\n\tExpecting '{separator}' as field separator."
    WRITING_MSG = "Writing to {file} ({encoding}).\n\tUsing '{separator}' as field separator."


    input_file = codecs.open(normalize_filepath(args.input_file), 'r', args.input_encoding)
    reader = csv.DictReader(input_file, delimiter=args.input_separator, restkey=RESTKEY)
    print '\n'
    print INPUT_INFO.format(
        filename=normalize_filepath(args.input_file),
        encoding=args.input_encoding,
        field_separator=args.input_separator
    )
    output_file = codecs.open(normalize_filepath(args.output_file), 'w', args.output_encoding)
    writer = csv.DictWriter(output_file, reader.fieldnames, dialect=csv.excel_tab, delimiter=args.output_separator)
    print OUTPUT_INFO.format(
        filename=normalize_filepath(args.output_file),
        encoding=args.output_encoding,
        field_separator=args.output_separator
    )

    lines_written = 0
    lines_read = 0
    lines_bad = 0
    try:
        writer.writeheader()
        lines_read = 1
        lines_written = 1

        for row in reader:
            lines_read += 1
            if RESTKEY in row:
                # skip rows with too many fields for the number of headers
                # basically, someone screwed up and didn't properly escape or quote
                # the data for the file, so we get to skip broken crap
                lines_bad += 1
                continue
            writer.writerow(row)
            lines_written += 1
    except Exception:
        raise  # re-raise; this is just here to make sure we properly close the files!
    finally:
        input_file.close()
        output_file.close()

    print OUTPUT_SUMMARY.format(read=lines_read, bad=lines_bad, written=lines_written)

#!/usr/bin/env python

import os
import argparse


def parse_arguments(args):
    """
    Parse Commandline Arguments
    :param args: *args positional arguments
    :return: Commandline arguments parsed by argparse
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--config",
        metavar="configuration_file",
        dest="configuration_file",
        help="File that contains the configuration.",
        required=True,
    )

    parser.add_argument(
        "--query-date",
        dest="query_date",
        help="Date to query in YYYYMMDD format",
        default=os.environ.get("QUERY_DATE", None),
    )

    return parser.parse_args(args)

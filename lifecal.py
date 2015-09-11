#!/usr/bin/env python

"""LifeCalendar

Usage:
  lifecal.py <date-of-birth>
  lifecal.py -h | --help
  lifecal.py --version

Options:
  -h --help          Show this screen.
  --version          Show version.
  -l <years>, --lifespan <years> Override default lifespan of 90 years

"""

from docopt import docopt
from helper import LifeCalendar
from datetime import datetime
from dateutil.relativedelta import relativedelta
from render import html
import os
import yaml

DATE_FORMAT = '%Y-%m-%d'


def main():
    opts = docopt(__doc__)
    cal = _init_calendar(opts)

    # Read config file for significant dates and date ranges
    _init_dates(cal)

    # Draw calendar
    _render_calendar(cal, opts)


def _init_calendar(opts):
    dob_arg = opts['<date-of-birth>']
    dob = datetime.strptime(dob_arg, DATE_FORMAT)

    if opts.has_key('--lifespan'):
        lifespan = opts['--lifespan']
        return LifeCalendar(dob, lifespan)

    return LifeCalendar(dob)


def _init_dates(cal):
    data = _open_data_file()

    for key, value in data['dates'].iteritems():
        if isinstance(value, basestring):
            value = _calculate_offset_date(cal.dob, eval(value))
        cal.add_significant_date(value, key)

    cal.add_significant_date(datetime.now(), "TODAY")

    for key, value in data['ranges'].iteritems():
        cal.add_range(value['start'], value['until'], key, "range{0}".format(cal.range_count()))


def _open_data_file():
    f = open("{0}/{1}".format(os.getcwd(), "dates.yaml"))
    data = yaml.safe_load(f)
    f.close()
    return data


def _calculate_offset_date(dob, value):
    year, month, day = value[0], value[1], value[2]
    offset_date = dob + relativedelta(years=year, months=month, days=day)
    print offset_date
    return offset_date


def _render_calendar(cal, opts):
    html(cal)

if __name__ == '__main__':
    main()
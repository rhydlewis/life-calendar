from isoweek import Week
from datetime import date


class LifeCalendar:
    def __init__(self, dob, lifespan=90):
        self.dob = dob
        self._years = dict()
        self._weeks = dict()
        self._ranges = []
        for i in range(dob.year, dob.year + lifespan):
            self._populate_year(i)

    def add_significant_date(self, sig_date, note):
        key = Week.withdate(sig_date)
        week = self._weeks[key]
        week.add_significant_date(note)
        print("Updated w/b {0} with {1}".format(key.monday(), note))

    def add_range(self, start, until, range_type, id_=""):
        date_range = {k: v for k, v in self._weeks.iteritems()
                      if k.monday() >= start and k.monday() < until}
        for week_info in date_range.values():
            week_info.add_range(range_type)
            week_info.add_id(id_)

        self._ranges.append(range_type)

    def populated_weeks(self):
        return {k: v for k, v in self._weeks.iteritems() if v.has_significant_date() or v.has_range()}

    def years(self):
        return sorted(self._years.values())

    def range_count(self):
        return len(self._ranges)

    def _populate_year(self, year):
        index = year - self.dob.year
        start_week = Week.withdate(date(year, self.dob.month, self.dob.day))
        end_week = Week.withdate(date(year + 1, self.dob.month, self.dob.day))
        next_week = start_week
        weeks = []

        while next_week.monday() < end_week.monday():
            week_info = WeekInfo(next_week)
            weeks.append(week_info)
            self._weeks[next_week] = week_info
            next_week += 1

        self._years[year] = dict(year=year, index=index, weeks=weeks)


class WeekInfo:
    def __init__(self, week):
        self.week = week
        self.number = week.week
        self.significant_dates = []
        self.range = ""
        self.id_ = ""

    def start_date(self):
        return self.week.monday()

    def has_significant_date(self):
        return len(self.significant_dates) > 0

    def has_range(self):
        return len(self.range) > 0

    def add_significant_date(self, info):
        self.significant_dates.append(info)

    def add_range(self, range_type):
        self.range = range_type

    def add_id(self, id_):
        self.id_ = id_

    def __repr__(self):
        dates = "".join(self.significant_dates)
        if not dates:
            dates = ""
        return "{0}".format(dates)

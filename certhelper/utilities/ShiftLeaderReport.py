from certhelper.utilities.utilities import get_from_summary, to_weekdayname


class ShiftLeaderReport:
    bad_keyword = "Bad"
    day_keyword = "day"
    num_runs_keyword = "number_of_runs"
    intlum_keyword = "int_lum"
    types = ["Collisions", "Cosmics"]
    recos = ["Prompt", "Express"]
    attributes = [num_runs_keyword, intlum_keyword]

    def __init__(self, runs):
        self.summary = runs.summary()
        self.bad_summary = runs.bad().summary()
        self.summary_per_day = runs.summary_per_day()
        self.bad_summary_per_day = runs.bad().summary_per_day()

    def get_item(self, runtype, reco, bad_only=False, day=None):
        if day:  # for single day
            summary = self.summary_per_day if not bad_only else self.bad_summary_per_day
            item = get_from_summary(summary, runtype, reco, day)
        else:  # for whole week/ all runs
            summary = self.summary if not bad_only else self.bad_summary
            item = get_from_summary(summary, runtype, reco)

        assert len(item) <= 1
        return item[0] if len(item) == 1 else {}

    def number_of_runs(self, runtype, reco, bad_only=False, day=None):
        return self.get_attribute("runs_certified", runtype, reco, bad_only, day)

    def sum_int_lum(self, runtype, reco, bad_only=False, day=None):
        return self.get_attribute("int_luminosity", runtype, reco, bad_only, day)

    def get_attribute(self, attribute, runtype, reco, bad_only=False, day=None, default_value=0):
        return self.get_item(runtype, reco, bad_only, day).get(attribute, default_value)

    def get_active_days_list(self):
        days_list = []
        for item in self.summary_per_day:
            day = item["date"].strftime('%Y-%m-%d')
            if day not in days_list:
                days_list.append(day)
        return days_list

    def get_context(self):
        context = self.fill_context()
        context[self.day_keyword] = {}

        active_days = self.get_active_days_list()
        for idx, day in enumerate(active_days):
            context[self.day_keyword][idx] = self.fill_context(day)
            context[self.day_keyword][idx]["name"] = to_weekdayname(day)
            context[self.day_keyword][idx]["date"] = day

        return context

    def build_context_structure(self):
        bad = self.bad_keyword
        context = {bad: {}}

        for type in self.types:
            context[type] = {}
            context[bad][type] = {}
            for reco in self.recos:
                context[type][reco] = {}
                context[bad][type][reco] = {}
                for attr in self.attributes:
                    context[type][reco][attr] = 0
                    context[bad][type][reco][attr] = 0

        return context

    def fill_context(self, day=None):
        bad = self.bad_keyword
        context = self.build_context_structure()

        for runtype in self.types:
            for reco in self.recos:
                context[runtype][reco] = {
                    self.num_runs_keyword: self.number_of_runs(runtype, reco, day=day),
                    self.intlum_keyword: self.sum_int_lum(runtype, reco, day=day)
                }
                context[bad][runtype][reco] = {
                    self.num_runs_keyword: self.number_of_runs(runtype, reco, bad_only=True, day=day),
                    self.intlum_keyword: self.sum_int_lum(runtype, reco, bad_only=True, day=day)
                }

        return context

from calendar import HTMLCalendar


class TrainingCalendar(HTMLCalendar):
    """Create a monthly training calendar in HTML"""
    month_css = ''
    training_css = ''

    def __init__(self, training_plan, month, year):
        super(TrainingCalendar, self).__init__()
        self.month = month
        self.year = year
        self.training_plan = training_plan
        self.trainings = self.get_trainings()

    def formatday(self, day, weekday):
        """Return a formatted day as a table cell."""
        if day == 0:  # table cells for days outside the month
            return f'<td class="{self.cssclass_noday}">&nbsp;</td>'

        if day in self.trainings:  # training days
            css_class = ''
            link = ''
            return f'<td class="{css_class}"><a href="{link}">{day}<br>' \
                   f'<div class="{self.training_css}">{self.trainings[day]}' \
                   f'</div></a></td>'

        else:  # non-training days
            css_class = ''
            link = ''
            return f'<td class="{css_class}"><a href="{link}">{day}</a></td>'

    def formatmonth(self, year, month, withyear=True):
        """Return a formatted month as a table."""
        result = []
        a = result.append
        a(f'<table border="0" cellpadding="0" cellspacing="0"'
          f' class="{self.month_css}">')
        a('\n')
        a(self.formatmonthname(year, month, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(year, month):
            a(self.formatweek(week))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(result)

    def get_trainings(self):
        """Create a dictionary mapping day with training."""
        trainings = self.training_plan.training_set.filter(
            date__year=self.year, date__month=self.month).order_by('date')
        return {t.date.day: t for t in trainings}

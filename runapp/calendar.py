from calendar import HTMLCalendar
from datetime import datetime

from django.shortcuts import reverse
from django.utils.http import urlencode


class TrainingCalendar(HTMLCalendar):
    """Create a monthly training calendar in HTML"""
    table_css = ''
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
            training = self.trainings[day]
            css_class = self.get_css_class(day, weekday, True)
            link = self.create_edit_training_url(training.pk)
            return f'<td class="{css_class}"><a href="{link}">{day}<br>' \
                   f'<div class="{self.training_css}">{training}' \
                   f'</div></a></td>'

        else:  # non-training days
            css_class = self.get_css_class(day, weekday, False)
            link = self.create_add_training_url(day)
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

    def create_date(self, day):
        """Return full date as datetime object."""
        return datetime(year=self.year, month=self.month, day=day)

    def create_add_training_url(self, day):
        """Create a link to add a new training on a specific day."""
        date = self.create_date(day)
        url = reverse('runapp:training_create', args=[self.training_plan.pk])
        return f'{url}?{urlencode({"date": date})}'

    @staticmethod
    def create_edit_training_url(training_pk):
        """Create a link to edit a scheduled training."""
        return reverse('runapp:training_edit', args=[training_pk])

    def get_css_class(self, day, weekday, is_training_day):
        """Create a string with css classes for a table cell."""
        date = self.create_date(day)
        css_classes = [self.cssclasses[weekday]]
        if date == self.get_date_today():
            css_classes.append('today')
        elif date == self.training_plan.start_date:
            css_classes.append('plan_start')
        elif date == self.training_plan.end_date:
            css_classes.append('plan_end')
        elif is_training_day:
            css_classes.append('training_day')
        return ' '.join(css_classes)

    @staticmethod
    def get_date_today():
        """Return today's date."""
        return datetime.today().date()

    def get_trainings(self):
        """Create a dictionary mapping day with training."""
        trainings = self.training_plan.training_set.filter(
            date__year=self.year, date__month=self.month).order_by('date')
        return {t.date.day: t for t in trainings}

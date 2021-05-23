from django.forms.widgets import DateInput


class DatePicker(DateInput):
    """Widget for choosing date from a popup calendar."""
    input_type = 'date'

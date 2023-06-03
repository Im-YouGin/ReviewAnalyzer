import django_filters

EMPTY_STRING = ""


class CustomMultipleChoiceFilter(django_filters.MultipleChoiceFilter):
    def filter(self, qs, value):
        return super().filter(qs, value)

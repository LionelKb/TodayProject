from .models import Occurrence, EventType
from django.shortcuts import render, redirect

from django.conf import settings
from core.utils import get_current_topic
from . import utils
from datetime import datetime, date, time

from .forms import IndexForm
import calendar
from . import swingtime_settings
from django.views.generic import DetailView
from django.core.urlresolvers import reverse

if swingtime_settings.CALENDAR_FIRST_WEEKDAY is not None:
    calendar.setfirstweekday(swingtime_settings.CALENDAR_FIRST_WEEKDAY)


def index(request, template='topic/research.html'):
    """
    :param request:
    :param template:
    :return: home template with index form
    """

    context = dict()
    topic = get_current_topic(request)

    if request.method == 'POST':
        form = IndexForm(topic, request.POST)

        if form.is_valid():
            # don't use city from now
            event_type_list = form.cleaned_data['quoi']
            print event_type_list is False
            event_type_id_string = '&'.join([str(event_type.id) for event_type in event_type_list])
            query_date = form.cleaned_data['quand']

            if event_type_list:
                return redirect(reverse('topic:single_day_event_type_list',
                                        kwargs={'year': query_date.year,
                                                'month': query_date.month,
                                                'day': query_date.day,
                                                'event_type_id_string': event_type_id_string
                                                },
                                        current_app=topic.name),
                                )

            else:
                return redirect(reverse('topic:daily_events',
                                        current_app=topic.name,
                                        kwargs={'year': query_date.year,
                                                'month': query_date.month,
                                                'day': query_date.day,
                                                }
                                        ))

    else:
        form = IndexForm(topic)

    context['form'] = form

    return render(request, template, context)


class OccurrenceDetail(DetailView):
    model = Occurrence
    template_name = "topic/single_event.html"

    def get_context_data(self, **kwargs):
        context = super(OccurrenceDetail, self).get_context_data(**kwargs)
        # TODO improve this using location.address
        if self.object.event.address != "non precise":
            address = self.object.event.address + ", France"
        else:
            address = False
        context['address'] = address

        return context


# mother function
def _get_events(request, template, event_type_list, start_time, end_time):

    site = settings.SITE_ID
    topic = get_current_topic(request)

    occurrences = Occurrence.objects.filter(event__event_type__topic=topic,
                                           event__site=site,
                                           event__event_type__in=event_type_list,
                                           start_time__gte=start_time,
                                           end_time__lte=end_time)

    context = dict({'occurrences': occurrences,
                   'event_types_list': event_type_list,
                    'days': utils.list_days(start_time, end_time),
                    })

    return render(request, template, context)


# functions for a date queries
def _event_by_date(request, event_type_list, start_time, end_time):
    template = 'topic/event_by_date.html'

    return _get_events(request, template, event_type_list, start_time, end_time)


def _all_events(request, start_time, end_time):
    event_type_list = EventType.objects.filter(topic=get_current_topic(request))
    return _event_by_date(request, event_type_list, start_time, end_time)


def today_events(request):
    return _all_events(request, start_time=datetime.now(), end_time=datetime.combine(date.today(), time.max))


def tomorrow_events(request):
    return _all_events(request, start_time=utils.tomorrow_morning(), end_time=utils.tomorrow_evening())


def coming_days_events(request):
    return _all_events(request, start_time=datetime.now(), end_time=utils.end_of_next_days(duration=3))


# functions for event_type queries
def _event_by_event_type(request, event_type_list, start_time, end_time):
    template = 'topic/date_by_event_type.html'

    return _get_events(request, template, event_type_list, start_time, end_time)


def single_day_event_type_list(request, event_type_id_string, year, month, day):
    event_type_list = utils.get_event_type_list(event_type_id_string, current_topic=get_current_topic(request))
    date_day = utils.construct_day(year, month, day)
    start_time = utils.construct_time(date_day, time.min)
    end_time = utils.construct_time(date_day, time.max)

    return _event_by_event_type(request, event_type_list, start_time, end_time)


def single_time_event_type_list(request, event_type_id_string, year, month, day, start_hour, end_hour):
    event_type_list = utils.get_event_type_list(event_type_id_string, current_topic=get_current_topic(request))
    date_day = utils.construct_day(year, month, day)
    start_time = utils.construct_time(date_day, utils.construct_hour(start_hour))
    end_time = utils.construct_time(date_day, utils.construct_hour(end_hour))

    return _event_by_event_type(request, event_type_list, start_time, end_time)


def event_type_coming_days(request, event_type_id_string):
    event_type_list = utils.get_event_type_list(event_type_id_string, current_topic=get_current_topic(request))
    start_time = datetime.now()
    end_time = utils.end_of_next_days(duration=3)

    return _event_by_event_type(request, event_type_list, start_time, end_time)


def daily_events(request, year, month, day):
    event_type_list = EventType.objects.filter(topic=get_current_topic(request))
    date_day = utils.construct_day(year, month, day)
    start_time = utils.construct_time(date_day, time.min)
    end_time = utils.construct_time(date_day, time.max)

    return _event_by_event_type(request, event_type_list, start_time, end_time)
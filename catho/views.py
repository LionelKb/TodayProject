import calendar
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404, get_list_or_404, render, redirect
from .forms import IndexForm
from .models import EventType, Occurrence, Event, EnjoyTodayUser
from core.models import Topic
from django.views.generic import DetailView, DayArchiveView, ListView
# from django.views.generic.list import MultipleObjectMixin
# from django.views.generic.detail import SingleObjectMixin
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.template import RequestContext
from . import swingtime_settings
from .apps import EVENT_TYPE_LIST


if swingtime_settings.CALENDAR_FIRST_WEEKDAY is not None:
    calendar.setfirstweekday(swingtime_settings.CALENDAR_FIRST_WEEKDAY)


def index(request, template='catho/research.html', **kwargs):
    """
    :param request:
    :param template:
    :return: home template with index form
    """

    if request.method == 'POST':
        form = IndexForm(request.POST)

        if form.is_valid():
            # dont use city from now
            event_type = form.cleaned_data['quoi']
            date = form.cleaned_data['quand']

            if event_type is not None:
                return redirect('catho:single_day_event_type',
                                event_type_id=event_type.pk,
                                year=date.year,
                                month=date.month,
                                day=date.day)
            else:
                return redirect('catho:daily_events',
                                year=date.year,
                                month=date.month,
                                day=date.day)
    else:
        form = IndexForm()

    context = {'form': form, }
    context['topic_sidebar'] = EVENT_TYPE_LIST

    return render(request, template, context)


class OccurrenceDetail(DetailView):
    model = Occurrence
    template_name = "catho/single_event.html"

    def get_context_data(self, **kwargs):
        context = super(OccurrenceDetail, self).get_context_data(**kwargs)
        #TODO improve this using location.address
        if self.object.event.address != "non precise":
            address = self.object.event.address + ", France"
        else:
            address = False
        context['address'] = address
        context['topic_sidebar'] = EVENT_TYPE_LIST

        return context


def get_occurrence(request, occurrence_id):
    occurrence = get_object_or_404(Occurrence, pk=occurrence_id)
    if occurrence.event.address != "non precise":
        address = occurrence.event.address + ", France"
    else:
        address = False

    context = dict({'occurrence': occurrence,
                    'address': address,
                    }
                   )

  #  context['topic_sidebar'] = EVENT_TYPE_LIST

    return render(request, 'catho/single_event.html', context)


#class OccurrenceDayArchiveView(DayArchiveView, dt='dt'):
 #   """
 #   All occurrences from every event_types in one day
  #  """
   # queryset = Occurrence.objects.daily_occurrences(dt='dt')
    # the research is based on occurrence end_time of the current day
#    date_field = "end_time"
#    allow_future = True
#    allow_empty = True
#    template_name = 'catho/event_by_date.html'
#    context_object_name = 'occurrences'

#    def get_context_data(self, **kwargs):
#        context = super(OccurrenceDayArchiveView, self).get_context_data(**kwargs)

#        events_list = [occurrence.event for occurrence in self.object_list]
#        event_types_list = list(set([event.event_type for event in events_list]))

 #       context['event_types_list'] = event_types_list
        # inutile normalement
  #      context['days'] = self.get_day()
   #     return context


def _events_in_a_period(request,
                        days,
                        template='catho/event_by_date.html',
                       ):
    """

    :param request:
    :param days: a list of days
    :return: context with occurrences, event_types_list and days
    """
    # not satisfying because len(moment) times database requests

    # print event_types occurrences
    # TODO: verify the following point: if no event at all in coming days => crash?!
    occurrences = []
    for day in days:
        occurrences_day = Occurrence.objects.daily_occurrences(dt=day)#.filter(is_multiple=False)
        for occurrence_day in occurrences_day:
            occurrences.append(occurrence_day)

    # get all related event_types  (double sorted)
    events_list = [occurrence.event for occurrence in occurrences]
    event_types_list = list(set([event.event_type for event in events_list]))

    context = dict({'occurrences': occurrences,
                   'event_types_list': event_types_list,
                    'days': days,

                    })
    context['topic_sidebar'] = EVENT_TYPE_LIST

    return render(request, template, context)


def today_events(request,
                 template='catho/event_by_date.html',
                 ):
    """

    :param request:
    :param template:
    :return: all events for topic
    """
    days = [datetime.today()]

    return _events_in_a_period(request, days, template)


def tomorrow_events(request,
                    template='catho/event_by_date.html',
                    ):
    """

    :param request:
    :param template:
    :return: all events for tomorrow
    """
    days = [datetime.today() + timedelta(days=+1)]

    return _events_in_a_period(request, days, template)


def coming_days_events(request,
                       next_days_duration=3,
                       template='catho/event_by_date.html',
                       ):
    """

    :param request:
    :param next_days_duration: how many days does "coming_days" mean
    :param template:
    :return: all events for coming_days
    """
    today = datetime.now()
    i = 0
    days = []
    while i < int(next_days_duration):
        days.append(today + timedelta(days=+i))
        i += 1


    return _events_in_a_period(request, days, template)


def daily_events(request,
                 year,
                 month,
                 day,
                 template='catho/event_by_date.html',
                 ):

    days = [datetime(int(year), int(month), int(day))]

    return _events_in_a_period(request, days, template)


def monthly_events(request,
                   year,
                   month,
                   template='catho/event_by_date.html',
                  ):

    year, month = int(year), int(month)
    cal = calendar.Calendar()
    weeks = cal.monthdatescalendar(year, month)
    days = []
    for week in weeks:
        for day in week:
            days.append(day)


    return _events_in_a_period(request, days, template)


def event_type_coming_days(request,
                           event_type_id,
                           next_days_duration=3,
                           template='catho/date_by_event_type.html',
                           ):
    """

    :param request:
    :param event_type_id:
    :param next_days_duration:
    :param template:
    :return: every occurrences of a single event_type within next_day_duration days
    """

    # list of next_day_duration days
    today = datetime.now()
    i = 0
    days = []
    while i < int(next_days_duration):
        days.append(today + timedelta(days=+i))
        i += 1

    # sort event_type.occurrences by day
    event_type = get_object_or_404(EventType, pk=int(event_type_id))
    occurrences = []
    for day in days:
        occurrences_day = Occurrence.objects.daily_occurrences(dt=day).filter(event__event_type=event_type)
        for occurrence_day in occurrences_day:
            occurrences.append(occurrence_day)

    context = dict({'occurrences': occurrences,
                    'event_type': event_type,

                    }
                   )
    context['topic_sidebar'] = EVENT_TYPE_LIST

    return render(request, template, context)


def _single_day_event_type(
        request,
        event_type_id,
        dt,
        template='catho/event_by_date.html',

        ):

    event_type = get_object_or_404(EventType, pk=int(event_type_id))
    occurrences = Occurrence.objects.daily_occurrences(dt=dt).filter(event__event_type=event_type)

    context = dict({'occurrences': occurrences,
                    'event_types_list': [event_type],
                    'days': [dt],

                    }
                   )
    context['topic_sidebar'] = EVENT_TYPE_LIST

    return render(request, template, context)


def today_event_type(
        request,
        event_type_id,
        template='catho/event_by_date.html',

        ):

    dt = datetime.today()
    return _single_day_event_type(request, event_type_id, dt, template,)


def tomorrow_event_type(
        request,
        event_type_id,
        template='catho/event_by_date.html',

        ):

    dt = datetime.today()+timedelta(days=+1)
    return _single_day_event_type(request, event_type_id, dt, template, )


def single_day_event_type(
        request,
        event_type_id,
        year,
        month,
        day,
        template='catho/event_by_date.html',

        ):

    dt = datetime(int(year), int(month), int(day))
    event_type = get_object_or_404(EventType, pk=int(event_type_id))
    occurrences = Occurrence.objects.daily_occurrences(dt=dt).filter(event__event_type=event_type)

    context = dict({'occurrences': occurrences,
                    'event_types_list': [event_type],
                    'days': [dt],

                    }
                   )
    context['topic_sidebar'] = EVENT_TYPE_LIST

    return render(request, template, context)


@login_required(login_url='connection:login')
def new_event(request):
    context = dict()
    context['topic_sidebar'] = EVENT_TYPE_LIST
    return render(request, 'catho/add_event_choice.html', context)

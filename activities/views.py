from collections import defaultdict
from django.views.generic import ListView
from django.shortcuts import redirect
from activities.models import Activity
from activities.forms import ActivityForm

class ActivityListView(ListView):
    model = Activity
    template_name = 'home.html'
    context_object_name = 'activities'
    ordering = ['-date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ActivityForm()

        # Get the latest 7 dates from the Activity model
        latest_dates = Activity.objects.values('date').order_by('-date').distinct()[:7]
        latest_dates = [entry['date'] for entry in latest_dates]

        # Filter activities to only include those with the latest 7 dates
        activities = Activity.objects.filter(date__in=latest_dates).order_by('-date', '-id')

        # Group activities by date and calculate total duration for each date
        grouped_activities = defaultdict(list)
        total_duration_per_day = defaultdict(int)

        for activity in activities:
            grouped_activities[activity.date].append(activity)
            if not activity.is_rest:  # Only count non-rest activities
                total_duration_per_day[activity.date] += activity.duration

        # Create a list of dictionaries with date, activities, and total duration
        date_activity_data = [
            {'date': date, 'activities': grouped_activities[date], 'total_duration': total_duration_per_day[date]}
            for date in grouped_activities
        ]

        # Pass the date-activity data to the context
        context['date_activity_data'] = date_activity_data
        return context

    def post(self, request, *args, **kwargs):
        form = ActivityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)

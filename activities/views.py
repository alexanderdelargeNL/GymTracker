from collections import defaultdict
from django.views.generic import ListView
from django.shortcuts import redirect
from django.utils import timezone
from activities.models import Activity
from activities.forms import ActivityForm
from datetime import timedelta

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
    
        # Group activities by date
        grouped_activities = defaultdict(list)
        for activity in activities:
            grouped_activities[activity.date].append(activity)

        # Pass the grouped activities to the context
        context['grouped_activities'] = dict(grouped_activities)  # Convert defaultdict to dict

        return context    

    def post(self, request, *args, **kwargs):
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)  # Don't save to the database yet
            if form.cleaned_data.get('rustperiode'):  # Check if the checkbox is checked
                # Implement the loop to insert new Activity records
                current_date = timezone.now().date() - timedelta(days=1)
                while True:
                    # Get the highest date from Activity.date
                    highest_date = Activity.objects.order_by('-date').first().date
                    if current_date == highest_date:
                        break  # Exit the loop if the current date is the highest date
                    else:
                        # Calculate Y as the highest date + 1 day
                        Y = highest_date + timezone.timedelta(days=1)
                        # Insert a new Activity record with Activity.date set to Y
                        Activity.objects.create(
                            date=Y,
                            duration=0,  # Assuming duration is 0 for rustperiode
                            is_rest=True,  # Assuming this should be a rest day
                            notes="Automatisch toegevoegde rustdagen"
                        )

            else:
                activity.save()  # Save the activity to the database

            return redirect('home')
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)

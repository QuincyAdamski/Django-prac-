import calendar
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout #idk if this should be signup
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import SignUpForm, EventForm
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Feature, Course, Event
from .forms import CourseForm, EventForm
from datetime import date, datetime, timedelta
from django.views import generic
from django.utils.safestring import mark_safe
from .models import *
from .utils import Calendar
from django.utils.timezone import now

# Create your views here.
def index(request):
    features = Feature.objects.all()
    return render(request, 'index.html', {'features': features})

def index2(request):
    return render(request, 'index2.html')#idk

def signup(request):#Sign up page
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Already in Use')
                return redirect('signup')#sends them back to the begining of the signup process
            elif User.objects.filter(username=username).exists():#send them back to the begining of the signup process
                #if the username is already being used but I don't think we have user names (i guess regular names is the same thing)
                messages.info(request, 'Username Already in Use')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)#this might differ
                #depending on our database
                user.save()
                return redirect('login')
        else:
            messages.info(request, 'Passwords do not Match')
            return redirect('signup')
    else:
        return render(request, 'signup.html')#so this will need to be typescript

def loginView(request):#login page
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials invalid')
            return redirect ('login')
    else:
        return render(request, 'login.html')


def logoutView(request):#not hooked up to anything since I don't think we've speciefed needing one.
    #Still, this should be the logic
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('index')

@login_required(login_url='/login/')
def courses(request):#displays the available courses- Functions are Enroll, Filter(i'd like to remove this), and Search
    query = request.GET.get('q', '')  # Get the search query
    if query:
        courses_list = Course.objects.filter(title__icontains=query)
    else:
        courses_list = Course.objects.all()
    
    return render(request, 'courses.html', {'courses': courses_list, 'query': query})


@login_required(login_url='/login/')
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if request.user in course.enrolled_users.all():
        messages.info(request, "You are already enrolled in this course.")
    else:
        course.enrolled_users.add(request.user)  # Add user to enrolled_users
        course.students_enrolled += 1
        course.save()
        messages.success(request, f"Successfully enrolled in {course.title}!")

    return redirect('courses')

@login_required(login_url='/login/')
def events(request):#displays events- Allows admins to create events (students can make meetings? I maybe missremembering)
    #and allows Registration for events
        events = Event.objects.filter(start_time__gte=now()).order_by('start_time')
        return render(request, "events.html", {"events": events})


@login_required(login_url='/login/')
def register_event(request, event_id):
    events = get_object_or_404(Event, id=event_id)
    if request.user in events.registered_users.all():
        messages.info(request, "You are already enrolled in this course.")
    else:
        events.registered_users.add(request.user)  # Add user to enrolled_users
        #events.students_enrolled += 1 i dont think we need to track this
        events.save()
        messages.success(request, f"Successfully registered for {events.title}!")

    return redirect('events')


@login_required(login_url='/login/')
def create_event(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            return redirect("event_list")
    else:
        form = EventForm()
    return render(request, "events/create_event.html", {"form": form})

@login_required(login_url='/login/')
def settings_page(request):#The admin dashboard- Allows Users, Courses, and Events to be added(removed as well?)

    if not request.user.is_staff:#can't I just use this for login?
        messages.error(request, "You do not have permission for this page, sorry.")
        return redirect('login')#sends them back to the landing page
    
    users = User.objects.all()
    courses = Course.objects.all()
    events = Event.objects.all()
    course_form = CourseForm()
    event_form = EventForm()

    if request.method == 'POST' and 'add_course' in request.POST:
        course_form = CourseForm(request.POST)
        if course_form.is_valid():
            course_form.save()
            messages.success(request, f'Course added successfully.')
            return redirect('settings')
        
    if request.method == 'POST' and 'add_event' in request.POST:
        event_form = EventForm(request.POST)
        if event_form.is_valid():
            event_form.save()
            messages.success(request, f'Event added successfully.')
            return redirect('settings')

    return render(request, 'settings.html', {
        'users' : users,
        'courses' : courses,
        'course_form' : course_form,
        'events' : events,
        'event_form' : event_form
    })


@login_required(login_url='/login/')
def delete_user(request, user_id):
    if not request.user.is_staff:
        messages.error(request, "Unauthorized access.")
        return redirect('settings')

    user_to_delete = get_object_or_404(User, id=user_id)

    if user_to_delete.is_superuser:
        messages.warning(request, "You can't delete a superuser!")

    if user_to_delete == request.user:
        messages.warning(request, "You can't delete yourself.")
    else:
        user_to_delete.delete()
        messages.success(request, "User deleted sucessfully.")
    
    return redirect('settings')

@login_required(login_url='/login/')
def delete_course(request, course_id):
    if not request.user.is_staff:
        messages.error(request, "Unauthorized.")
        return redirect('settings')
    
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    messages.success(request, "Course deleted.")
    
    return redirect('settings')

@login_required(login_url='/login/')
def delete_event(request, event_id):
    if not request.user.is_staff:
        messages.error(request, "Unauthorized.")
        return redirect('settings')
    
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    messages.success(request, "Event deleted.")

    return redirect('settings')


class CalendarView(generic.ListView):
    model = Event
    template_name = 'cal/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        
        # use today's date for the calendar
        d = get_date(self.request.GET.get('month', None))

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context
    
def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()



from django.shortcuts import redirect, render
from app.models import Categories,Course,Level,Video, UserCourse
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Sum

def BASE(request):
    return render(request, 'base.html')


def HOME(request):
    category=Categories.objects.all().order_by('id')[0:5]
    course = Course.objects.filter(status='PUBLISH').order_by('-id')
    context={
        'category': category,
        'course': course,

    }
    return render(request, 'main/home.html', context)


def SINGLE_COURSE(request):
    category=Categories.get_all_category(Categories)
    level=Level.objects.all()
    course=Course.objects.all()
    freeCourse_count=Course.objects.filter(price = 0).count()
    paidCourse_count=Course.objects.filter(price__gte=1).count()
    context={
        'category':category,
        'level':level,
        'course': course,
        'freeCourse_count':freeCourse_count,
        'paidCourse_count':paidCourse_count,

    }
    return render(request, 'main/single_course.html',context)

def filter_data(request):
    categories = request.GET.getlist('category[]')
    level = request.GET.getlist('level[]')
    price = request.GET.getlist('price[]')
    print(price)

    if price == ['pricefree']:
        course = Course.objects.filter(price=0)
    elif price == ['pricepaid']:
        course = Course.objects.filter(price__gte=1)
    elif price == ['priceall']:
        course = Course.objects.all()
    elif categories:
        course = Course.objects.filter(category__id__in=categories).order_by('-id')
    elif level:
        course = Course.objects.filter(level__id__in=level).order_by('-id')
    else:
        course = Course.objects.all().order_by('-id')

    t = render_to_string('ajax/course.html', {'course': course})

    return JsonResponse({'data': t})


def CONTACT(request):
    category=Categories.get_all_category(Categories)
    context={
        'category':category,
    }
    return render(request, 'main/contact_us.html',context)

def ABOUT(request):
    category = Categories.get_all_category(Categories)
    context = {
        'category': category,
    }
    return render(request, 'main/about_us.html',context)


def SEARCH_COURSE(request):
    query = request.GET['query']
    course = Course.objects.filter(title__icontains = query)
    category = Categories.get_all_category(Categories)
    context = {
        'course':course,
        'category':category,
    }
    return render(request,'search/search.html',context)


def COURSE_DETAILS(request,slug):
    course=Course.objects.filter(slug=slug)
    course_id=Course.objects.get(slug=slug)
    try:
        check_enroll = UserCourse.objects.get(user=request.user, course=course_id)
    except UserCourse.DoesNotExist:
        check_enroll = None

    time_duration = Video.objects.filter(course__slug = slug).aggregate(sum=Sum('time_duration'))
    category = Categories.get_all_category(Categories)
    if course.exists():
        course=course.first()
    else:
        return redirect('404')

    context={
        'course':course,
        'category':category,
        'time_duration':time_duration,
        'check_enroll':check_enroll,
    }
    return render(request, 'course/course_details.html',context)


def PAGE_NOT_FOUND(request):
    category = Categories.get_all_category(Categories)
    context = {
        'category': category,
    }
    return render(request,'error/404.html',context)

def CHECKOUT(request,slug):
    course = Course.objects.get( slug = slug)
    if course.price == 0:
        course = UserCourse(
            course= course,
            user=request.user,
        )
        course.save()
        messages.success(request, 'Successfully Enrolled. Happy Learning!')
        return redirect('my_course')
    return render(request, 'checkout/checkout.html')


def MY_COURSE(request):
    course=UserCourse.objects.filter(user=request.user)
    category = Categories.get_all_category(Categories)
    context = {
        'course': course,
        'category': category,
    }
    return render(request,'course/my_course.html', context)
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from .forms import RegistrationForm, UserChangingForm
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from sslcommerz_lib import SSLCOMMERZ

from django.views.generic import ListView, DetailView, CreateView
from .models import Course, CourseVideos, CourseRequirements, CourseLearns, UserCourse, Shipment



class CourseList(ListView):
    model = Course
    template_name = "courses/courses.html"
    
    def get_queryset(self):
        if self.request.GET:
            query = self.request.GET.get('search')
            print(query)
            if query:
                object_list = self.model.objects.filter(name__icontains=query)
            else:
                object_list = self.model.objects.none()
        else:
            object_list = self.model.objects.all()
        
        return object_list
    
        
class CourseDetail(DetailView):
    queryset = Course.objects.all()
    template_name = "courses/course_details.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = context['object'].id
        context['videos'] = CourseVideos.objects.filter(course=id)
        context['requirements'] = CourseRequirements.objects.filter(course=id)
        context['learns'] = CourseLearns.objects.filter(course=id)
        
        return context

@login_required()
def profile(request):
    if request.POST:
        form = UserChangingForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    return render(request, 'user/profile.html', {'form':UserChangingForm})

    
def register(request):
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
     
    return render(request, 'user/register.html', {'form':RegistrationForm})


def login(request):
    if request.POST:
        email = request.POST['email']
        password = request.POST['password']
        account = authenticate(email=email, password=password)
        auth_login(request, account)
        
        return redirect('home')
    
    return render(request, 'user/login.html')


def signout(request):
    logout(request)
    return redirect('login')



def home(request):
    return render(request, 'courses/courses.html')


# def course_details(request):
#     return render(request, 'courses/course_details.html')


@login_required()
def my_courses(request):
    myCourse = UserCourse.objects.filter(user=request.user)
    return render(request, 'courses/my_courses.html', {'myCourse':myCourse})


@login_required()
def checkout(request, pk):
    course = Course.objects.get(id=pk)
    
    if request.POST:
            course_name = request.POST['courseName']
            user_name = request.POST['name']
            email = request.POST['email']
            address = request.POST['address']
            telephone_number = request.POST['mobile']
            total_amount = int(request.POST['amount'])
            
            order = Shipment.objects.create(
                course_name = course_name,
                user_name = user_name,
                email = email,
                address = address,
                telephone_number = telephone_number,
                course_price = total_amount,
            )
            
            user_course = UserCourse.objects.create(
                user = request.user,
                course = course
            )
            
            success_url = "http://127.0.0.1:8000/payment-done/"+str(order.id)+"/"
            
        
            sslcz = SSLCOMMERZ({'store_id': 'ecomm642ab791870c9',
                            'store_pass': 'ecomm642ab791870c9@ssl', 'issandbox': True})

            post_body = {}
            post_body['total_amount'] = total_amount
            post_body['currency'] = "BDT"
            post_body['tran_id'] = "12345"
            post_body['success_url'] = success_url
            post_body['fail_url'] = "your fail url"
            post_body['cancel_url'] = "http://127.0.0.1:8000/payment-cancelled/"
            post_body['emi_option'] = 0
            post_body['cus_name'] = request.user.name
            post_body['cus_email'] = request.POST['email']
            post_body['cus_phone'] = request.POST['mobile']
            post_body['cus_add1'] = request.POST['address']
            post_body['cus_city'] = "Dhaka"
            post_body['cus_country'] = "Bangladesh"
            post_body['shipping_method'] = "NO"
            post_body['multi_card_name'] = ""
            post_body['num_of_item'] = 1
            post_body['product_name'] = "Test"
            post_body['product_category'] = "Test Category"
            post_body['product_profile'] = "general"

            response = sslcz.createSession(post_body)
            print('after')
            return redirect(response['GatewayPageURL'])
    
    return render(request, 'checkout.html', {'course':course})



@csrf_exempt
def payment_done(request, pk):
    
    order = Shipment.objects.get(id=pk)
    order.paid_status = 'paid'
    order.invoice = 'INV'+str(order.id)
    
    order.save()
    
    return HttpResponse('Payment done')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment-fail.html')


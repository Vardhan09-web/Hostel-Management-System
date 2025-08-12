from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout,get_user_model

from Hostelmanagementproject1 import settings
from .forms import LoginForm
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password,check_password
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import user_passes_test
from .models import Hosteller_reg, AdmissionRequest, Hstlin_reg, Attendance,RoomRequest
from django.utils import timezone
from datetime import datetime



User = get_user_model()

# Create your views here.
#home page logic
def home_view(request):
    return render(request, 'Home_page.html')


# def hosteller_type(request):
#     return render(request,'select_hostel_type.html')

#admin login page logic
def login_view(request):
    success_message1 = ''
    error_message1 = ''
    error_message2 = ''
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                success_message1 = 'Congratulations on successful login'
                return redirect('admin_dashboard')
            else:
                error_message1 = 'Invalid username or password'
                return render(request, 'login.html', {'form': form, 'error_message': error_message1})
        else:
            error_message2 = 'Form is not valid'
            return render(request, 'login.html', {'form': form, 'error_message': error_message2})
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form, 'success_message': success_message1, 'error_message': error_message1})

#admin dashboard viewfrom django.shortcuts import render
from .models import Hstlin_reg, Hosteller_reg # Make sure these models are imported

def admin_dashboard(request):
    total_incharges = Hstlin_reg.objects.count()
    total_hostellers = Hosteller_reg.objects.count()
    pending_incharges = Hstlin_reg.objects.filter(status='pending').count()  # Example filter
    pending_admissions = Hosteller_reg.objects.filter(status='pending').count()  # Example filter
    latest_notice = Notice.objects.filter(is_active=True).order_by('-created_at').first()
    
    context = {
        'total_incharges': total_incharges,
        'total_hostellers': total_hostellers,
        'pending_incharges': pending_incharges,
        'pending_admissions': pending_admissions,
        'latest_notice':latest_notice
    }
    return render(request, 'admin_dashboard.html', context)


def hosteller_details(request):
    hostellers = Hosteller_reg.objects.all()
    context = {
        'hostellers': hostellers
    }
    return render(request, 'hosteller_details.html', context)


def incharge_details(request):
    incharges = Hstlin_reg.objects.all()
    context = {
        'incharges': incharges
    }
    return render(request, 'incharge_details.html', context)

#adminlogout logic
def admin_logout(request):
    logout(request)
    return redirect('Home_page') 

# hostel incharge registration logic
def hstlin_register(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        phn = request.POST.get('phn')
        admission_date = request.POST.get('admission_date')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        passwd = request.POST.get('passwd')

        if not all([fname, lname, email, phn, admission_date, address, gender, passwd]):
            return render(request, 'hstlin_register.html', {'error': 'All fields are required.'})

        if Hstlin_reg.objects.filter(email=email).exists():
            return render(request, 'hstlin_register.html', {'error': 'Email already registered.'})

        # Hash the password before saving
        hashed_password = make_password(passwd)
        
        Hstlin_reg.objects.create(
            fname=fname,
            lname=lname,
            email=email,
            phn=phn,
            admission_date=admission_date,
            address=address,
            gender=gender,
            passwd=hashed_password,  # Save the hashed password
            status='pending'
        )

        messages.success(request, 'Registration successful. Awaiting admin approval.')
        return redirect('hstlin_login')

    return render(request, 'hstlin_register.html')

# hostel incharge login logic

def hstlin_login(request):
    success_message = ''
    error_message = ''
    if request.method == 'POST':
        email = request.POST.get('email')
        passwd = request.POST.get('password')

        if not email or not passwd:
            error_message = 'Email and password are required.'
        else:
            try:
                hstlin = Hstlin_reg.objects.get(email=email)
                
                if check_password(passwd, hstlin.passwd):
                    if hstlin.status == 'approved':
                        request.session['hstlin_email'] = hstlin.email
                        request.session['hstlin_id'] = hstlin.incharge_id
                        success_message = 'Login successful!'
                        return redirect('incharge_dashboard')
                    elif hstlin.status == 'pending':
                        error_message = 'Your registration is still pending approval.'
                    else:
                        error_message = 'Your registration has been rejected.'
                else:
                    error_message = 'Invalid email or password.'
            except Hstlin_reg.DoesNotExist:
                error_message = 'Invalid email or password.'
    
    return render(request, 'hstlin_login.html', {'success_message': success_message, 'error_message': error_message})

# def hstlin_login(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         passwd = request.POST.get('password')

#         if not email or not passwd:
#             messages.error(request, 'Email and password are required.')
#             return render(request, 'hstlin_login.html')

#         try:
#             hstlin = Hstlin_reg.objects.get(email=email)
#             # request.session['incharge_id'] = hstlin_register.incharge_id
#             # print(f"Found user: {hstlin.email}")  # Debugging
#             # print(f"Entered password: {passwd}, Stored hashed password: {hstlin.passwd}")  # Debugging

#             if check_password(passwd, hstlin.passwd):  # Check the hashed password
#                 print("Password match")  # Debugging
#                 if hstlin.status == 'approved':
#                     request.session['hstlin_id'] = hstlin.email
#                     messages.info(request, 'Login successful.')
#                     return redirect('incharge_dashboard')
#                 elif hstlin.status == 'pending':
#                     messages.error(request, 'Your registration is still pending approval.')
#                 else:
#                     messages.error(request, 'Your registration has been rejected.')
#             else:
#                 print("Password does not match")  # Debugging
#                 messages.error(request, 'Invalid email or password.')
#         except Hstlin_reg.DoesNotExist:
#             print("User does not exist")  # Debugging
#             messages.error(request, 'Invalid email or password.')

#     return render(request, 'hstlin_login.html')

# hostel incharge logout logic
def hstlin_logout(request):
    if 'hstlin_id' in request.session:
        del request.session['hstlin_id']
        messages.success(request, 'You have been logged out.')
    return redirect('hstlin_login')


def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def pending_incharges(request):
    pending_incharges = Hstlin_reg.objects.filter(status='pending')
    return render(request, 'pending_incharges.html', {'pending_incharges': pending_incharges})

@user_passes_test(is_admin)
def approve_incharge(request, incharge_id):
    incharge = get_object_or_404(Hstlin_reg, email=incharge_id)
    incharge.status = 'approved'
    incharge.save()
    return redirect('pending_incharges')

@user_passes_test(is_admin)
def reject_incharge(request, incharge_id):
    incharge = get_object_or_404(Hstlin_reg, email=incharge_id)
    incharge.status = 'rejected'
    incharge.save()
    return redirect('pending_incharges')

# hosteler registration logic
def register_hosteller(request):
    if request.method == 'POST':
        hstlr_fname = request.POST.get('hstlr_fname')
        hstlr_lname = request.POST.get('hstlr_lname')
        hstlr_email = request.POST.get('hstlr_email')
        hstlr_phn = request.POST.get('hstlr_phn')
        admission_date = request.POST.get('admission_date')
        hstlr_address = request.POST.get('hstlr_address')
        f_name = request.POST.get('f_name')
        f_phn = request.POST.get('f_phn')
        hstlr_gender = request.POST.get('hstlr_gender')
        branch = request.POST.get('branch')
        hstlr_passwd = request.POST.get('hstlr_passwd')

        if not all([hstlr_fname, hstlr_lname, hstlr_email, hstlr_phn, admission_date, hstlr_address, f_name, f_phn, hstlr_gender, branch, hstlr_passwd]):
            return render(request, 'hstlr_registration.html', {'error': 'All fields are required.'})

        if Hosteller_reg.objects.filter(hstlr_email=hstlr_email).exists():
            return render(request, 'hstlr_registration.html', {'error': 'Email already registered.'})

        hosteller = Hosteller_reg.objects.create(
            hstlr_fname=hstlr_fname,
            hstlr_lname=hstlr_lname,
            hstlr_email=hstlr_email,
            hstlr_phn=hstlr_phn,
            admission_date=admission_date,
            hstlr_address=hstlr_address,
            f_name=f_name,
            f_phn=f_phn,
            hstlr_gender=hstlr_gender,
            branch=branch,
            hstlr_passwd=hstlr_passwd,
            status='pending'
        )

        messages.success(request, 'Registration successful. Awaiting admin approval.')
        return redirect('hstlr_login')
    
    return render(request, 'hstlr_registration.html')

def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def pending_users(request):
    pending_users = Hosteller_reg.objects.filter(status='pending')
    return render(request, 'pending_users.html', {'pending_users': pending_users})

@user_passes_test(is_admin)
def approve_user(request, hstlr_id):
    user = get_object_or_404(Hosteller_reg, pk=hstlr_id)
    print(hstlr_id)
    user.status = 'approved'
    user.save()
    return redirect('pending_users')

@user_passes_test(is_admin)
def reject_user(request, hstlr_id):
    user = get_object_or_404(Hosteller_reg, pk=hstlr_id)
    user.status = 'rejected'
    user.save()
    return redirect('pending_users')

def registration_pending(request):
    return render(request, 'hstlr_regpending.html')

@user_passes_test(is_admin)
def admin_approve_requests(request):
    if not request.user.is_staff:
        return redirect('Home_page')

    if request.method == 'POST':
        admission_request = get_object_or_404(Hosteller_reg, pk=request.POST.get('admission_request_id'))
        admission_request.status = 'approved'
        admission_request.save()
        return redirect('admin_approval_requests')

    admission_requests = Hosteller_reg.objects.filter(status='pending')
    return render(request, 'admin_approval_request.html', {'admission_requests': admission_requests})

# hosteller login logic

from django.shortcuts import render, redirect
from .models import Hosteller_reg

def hstlr_login(request):
    if request.method == 'POST':
        hstlr_email = request.POST.get('hstlr_email')
        hstlr_passwd = request.POST.get('hstlr_passwd')
        
        error_message = None
        success_message = None

        if not hstlr_email or not hstlr_passwd:
            error_message = 'Email and password are required.'
        else:
            try:
                hosteller = Hosteller_reg.objects.get(hstlr_email=hstlr_email)
                if hosteller.hstlr_passwd == hstlr_passwd:
                    if hosteller.status == 'approved':
                        request.session['hosteller_email'] = hosteller.hstlr_email  
                        request.session['hosteller_id'] = hosteller.hstlr_id  

                        success_message = 'Login successful.'
                        return redirect('hosteller_dashboard', hstlr_id=hosteller.hstlr_id)
                    elif hosteller.status == 'pending':
                        return render(request, 'hstlr_regpending.html')
                    else:
                        error_message = 'Your registration has been rejected.'
                else:
                    error_message = 'Invalid email or password.'
            except Hosteller_reg.DoesNotExist:
                error_message = 'Invalid email or password.'

        context = {
            'hstlr_email': hstlr_email,
            'error_message': error_message,
            'success_message': success_message,
        }

        return render(request, 'hstlr_login.html', context)

    return render(request, 'hstlr_login.html')



# hosteler logout logic
def hstlr_logout(request):
    if 'hosteller_id' in request.session:
        del request.session['hosteller_id']
        messages.success(request, 'You have been logged out.')
    return redirect('hstlr_login')


# hosteler password reset logic
from django.core.mail import send_mail,EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.urls import reverse
from .tokens import account_activation_token

def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get("email")
        print(email)
        try:
            user = Hosteller_reg.objects.get(hstlr_email=email)
            token = account_activation_token.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = request.build_absolute_uri(reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token}))
            mail_subject = 'Reset your password'
            # message = render_to_string('password_reset_email.html', {
            #     'user': user,
            #     'reset_link': reset_link,
            # })
             # HTML message with the password
            message = f"""\
            <html>
            <body>
            <p>Hi { user.hstlr_fname }</p>
            <p>Click the link below to reset your password:</p>
            <p><a href="{reset_link }">{ reset_link }</a></p>

            </body>
            </html>
            """
            # send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [email])
            emailm = EmailMessage(
                 mail_subject,
                message,
                settings.EMAIL_HOST_USER,
                [email]
            )
            emailm.content_subtype = 'html'  # Set the content to HTML
            emailm.send(fail_silently=False)
            return redirect('password_reset_done')
        except Hosteller_reg.DoesNotExist:
            return render(request, "password_reset_form.html", {'error': 'Email does not exist'})
    return render(request, "password_reset_form.html")

def password_reset_done(request):
    return render(request, "password_reset_done.html")

def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Hosteller_reg.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Hosteller_reg.DoesNotExist):
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        if request.method == "POST":
            new_password = request.POST.get("new_password")
            user.hstlr_passwd= new_password  # You should hash the password before saving
            user.save()
            return redirect('password_reset_complete')
        return render(request, 'password_reset_confirm.html', {'uidb64': uidb64, 'token': token})
    else:
        return redirect('password_reset_invalid')

def password_reset_complete(request):
    return render(request, "password_reset_complete.html")

def password_reset_invalid(request):
    return render(request, "password_reset_invalid.html")


# incharge dashboard logic
def incharge_dashboard(request):
    hostellers = Hosteller_reg.objects.all()
    pending_requests = RoomRequest.objects.filter(is_pending=True)
    attendance_records = Attendance.objects.all().order_by('-date')
    vacant_rooms=Room.objects.filter(is_vacant=True)
    allocated_rooms= RoomRequest.objects.filter(is_approved=True)
    latest_notice = Notice.objects.filter(is_active=True).order_by('-created_at').first()
    total_rooms=Room.objects.all()
    
    
    if request.method == 'POST' and 'allocate_room' in request.POST:
        request_id = request.POST.get('request_id')
        room_number = request.POST.get('room_number')
        room_request = get_object_or_404(RoomRequest, id=request_id)
        room = get_object_or_404(Room, room_number=room_number)


    context = {
        'hostellers': hostellers,
        'pending_requests': pending_requests,
        'attendance_records': attendance_records,
        'allocated_rooms':allocated_rooms,
        'vacant_rooms': vacant_rooms,
        'total_hostellers': hostellers.count(),
        'attendance_rate': Attendance.objects.filter(status='Present').count() / Attendance.objects.count() * 100 if Attendance.objects.count() > 0 else 0,
        'latest_notice':latest_notice,
        'total_rooms':total_rooms
        
    }
    return render(request, 'incharge_dashboard.html', context)

# logic for to see room allocation details
def room_allocation_details(request):
    room_requests = RoomRequest.objects.all()

    context = {
        'room_requests': room_requests
    }
    return render(request, 'room_allocation_details.html', context)
    
# logic to add rooms 
from .models import Room
def add_room(request):
    if request.method == 'POST':
        room_number = request.POST.get('room_number')
        capacity = int(request.POST.get('capacity'))  # Ensure capacity is converted to int
        is_vacant = request.POST.get('is_vacant') == 'True'
        
        # Check if room number already exists
        if Room.objects.filter(room_number=room_number).exists():
            messages.error(request, 'Room number already exists.')
        else:
            # Create and save new room
            Room.objects.create(room_number=room_number, capacity=capacity, is_vacant=is_vacant)
            messages.success(request, 'Room added successfully.')

        return redirect('add_room')

    return render(request, 'add_room.html')


# views.py
from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Room, RoomRequest, Hosteller_reg

# View for the hosteller to see available rooms and request a room
def room_list(request):
    rooms = Room.objects.all()
    context = {
        'rooms': rooms,
    }
    return render(request, 'room_list.html', context)
from django.shortcuts import render


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from .models import RoomRequest, Room

def approve_room_allocation(request, request_id):
    room_request = get_object_or_404(RoomRequest, pk=request_id)

    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        room = get_object_or_404(Room, pk=room_id)

        if room_request.is_pending and room.is_vacant:
            room_request.is_pending = False
            room_request.is_approved = True
            room_request.allocation_date = timezone.now()
            room_request.assigned_room_number = room.room_number
            room_request.save()

            # Update room capacity and vacancy status
            room.current_capacity += 1
            if room.current_capacity >= room.capacity:
                room.is_vacant = False
            room.save()

            messages.success(request, f'Room {room.room_number} allocated successfully to {room_request.hosteller.hstlr_fname}.')
        else:
            messages.error(request, 'No vacant room available or room request has already been processed.')
    return redirect('pending_room_allocations')


def decline_room_allocation(request, request_id):
    if request.method == 'POST':
        room_request = get_object_or_404(RoomRequest, pk=request_id)
        room_request.is_pending = False
        room_request.is_approved = False
        room_request.save()
        messages.success(request, f'Request from {room_request.hosteller.hstlr_fname} denied successfully.')
    return redirect('pending_room_allocations')



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Hosteller_reg, Room, RoomRequest
import logging

logger = logging.getLogger(__name__)

def request_entry(request, room_id):
    # error_message1='none'
    # error_message2='none'
    # Get hosteller email from session
    hosteller_email = request.session.get('hosteller_email')
    logger.debug(f"Hosteller Email from session: {hosteller_email}")
    
    # If no email in session, redirect to login
    if not hosteller_email:
        messages.error(request, 'You must be logged in to request a room.')
        return redirect('hstlr_login')

    # Get hosteller based on email
    try:
        hosteller = Hosteller_reg.objects.get(hstlr_email=hosteller_email)
    except Hosteller_reg.DoesNotExist:
        messages.error(request, 'You must be registered as a hosteller to request a room.')
        return redirect('available_rooms')

    # Get room object based on room_id
    room = get_object_or_404(Room, pk=room_id)

    # Check if hosteller already has a pending or approved request
    if RoomRequest.objects.filter(hosteller=hosteller, is_pending=True).exists() or RoomRequest.objects.filter(hosteller=hosteller, is_pending=False).exists():
        messages.error(request, 'You already have a pending or approved room request.')
        return redirect('available_rooms', hosteller.hstlr_id)

    # Create a new room request
    room_request = RoomRequest.objects.create(
        hosteller=hosteller,
        assigned_room_number=room.room_number,
        is_pending=True
    )
    messages.success(request, 'Room request submitted successfully.')
    return redirect('available_rooms', hosteller.hstlr_id)

from django.shortcuts import render, get_object_or_404
from .models import Hosteller_reg, Room, RoomRequest
import logging

logger = logging.getLogger(__name__)

def available_rooms(request, hstlr_id):
    rooms = Room.objects.all()
    hosteller = get_object_or_404(Hosteller_reg, pk=hstlr_id)

    pending_request_exists = RoomRequest.objects.filter(hosteller=hosteller, is_pending=True).exists()
    allocated_room = RoomRequest.objects.filter(hosteller=hosteller, is_pending=False).first()

    return render(request, 'available_rooms.html', {
        'rooms': rooms,
        'pending_request_exists': pending_request_exists,
        'allocated_room': allocated_room,
        'hosteller': hosteller,
    })

from django.shortcuts import render
from .models import Room, RoomRequest
import logging

logger = logging.getLogger(__name__)

def pending_room_allocations(request):
    pending_requests = RoomRequest.objects.filter(is_pending=True).select_related('hosteller')
    available_rooms = Room.objects.filter(is_vacant=True)

    context = {
        'pending_requests': pending_requests,
        'available_rooms': available_rooms
    }
    return render(request, 'pending_room_allocations.html', context)


from datetime import date
def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'room_list.html', {'rooms': rooms})

def room_detail(request, room_number):
    room = Room.objects.get(room_number=room_number)
    return render(request, 'room_detail.html', {'room': room})


# attendance related logic
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from .models import Hosteller_reg, Attendance
import logging

logger = logging.getLogger(__name__)

def attendance_list(request):
    branches = Hosteller_reg.BRANCH_CHOICES
    context = {'branches': branches}
    return render(request, 'attendance_list.html', context)

def take_attendance(request):
    branch = request.GET.get('branch')
    current_date = timezone.now()
    if request.method == 'POST':
        hosteller_ids = [key.split('_')[1] for key in request.POST.keys() if key.startswith('hosteller_')]

        try:
            with transaction.atomic():
                for hosteller_id in hosteller_ids:
                    status = request.POST.get(f'hosteller_{hosteller_id}')
                    hosteller = get_object_or_404(Hosteller_reg, pk=hosteller_id)
                    Attendance.objects.create(hosteller=hosteller, status=status)

            messages.success(request, 'Attendance recorded successfully.')
            return redirect('attendance_list')

        except Exception as e:
            messages.error(request, f'Failed to record attendance: {str(e)}')
            return redirect('take_attendance', branch=branch)

    hostellers = Hosteller_reg.objects.filter(branch=branch)
    # context = {'hostellers': hostellers, 'branch': branch}
    context = {'hostellers': hostellers, 'branch': branch, 'current_date': current_date}
    return render(request, 'take_attendance.html', context)

def view_attendance(request):
    branch = request.GET.get('branch')
    logger.debug(f"Branch: {branch}")  # Debugging statement
    try:
        attendances = Attendance.objects.filter(hosteller__branch=branch).order_by('-date')
        logger.debug(f"Attendances: {attendances}")
        context = {'attendances': attendances, 'branch': branch}
        return render(request, 'view_attendance.html', context)
    except Exception as e:
        logger.error(f"Error in view_attendance: {str(e)}")
        # return render(request, 'error.html', {'message': str(e)})


# complaints logic
from django.shortcuts import render, get_object_or_404, redirect
from .models import Complaint
def complaint_list(request):
    if 'hstlin_id' in request.session:
        print("Incharge logged in.")
        complaints = Complaint.objects.all()
    elif 'hosteller_id' in request.session:
        hosteller_id = request.session.get('hosteller_id')
        print(f"Hosteller logged in with ID: {hosteller_id}")
        complaints = Complaint.objects.filter(hosteller__hstlr_id=hosteller_id)
    else:
        print("No user logged in.")
        complaints = Complaint.objects.none()
    
    return render(request, 'complaint_list.html', {'complaints': complaints})



def complaint_detail(request, complaint_id):
    complaint = get_object_or_404(Complaint, pk=complaint_id)

    if request.method == 'POST' and request.session.get('hstlin_id'):
        response = request.POST.get('response')
        if response:
            complaint.response = response
            complaint.status = 'resolved'
            complaint.save()
            # Redirect to the same page to show the updated status and response
            return redirect('complaint_detail', complaint_id=complaint_id)

    return render(request, 'complaint_detail.html', {'complaint': complaint})


from django.shortcuts import render, get_object_or_404,redirect
from .models import Hosteller_reg, Attendance,Room,RoomRequest
from django.utils import timezone

# hosteller dashboard logic
def hosteller_dashboard(request, hstlr_id):
    hosteller = get_object_or_404(Hosteller_reg, hstlr_id=hstlr_id)
    room_requests = RoomRequest.objects.filter(hosteller=hosteller).order_by('-request_date')
    notices = Notice.objects.filter(is_active=True)

    # Get the latest room request
    latest_request = room_requests.first() if room_requests.exists() else None

    if request.method == 'POST' and 'request_room' in request.POST:
        if latest_request and latest_request.is_approved:
            messages.error(request, 'Your room is already allocated.')
        else:
            RoomRequest.objects.create(
                hosteller=hosteller,
                request_date=timezone.now().date(),
                is_pending=True,
                is_approved=False
            )
            messages.success(request, 'Room request submitted successfully.')
        return redirect('hosteller_dashboard', hstlr_id=hstlr_id)

    context = {
        'hosteller': hosteller,
        'room_requests': room_requests,
        'latest_request': latest_request,
        'notices': notices,
    
    }
    
    return render(request, 'hosteller_dashboard.html', context)



def check_attendance(request, hstlr_id):
    hosteller = get_object_or_404(Hosteller_reg, pk=hstlr_id)
    attendances = Attendance.objects.filter(hosteller=hosteller)
    context = {
        'hosteller': hosteller,
        'attendances': attendances,
    }
    return render(request, 'attendance_record.html', context)

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Hosteller_reg, Complaint

def submit_complaint(request):
    hosteller_id = request.session.get('hosteller_id')
    if not hosteller_id:
        messages.error(request, 'You need to be logged in to submit a complaint.')
        return redirect('hstlr_login')  # Replace with the actual login URL name

    try:
        hosteller = Hosteller_reg.objects.get(hstlr_id=hosteller_id)
    except Hosteller_reg.DoesNotExist:
        messages.error(request, 'Hosteller not found. Please log in again.')
        return redirect('hstlr_login')  # Handle the case where hosteller is not found

    if request.method == 'POST':
        category = request.POST.get('category')
        description = request.POST.get('description')

        if category and description:
            Complaint.objects.create(
                hosteller=hosteller,
                category=category,
                description=description
            )
            messages.success(request, 'Complaint submitted successfully.')
            # Redirect to the same page with a success message
            return render(request, 'submit_complaint.html', {'hosteller': hosteller, 'success_message': 'Complaint submitted successfully.'})
        else:
            messages.error(request, 'All fields are required.')

    # If GET request or form submission failed, render the form again
    context = {
        'hosteller': hosteller,
    }
    return render(request, 'submit_complaint.html', context)



def complaint_list1(request):
    hosteller_id = request.session.get('hosteller_id')
    if not hosteller_id:
        messages.error(request, 'You need to be logged in to view complaints.')
        return redirect('hstlr_login')  # Replace with your actual login URL

    complaints = Complaint.objects.filter(hosteller__hstlr_id=hosteller_id)
    return render(request, 'complaint_list1.html', {'complaints': complaints})

# views.py
from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
from .models import Notice

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notice

def is_incharge(user):
    return user.groups.filter(name='incharge').exists()

@login_required
def notice_create(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        Notice.objects.create(title=title, content=content)
        
        if is_incharge(request.user):
            print("User is incharge")
            return redirect('incharge_dashboard')
        elif request.user.is_superuser:
            print("User is superuser")
            return redirect('admin_dashboard')
        
    return render(request, 'create_notice.html')

def notice_list(request):
    notices = Notice.objects.all().order_by('-created_at')
    return render(request, 'notice_list.html', {'notices': notices})

def notice_detail(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    return render(request, 'notice_detail.html', {'notice': notice})

@login_required
def notice_board(request):
    notices = Notice.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'notice_board.html', {'notices': notices})


def about(request):
    return render(request, 'about_us.html')

from django.core.mail import send_mail
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        full_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        
        # send_mail(
        #     subject,
        #     full_message,
        #     'your-email@example.com',  # Replace with your email
        #     ['recipient@example.com'],  # Replace with the recipient's email
        #     fail_silently=False,
        # )
        emailm = EmailMessage(
                 subject,
                message,
                settings.EMAIL_HOST_USER,
                [email]
            )
        return render(request, 'contact_us.html', {'success': True})
    
    return render(request, 'contact_us.html')

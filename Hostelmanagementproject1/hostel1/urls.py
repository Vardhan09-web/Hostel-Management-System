
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    # admin related urls
    path('',views.home_view,name='Home_page'),
    path('login/',views.login_view,name='login'),
    path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('admin_logout/',views.admin_logout,name='admin_logout'),
    path('hosteller_details/', views.hosteller_details, name='hosteller_details'),
    path('incharge_details/', views.incharge_details, name='incharge_details'),
    path('hstlr_regpending/', views.registration_pending, name='hstlr_regpending'),
    path('pending-incharges/', views.pending_incharges, name='pending_incharges'), 
    
    # hosteller related urls
    path('hstlr_registration/', views.register_hosteller, name='hstlr_registration'),  
    path('hstlr_login/',views.hstlr_login,name='hstlr_login'),
    path('hstlr_logout/', views.hstlr_logout, name='hstlr_logout'),
    path('pending_users/', views.pending_users, name='pending_users'),
    path('approve_user/<int:hstlr_id>/', views.approve_user, name='approve_user'),
    path('reject_user/<int:hstlr_id>/', views.reject_user, name='reject_user'),
    path('hosteller_dashboard/<int:hstlr_id>/', views.hosteller_dashboard, name='hosteller_dashboard'),
    path('attendance_record/<int:hstlr_id>/',views.check_attendance,name='attendance_record'),
    path('availabe_rooms/<int:hstlr_id>', views.available_rooms, name='available_rooms'),
    path('request_entry/<int:room_id>/', views.request_entry, name='request_entry'),  
   
    # incharge related urls
    path('hstlin_register/', views.hstlin_register, name='hstlin_register'),
    path('hstlin_login/', views.hstlin_login, name='hstlin_login'),
    path('hstlin_logout/', views.hstlin_logout, name='hstlin_logout'),
    path('incharge_dashboard/', views.incharge_dashboard, name='incharge_dashboard'),
    path('approve-incharge/<str:incharge_id>/', views.approve_incharge, name='approve_incharge'),
    path('reject-incharge/<str:incharge_id>/', views.reject_incharge, name='reject_incharge'),
    path('add_room/',views.add_room,name='add_room'),
    path('attendance_list/', views.attendance_list, name='attendance_list'),
    path('take_attendance/', views.take_attendance, name='take_attendance'),
    path('view_attendance/',views.view_attendance,name='view_attendance'),
    path('approve_request/<int:request_id>/', views.approve_room_allocation, name='approve_request'),
    path('deny_request/<int:request_id>/', views.decline_room_allocation, name='deny_request'),
    path('room_allocation_details/',views.room_allocation_details,name="room_allocation_details"),
    path('pending_room_allocations/', views.pending_room_allocations, name='pending_room_allocations'),

    #Reset password urls 
    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('password_reset/done/', views.password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', views.password_reset_complete, name='password_reset_complete'),
    path('reset/invalid/', views.password_reset_invalid, name='password_reset_invalid'),

    # complaint related urls
    path('complaint/submit/', views.submit_complaint, name='submit_complaint'),
    path('complaint/list/', views.complaint_list, name='complaint_list'),
    path('complaint_list1/', views.complaint_list1, name='complaint_list1'),
    path('complaint/<int:complaint_id>/', views.complaint_detail, name='complaint_detail'),

    # notice related urls
    path('notices/', views.notice_list, name='notice_list'),
    path('notices/<int:pk>/', views.notice_detail, name='notice_detail'),
    path('notices/new/', views.notice_create, name='create_notice'),
    path('notice-board/', views.notice_board, name='notice_board'),
    path('about/',views.about,name='about_us'),
    path('contact/',views.contact_us,name='contact_us'),


    # path('select_hostel_type/',views.hosteller_type,name='select_hostel_type')

]


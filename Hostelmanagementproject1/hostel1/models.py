from django.db import models

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
)


STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
)

# hosteller_registration model
class Hosteller_reg(models.Model):
    BRANCH_CHOICES = (
        ('CSE', 'Computer Science And Engineering'),
        ('IT', 'Information Technology'),
        ('ECE', 'Electronics and Communication Engineering'),
        ('ME', 'Mechanical Engineering'),
        ('CE', 'Civil Engineering'),
        ('EEE', 'Electrical and Electronics Engineering'),
        ('Other','other branch'),
)
    hstlr_id = models.AutoField(primary_key=True)
    hstlr_fname = models.CharField(max_length=20, null=False)
    hstlr_lname = models.CharField(max_length=20, null=False)
    hstlr_email = models.EmailField(unique=True, null=False)
    hstlr_phn = models.BigIntegerField(null=False)
    admission_date = models.DateField()
    hstlr_address = models.CharField(max_length=200, null=False)
    f_name = models.CharField(max_length=40, null=False)
    f_phn = models.BigIntegerField(null=False)
    hstlr_gender = models.CharField(max_length=3, choices=GENDER_CHOICES, null=False)
    branch = models.CharField(max_length=5, choices=BRANCH_CHOICES, null=False)
    hstlr_passwd = models.CharField(max_length=128, null=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.hstlr_fname} {self.hstlr_lname}"

    class Meta:
        verbose_name = "Hosteller Admission"
        verbose_name_plural = "Hosteller Admission"

# AdmissiomRequest table
class AdmissionRequest(models.Model):
    hosteller = models.OneToOneField(Hosteller_reg, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.hosteller.hstlr_fname} {self.hosteller.hstlr_lname} - {'Approved' if self.is_approved else 'Pending'}"

# hostel_incharge registration table
class Hstlin_reg(models.Model):
    incharge_id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=20, null=False)
    lname = models.CharField(max_length=20, null=False)
    email = models.EmailField(unique=True, null=False)
    phn = models.BigIntegerField(null=False)
    admission_date = models.DateField()
    address = models.CharField(max_length=200, null=False)
    gender = models.CharField(max_length=3, choices=GENDER_CHOICES, null=False)
    passwd = models.CharField(max_length=128, null=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.email} {self.phn}"

    class Meta:
        verbose_name = "Hostel Incharge Admission"
        verbose_name_plural = "Hostel Incharge Admission"

# Attendance Table
class Attendance(models.Model):
    hosteller = models.ForeignKey(Hosteller_reg, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, default='present')

    def __str__(self):
        return f"{self.hosteller.hstlr_fname} - {self.date} - {self.status}"
     

# class Room(models.Model):
#     room_number = models.CharField(max_length=10, unique=True)
#     capacity = models.IntegerField()
#     is_vacant = models.BooleanField(default=True)

#     def __str__(self):
#         return f"Room {self.room_number}"

# Room table
class Room(models.Model):
    room_number = models.CharField(max_length=10, unique=True)
    capacity = models.IntegerField()
    current_capacity = models.IntegerField(default=0)
    is_vacant = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Update is_vacant based on current_capacity
        self.is_vacant = self.current_capacity < self.capacity
        super().save(*args, **kwargs)
    
    def allocate(self):
        if self.current_capacity < self.capacity:
            self.current_capacity += 1
            self.save()

    # def deallocate(self):
    #     if self.current_capacity > 0:
    #         self.current_capacity -= 1
    #         self.save()

    def __str__(self):
        return f"Room {self.room_number}"
    
# Roomrequsets details Table 
class RoomRequest(models.Model):
    hosteller = models.ForeignKey(Hosteller_reg, on_delete=models.CASCADE)
    request_date = models.DateField(auto_now_add=True)
    allocation_date=models.DateField(blank=True,null=True)
    is_approved=models.BooleanField(default=False)
    is_pending=models.BooleanField(default=True)
    assigned_room_number=models.CharField(max_length=10,blank=True,null=True)


# class MessBill(models.Model):
#     hosteller = models.ForeignKey(Hosteller_reg, on_delete=models.CASCADE)
#     month = models.CharField(max_length=10)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)

# Notice table
class Notice(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    posted_by = models.CharField(max_length=20,null=True,default='HM')

    def __str__(self):
        return self.title

#Complaints Table
class Complaint(models.Model):
    CATEGORY_CHOICES = [
        ('room', 'Room'),
        ('mess', 'Mess'),
        ('washrooms','Washrooms'),
        ('other issues','Other Issues'),
        
    ]

    hosteller = models.ForeignKey('Hosteller_reg', on_delete=models.CASCADE)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, default='pending')
    incharge = models.ForeignKey('Hstlin_reg', related_name='incharge', on_delete=models.CASCADE, null=True, blank=True)
    response = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.hosteller.hstlr_fname} {self.hosteller.hstlr_lname} - {self.category} - {self.status}'

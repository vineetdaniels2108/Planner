from django.db import models
import re
import bcrypt

# Create your models here.

class UserManager(models.Manager):
    def RegistrationValidator(self, postData):
        errors = {}
        
        if len(postData['first_name']) <2:
            errors['first_name'] = 'First Name should be greater than 2 characters'
        
        if len(postData['last_name']) <2:
            errors['last_name'] = 'Last Name should be greater than 2 characters'
            
        if len(postData['password']) <8:
            errors['password'] = 'Password should be greater than 8 characters'
            
        UserRegex = re.compile(r'^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$')
        
        if not UserRegex.match (postData['email']):
            errors['email'] = 'Email is not valid'
            
        email_check = User.objects.filter(email = postData['email']) 
        
        if len(email_check) > 0:
            errors['email_exist'] = 'Email already in use'
            
        if postData['password'] != postData['confirm_password']:
            errors['confirm_password'] = 'Confrim password does not match'
            
        return errors
    
    def LoginValidator(self, postData):
        errors = {}
        login_user = User.objects.filter(email = postData['email'])
        if len(login_user)> 0:
            if bcrypt.checkpw(postData['password'].encode(), login_user[0].password.encode()):
                print ('password matches')
            else:
                errors['password'] = 'Password does not match'
        else:
            errors['email'] = 'There is no user with that email'
        
        return errors
    

destination_choices = (
    ("1","cartagena"),
    ("2","vancouver"),
    ("3","sanfrancisco"),
    ("4","losangeles"),
)

month_choices = (
    ("1","January"),
    ("2","Feb"),
    ("3","March"),
    ("4","April"),
    ("5","May"),
    ("6","June"),
    ("7","July"),
    ("8","August"),
    ("9","September"),
    ("10","October"),
    ("11","November"),
    ("12","December"),
)

budget_choices = (
    ("1","low"),
    ("2","Medium"),
    ("3","High"),
    ("4","luxury"),
)

activity_choices = (
    ("Budget Planning","Budget Planning"),
    ("Attire","Attire"),
    ("Flowers","Flowers"),
    ("Decor","Decor"),
    ("Music","Music"),
    ("6","Photography"),
    ("7","Gifts"),
    ("8","Ceremony"),
    ("9","Stationary"),
    ("10","Wedding Rings"),
    ("11","Transportation"),
    ("12","Misc"),
)

class User(models.Model):
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length = 30)
    email = models.CharField(max_length = 80)
    password = models.CharField (max_length = 32)
    role = models.CharField(max_length = 32)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField (auto_now = True)
    objects = UserManager()
    
class Planner(models.Model):
    planner = models.ForeignKey(User, related_name='planner', on_delete=models.CASCADE)
    destination = models.CharField(max_length= 240, choices=destination_choices, unique=False)
    months = models.CharField(max_length= 240, choices=month_choices, unique=False)
    budget = models.CharField(max_length= 240, choices=budget_choices, unique=False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField (auto_now = True)

class Customer(models.Model): 
    customer = models.ForeignKey(User, related_name='customer', on_delete=models.CASCADE)
    destination = models.CharField(max_length= 240, choices=destination_choices, unique=False)
    months = models.CharField(max_length= 240, choices=month_choices, unique=False)
    budget = models.CharField(max_length= 240, choices=budget_choices, unique=False)
    activity = models.CharField(max_length= 240, choices=activity_choices, unique=False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField (auto_now = True)
    
class Message(models.Model):
    message = models.TextField()
    posted_by = models.ForeignKey(User, related_name='posted_by', on_delete=models.CASCADE)
    posted_for = models.ForeignKey(User, related_name='posted_for', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField (auto_now = True)

class Comment(models.Model):
    comment = models.TextField()
    posted_by = models.ForeignKey(User, related_name='user_comment', on_delete=models.CASCADE)
    message = models.ForeignKey(Message, related_name = 'message_comment', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField (auto_now = True)
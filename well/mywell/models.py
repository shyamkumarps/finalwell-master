from django.db import models
from django_measurement.models import MeasurementField
from measurement.measures import Distance
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager ,PermissionsMixin

# import that we need for authentication token
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import Group
from passlib.hash import pbkdf2_sha256



class CustomGroup(models.Model):
    group                   =   models.OneToOneField(Group, verbose_name="group", on_delete=models.CASCADE)
    Number_of_Users         =   models.IntegerField(blank=True, null=True)
    License_Start_Date      =   models.DateField(auto_now_add=False,verbose_name="License_Start_Date",blank=True,null=True)
    License_End_Date        =   models.DateField(auto_now_add=False,verbose_name="License_End_Date",blank=True,null=True)
    status 				    =   models.CharField(max_length=30,blank=True,null=True)

    def __str__(self):
        return f"{self.group},{self.Number_of_Users}"






class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError('Users must have an email address')
		if not username:
			raise ValueError('Users must have a username')

		user = self.model(
			email=self.normalize_email(email),
			username=username,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
		)
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user

# User 
class Account(AbstractBaseUser):
    
    email 					=   models.EmailField(verbose_name="email", max_length=60, unique=True,blank=True,null=True)
    phonenumber             =   models.CharField( max_length=30,unique=True,blank=True,null=True)
    username 				=   models.CharField(max_length=30,unique=True,blank=True,null=True)
    date_joined				=   models.DateTimeField(verbose_name='date joined', auto_now_add=True,blank=True,null=True)
    last_login				=   models.DateTimeField(verbose_name='last login', auto_now=True,blank=True,null=True)
    role                    =   models.CharField(max_length=30,unique=True,blank=True,null=True)
    is_active				=   models.BooleanField(default=True,blank=True,null=True)
    is_staff				=   models.BooleanField(default=False,blank=True,null=True)
    is_superuser			=   models.BooleanField(default=False,blank=True,null=True)
    Company                 =   models.ForeignKey(Group,on_delete=models.CASCADE,blank=True,null=True)
    Company_Name            =   models.CharField(max_length=200,blank=True,null=True)
    

    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = MyAccountManager()
    # Account.verify_password and pass string 
    def verify_password(self,raw_password):
        return pbkdf2_sha256.verify(raw_password,self.password)


    def __str__(self):
        return f"{self.Company},{self.username}"

    def has_perm(self, perm, obj=None):
	    return self.is_superuser

    def has_module_perms(self, app_label):
        return True






class project(models.Model):
    user                =   models.ForeignKey(Account, on_delete=models.CASCADE)
    Project             =   models.CharField(max_length=200, blank=True, null=True)
    Location            =   models.TextField()
    Bearing_of_hole     =   models.CharField(max_length=200, blank=True, null=True)
    #Collar_elevation   =   MeasurementField(measurement=Distance,default=None)
    Collar_elevation    =   models.FloatField("Collar_elevation-float-m")
    Date_of_start       =   models.DateField(auto_now_add=False,verbose_name="Date_of_start")
    Type_of_core_barrel =   models.CharField(max_length=200, blank=True, null=True)
    Drilling_Agency     =   models.CharField(max_length=200, blank=True, null=True)
    Co_ordinate_east    =   models.FloatField("co-ordinates-float-east")
    Co_ordinate_north   =   models.FloatField("co-ordinates-float-north")
    Drill_hole_no       =   models.CharField(max_length=200, blank=True, null=True)
    #Total_depth        =   MeasurementField(measurement=Distance,default=None)
    Total_depth         =   models.IntegerField("Total_depth-meters")
    Page_no             =   models.IntegerField("page_no")
    Date_of_completion  =   models.DateField(auto_now_add=False,verbose_name="Date_of_completion")
    Rig_type            =   models.CharField(max_length=200, blank=True, null=True)


    def __str__(self):
        return f"{self.Location},{self.Project}"
    
def upload_location(instance, filename, **kwargs):
	file_path = 'project/{project_id}/{IS_classification}-{filename}'.format(
			project_id=str(instance.project), IS_classification=str(instance.IS_classification), filename=filename
		) 
	return file_path

class project_detail(models.Model):  
    project                         =   models.ForeignKey(project, on_delete=models.CASCADE)
    Depth_from                      =   models.FloatField("Depth_from-float")
    Depth_to                        =   models.FloatField("Depth_to-float")
    Ground_elevation                =   models.FloatField("Ground_elevation-float(m)")
    Description                     =   models.CharField(max_length=200, blank=True, null=True)
    Litholog                        =   models.ImageField(upload_to=upload_location, null=False, blank=True)
    Structure_condition             =   models.TextField(default="null")

    Size_of_core_piceses_lt_10      =   models.IntegerField("Size_of_core_piceses_lt_10", blank=True, null=True)
    Size_of_core_piceses_10_25      =   models.IntegerField("Size_of_core_piceses_10_25", blank=True, null=True)
    Size_of_core_piceses_25_75      =   models.IntegerField("Size_of_core_piceses_25_75", blank=True, null=True)
    Size_of_core_piceses_75_150     =   models.IntegerField("Size_of_core_piceses_75_150", blank=True, null=True)
    Size_of_core_piceses_gt_150     =   models.IntegerField("Size_of_core_piceses_gt_150", blank=True, null=True)

    Core_recovery_0_20              =   models.IntegerField("Core_recovery_0_20", blank=True, null=True)
    Core_recovery_20_40             =   models.IntegerField("Core_recovery_20_40", blank=True, null=True)
    Core_recovery_40_60             =   models.IntegerField("Core_recovery_40_60", blank=True, null=True)
    Core_recovery_60_80             =   models.IntegerField("Core_recovery_60_80", blank=True, null=True)
    Core_recovery_80_100            =   models.IntegerField("Core_recovery_80_100", blank=True, null=True)

    RQD_0_25                        =   models.IntegerField("RQD_0_25", blank=True, null=True)
    RQD_25_50                       =   models.IntegerField("RQD_25_50", blank=True, null=True)
    RQD_50_75                       =   models.IntegerField("RQD_50_75", blank=True, null=True)
    RQD_75_100                      =   models.IntegerField("RQD_75_100", blank=True, null=True)

    SPT_N_Value                     =   models.CharField(max_length=200, blank=True, null=True)
    Penetration_Rate                =   models.FloatField("Penetration_Rate(cm/min)")
    Size_of_Hole                    =   models.CharField(max_length=200, blank=True, null=True)
    Casing                          =   models.CharField(max_length=200, blank=True, null=True)
    Drill_Water_Loss_Nill           =   models.CharField(max_length=200, blank=True, null=True)
    Drill_Water_Loss_Partial        =   models.CharField(max_length=200, blank=True, null=True)
    Drill_Water_Loss_complete       =   models.CharField(max_length=200, blank=True, null=True)

    Permeability_K_value_Lugon      =   models.FloatField("Permeability_K_value_or_Lugon")
    IS_classification               =   models.CharField(max_length=200, blank=True, null=True)


    def __str__(self):
        return f"{self.project}"


@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
	# if a account object is created and inserted and save to db then we have create TOKEN 
	if created:
		Token.objects.create(user=instance)





















    # Rediish_Brown_Clay_Soil      = 'RBCS'
    # Yellowish_Gray_clay_soil     = 'YGCS'
    # Yellowish_clayey_sand        = 'YCS'
    # Yellowish_Silty_Sand         = 'YSS'
    # Medium_Grain_Size_silty_sand = 'MGSS'
    # SOIL_CHOICES = [
    #     (Rediish_Brown_Clay_Soil, 'RBCS'),
    #     (Yellowish_Gray_clay_soil, 'YGCS'),
    #     (Yellowish_clayey_sand, 'YCS'),
    #     (Yellowish_Silty_Sand, 'YSS'),
    #     (Medium_Grain_Size_silty_sand, 'MGSS'),
    # ]

    
    # Description     = models.CharField(
    #     max_length  =50,
    #     choices     = SOIL_CHOICES,
    #     default     =Rediish_Brown_Clay_Soil)

    
    

    # CHOICES = [(i,i) for i in range(101)]

    # Size_of_core_piceses = models.IntegerField(
    #     choices = CHOICES,
    #     default="null")


    # Core_recovery = models.IntegerField(
    #     choices = CHOICES,
    #     default="null")
    

    # CHOICES = [(i,i) for i in range(101)]

    # RQD = models.IntegerField(
    #     choices = CHOICES,
    #     default="null")

    # nill = 'nill'
    # gt_100 = '>100'
    # SPT_N_Value_CHOICES = [
    #     (nill, 'nill'),
    #     (gt_100, '>100'),
        
    # ]


    # SPT_N_Value = models.CharField(
    #     max_length=50,
    #     choices = SPT_N_Value_CHOICES,
    #     default="null")

    # # Penetration_Rate = MeasurementField(measurement=Distance,default=None)
    # Penetration_Rate = models.FloatField("Penetration_Rate(cm/min)")

    # PX = 'PX'
    # HX = 'HX'
    # NX = 'NX'
    # Size_of_Hole_CHOICES = [
    #     (PX, 'PX'),
    #     (HX, 'HX'),
    #     (NX, 'NX'),
        
    # ]
    # Size_of_Hole = models.CharField(
    #     max_length=50,
    #     choices = Size_of_Hole_CHOICES,
    #     default="null")

    # # Casing = MeasurementField(measurement=Distance,default=None)
    # Casing = models.IntegerField("Casing-mm")
    # # Depth_of_Water_Table = MeasurementField(measurement=Distance,default=None)
    # Depth_of_Water_Table = models.CharField(max_length=200, blank=True, null=True)

    # Nil = 'Nil'
    # Partial = 'Partial'
    # Complete = 'Complete'
    # Drill_Water_Loss_CHOICES = [
    #     (Nil, 'Nil'),
    #     (Partial, 'Partial'),
    #     (Complete, 'Complete'),
    # ]
    # Drill_Water_Loss = models.CharField(
    #     max_length=50,
    #     choices = Drill_Water_Loss_CHOICES,
    #     default="null")

    # Permeability_K_value_or_Lugon = models.FloatField("Permeability_K_value_or_Lugon")
    # IS_classification = models.CharField(max_length=200, blank=True, null=True)

    





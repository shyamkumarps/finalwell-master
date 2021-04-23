from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import *
from .models import *

from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from django.contrib.auth import authenticate
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter,SearchFilter
import datetime
# from django.contrib.auth.hashers import make_password,check_password
from passlib.hash import pbkdf2_sha256
# Create your views here.



class AccountView(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    # filter_backends =(DjangoFilterBackend,)
    # filter_fields =('groups',)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            id = instance.id
            user_id = instance.user_id

            self.perform_destroy(instance)
            admin_user = Account.objects.filter(user_id= user_id).delete()

        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)


class projectView(viewsets.ModelViewSet):
    queryset = project.objects.all()
    serializer_class = projectSerializer

    # filter_backends =(DjangoFilterBackend,)
    # filter_fields =('groups',)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            id = instance.id
            user_id = instance.user_id

            self.perform_destroy(instance)
            admin_user = project.objects.filter(user_id= user_id).delete()

        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomGroupView(APIView):
    # serializer_class = CustomGroupSerializer

    # def get_queryset(self):
    #     CustomGroup_data = CustomGroup.objects.all()
    #     return CustomGroup_data
    
    def post(self, request):
        response = {}
        data =request.data
        print(data)
        Group_name = data.get('name')
        print(Group_name)
        create_new_grp = Group.objects.create(name= Group_name)
        create_new_grp.save()

        Number_of_Users = data.get('Number_of_Users')
        License_Start_Date = data.get('License_Start_Date')
        License_End_Date = data.get('License_End_Date')
        status_sample = data.get('status')
        new_custom_group=CustomGroup.objects.create(group_id = create_new_grp.id,Number_of_Users= Number_of_Users ,License_Start_Date = License_Start_Date ,License_End_Date= License_End_Date, status= status_sample )
        new_custom_group.save()


        response['result'] = 'Register Sucessfully'

        return Response(response)

    

    # check_user_grp = Account.objects.get(id= frntend_retun_id)
    
    # comp_details = CustomGropu.objects.get(Company_id = check_user_grp.company_id)

    # no_of_users_added = Account.objects.get(Company_id= comp_details.Company_id).count()

    # l_start = comp_details.li
    # l_end = comp_details
    # no_of_users = comp_details.Number_of_Users

    # if comp_details.Number_of_Users < no_of_users_added:
    #     ....
    # else:
    #     return error


class RegisterAPI(APIView):

    def post(self, request):
        
        data = request.data
        
        signup_user = data.get('role')

        response = {} 

        if signup_user == 'User':

            user_id = data.get('user_id')

            check_user_grp          = Account.objects.get(id=user_id)
            comp_details            = CustomGroup.objects.get(group_id = check_user_grp.Company_id)
            no_of_users_added       = Account.objects.filter(Company_id= check_user_grp.Company_id).count()

            print(comp_details.Number_of_Users)
            print(no_of_users_added)


            if int(comp_details.Number_of_Users) > int(no_of_users_added):

                User_Company_ID = data.get('Company_ID')
                User_email = data.get('email')
                User_password = data.get('password')
                User_phonenumber = data.get('phonenumber')

                enc_password = pbkdf2_sha256.encrypt(User_password,rounds=12000,salt_size=32)

                user_create = Account.objects.create(username=User_email,email=User_email,password=enc_password,Company_id= check_user_grp.Company_id,phonenumber=User_phonenumber)
                
                response['result'] = 'Register Sucessfully'
            else:
                response['result'] = 'Maximum Numbers of Users Limit Reached.'


        elif signup_user == 'Admin':

            Admin_Company_Name = data.get('Company_Name')
        
            Admin_email = data.get('email')
            Admin_password = data.get('password')
            Admin_phonenumber = data.get('phonenumber')
            
            comp_details = Group.objects.get(name = Admin_Company_Name)
    
            enc_password = pbkdf2_sha256.encrypt(Admin_password,rounds=12000,salt_size=32)

            user_create = Account.objects.create(username=Admin_email,email=Admin_email,password=enc_password,Company_Name=comp_details.name,Company_id= comp_details.id,)
            

            user_create.save()
            response['result'] = 'Register Sucessfully'
        else:
            response['result'] = 'something went wrong check the role given!!'
        

        return Response(response)

        
class projectAPI(APIView):
    serializer_class = projectSerializer

    def post(self, request):
        data = request.data 


        user = data.get('user')
        Project = data.get('Project')
        Location = data.get('Location')
        Bearing_of_hole = data.get('Bearing_of_hole')
        Collar_elevation = data.get('Collar_elevation')
        Date_of_start = data.get('Date_of_start')
        Type_of_core_barrel = data.get('Type_of_core_barrel')
        Drilling_Agency = data.get('Drilling_Agency')
        Co_ordinate_east = data.get('Co_ordinate_east')
        Co_ordinate_north = data.get('Co_ordinate_north')
        Drill_hole_no = data.get('Drill_hole_no')
        Total_depth = data.get('Total_depth')
        Page_no = data.get('Page_no')
        Date_of_completion = data.get('Date_of_completion')
        Rig_type = data.get('Rig_type')
        

        project_create = project.objects.create(user=user,Project=Project,Location=Location,Bearing_of_hole=Bearing_of_hole,Collar_elevation= Collar_elevation,Date_of_start=Date_of_start,Type_of_core_barrel=Type_of_core_barrel,Drilling_Agency=Drilling_Agency,Co_ordinate_east=Co_ordinate_east,Co_ordinate_north=Co_ordinate_north,Drill_hole_no=Drill_hole_no,Total_depth=Total_depth,Page_no=Page_no,Date_of_completion=Date_of_completion,Rig_type=Rig_type)

        project_create.save()
        print(project_create)
        
        serializer = projectSerializer(project_create)
        return Response(serializer.data)




class projectdetailAPI(APIView):
    serializer_class = project_detailSerializer

    def post(self, request):
        data = request.data 



        project = data.get('project')
        Depth_from = data.get('Depth_from')
        Depth_to = data.get('Depth_to')
        Ground_elevation = data.get('Ground_elevation')
        Description = data.get('Description')
        Litholog = data.get('Litholog')
        Structure_condition = data.get('Structure_condition')
        Size_of_core_piceses_lt_10 = data.get('Size_of_core_piceses_lt_10')
        Size_of_core_piceses_10_25 = data.get('Size_of_core_piceses_10_25')
        Size_of_core_piceses_25_75 = data.get('Size_of_core_piceses_25_75')
        Size_of_core_piceses_75_150 = data.get('Size_of_core_piceses_75_150')
        Size_of_core_piceses_gt_150 = data.get('Size_of_core_piceses_gt_150')
        Core_recovery_0_20 = data.get('Core_recovery_0_20')
        Core_recovery_20_40 = data.get('Core_recovery_20_40')
        Core_recovery_40_60 = data.get('Core_recovery_40_60')
        Core_recovery_60_80 = data.get('Core_recovery_60_80')
        Core_recovery_80_100 = data.get('Core_recovery_80_100')
        RQD_0_25 = data.get('RQD_0_25')
        RQD_25_50 = data.get('RQD_25_50')
        RQD_50_75 = data.get('RQD_50_75')
        RQD_75_100 = data.get('RQD_75_100')
        SPT_N_Value = data.get('SPT_N_Value')
        Penetration_Rate = data.get('Penetration_Rate')
        Size_of_Hole = data.get('Size_of_Hole')
        Casing = data.get('Casing')
        Drill_Water_Loss_Nill = data.get('Drill_Water_Loss_Nill')
        Drill_Water_Loss_Partial = data.get('Drill_Water_Loss_Partial')
        Drill_Water_Loss_complete = data.get('Drill_Water_Loss_complete')
        Permeability_K_value_Lugon = data.get('Permeability_K_value_Lugon')
        IS_classification = data.get('IS_classification')




        projectdetail_create = project_detail.objects.create(project=project,Depth_from=Depth_from,Depth_to=Depth_to,Ground_elevation=Ground_elevation,
                            Description=Description,Litholog=Litholog,Structure_condition=Structure_condition,Size_of_core_piceses_lt_10=Size_of_core_piceses_lt_10,
                            Size_of_core_piceses_10_25=Size_of_core_piceses_10_25,Size_of_core_piceses_25_75=Size_of_core_piceses_25_75,
                            Size_of_core_piceses_75_150=Size_of_core_piceses_75_150,Size_of_core_piceses_gt_150=Size_of_core_piceses_gt_150,
                            Core_recovery_0_20=Core_recovery_0_20,Core_recovery_20_40=Core_recovery_20_40,Core_recovery_40_60=Core_recovery_40_60,
                            Core_recovery_60_80=Core_recovery_60_80,Core_recovery_80_100=Core_recovery_80_100,RQD_0_25=RQD_0_25,RQD_25_50=RQD_25_50,RQD_50_75=RQD_50_75,
                            RQD_75_100=RQD_75_100,SPT_N_Value=SPT_N_Value,Penetration_Rate=Penetration_Rate,Size_of_Hole=Size_of_Hole,Casing=Casing,Drill_Water_Loss_Nill=Drill_Water_Loss_Nill,
                            Drill_Water_Loss_Partial=Drill_Water_Loss_Partial,Drill_Water_Loss_complete=Drill_Water_Loss_complete,Permeability_K_value_Lugon=Permeability_K_value_Lugon,
                            IS_classification=IS_classification)

        projectdetail_create.save()
        print(projectdetail_create)
        
        serializer = project_detailSerializer(projectdetail_create)
        return Response(serializer.data)















class CustomAuthToken(ObtainAuthToken):

    def post(self, request):
        curr_date= datetime.date.today()
        data = request.data
        print(data)

        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        if user:
            
            cust_gp_data = CustomGroup.objects.get(group_id= user.Company_id)

            if curr_date <= cust_gp_data.License_End_Date:
                
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'user_id': user.pk,
                    'email': user.email,
                    'username':user.username,
                    'result': 'Login Sucessfully'
                })

            else:
                return Response({'result':'License has been expired.Please contact administrator.'})
        else:
                return  Response({'result':'Enter Valid Username and Password.'})





class ObtainAuthTokenView(APIView):

	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	def post(self, request):
		context = {}

		email = request.POST.get('username')
		password = request.POST.get('password')
		Account = authenticate(email=email, password=password)
		if Account:
			try:
				token = Token.objects.get(user=Account)
			except Token.DoesNotExist:
				token = Token.objects.create(user=Account)
			context['response'] = 'Successfully authenticated.'
			context['pk'] = Account.pk
			context['email'] = email
			context['token'] = token.key
		else:
			context['response'] = 'Error'
			context['error_message'] = 'Invalid credentials'

		return Response(context)




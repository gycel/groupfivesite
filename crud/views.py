from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages 
from .models import Genders, Users
from django.contrib.auth.hashers import make_password, check_password
from .utils import login_required_custom

@login_required_custom
def login_view(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')

            try:
                user = Users.objects.get(email=email)
                if check_password(password, user.password):
                    request.session['user_id'] = user.user_id
                    return redirect('/user/list')
                else:
                    return render(request, 'layout/LogIn.html', {'error': 'Invalid password'})
            except Users.DoesNotExist:
                messages.warning(request, 'User does not exist.')
                return render(request, 'layout/LogIn.html', {'error': 'User not found'})

        return render(request, 'layout/LogIn.html')
    except Exception as e:
        return HttpResponse(f'Error occurred during login: {e}')

def gender_list(request):
    try:
        genderObj = Genders.objects.all()

        data = {
            'genders':genderObj
        }

        return render(request, 'gender/GendersList.html', data)
    except Exception as e:
        return HttpResponse(f'Error occured during load genders: {e}')

def add_gender(request):
    try:
        if request.method == 'POST':
            gender = request.POST.get('gender')

            Genders.objects.create(gender=gender).save()
            messages.success(request, 'Gender added successfully!')
            return redirect('/gender/list')
        else:
            return render(request, 'gender/AddGender.html')
    except Exception as e:
        return HttpResponse(f'Error occured during add gender: {e}')
    
def edit_gender(request, genderId):
    try:
        if request.method == 'POST':
            genderObj = Genders.objects.get(pk=genderId)

            gender = request.POST.get('gender')

            genderObj.gender = gender
            genderObj.save()

            messages.success(request, 'Gender updated successfully!')
            
            data = {
                'gender': genderObj 
            }
            
            return render(request, 'gender/EditGender.html', data)
        else:
            genderObj = Genders.objects.get(pk=genderId)

            data = {
                'gender': genderObj 
            }

            return render(request, 'gender/EditGender.html', data)
        
    except Exception as e:
        return HttpResponse(f'Error occured during edit gender: {e}')
    
def delete_gender(request, genderId):
    try:
        if request.method == 'POST':
            genderObj = Genders.objects.get(pk=genderId)
            genderObj.delete()

            messages.success(request, 'Gender deleted successfully!')
            return redirect('/gender/list')
        else:
            genderObj = Genders.objects.get(pk=genderId)

            data = {
                'gender': genderObj 
            }
            
        return render(request, 'gender/DeleteGender.html', data)
    except Exception as e:
        return HttpResponse(f'Error occured during delete gender: {e}')

def user_list(request):
    try:
        userObj = Users.objects.select_related('gender')

        data = {
            'users':  userObj
        }

        return render(request, 'user/UsersList.html', data)
    except Exception as e:
        return HttpResponse(f'Error occured during load users: {e}')

def add_user(request):
    try:
        if request.method == 'POST':
            fullName = request.POST.get('full_name')
            gender = request.POST.get('gender')
            birthDate = request.POST.get('birth_date')
            address = request.POST.get('address')
            contactNumber = request.POST.get('contact_number')
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            confirmPassword = request.POST.get('confirm_password')

            # if password != confirmPassword:
                # if password and confirmPassword do not match, show error message

            Users.objects.create(
                full_name=fullName,
                gender=Genders.objects.get(pk=gender),
                birth_date=birthDate,
                address=address,
                contact_number=contactNumber,
                email=email,
                username=username,
                password=make_password(password),
            ).save()

            messages.success(request, 'User added successfully!')
            return redirect('/user/add')
        else:
            genderObj = Genders.objects.all()

            data = {
            'genders': genderObj
            }
        return render(request, 'user/AddUser.html', data)
    except Exception as e:
        return HttpResponse(f'Error occured during add user: {e}')
    
# def logout(request):
#     request.session.flush()
#     return redirect('/layout/login') 
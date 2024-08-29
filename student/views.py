from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import random
from django.shortcuts import get_object_or_404



from main.models import Profile , Lecture , StudentLectureObject, LectureCode ,  Part , StudentPartObject, Chapter , ChapterLecture , Group , GroupMember , GroupLecture, GroupMessage ,GroupRequest, BuyLesson , BuyChapter
from main.models import Code , Notification , Transaction , LikeLecture , StudentQuestion ,  StudentQuestionAnswer 
from main.models import Assignment , AssignmentOpen  , AssignmentSubmit ,Question , Answer ,   News ,GetPremium ,RechargeRequest , LoginInfo           
from main.models import SocialLink         



# Main Page 

@login_required(login_url='login')
def main(request, pk):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''



    profile_object = User.objects.get(username=pk)
    profile = Profile.objects.get(user=profile_object)

    purchased_lectures = BuyLesson.objects.filter(user=profile.user)

    total_answers = 0
    true_answers = 0
    percentage = 0

    if AssignmentSubmit.objects.filter(user=profile_object).first():
        student_submit_objects = AssignmentSubmit.objects.filter(user=profile_object)
        for x in student_submit_objects:
            true_answers = true_answers + x.true_answers
            student_answers = Answer.objects.filter(user=profile_object , assignment_id=x.assignment_id)
            for z in student_answers:
                total_answers = total_answers + 1
        percentage = round(true_answers / total_answers * 100)



    zero = 0

    payments = 0
    for x in purchased_lectures:
        payments = payments + x.lecture_value

    transactions = Transaction.objects.filter(user=profile.user).order_by('-created_at')

    new_replys_count = 0
    if StudentQuestionAnswer.objects.filter(seen=False , answered_to_profile = profile).first():
        new_replys = StudentQuestionAnswer.objects.filter(seen=False , answered_to_profile = profile)
        for x in new_replys:
            new_replys_count = new_replys_count + 1


    notifications_objects = Notification.objects.filter(second_user=profile_object.username).order_by('-created_at')
    
    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'profile': profile,
        'profile_object': profile_object,
        'notifications' : notifications_count ,

        'notifications_objects':notifications_objects,
        
        'payments' : payments,
        'transactions' : transactions ,

        'total_answers':total_answers,
        'true_answers':true_answers ,
        'percentage': percentage,

        'new_replys_count':new_replys_count,

    }

    if request.user.username == pk:
        return render(request, 'profile/main.html', context)
    else:
        if user_profile.instructor == True:
            return render(request, 'profile/main.html', context)
        else:
            return redirect('/profile/' + request.user.username)


# Wallet Start
@login_required(login_url='login')
def wallet_recharge(request , pk):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    profile_object = User.objects.get(username=pk)
    profile = Profile.objects.get(user=profile_object)

        
    return render(request, 'profile/wallet-recharge.html' , {'user_profile': user_profile ,'profile': profile, 'profile_object': profile_object, 'notifications' : notifications_count })



@login_required(login_url='login')
def wallet_subscriptions(request , pk):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    profile_object = User.objects.get(username=pk)
    profile = Profile.objects.get(user=profile_object)

    studentPurchases = BuyLesson.objects.filter(user=profile.user).order_by('-created_at')


    return render(request, 'profile/wallet-subscriptions.html' , {'user_profile': user_profile ,'profile': profile, 'profile_object': profile_object, 'notifications' : notifications_count , 'purchases' : studentPurchases })


@login_required(login_url='login')
def wallet_transactions(request , pk):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''


    profile_object = User.objects.get(username=pk)
    profile = Profile.objects.get(user=profile_object)

    transactions = Transaction.objects.filter(user=profile.user).order_by('-created_at')


    return render(request, 'profile/wallet-transactions.html' , {'user_profile': user_profile ,'profile': profile, 'profile_object': profile_object, 'notifications' : notifications_count  ,'transactions' : transactions})
# Wallet End


# Groups Start
@login_required(login_url='login')
def groups(request , pk):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    profile_object = User.objects.get(username=pk)
    profile = Profile.objects.get(user=profile_object)

    all_groups = Group.objects.all().order_by('-last_update')

    groups = []
    student_group_member_obects = GroupMember.objects.filter(user=profile_object).order_by('-created_at')
    # for x in student_group_member_obects:
    #     if Group.objects.filter(id=x.group_id).first():
    #         group = Group.objects.get(id=x.group_id)
    #         groups.append(group)

    for x in all_groups:
        if GroupMember.objects.filter(group_id=x.id , user=profile_object).first():
            student_group_member_object_for_updates = GroupMember.objects.get(group_id=x.id , user=profile_object)
            x.new_updates = int(student_group_member_object_for_updates.new_lectures) + int(student_group_member_object_for_updates.new_messages)
            x.save()
            groups.append(x)

    student_requests = GroupRequest.objects.filter(user=profile_object)

    groups_that_user_isnt_in = []
    for x in all_groups:
        if GroupRequest.objects.filter(user=profile_object , group_id=x.id).first():
            do_nothing = ''
        else:
            if GroupMember.objects.filter(user=profile_object , group_id=x.id).first():
                do_nothing23 = ''
            else:
                groups_that_user_isnt_in.append(x)


    if GroupRequest.objects.filter(user=profile_object).first():
        group_requests = GroupRequest.objects.filter(user=profile_object).order_by('-created_at')
    else:
        group_requests = []
        
        


    return render(request, 'profile/groups.html' , {'groups':groups , 'groups_that_user_isnt_in':groups_that_user_isnt_in ,'group_requests':group_requests , 'user_profile': user_profile ,'profile': profile, 'profile_object': profile_object, 'notifications' : notifications_count })


@login_required(login_url='login')
def group(request , pk , gr):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    profile_object = User.objects.get(username=pk)
    profile = Profile.objects.get(user=profile_object)

    if Group.objects.filter(id=gr).first():
        group = Group.objects.get(id=gr)

        group_lectures = GroupLecture.objects.filter(group_id=group.id).order_by('-created_at')
        if GroupMessage.objects.filter(group_id=group.id).first():
            group_messages = GroupMessage.objects.filter(group_id=group.id).order_by('-created_at')
            group_messages_number = group_messages.count()
        else:
            group_messages = ''
            group_messages_number = 0
        
        if GroupMember.objects.filter(user=profile_object , group_id=group.id).first():
            group_member_object = GroupMember.objects.get(user=profile_object , group_id=group.id)
        else:
            return redirect('/profile/' + str(profile_object.username) + '/groups')
        new_lectures = int(group_member_object.new_lectures)
        new_messages = int(group_member_object.new_messages)

        if new_messages == 0:
            old_messages_objects = group_messages
            new_messages_objects = []
        else:
            old_messages_objects = []
            new_messages_objects = []

            old_messages_number = group_messages_number - new_messages  
            loop_number = int(old_messages_number) + 1
            for x in group_messages[1:loop_number]:
                old_messages_objects.append(x)

            for x in group_messages:
                if x in old_messages_objects:
                    do_nothing = ''
                else:
                    new_messages_objects.append(x)



        page_type = request.GET.get('type')
        str_page_type = str(page_type)
        if str_page_type == 'lectures' :
            group_member_object.new_lectures = 0
            group_member_object.save()
        else:
            if str_page_type == 'messages' :
                group_member_object.new_messages = 0
                group_member_object.save()
            else:
                return redirect('/profile/' + str(profile_object.username) + '/groups')

    else:
        return redirect('/profile/' + str(profile_object.username) + '/groups')


    return render(request, 'profile/group.html' , {'group':group , 'lectures':group_lectures , 'lecture_messages':group_messages , 'new_lectures':new_lectures , 'new_messages':new_messages , 'page_type' :str_page_type ,'old_messages_objects':old_messages_objects , 'new_messages_objects': new_messages_objects , 'user_profile': user_profile ,'profile': profile, 'profile_object': profile_object, 'notifications' : notifications_count })


@login_required(login_url='login')
def group_join_link(request , group_link):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    profile_object = user_object
    profile = user_profile

    link = group_link

    invitation_type = request.GET.get('method')
    if str(invitation_type) == 'link':
        type = 'link'
    else:
        if str(invitation_type) == 'qr_code':
            type = 'qr_code'
        else:
            return redirect('/profile/' + str(profile_object.username) + '/groups')
        



    if Group.objects.filter(link=link).first():
        group = Group.objects.get(link=link)
        group_lectures = GroupLecture.objects.filter(group_id=group.id)

        if Group.objects.filter(link=link).first():
            if GroupMember.objects.filter(user=profile_object , group_id=group.id).first():
                messages.info(request, 'انت بالفعل داخل هذه المجموعة')
                return redirect('/profile/' + str(profile_object.username) + '/groups')
            else:

                page_type = request.GET.get('page')
                if str(page_type) == 'view':
                    return render(request, 'profile/group-join.html' , {'group':group ,'invitation_type':type , 'user_profile': user_profile ,'profile': profile, 'profile_object': profile_object, 'notifications' : notifications_count })
                else:
                    if str(page_type) == 'join':
                        new_member = GroupMember.objects.create(user=profile_object, user_name=profile_object.username , member_name=profile.name , group_id=group.id , group_title=group.title , image=profile.image ,method=type)
                        new_member.save()

                        group.no_of_students = group.no_of_students + 1
                        group.save()

                        for x in group_lectures:
                            if BuyLesson.objects.filter(user=profile_object , lecture_id=x.lecture_id).first():
                                nothing = 'Do Nothing'
                            else:
                                purchase_lecture_for_member = BuyLesson.objects.create(user=profile_object , user_name=profile.name ,user_image=profile.image , lecture_id=x.lecture_id , lecture_title=x.title , method='group' )
                                purchase_lecture_for_member.save()

                                lecture = Lecture.objects.get(id=x.lecture_id)
                                lecture.no_of_buys = lecture.no_of_buys + 1
                                lecture.save()

                                user_lecture_object = StudentLectureObject.objects.get(lecture_id=x.lecture_id , user=profile_object)
                                user_lecture_object.purchased = True
                                user_lecture_object.save()

                                lecture_instructor_profile = Profile.objects.get(user=lecture.user)
                                lecture_instructor_profile.no_of_sells = lecture_instructor_profile.no_of_sells + 1
                                lecture_instructor_profile.save()


                        redirction_link = group.id
                        messages.success(request, 'تم الانضمام للجروب بنجاح')
                        return redirect('/profile/' + str(profile_object.username) + '/group/' + str(redirction_link) + '?type=lectures')
            
                    else:
                        return redirect('/profile/' + str(profile_object.username) + '/groups')
        else:
            messages.warning(request, 'اللينك الذي ادخلته خطأ')
            return redirect('/profile/' + str(profile_object.username) + '/groups')
    else:
        messages.warning(request, 'اللينك الذي ادخلته خطأ')
        return redirect('/profile/' + str(profile_object.username) + '/groups')
# Groups End



# Accounts Start

@login_required(login_url='login')
def account(request , pk):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    profile_object = User.objects.get(username=pk)
    profile = Profile.objects.get(user=profile_object)


    if request.method == 'POST':
        
        if request.FILES.get('image') == None:
            image = profile.image
            email = request.POST['email']
            phone = request.POST['phone']
            year = request.POST['year']
            name = request.POST['name']
            location = request.POST['location']

            profile.image = image
            profile.user.email = email
            profile.phone = phone
            profile.year = year
            profile.name = name
            profile.location = location
            profile.save()

        


        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            email = request.POST['email']
            phone = request.POST['phone']
            year = request.POST['year']
            name = request.POST['name']
            location = request.POST['location']

            profile.image = image
            profile.user.email = email
            profile.phone = phone
            profile.year = year
            profile.name = name
            profile.location = location
            profile.save()


    return render(request, 'profile/account.html' , {'profile': profile, 'profile_object': profile_object , 'user_profile': user_profile , 'notifications' : notifications_count })


@login_required(login_url='login')
def connections(request , pk):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''
        
    profile_object = User.objects.get(username=pk)
    profile = Profile.objects.get(user=profile_object)


    if SocialLink.objects.filter(user=profile_object).first():
        social_links = SocialLink.objects.get(user=profile_object)
    else:
        social_links = ''


    
    if request.method == 'POST':
        student_username = request.POST['student_username']
        function = request.POST['function']
        social_link = request.POST['social_link']

        student_user = User.objects.get(username=student_username)


        if function == 'delete':
            student_social_links_object = SocialLink.objects.get(user=student_user)

            if social_link == 'facebook':
                student_social_links_object.facebook = ''
                student_social_links_object.save()

            if social_link == 'instagram':
                student_social_links_object.instagram = ''
                student_social_links_object.save()

            if social_link == 'whatsapp':
                student_social_links_object.whatsapp = ''
                student_social_links_object.save()

            messages.info(request, 'لقد تم مسح ربط الحساب بنجاح')
            return redirect('/profile/' + str(student_user.username) + '/account/connections')
    
        if function == 'add':
            if SocialLink.objects.filter(user=student_user).first():
                student_social_links_object = SocialLink.objects.get(user=student_user)

                if social_link == 'facebook':
                    facebook_link = request.POST['facebook_link']
                    student_social_links_object.facebook = facebook_link
                    student_social_links_object.save()

                if social_link == 'instagram':
                    instagram_link = request.POST['instagram_link']
                    student_social_links_object.instagram = instagram_link
                    student_social_links_object.save()

                if social_link == 'whatsapp':
                    whatsapp_link = request.POST['whatsapp_link']
                    student_social_links_object.whatsapp = whatsapp_link
                    student_social_links_object.save()

                messages.info(request, 'لقد تم ربط الحساب بنجاح')
                return redirect('/profile/' + str(student_user.username) + '/account/connections')
            else:
                student_social_links_object = SocialLink.objects.create(user=student_user , username=student_user.username)
                student_social_links_object.save()

                if social_link == 'facebook':
                    facebook_link = request.POST['facebook_link']
                    student_social_links_object.facebook = facebook_link
                    student_social_links_object.save()

                if social_link == 'instagram':
                    instagram_link = request.POST['facebook_link']
                    student_social_links_object.instagram = instagram_link
                    student_social_links_object.save()

                if social_link == 'whatsapp':
                    whatsapp_link = request.POST['whatsapp_link']
                    student_social_links_object.whatsapp = whatsapp_link
                    student_social_links_object.save()

                messages.info(request, 'لقد تم ربط الحساب بنجاح')
                return redirect('/profile/' + str(student_user.username) + '/account/connections')



    return render(request, 'profile/connections.html' , {'user_profile': user_profile ,'profile': profile, 'profile_object': profile_object, 'social_links':social_links , 'notifications' : notifications_count })


@login_required(login_url='login')
def login_history(request , pk):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    profile_object = User.objects.get(username=pk)
    profile = Profile.objects.get(user=profile_object)

    if LoginInfo.objects.filter(user=profile.user).first():
        logins = LoginInfo.objects.filter(user=profile.user).order_by('-time')
    else:
        logins = ''


    return render(request, 'profile/login-history.html' , {'logins':logins , 'user_profile': user_profile ,'profile': profile, 'profile_object': profile_object, 'notifications' : notifications_count })
# Accounts End







# Notifications And Inbox Start
@login_required(login_url='login')
def notifications(request , pk):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    profile_object = User.objects.get(username=pk)
    profile = Profile.objects.get(user=profile_object)

    notifications_objects = Notification.objects.filter(second_user=profile_object.username).order_by('-created_at')

    return render(request, 'profile/notifications.html' , {'notifications_objects':notifications_objects, 'user_profile': user_profile ,'profile': profile, 'profile_object': profile_object, 'notifications' : notifications_count })


# Notifications And Inbox Start
@login_required(login_url='login')
def delete_notification(request):
    if request.method == 'POST':
        notification_id = request.POST['notification-id']
        student_username = request.POST['student-username']

        if Notification.objects.filter(notification_id=notification_id).first():
            notification_object = Notification.objects.get(notification_id=notification_id)
            notification_object.delete()

            messages.success(request, 'تم مسح الاشعار بنجاح')
            return redirect("/profile/" + str(student_username) + '/notifications')

        else:
            return redirect("/profile/" + str(student_username) + '/notifications')

    else:
        return redirect("/profile/" + str(student_username) + '/notifications')
    

    



    
@login_required(login_url='login')
def inbox(request , pk):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    profile_object = User.objects.get(username=pk)
    profile = Profile.objects.get(user=profile_object)


    student_questions = StudentQuestion.objects.filter(user=profile_object).order_by('-created_at')

    new_replys_objects = []
    new_replys_count = 0
    if StudentQuestionAnswer.objects.filter(seen=False , answered_to_profile=profile).first():
        new_replys = StudentQuestionAnswer.objects.filter(seen=False , answered_to_profile=profile).order_by('-created_at')
        for x in new_replys:
            new_replys_objects.append(x)
            new_replys_count = new_replys_count + 1


    old_replys_objects = []
    if StudentQuestionAnswer.objects.filter(seen=True , answered_to_profile=profile).first():
        old_replys = StudentQuestionAnswer.objects.filter(seen=True , answered_to_profile=profile).order_by('-created_at')
        for x in old_replys:
            old_replys_objects.append(x)

    if user_profile == profile:
        if StudentQuestionAnswer.objects.filter(seen=False , answered_to_profile=profile).first():
            new_replys_for_function = StudentQuestionAnswer.objects.filter(seen=False , answered_to_profile=profile)
            for x in new_replys_for_function:
                x.seen = True
                x.save()


    if StudentQuestionAnswer.objects.filter(answered_to_profile=profile).first():
        replys_count = ''
    else:
        replys_count = 0

    return render(request, 'profile/inbox.html' , {'new_replys':new_replys_objects , 'old_replys':old_replys_objects ,'replys_count':replys_count , 'new_replys_count':new_replys_count ,'student_questions':student_questions, 'user_profile': user_profile ,'profile': profile, 'profile_object': profile_object, 'notifications' : notifications_count })
# Notifications And Inbox End





# Student Section Start
@login_required(login_url='login')
def lectures(request , pk):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    profile_object = User.objects.get(username=pk)
    profile = Profile.objects.get(user=profile_object)

    if StudentLectureObject.objects.filter(user=profile.user).first():
        lectures = StudentLectureObject.objects.filter(user=profile.user , purchased=True).order_by('-created_at')
    else:
        lectures = ''

    return render(request, 'profile/lectures.html' , {'lectures':lectures ,'user_profile': user_profile ,'profile': profile, 'profile_object': profile_object, 'notifications' : notifications_count })

@login_required(login_url='login')
def homeworks(request , pk):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    profile_object = User.objects.get(username=pk)
    profile = Profile.objects.get(user=profile_object)

    homeworks = AssignmentSubmit.objects.filter(user=profile_object , assignment_type='homework')


    return render(request, 'profile/homeworks.html' , {'homeworks':homeworks , 'user_profile': user_profile ,'profile': profile, 'profile_object': profile_object, 'notifications' : notifications_count })

@login_required(login_url='login')
def exams(request , pk):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    profile_object = User.objects.get(username=pk)
    profile = Profile.objects.get(user=profile_object)

    exams = AssignmentSubmit.objects.filter(user=profile_object , assignment_type='test')

    return render(request, 'profile/exams.html' , {'exams':exams ,'user_profile': user_profile ,'profile': profile, 'profile_object': profile_object, 'notifications' : notifications_count })

@login_required(login_url='login')
def statistics(request , pk):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    profile_object = User.objects.get(username=pk)
    profile = Profile.objects.get(user=profile_object)

    tests_total_answers = 0
    tests_true_answers = 0
    tests_percentage = 0

    if AssignmentSubmit.objects.filter(user=profile_object , assignment_type='test').first():
        student_submit_objects = AssignmentSubmit.objects.filter(user=profile_object , assignment_type='test')
        for x in student_submit_objects:
            tests_true_answers = tests_true_answers + x.true_answers
            student_answers = Answer.objects.filter(user=profile_object , assignment_id=x.assignment_id)
            for z in student_answers:
                tests_total_answers = tests_total_answers + 1
        tests_percentage = round(tests_true_answers / tests_total_answers * 100)
    tests = {'tests_total_answers':tests_total_answers , 'tests_true_answers':tests_true_answers , 'tests_percentage':tests_percentage}


    homeworks_total_answers = 0
    homeworks_true_answers = 0
    homeworks_percentage = 0

    if AssignmentSubmit.objects.filter(user=profile_object , assignment_type='homework').first():
        student_submit_objects = AssignmentSubmit.objects.filter(user=profile_object , assignment_type='homework')
        for x in student_submit_objects:
            homeworks_true_answers = homeworks_true_answers + x.true_answers
            student_answers = Answer.objects.filter(user=profile_object , assignment_id=x.assignment_id)
            for z in student_answers:
                homeworks_total_answers = homeworks_total_answers + 1
        homeworks_percentage = round(homeworks_true_answers / homeworks_total_answers * 100)
    homeworks = {'homeworks_total_answers':homeworks_total_answers , 'homeworks_true_answers':homeworks_true_answers , 'homeworks_percentage':homeworks_percentage}

    return render(request, 'profile/statistics.html' , {'tests':tests, 'homeworks':homeworks , 'user_profile': user_profile ,'profile': profile, 'profile_object': profile_object, 'notifications' : notifications_count })
# Student Section End




# Functions 
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
        destination = request.POST['destination']

        student_username = request.POST['student_username']
        student_user = User.objects.get(username=student_username)
        student_profile = Profile.objects.get(user=student_user)


        if Code.objects.filter(code_id=code).first():
            valid_code = Code.objects.get(code_id=code)
            valid_code_money = valid_code.money
            student_profile .money = student_profile .money + valid_code_money



            student_profile .save()
            student_profile .save()
            text = 'yes'


            valid_code.active = False
            valid_code.student = student_user.username
            valid_code.save()

            invoice = Transaction.objects.create(user=student_user , user_name=student_user.username , value=valid_code_money , wallet=user_profile.money , transaction_type='charge' , purchase_type='code' )
            invoice.save()

            if user_profile.instructor == True:
                 messages.info(request, 'تم شحن مبلغ ' + str(valid_code.money) + ' جنية في محقظة ' + student_user.username)
            else:
                messages.info(request, 'تم شحن مبلغ ' + str(valid_code.money) + ' جنية في محفظنك بنجاح')
               


            if destination == 'profile-recharge-page':
                return redirect('/profile/' + str(student_user.username) + '/wallet/recharge')
            
            if destination == 'profile-main-page':
                return redirect('/profile/' + str(student_user.username))

        else:
            messages.info(request, 'الكود الذي ادخلته غير صالح او مستخدم من قبل')
            if destination == 'profile-recharge-page':
                return redirect('/profile/' + str(student_user.username) + '/wallet/recharge')
            
            if destination == 'profile-main-page':
                return redirect('/profile/' + str(student_user.username))



@login_required(login_url='register')
def vodaphone_charge_function(request):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    if request.method == 'POST':
        student_username = request.POST['student_username']

        student_user = User.objects.get(username=student_username)
        student_profile = Profile.objects.get(user=student_user)

    messages.info(request, 'الخدمة غير متاحة الان')
    return redirect('/profile/' + str(student_user.username) + '/wallet/recharge')


# Student Questions 

@login_required(login_url='register')
def questions_functions(request):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    if request.method == 'POST':
        function_type = request.POST['function-type']

        if str(function_type) == 'send-question':
            question = request.POST['question']
            destination = request.POST['destination']

            student_username = request.POST['student-username']
            student_user = User.objects.get(username=student_username)
            student_profile = Profile.objects.get(user=student_user)

            if str(destination) == 'lecture':
                lecture_id = request.POST['lecture-id']
                create_question = StudentQuestion.objects.create(lecture_id=lecture_id , user=student_user , user_name=student_profile.name , user_image=student_profile.image ,question=question)
                messages.success(request, 'تم ارسال سؤالك بنجاح')
                return redirect("/lecture/" + str(lecture_id))


            if str(destination) == 'inbox':
                create_question = StudentQuestion.objects.create(user=student_user , user_name=student_profile.name , user_image=student_profile.image ,question=question)
                messages.success(request, 'تم ارسال سؤالك بنجاح')
                return redirect("/profile/" + student_user.username + '/inbox')
            
        if str(function_type) == 'delete-question':
            question_id = request.POST['question-id']
            
            
            if StudentQuestion.objects.filter(question_id=question_id).first():
                question = StudentQuestion.objects.get(question_id=question_id)
                if user_profile.instructor == True:
                    question.delete()
                    messages.success(request, 'تم مسح السؤال بنجاح')
                    return redirect("/dashboard/questions")
                else:
                    if user_object == question.user:
                        question.delete()
                        messages.success(request, 'تم مسح السؤال بنجاح')
                        return redirect("/profile/" + question.user.username + '/inbox')
                    else:
                        return redirect("/")
            


        if str(function_type) == 'send-reply':
            question_id = request.POST['question-id']
            reply = request.POST['reply']
            
            if user_profile.instructor == True:
                if StudentQuestion.objects.filter(question_id=question_id).first():
                    question = StudentQuestion.objects.get(question_id=question_id)
                    student_user = User.objects.get(username=question.user.username)
                    student_profile = Profile.objects.get(user=student_user)

                    create_reply = StudentQuestionAnswer.objects.create(question_id=question.question_id , user=request.user , user_name=user_profile.name , answered_to_profile=student_profile , question_text = question.question , answer=reply)
                    create_reply.save()

                    question.replyed = True
                    question.no_of_answers = question.no_of_answers + 1
                    question.save()

                    make_notification = Notification.objects.create(user=request.user , user_name= user_profile.name , notification_type='reply' , second_user=student_user.username)
                    make_notification.save()
                    
                    messages.success(request, 'تم الرد علي السؤال بنجاح ')
                    return redirect("/dashboard/questions")
            else:
                return redirect("/")
            



# Student Questions 
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import random
from django.shortcuts import get_object_or_404
from main.models import *


from main.views import instructor_username as instructor_username_k
# necessary imports
import secrets
import string


# Variables 
instructor_username = instructor_username_k
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

# Variables 


# Views 
@login_required(login_url='login')
def lecture_assignment(request , id , assignment):
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

    videos_count = Part.objects.filter(lecture_id=lecture.id , type='video').count()
    assignments_count = Part.objects.filter(lecture_id=lecture.id , type='assignment').count() 
    total_questions_number = 0
    links_count = Part.objects.filter(lecture_id=lecture.id , type='link').count()
    files_count = Part.objects.filter(lecture_id=lecture.id , type='file').count()
    attachments_count = int(links_count) + int(files_count)

    students = BuyLesson.objects.filter(lecture_id=id)

    related_assignments = Assignment.objects.filter(lecture_id=lecture.id)
    for x in related_assignments:
        total_questions_number = total_questions_number + x.questions_count







    if Part.objects.filter(part_id=assignment).first():
        part = Part.objects.get(part_id=assignment)
        assignment = Assignment.objects.get(assignment_id=part.assignment_id)
        mode = 'assignment'
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


    all_lectures = Lecture.objects.all()
    another_lectures = []
    for x in all_lectures:
        if x.id == lecture.id:
            do_nothing_4 = ''
        else:
            another_lectures.append(x)
            if str(x.id) == str(assignment.award_lecture_id):
                x.activated = True
                x.save()
            else:
                x.activated = False
                x.save()



    assignment_opened_context = ''
    student_submit_assignment = ''

    bar_color = ''

    view_answers = False
    student_answer_for_review = ''
    student_answers_for_review = ''

    questions_for_instructor =''
    applicants = ''
    assignments_discounts = ''
    rewarded_students_percentage = ''

    if User.objects.filter(username=request.user.username).first():
        if user_profile.instructor == True:
            do_nothing = ''
            assignment_status = 'instructor'
            questions_for_instructor = Question.objects.filter(assignment_id=assignment.assignment_id)
            applicants = AssignmentSubmit.objects.filter(assignment_id=assignment.assignment_id)

            assignments_discounts = LectureDiscount.objects.filter(type='assignment_reward' , assignment_id=assignment.assignment_id)
            if assignments_discounts.count() == 0:
                rewarded_students_percentage = 0
            else:
                if applicants.count() == 0:
                    rewarded_students_percentage = 0
                else:
                    rewarded_students_percentage = round(int(assignments_discounts.count()) / int(applicants.count()) * 100)

        else:
            if AssignmentOpen.objects.filter(user=request.user ,assignment_id=assignment.assignment_id).first():
                if AssignmentSubmit.objects.filter(user=request.user ,assignment_id=assignment.assignment_id).first():
                    assignment_status = 'submitted'



                    student_submit_assignment = AssignmentSubmit.objects.get(user=request.user ,assignment_id=assignment.assignment_id)
                    

                    percentage = int(student_submit_assignment.true_answers_percent)
                    if percentage >= 50:
                        bar_color = '#71dd37'
                    else:
                        bar_color = '#ff3e1d'



                    view_answers_request = request.GET.get('view-answers')
                    if str(view_answers_request) == 'true':
                        student_submit_serial = request.GET.get('serial')
                        if student_submit_assignment.serial == student_submit_serial:
                            if len(str(request.GET.get('question'))) != 0:
                                question_id_for_review = request.GET.get('question')
                                if Answer.objects.filter(question_id=question_id_for_review , user=request.user).first():
                                    student_answer_for_review = Answer.objects.get(question_id=question_id_for_review , user=request.user)
                                    view_answers = True
                                    student_answers_for_review = Answer.objects.filter(assignment_id=assignment.assignment_id , user=request.user)
                                else:
                                    first_question = Question.objects.get(assignment_id=assignment.assignment_id , question_number=1)
                                    student_answer_for_review = Answer.objects.get(question_id=first_question.question_id , user=request.user)
                                    view_answers = True
                                    student_answers_for_review = Answer.objects.filter(assignment_id=assignment.assignment_id , user=request.user)
                                    return redirect('/lecture/' + str(lecture.id) + '/assignment/' + str(part.part_id) + '?view-answers=true&serial=' + student_submit_serial + '&question=' + str(first_question.question_id) + '#reviewAnswers')
                            else:
                                first_question = Question.objects.get(assignment_id=assignment.assignment_id , question_number=1)
                                student_answer_for_review = Answer.objects.get(question_id=first_question.question_id , user=request.user)
                                view_answers = True
                                student_answers_for_review = Answer.objects.filter(assignment_id=assignment.assignment_id , user=request.user)

                                return redirect('/lecture/' + str(lecture.id) + '/assignment/' + str(part.part_id) + '?view-answers=true&serial=' + student_submit_serial + '&question=' + str(first_question.question_id) + '#reviewAnswers')
                else:
                    assignment_status = 'opened'

                    question_id = request.GET.get('q')

                    if Question.objects.filter(question_id=question_id).first():
                        question = Answer.objects.get(question_id=question_id , user=request.user)
                    else:
                        if Question.objects.filter(assignment_id=assignment.assignment_id).first():
                            first_question = Question.objects.get(assignment_id=assignment.assignment_id , question_number=1)
                            return redirect('/lecture/' + str(lecture.id) + '/assignment/' + str(part.part_id) + '?q=' + str(first_question.question_id))
                        else:
                            return redirect('/lecture/' + str(lecture.id) )


                    questions = Answer.objects.filter(assignment_id=assignment.assignment_id , user=request.user)

                    answered_questions_number = Answer.objects.filter(assignment_id=assignment.assignment_id , user=request.user , answered=True).count()
                    student_assignment_open_object =AssignmentOpen.objects.get(assignment_id=assignment.assignment_id , user=request.user)

                    assignment_duration_by_secs = student_assignment_open_object.remain_secs



                    
                    if Question.objects.filter(question_id=question_id , question_number=1).first():
                        previous = False
                        next = True
                        btn_mode = 'first'
                    else:
                        if Question.objects.filter(question_id=question_id , question_number=assignment.questions_count).first():
                            previous = True
                            next = False
                            btn_mode = 'last'
                        else:
                            btn_mode = 'normal'



                    assignment_opened_context = {'question':question , 'answered_questions_number' : answered_questions_number , 'assignment_duration_by_secs':assignment_duration_by_secs , 'btn_mode':btn_mode , 'student_answers':questions}
            else:
                assignment_status = 'not-started'




    return render(request, 'lectures/lecture.html' , { 'part':part , 'assignment':assignment, 'assignment_status':assignment_status , 'student_submit_assignment':student_submit_assignment ,'applicants':applicants ,    'mode':mode , 'status':status , 'lecture':lecture , 'parts':parts, 'videos_count' : videos_count, 'attachments_count' : attachments_count , 'assignments_count':assignments_count ,'students':students , 'total_questions_number':total_questions_number , 'assignment_opened_context':assignment_opened_context , 'view_answers':view_answers , 'student_answer_for_review':student_answer_for_review , 'student_answers_for_review':student_answers_for_review, 'bar_color':bar_color,'questions_for_instructor':questions_for_instructor, 'another_lectures':another_lectures,'assignments_discounts':assignments_discounts,'rewarded_students_percentage':rewarded_students_percentage, 'user_profile': user_profile , 'notifications' : notifications_count ,  'platform':platform} ,)








# Functions 
@login_required(login_url='register')
def create_assignment(request):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    if request.method == 'POST':
        assignment_name = request.POST['title']
        assignment_time = request.POST['time']
        assignment_type = request.POST['type']
        assignment_lecture_id = request.POST['lecture-id']

        lecture = Lecture.objects.get(id=assignment_lecture_id)



        # Create Assignment Part Objects 

        new_assignment= Assignment.objects.create(lecture_id=assignment_lecture_id , user=request.user , user_name=user_profile.name , assignment_name=assignment_name , assignment_type=assignment_type , minutes=assignment_time)
        new_assignment.save()

        lecture_parts_number = lecture.parts_number
        part_number = lecture_parts_number + 1


        new_part = Part.objects.create(lecture_id=assignment_lecture_id , assignment_id=new_assignment.assignment_id , user=request.user , user_name=request.user.username , type='assignment'  , title=assignment_name , part_number=part_number , visible=True , original=True)
        new_part.save()
        lecture.parts_number = lecture.parts_number + 1
        lecture.save()


        new_assignment.part_id = new_part.part_id
        new_assignment.save()


        # Create Part Object For Each User In The Platform And Edit Lecture Object
        students = Profile.objects.all()
        for x in students:
            student_user = User.objects.get(username=x.username)
            create_part_object = StudentPartObject.objects.create(part_id=new_part.part_id , lecture_id=new_part.lecture_id , assignment_id=new_assignment.assignment_id , user=student_user , user_name=student_user.username , type='assignment'  , title=new_part.title , part_number=new_part.part_number , visible=new_part.visible)
            create_part_object.save()

            student_lecture_object = StudentLectureObject.objects.get(user=student_user , lecture_id=new_part.lecture_id)
            student_lecture_object.parts_number = student_lecture_object.parts_number + 1
            student_lecture_object.save()
        # Create Part Object For Each User In The Platform And Edit Lecture Object


        # Create Assignment Part Objects 
        

        return redirect('/lecture/' + str(Lecture.objects.get(id=assignment_lecture_id).id) + '/assignment/' + str(new_part.part_id) )



@login_required(login_url='register')
def assignment_functions(request):
    if User.objects.filter(username=request.user.username).first():
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        notifications_count = Notification.objects.filter(user=request.user).count()
    else:
        user_profile = ''
        notifications_count = ''

    if request.method == 'POST':
        function_type = request.POST['function-type']

        assignment_id = request.POST['assignment-id']
        lecture_id = request.POST['lecture-id']
        part_id = request.POST['part-id']



        if Assignment.objects.filter(assignment_id=assignment_id).first():
            assignment = Assignment.objects.get(assignment_id=assignment_id)
            assignment_questions = Question.objects.filter(assignment_id=assignment.assignment_id)
            # assignment_part =
        else:
            return redirect('/lectures')

        if Lecture.objects.filter(id=lecture_id).first():
            lecture = Lecture.objects.get(id=lecture_id)
        else:
            return redirect('/lectures')
        

        if str(function_type) == 'start-assignment':

            if AssignmentOpen.objects.filter(user=request.user , assignment_id=assignment_id).first():
                return redirect('/lecture/' + lecture_id + '/assignment/' + part_id)
            else:
                remain_seconds = int(assignment.minutes) * 60
                new_assignment_start = AssignmentOpen.objects.create(remain_secs=remain_seconds ,  user=request.user , user_name=user_profile.name, assignment_id=assignment_id , assignment_name=assignment.assignment_name , questions_count=assignment_questions.count() )
                new_assignment_start.save()

                assignment_opens = AssignmentOpen.objects.filter(assignment_id=assignment_id)
                assignment.no_of_applicants = int(assignment_opens.count())
                assignment.save()


                for x in assignment_questions:
                    create_answer = Answer.objects.create(assignment_id=assignment.assignment_id ,assignment_name=assignment.assignment_name , question_id=x.question_id ,question_number=x.question_number ,user=request.user ,user_name=user_profile.name ,question=x.question ,question_image=x.question_image ,question_true=x.true ,  answer1=x.answer1 , answer2=x.answer2 , answer3=x.answer3 , answer4=x.answer4 )
                    create_answer.save()

                return redirect('/lecture/' + lecture_id + '/assignment/' + part_id)

                
        
        if str(function_type) == 'assignment-settings' :
            title = request.POST.get('title')
            duration = request.POST.get('duration')
            visible = request.POST.get('visible')
            assignment_type = request.POST.get('type')

            if visible == 'on':
                visible_value = True
            else:
                visible_value = False

            part = Part.objects.get(part_id=part_id)
            lecture_parts = Part.objects.filter(lecture_id=lecture.id)

            part.title = title
            part.visible = visible_value
            part.save()

            assignment.assignment_name = title
            assignment.minutes = duration
            assignment.assignment_type=assignment_type
            assignment.save()







            related_parts_objects = StudentPartObject.objects.filter(part_id=part.part_id)
            for x in related_parts_objects:
                x.title = part.title
                x.visible = part.visible
                x.save()


            messages.success(request, 'تم تعديل التكليف بنجاح')
            return redirect('/lecture/' + str(lecture.id) + '/' + str(part.type) + "/" + str(part.part_id))
        
        
        if str(function_type) == 'delete-assignment' :
            confirmation = request.POST.get('confirmation')


            if confirmation == 'on':
                assignment_part = Part.objects.get(part_id=part_id)


                lecture.parts_number = lecture.parts_number - 1
                lecture.save()


                # Create Part Object For Each User In The Platform And Edit Lecture Object
                students = Profile.objects.all()
                for x in students:
                    student_user = User.objects.get(username=x.username)

                    student_lecture_object = StudentLectureObject.objects.get(user=student_user , lecture_id=assignment_part.lecture_id)
                    student_lecture_object.parts_number = student_lecture_object.parts_number - 1
                    student_lecture_object.save()
                # Create Part Object For Each User In The Platform And Edit Lecture Object



                assignment_part.delete()
                students_part_objects = StudentPartObject.objects.filter(assignment_id=assignment_id).delete()

                assignment_opens = AssignmentOpen.objects.filter(assignment_id=assignment.assignment_id).delete()
                assignment_submits = AssignmentSubmit.objects.filter(assignment_id=assignment.assignment_id).delete()
                assignment_questions = Question.objects.filter(assignment_id=assignment.assignment_id).delete()
                assignment_answers = Answer.objects.filter(assignment_id=assignment.assignment_id).delete()


                assignment.delete()
                

                return redirect('/lecture/' + str(lecture_id) )
            else:
                return redirect('/lecture/' + str(lecture_id) + '/assignment/' + str(part_id))

        if str(function_type) == 'add-question':

            if user_profile.instructor == True:

                question_number = assignment.questions_count + 1

                if len(str(request.POST.get('q_a1'))) != 0:
                    question_type = 'q_choices'
                    question = request.POST.get('question')

                if len(str(request.POST.get('question-writing'))) != 0:
                    question_type = 'writing'
                    question = request.POST.get('question-writing')



                if str(question_type) == 'q_choices':
                    question_true = request.POST.get('true')
                    question_answer1 = request.POST.get('q_a1')
                    question_answer2 = request.POST.get('q_a2')
                    question_answer3 = request.POST.get('q_a3')
                    question_answer4 = request.POST.get('q_a4')
                else:
                    if str(question_type) == 'writing':
                        question_true = ''
                        question_answer1 = ''
                        question_answer2 = ''
                        question_answer3 = ''
                        question_answer4 = ''



                if len(request.FILES) != 0:
                    question_image = request.FILES['question-image-upload']
                else:
                    question_image = ''
                



                new_question = Question.objects.create(assignment_id=assignment.assignment_id ,assignment_name=assignment.assignment_name , user=request.user, user_name=request.user.username , question_number=question_number , question_type=question_type , question=question ,question_image=question_image, true=question_true , answer1=question_answer1 , answer2=question_answer2 , answer3=question_answer3 , answer4=question_answer4)
                new_question.save()


                assignment.questions_count = Question.objects.filter(assignment_id=assignment.assignment_id).count()
                assignment.save()

                part_object = Part.objects.get(lecture_id=lecture_id , assignment_id=assignment.assignment_id)
                student_part_objects = StudentPartObject.objects.filter(lecture_id=lecture_id , assignment_id=assignment.assignment_id)


                part_object.assignment_questions_number = part_object.assignment_questions_number + 1
                part_object.save()

                for x in student_part_objects:
                    x.assignment_questions_number = x.assignment_questions_number + 1
                    x.save()
                
                messages.info(request, 'تم حفظ السؤال بنجاح')
                return redirect('/lecture/' + str(lecture.id) + '/assignment/' + str(part_id))
            else:
                return redirect('/' )

        if str(function_type) == 'delete-question':

            if user_profile.instructor == True:

                question_id = request.POST.get('question-id')


                assignment.questions_count = assignment.questions_count - 1
                assignment.save()


                part_object = Part.objects.get(lecture_id=lecture_id , assignment_id=assignment.assignment_id)
                student_part_objects = StudentPartObject.objects.filter(lecture_id=lecture_id , assignment_id=assignment.assignment_id)


                part_object.assignment_questions_number = part_object.assignment_questions_number - 1
                part_object.save()

                for x in student_part_objects:
                    x.assignment_questions_number = x.assignment_questions_number - 1
                    x.save()

                question = Question.objects.get(question_id=question_id)
                question.delete()



                
                messages.info(request, 'تم مسح السؤال بنجاح')
                return redirect('/lecture/' + str(lecture.id) + '/assignment/' + str(part_id))
            else:
                return redirect('/' )
            

        if str(function_type) == 'edit-question':

            if user_profile.instructor == True:

                question_id = request.POST.get('question-id')
                question_type = request.POST.get('question-type')
                print(question_type)

                question = request.POST.get('question')


                if str(question_type) == 'q_choices':
                    question_true = request.POST.get('true')
                    question_answer1 = request.POST.get('q_a1')
                    question_answer2 = request.POST.get('q_a2')
                    question_answer3 = request.POST.get('q_a3')
                    question_answer4 = request.POST.get('q_a4')
                else:
                    if str(question_type) == 'writing':
                        question_true = ''
                        question_answer1 = ''
                        question_answer2 = ''
                        question_answer3 = ''
                        question_answer4 = ''

                question_item = Question.objects.get(question_id=question_id)

                
                question_item.question = question
                question_item.true = question_true
                question_item.answer1 = question_answer1
                question_item.answer2 = question_answer2
                question_item.answer3 = question_answer3
                question_item.answer4 = question_answer4


                if len(request.FILES) != 0:
                    question_image = request.FILES['question-image-upload']
                    question_item.question_image = question_image

                question_item.save()

                




               
                messages.info(request, 'تم تعديل السؤال بنجاح')
                return redirect('/lecture/' + str(lecture.id) + '/assignment/' + str(part_id))
            else:
                return redirect('/' )

        if str(function_type) == 'save-answer':


            question_id = request.POST['question-id']
            question_type = request.POST['question-type']

            destination = request.POST['destination']

            remainingTime = request.POST['remainingTime']

            student_assignment_open_object = AssignmentOpen.objects.get(user=request.user , assignment_id=assignment.assignment_id)
            student_assignment_open_object.remain_secs = float(remainingTime) 
            student_assignment_open_object.save()

            question = Question.objects.get(question_id=question_id)
            student_answer = Answer.objects.get(question_id=question_id , user=request.user)

            if str(question_type) == 'q_choices':
                student_answer_input = request.POST['answer']

                student_answer.answer = student_answer_input

                if student_answer.question_true == student_answer_input:
                    student_answer.true = True
                else:
                    student_answer.true = False


            else:
                if str(question_type) == 'writing':
                    student_writing_answer_input = request.POST['writing-answer']

                    student_answer.writing_answer = student_writing_answer_input




            student_answer.answered = True
            student_answer.save()

            if str(destination) == 'next':
                current_question_no = question.question_number
                destination_question = Question.objects.get(assignment_id=assignment.assignment_id , question_number=int(current_question_no + 1)) 
                return redirect('/lecture/' + str(lecture.id) + '/assignment/' + str(part_id) + '?q=' + str(destination_question.question_id) + '#questionsSection')
            else:

                if str(destination) == 'previous':
                    current_question_no = question.question_number
                    destination_question = Question.objects.get(assignment_id=assignment.assignment_id , question_number=int(current_question_no - 1)) 
                    return redirect('/lecture/' + str(lecture.id) + '/assignment/' + str(part_id) + '?q=' + str(destination_question.question_id) + '#questionsSection')
                else:

                    if str(destination) == 'submit':
                        assignment_questions_count = assignment.questions_count



                        student_true_answers_count = Answer.objects.filter(true=True , assignment_id=assignment.assignment_id , user=request.user).count()
                        student_false_answers_count = Answer.objects.filter(true=False , assignment_id=assignment.assignment_id , user=request.user).count()

                        true_answers_percent = round(int(student_true_answers_count) / int(assignment.questions_count) * 100)

                        if AssignmentSubmit.objects.filter(assignment_id=assignment_id , user=request.user).first():
                            return redirect('/lecture/' + str(lecture.id) + '/assignment/' + str(part_id) )
                        else:
                            assignment_duration = int(assignment.minutes) - ( int(remainingTime) / 60)
                            assignment_duration_rounded = round(assignment_duration , 2)


                            # Serial Generation 

                            digits = string.digits
                            alphabet = digits
                            pwd_length = 7
                            pwd = ''
                            for i in range(pwd_length):
                                pwd += ''.join(secrets.choice(alphabet))

                            if AssignmentSubmit.objects.filter(serial=pwd).first():
                                redo_serial = ''
                                for i in range(pwd_length):
                                    pwd += ''.join(secrets.choice(alphabet))
                            # Serial Generation 

                            student_assignment_open_object = AssignmentOpen.objects.get(user=request.user , assignment_id=assignment.assignment_id)
                            submit_assignment = AssignmentSubmit.objects.create(user=request.user , user_name=user_profile.name, assignment_id=assignment.assignment_id  , assignment_name=assignment.assignment_name , questions_count=assignment_questions_count , true_answers=student_true_answers_count , false_answers=student_false_answers_count , opened_at=student_assignment_open_object.start_at , assignment_duration=assignment_duration_rounded , true_answers_percent=true_answers_percent , serial=pwd , assignment_type=assignment.assignment_type , lecture_id=lecture.id , part_id=part_id)
                            submit_assignment.save()

                            assignment.no_of_applicants = assignment.no_of_applicants + 1
                            assignment.save()

                            # Update User Part 
                            student_assignment_part_object = StudentPartObject.objects.get(assignment_id=assignment.assignment_id , user=request.user)
                            student_assignment_part_object.assignment_user_percentage = int(true_answers_percent)
                            student_assignment_part_object.save()
                            # Update User Part

                            
                            # Award System 
                            if assignment.award_system == True:
                                if int(true_answers_percent) >= int(assignment.award_percentage_needed):
                                    if Lecture.objects.filter(id=assignment.award_lecture_id).first():
                                        award_lecture = Lecture.objects.get(id=assignment.award_lecture_id)
                                        submit_assignment.award_lecture_name = award_lecture.title
                                        submit_assignment.award_discount_value = assignment.award_discount_value
                                        submit_assignment.award_lecture_id = assignment.award_lecture_id


                                        # Code Generation 
                                        letters_for_discount = string.ascii_letters
                                        alphabet_for_discount = letters_for_discount + digits
                                        pwd_length_for_discount = 8
                                        pwd_for_discount = ''
                                        for i in range(pwd_length_for_discount):
                                            pwd_for_discount += ''.join(secrets.choice(alphabet_for_discount))
                                        # Code Generation 

                                        create_discount = LectureDiscount.objects.create(discount_id=pwd_for_discount , lecture_id=assignment.award_lecture_id , user=assignment.user , total_students_number=1 , discount_value=assignment.award_discount_value ,type='assignment_reward' , assignment_id=assignment.assignment_id , awarded_username=request.user.username )
                                        create_discount.save()

                                        submit_assignment.award_discount = create_discount.discount_id
                                        submit_assignment.save()
                            # Award System 



                            return redirect('/lecture/' + str(lecture.id) + '/assignment/' + str(part_id) )
                        
                    else:

                        if Question.objects.filter(question_id=destination).first():
                            destination_question = Question.objects.get(assignment_id=assignment.assignment_id ,question_id=destination ) 
                            return redirect('/lecture/' + str(lecture.id) + '/assignment/' + str(part_id) + '?q=' + str(destination_question.question_id) + '#questionsSection')

        if str(function_type) == 'delete-trial':

            if user_profile.instructor == True:

                trial_serial = request.POST.get('serial')

                assignment_submit_object = AssignmentSubmit.objects.get(serial=trial_serial)
                assignment_open_object = AssignmentOpen.objects.get(user=assignment_submit_object.user)
                assignment_answers = Answer.objects.filter(assignment_id=assignment_submit_object.assignment_id , user=assignment_submit_object.user)

                assignment_submit_object.delete()
                assignment_open_object.delete()
                assignment_answers.delete()

                assignment.no_of_applicants =  assignment.no_of_applicants - 1
                assignment.save()

                part = Part.objects.get(part_id=part_id)
                part.assignment_total_applicants = assignment.no_of_applicants
                part.save()

                student_parts_objects = StudentPartObject.objects.filter(part_id=part.part_id)
                for x in student_parts_objects:
                    x.assignment_total_applicants = assignment.no_of_applicants
                    x.save()

                return redirect('/lecture/' + str(lecture.id) + '/assignment/' + str(part_id))
            else:
                return redirect('/' )
            



        if str(function_type) == 'reward-system' :
            percentage = request.POST.get('percentage')
            discount = request.POST.get('discount')
            award_lecture_id = request.POST.get('award_lecture_id')
            award_system = request.POST.get('award_system')

            if award_system == 'on':
                award_system_value = True
            else:
                award_system_value = False

            part = Part.objects.get(part_id=part_id)



            assignment.award_system = award_system_value
            assignment.award_discount_value = discount
            assignment.award_percentage_needed=percentage
            assignment.award_lecture_id=award_lecture_id
            assignment.save()






            messages.success(request, 'تم تعديل التكليف بنجاح')
            return redirect('/lecture/' + str(lecture.id) + '/' + str(part.type) + "/" + str(part.part_id))
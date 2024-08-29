from django.contrib import admin
from .models import PlatformSettings , Profile , Lecture , StudentLectureObject , LectureCode ,  Part , StudentPartObject , View
from .models import Chapter , ChapterLecture , Group , GroupMember , GroupLecture ,GroupMessage ,GroupRequest, BuyLesson , BuyChapter
from .models import Code , Notification , Transaction , LikeLecture , StudentQuestion ,  StudentQuestionAnswer 
from .models import Assignment , AssignmentOpen  , AssignmentSubmit ,Question , Answer ,   News ,GetPremium ,RechargeRequest , LoginInfo        
from .models import Theme , SocialLink       



class MainAdmin(admin.ModelAdmin):
    list_display =  ['user' ,'phone' , 'year' , 'premium' , 'instructor' , 'admin' , 'public', 'money' , 'no_of_buys']
    list_editable = ['year' , 'premium' , 'instructor' , 'admin' ,'public', 'money' , 'no_of_buys']



admin.site.register(Profile , MainAdmin)
admin.site.register(PlatformSettings)
admin.site.register(Lecture)
admin.site.register(StudentLectureObject)
admin.site.register(LectureCode)
admin.site.register(Part)
admin.site.register(StudentPartObject)
admin.site.register(View)

admin.site.register(Chapter)
admin.site.register(ChapterLecture)

admin.site.register(Group)
admin.site.register(GroupMember)
admin.site.register(GroupLecture)
admin.site.register(GroupMessage)
admin.site.register(GroupRequest)

admin.site.register(BuyLesson)
admin.site.register(BuyChapter)


admin.site.register(Code)
admin.site.register(Notification)
admin.site.register(Transaction)

admin.site.register(LikeLecture)
admin.site.register(StudentQuestion)
admin.site.register(StudentQuestionAnswer)


admin.site.register(LoginInfo)
admin.site.register(Theme)
admin.site.register(SocialLink)
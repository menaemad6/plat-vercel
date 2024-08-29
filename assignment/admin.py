from django.contrib import admin


from main.models import *

# Register your models here.


admin.site.register(Assignment)
admin.site.register(AssignmentOpen)
admin.site.register(AssignmentSubmit)
admin.site.register(Question)
admin.site.register(Answer)


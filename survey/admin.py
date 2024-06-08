from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Question, Ec, Inscription, Result

# Enregistrement des modèles dans l'interface d'administration
admin.site.register(Question)
admin.site.register(Ec)
admin.site.register(Inscription)
admin.site.register(Result)
#admin.site.register(StudentProfile)

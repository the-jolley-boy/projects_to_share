from django.contrib import admin
from projects.models import Project, Category

# Register your models here.
class ProjectAdmin(admin.ModelAdmin):
	list_display = ["title", "technology"]
	pass

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    pass

admin.site.register(Project, ProjectAdmin)
admin.site.register(Category, CategoryAdmin)
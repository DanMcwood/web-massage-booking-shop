from django.contrib import admin
from .models import Category, Service, ServiceDetail

class ServiceDetailInline(admin.TabularInline):
    model = ServiceDetail
    extra = 1  # сколько пустых форм показывать для новых подробных услуг

class ServiceInline(admin.TabularInline):
    model = Service
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'type')
    list_filter = ('type',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ServiceInline]

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'sessions_count', 'available')
    list_filter = ('category', 'available')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ServiceDetailInline]  # подключаем подробные услуги в виде инлайна

    def get_fields(self, request, obj=None):
        if obj and obj.category and obj.category.type == 'default':
            return ('name', 'category', 'slug', 'description', 'available', 'photo')
        else:
            return ('name', 'category', 'slug', 'description', 'price', 'sessions_count', 'available', 'photo')

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.category and obj.category.type == 'default':
            return ('price', 'sessions_count')
        return ()

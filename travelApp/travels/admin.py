from django.contrib import admin
from django.utils.safestring import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Category, Tour, User, News, Tag
# Register your models here.
class TourTagInlineAdmin(admin.TabularInline):
    model = Tour.tags.through


class TourForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)
    class Meta:
        model = Tour
        fields = '__all__'

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    list_filter = ['id', 'name']


class TourAdmin(admin.ModelAdmin):
    list_display = ['id', 'tour_name', 'description']
    search_fields = ['tour_name']
    list_filter = ['id', 'tour_name', 'price_adult']
    readonly_fields = ['img']
    inlines = [TourTagInlineAdmin]

    def img(self, obj):
        if obj:
            return mark_safe(
                '<img src="/static/{url}" width="200" />' \
                    .format(url=obj.image.name)
            )

    form = TourForm

    class Media:
        css = {
            'all': ('/static/css/style.css',)
        }


admin.site.register(Category, CategoryAdmin)
admin.site.register(User)
admin.site.register(Tour, TourAdmin)
admin.site.register(Tag)
admin.site.register(News)
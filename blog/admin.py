from django.contrib import admin
from .models import Post
# Register your models here.

# use the @admin.register decorator to register the Post model with the admin site same as admin.site.register(Post)
@admin.register(Post)
# create a class that inherits from admin.ModelAdmin and customize the display of the Post model in the admin interface
class PostAdmin(admin.ModelAdmin):
    # list_display attribute allows you to set the fields of your model that you want to display on the admin object list page
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    # list_filter attribute allows you to filter the results of the admin object list page by the fields included in list_filter
    list_filter = ('status', 'created', 'publish', 'author')
    # search_fields attribute allows you to define the fields on which you want to enable a search box on the admin object list page
    search_fields = ['title', 'body']
    # prepopulated_fields attribute is a dictionary that maps field names to the fields it depends on
    prepopulated_fields = {'slug' : ('title',)}
    # raw_id fields attribute allows you to change the widget used to select the related object
    # in this case, the author field is displayed with a lookup widget that can scale much better than a drop-down select input when you have thousands of users
    raw_id_fields = ['author']
    # date_heirarchy attribute allows you to set the fields that will be displayed in the detail view of the object
    date_hierarchy = 'publish'
    # ordering attribute allows you to set the default ordering for the admin object list page
    ordering = ['status', 'publish']
    # show_facets you can use in a ModelAdmin class to control the display of facets (counts) in the admin interface
    show_facets = admin.ShowFacets.ALWAYS

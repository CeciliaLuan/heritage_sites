from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from leaflet.admin import LeafletGeoAdmin

from .models import Profile, HeritageSite, Favourite

# Get the User model (your custom or default User model)
User = get_user_model()

# Inline admin to manage user profiles directly from the user admin
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'
    fk_name = 'user'

# Extend the existing User admin to include the Profile in the same form
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_select_related = ('profile',)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super(UserAdmin, self).get_inline_instances(request, obj)

# Unregister the default User admin and register the extended version
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Admin for HeritageSite model using LeafletGeoAdmin for geographic fields
@admin.register(HeritageSite)
class HeritageSiteAdmin(LeafletGeoAdmin):
    list_display = ('name', 'description', 'latitude', 'longitude', 'location')
    search_fields = ['name', 'description']
    list_filter = ('name',)  # Optional: filter by name

# Admin for Favourite model
@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'site_name', 'latitude', 'longitude')
    search_fields = ['user__username', 'site_name']
    list_filter = ('user',)

# Register Profile admin separately if needed
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location')
    search_fields = ['user__username', 'user__email']

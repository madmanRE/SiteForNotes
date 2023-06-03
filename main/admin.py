from django.contrib import admin
from .models import Note, Theme, Profile


class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'created', 'theme', 'importance', 'short_text', 'is_active']
    search_fields = 'title', 'text', 'theme'

    def short_text(self, obj):
        if len(obj.text) > 50:
            return obj.text[:50] + "..."
        else:
            return obj.text

    short_text.short_description = "Фрагмент текста"


class ThemeAdmin(admin.ModelAdmin):
    list_display = ['title', 'amount']

    def amount(self, obj):
        return obj.count_notes()

    amount.short_description = "Количество заметок в данной теме"


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'count_notes']

    def count_notes(self, obj):
        return obj.count_notes()

    count_notes.short_description = "Количество заметок пользователя"



admin.site.register(Note, NoteAdmin)
admin.site.register(Theme, ThemeAdmin)
admin.site.register(Profile, ProfileAdmin)

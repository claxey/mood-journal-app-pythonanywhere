from django.contrib import admin
from .models import Entry, DailyTask, Goal, PointedJournal, DailyTracker, Vent, Tag

admin.site.register(Entry)
admin.site.register(DailyTask)
admin.site.register(Goal)
admin.site.register(PointedJournal)
admin.site.register(DailyTracker)
admin.site.register(Vent)
admin.site.register(Tag)

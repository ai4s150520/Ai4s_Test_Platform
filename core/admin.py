# core/admin.py

from django.contrib import admin
from .models import Category, Test, Question, Answer, TestAttempt

# This class allows you to see and edit Answers directly on the Question page
class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1  # How many extra empty answer forms to show
    fields = ('text', 'is_correct')

# This class allows you to see and edit Questions directly on the Test page
class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1 # How many extra empty question forms to show
    show_change_link = True # Adds a link to edit the question in its own window

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for the Category model."""
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)} # Automatically creates the slug from the name

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    """Admin configuration for the Test model."""
    list_display = ('title', 'category', 'difficulty', 'creator', 'number_of_questions')
    list_filter = ('difficulty', 'category', 'creator')
    search_fields = ('title', 'description')
    inlines = [QuestionInline] # This line enables adding questions directly on the test page
    list_per_page = 20

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Admin configuration for the Question model."""
    list_display = ('text', 'test')
    list_filter = ('test',)
    search_fields = ('text',)
    inlines = [AnswerInline] # This line enables adding answers directly on the question page

@admin.register(TestAttempt)
class TestAttemptAdmin(admin.ModelAdmin):
    """Admin configuration for the TestAttempt model."""
    list_display = ('user', 'test', 'score', 'completed_at')
    list_filter = ('test', 'user')
    # These fields should not be editable in the admin panel
    readonly_fields = ('user', 'test', 'score', 'completed_at', 'selected_answers')
    list_per_page = 25
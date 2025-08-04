from django.db import models
from django.conf import settings
from django.utils import timezone
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill



class Category(models.Model):
    """Model for categorizing tests (e.g., SAP FICO, SAP MM)."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, help_text="A URL-friendly version of the name.")

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Test(models.Model):
    """Model representing a single test or assessment."""
    
    # --- Status Choices (New) ---
    class TestStatus(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'
    
    class Difficulty(models.TextChoices):
        BEGINNER = 'beginner', 'Beginner'
        INTERMEDIATE = 'intermediate', 'Intermediate'
        EXPERT = 'expert', 'Expert'

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_tests')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='tests')
    title = models.CharField(max_length=255)
    description = models.TextField(help_text="A brief description of the test.")
    difficulty = models.CharField(max_length=20, choices=Difficulty.choices, default=Difficulty.INTERMEDIATE)
    duration_in_minutes = models.PositiveIntegerField(help_text="Duration of the test in minutes.")
    image = models.ImageField(upload_to='test_images/', null=True, blank=True, help_text="An optional image for the test card.")
    
    duration_in_minutes = models.PositiveIntegerField(help_text="Duration of the test in minutes.")
    
    # --- THIS IS THE MODIFIED FIELD ---
    image = ProcessedImageField(
        upload_to='test_images/originals/', # Save originals in a subfolder
        processors=[ResizeToFill(300, 200)], # Resize to a 600x400 box, cropping if needed
        format='PNG',
        options={'quality': 75}, # Adjust quality to balance file size and appearance
        null=True,
        blank=True,
        help_text="Image will be resized to 300x200 pixels."
    )
    
    # --- Status Field (New) ---
    # This field is added with a default value, which is safe for migrations.
    status = models.CharField(
        max_length=20,
        choices=TestStatus.choices,
        default=TestStatus.DRAFT,
        help_text="Tests are 'Draft' by default. They become 'Published' after reaching 15 questions."
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def number_of_questions(self):
        return self.questions.count()

    def __str__(self):
        return self.title


# --- NEW AND IMPROVED QUESTION MODEL ---
class Question(models.Model):
    """A question that belongs to a specific Test."""
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField(help_text="The full text of the question.")

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.text[:50] + "..."

    # --- Helper Method to Update Status (New) ---
    def _update_test_status(self):
        """
        Private helper method to check question count and update the parent test's status.
        This logic is centralized here so it's not repeated.
        """
        MIN_QUESTIONS_FOR_PUBLISH = 15
        question_count = self.test.questions.count()
        
        # Determine the new status
        new_status = Test.TestStatus.PUBLISHED if question_count >= MIN_QUESTIONS_FOR_PUBLISH else Test.TestStatus.DRAFT
        
        # Only save to the database if the status has actually changed
        if self.test.status != new_status:
            self.test.status = new_status
            self.test.save()

    # --- Overridden save() Method (New) ---
    def save(self, *args, **kwargs):
        """
        Override the default save method.
        After saving a new question, it triggers the status update on its parent test.
        """
        is_new = self.pk is None # Check if this is a new question being created
        super().save(*args, **kwargs) # Save the question to the database
        
        # Only run the status update if it's a new question to avoid unnecessary checks on updates
        if is_new:
            self._update_test_status()

    # --- Overridden delete() Method (New) ---
    def delete(self, *args, **kwargs):
        """
        Override the default delete method.
        Before deleting the question, it triggers a status update on its parent test.
        """
        # Store the parent test in a variable before deletion
        parent_test = self.test
        super().delete(*args, **kwargs) # Delete the question from the database
        
        # After deletion, update the status of the parent test
        # We need to manually recount here
        question_count = parent_test.questions.count()
        MIN_QUESTIONS_FOR_PUBLISH = 15
        new_status = Test.TestStatus.PUBLISHED if question_count >= MIN_QUESTIONS_FOR_PUBLISH else Test.TestStatus.DRAFT
        if parent_test.status != new_status:
            parent_test.status = new_status
            parent_test.save()


class Answer(models.Model):
    """An answer option for a Question."""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False, help_text="Mark this if it is the correct answer.")

    def __str__(self):
        return f"{self.text} (for question: {self.question.id})"

class TestAttempt(models.Model):
    """Records a user's attempt at a test."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='test_attempts')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='attempts')
    score = models.FloatField(help_text="The final score in percentage (e.g., 85.5).")
    completed_at = models.DateTimeField(default=timezone.now)
    # Store which answers the user selected for detailed review
    selected_answers = models.ManyToManyField(Answer, related_name='test_attempts')

    def __str__(self):
        return f"{self.user.username}'s attempt on {self.test.title}"
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction # For ensuring data integrity
from .models import Test, TestAttempt, Answer 
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST
from .models import Test, Question, Answer, Category
from .forms import TestCreateForm, QuestionForm, AnswerFormSet
import json



User = get_user_model()

# --- Static and Dashboard Views ---

class HomeView(TemplateView):
    template_name = 'core/home.html'

@login_required
def test_list(request):
    """
    Displays a list of tests.
    - Regular users see only 'Published' tests.
    - Staff members see ALL tests, including their 'Drafts'.
    """
    # Check if the currently logged-in user is a staff member
    if request.user.is_staff:
        # Staff members see all tests, so they can track their drafts
        tests = Test.objects.all().order_by('-created_at')
    else:
        # Regular users only see tests that are marked as 'Published'
        tests = Test.objects.filter(status=Test.TestStatus.PUBLISHED).order_by('-created_at')
        
    # We can also pass all categories to the template for the filter dropdown
    categories = Category.objects.all()

    context = {
        'tests': tests,
        'categories': categories,
    }
    return render(request, 'core/test_list.html', context)

@login_required
def test_detail(request, test_id):
    """
    Shows details for a single test before the user starts it.
    Corresponds to: test_detail.html
    """
    test = get_object_or_404(Test, pk=test_id)
    context = {
        'test': test
    }
    return render(request, 'core/test_detail.html', context)


@login_required
def take_test(request, test_id):
    """
    Displays the actual test form with questions and answers.
    Corresponds to: take_test.html
    """
    test = get_object_or_404(Test, pk=test_id)
    # Eagerly load related questions and answers to reduce database queries
    questions = test.questions.prefetch_related('answers')
    context = {
        'test': test,
        'questions': questions
    }
    return render(request, 'core/take_test.html', context)


@require_POST # Security: This action should only be done via a POST request.
@login_required
def toggle_test_status(request, test_id):
    """
    Toggles the status of a test between 'Draft' and 'Published'.
    Restricted to staff members only.
    """
    # Security check
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('core:home')

    test = get_object_or_404(Test, pk=test_id)

    # Flip the status
    if test.status == Test.TestStatus.DRAFT:
        test.status = Test.TestStatus.PUBLISHED
        messages.success(request, f"The test '{test.title}' has been published and is now visible to students.")
    else:
        test.status = Test.TestStatus.DRAFT
        messages.success(request, f"The test '{test.title}' has been reverted to a draft and is now hidden from students.")
        
    test.save()
    
    # Redirect back to the same management page
    return redirect('core:manage_test', test_id=test.id)


@login_required
@transaction.atomic
def submit_test(request, test_id):
    """
    Processes submitted test answers with improved resilience against data errors.
    """
    if request.method == 'POST':
        test = get_object_or_404(Test, pk=test_id)
        questions = test.questions.all()
        correct_answers_count = 0
        selected_answer_pks = []

        for question in questions:
            selected_answer_id_str = request.POST.get(f'question_{question.id}')
            if selected_answer_id_str:
                selected_answer_pks.append(selected_answer_id_str)
                
                # --- THE FIX: Use a try/except block ---
                try:
                    # Find the designated correct answer for this question
                    correct_answer = Answer.objects.get(question=question, is_correct=True)
                    # Compare the user's choice with the correct answer's ID
                    if int(selected_answer_id_str) == correct_answer.id:
                        correct_answers_count += 1
                except Answer.DoesNotExist:
                    # This question has a data integrity issue (no correct answer).
                    # Log this error for the admin and mark the user's answer as incorrect.
                    print(f"CRITICAL DATA ERROR: Question ID {question.id} has no correct answer designated.")
                    pass # The count of correct_answers_count does not increase.
        
        total_questions = questions.count()
        score = 0
        if total_questions > 0:
            score = (correct_answers_count / total_questions) * 100
        
        attempt = TestAttempt.objects.create(
            user=request.user,
            test=test,
            score=score
        )
        attempt.selected_answers.set(selected_answer_pks)
        
        # Redirect to the results page, which will then link to the dashboard
        messages.success(request, f"You have completed the test: {test.title}.")
        return redirect('core:results', attempt_id=attempt.id)
    
    return redirect('core:test_detail', test_id=test_id)

@login_required
def results(request, attempt_id):
    """
    Displays the results of a specific test attempt.
    Corresponds to: results.html
    """
    attempt = get_object_or_404(TestAttempt, pk=attempt_id)
    
    # Security Check: Ensure the user viewing the result is the one who took it
    if request.user != attempt.user:
        messages.error(request, "You are not authorized to view these results.")
        return redirect('core:dashboard')

    context = {
        'attempt': attempt
    }
    return render(request, 'core/results.html', context)


@login_required
def dashboard(request):
    """
    Intelligently displays the correct dashboard based on the user's role.
    - Renders admin_dashboard.html for staff users.
    - Renders dashboard.html for regular users.
    """
    
    # --- THIS IS THE CORE LOGIC ---
    # Check if the user is a staff member.
    if request.user.is_staff:
        
        # --- Admin Logic ---
        # This is the data needed for the admin_dashboard.html template.
        student_count = User.objects.filter(is_staff=False).count()
        test_count = Test.objects.count()
        total_attempts_count = TestAttempt.objects.count()
        recent_attempts = TestAttempt.objects.select_related('user', 'test').order_by('-completed_at')[:20]

        context = {
            'student_count': student_count,
            'test_count': test_count,
            'total_attempts_count': total_attempts_count,
            'recent_attempts': recent_attempts,
        }
        
        # Render the admin-specific template
        return render(request, 'core/admin_dashboard.html', context)
        
    else:
        
        # --- Student Logic ---
        # This is the data needed for the regular dashboard.html template.
        attempts = TestAttempt.objects.filter(user=request.user).order_by('-completed_at')
        
        context = {
            'attempts': attempts
        }
        
        # Render the student-specific template
        return render(request, 'core/dashboard.html', context)

@login_required
def create_test(request):
    """
    Handles the creation of a new test instance.
    """
    # --- THIS IS THE SECURITY CHECK ---
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to create a test.")
        return redirect('core:dashboard') # Redirect non-staff users away

    if request.method == 'POST':
        form = TestCreateForm(request.POST, request.FILES)
        if form.is_valid():
            test = form.save(commit=False)
            test.creator = request.user
            test.save()
            messages.success(request, f'Test "{test.title}" created successfully! Now add some questions.')
            return redirect('core:manage_test', test_id=test.id)
    else:
        form = TestCreateForm()
        
    return render(request, 'core/add_test.html', {'form': form})


@login_required
def manage_test(request, test_id):
    """
    Displays the management page for a single test.
    This view is now protected and only accessible by staff members.
    """
    # --- THIS IS THE NEW, CORRECT SECURITY CHECK ---
    # Check if the logged-in user is a staff member.
    if not request.user.is_staff:
        # If not, show an error and redirect them to a safe page (like the dashboard).
        messages.error(request, "You do not have the required permissions to access this page.")
        return redirect('core:dashboard')
        
    # --- The rest of the view only runs if the user IS staff ---
    
    test = get_object_or_404(Test, pk=test_id)
    
    # The old check `if request.user != test.creator:` is no longer needed
    # because the `is_staff` check is more general and powerful.

    question_form = QuestionForm()
    answer_formset = AnswerFormSet(queryset=Answer.objects.none())

    context = {
        'test': test,
        'question_form': question_form,
        'answer_formset': answer_formset,
    }
    return render(request, 'core/manage_test.html', context)

@login_required
@transaction.atomic
def add_question(request, test_id):
    """
    Handles adding a question with the correct validation order.
    """
    test = get_object_or_404(Test, pk=test_id)
    
    # Security check remains the same
    if not request.user.is_staff:
        messages.error(request, "You are not authorized to add questions to this test.")
        return redirect('core:test_list')

    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        # We still need a temporary instance for the formset
        temp_question = Question(test=test)
        answer_formset = AnswerFormSet(request.POST, instance=temp_question)

        # --- THIS IS THE CORRECTED LOGIC ---

        # 1. First, check if both the main form and the formset are valid.
        # This populates the `cleaned_data` for all forms.
        if question_form.is_valid() and answer_formset.is_valid():
            
            # 2. Now that they are valid, we can safely perform our custom check.
            is_correct_count = 0
            for form in answer_formset:
                # This will now work because `cleaned_data` exists.
                if form.cleaned_data.get('is_correct'):
                    is_correct_count += 1
            
            # 3. Check the result of our custom validation.
            if is_correct_count == 1:
                # If all checks pass, save the data to the database.
                question = question_form.save(commit=False)
                question.test = test
                question.save()
                
                # Associate the now-saved question with the formset and save the answers.
                answer_formset.instance = question
                answer_formset.save()
                
                messages.success(request, "New question has been added successfully.")
            else:
                # Custom validation failed. Show a specific error.
                messages.error(request, "You must select exactly one correct answer for the question.")
        
        else:
            # The initial .is_valid() check failed. Show a generic error.
            messages.error(request, "There was an error with your submission. Please check the forms.")
            # For debugging, you can print the errors to the console:
            # print(question_form.errors)
            # print(answer_formset.errors)

    # Always redirect back to the management page after a POST request.
    return redirect('core:manage_test', test_id=test_id)

@require_POST
@login_required
def delete_question(request, question_id):
    """
    Deletes a specific question and its related answers.
    This action is restricted to staff members.
    """
    # Security check: ensure the user is staff
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('core:home')

    # Find the question object or return a 404 error
    question = get_object_or_404(Question, pk=question_id)
    
    # We need the test_id so we know where to redirect back to after deletion
    test_id = question.test.id

    # Another security check: ensure the user is the creator of the test
    # This is a good second layer, but is_staff is the primary gatekeeper
    if request.user != question.test.creator and not request.user.is_superuser:
        messages.error(request, "You are not authorized to delete questions for this test.")
        return redirect('core:manage_test', test_id=test_id)
        
    # If all checks pass, delete the question
    question.delete()
    
    messages.success(request, "The question was successfully deleted.")
    
    # Redirect the user back to the test management page
    return redirect('core:manage_test', test_id=test_id)
# --- END OF THE NEW FUNCTION ---


@require_POST # Security: This view only accepts POST requests.
@login_required
def delete_test(request, test_id):
    """
    Deletes an entire Test object and all its related children.
    This action is restricted to superusers for maximum security.
    """
    # Find the test or raise a 404 error if it doesn't exist
    test = get_object_or_404(Test, pk=test_id)
    
    # --- THIS IS THE CRITICAL SECURITY CHECK ---
    # Only a superuser can delete an entire test.
    if not request.user.is_superuser:
        messages.error(request, "This is an administrative action requiring superuser privileges.")
        # Redirect back to the manage page if the user is not authorized.
        return redirect('core:manage_test', test_id=test.id)

    # Get the title for the success message before deleting the object
    test_title = test.title
    
    # Delete the test object. All related questions, answers, and attempts
    # will be deleted automatically because of the cascade settings in your models.
    test.delete()
    
    messages.success(request, f"The test '{test_title}' was permanently deleted.")
    
    # After deleting, redirect to the main test list, as the manage page no longer exists.
    return redirect('core:test_list')


@require_POST # Security: This view should only accept POST requests.
@login_required
@transaction.atomic # This is critical: makes the entire function an all-or-nothing database operation.
def bulk_add_questions(request, test_id):
    """
    Handles the bulk upload of questions and answers from a JSON file.
    """
    test = get_object_or_404(Test, pk=test_id)
    
    # Security check to ensure only staff can perform this action.
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('core:home')

    json_file = request.FILES.get('json_file')

    # File Validation
    if not json_file:
        messages.error(request, "No file was selected. Please choose a JSON file to upload.")
        return redirect('core:manage_test', test_id=test_id)
        
    if not json_file.name.endswith('.json'):
        messages.error(request, "Invalid file type. Only .json files are accepted.")
        return redirect('core:manage_test', test_id=test_id)

    # Data Processing and Validation
    try:
        file_content = json_file.read().decode('utf-8')
        data = json.loads(file_content)
        
        if not isinstance(data, list):
            raise ValueError("The root of the JSON file must be a list [...] of questions.")

        questions_added_count = 0
        
        sid = transaction.savepoint()
        
        for i, question_data in enumerate(data, 1):
            text = question_data.get('text')
            answers_data = question_data.get('answers')
            if not text or not answers_data or not isinstance(answers_data, list):
                raise ValueError(f"Invalid data structure for question #{i}.")
            correct_answers_count = sum(1 for ans in answers_data if ans.get('is_correct') is True)
            if correct_answers_count != 1:
                raise ValueError(f"Question #{i} ('{text[:30]}...') must have exactly one correct answer.")
            
            question = Question.objects.create(test=test, text=text)
            for answer_data in answers_data:
                Answer.objects.create(
                    question=question,
                    text=answer_data.get('text'),
                    is_correct=answer_data.get('is_correct', False)
                )
            questions_added_count += 1

        transaction.savepoint_commit(sid)
        messages.success(request, f"Successfully added {questions_added_count} new questions to the test.")

    except json.JSONDecodeError:
        transaction.savepoint_rollback(sid)
        messages.error(request, "Invalid JSON file. The file contains syntax errors.")
    except ValueError as e:
        transaction.savepoint_rollback(sid)
        messages.error(request, f"Data validation failed: {e}")
    except Exception as e:
        transaction.savepoint_rollback(sid)
        messages.error(request, f"An unexpected error occurred: {e}")
    
    return redirect('core:manage_test', test_id=test_id)
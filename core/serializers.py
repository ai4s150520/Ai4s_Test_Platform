from rest_framework import serializers
from .models import Category, Test, Question, Answer, TestAttempt
from django.contrib.auth import get_user_model

User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'is_correct']

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'answers']

class TestSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')
    category = serializers.StringRelatedField()
    questions = QuestionSerializer(many=True, read_only=True)
    number_of_questions = serializers.IntegerField(read_only=True)

    class Meta:
        model = Test
        fields = [
            'id', 'title', 'creator', 'category', 'description', 
            'difficulty', 'duration_in_minutes', 'image', 'number_of_questions', 'questions'
        ]

class UserAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class TestAttemptSerializer(serializers.ModelSerializer):
    user = UserAttemptSerializer(read_only=True)
    test = TestSerializer(read_only=True)
    selected_answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = TestAttempt
        fields = ['id', 'user', 'test', 'score', 'completed_at', 'selected_answers']
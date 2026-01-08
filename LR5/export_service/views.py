from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import csv
import json
from io import StringIO
from polls.models import Question, Choice


class ExportCSVAPI(APIView):
    """Экспорт данных конкретного вопроса в CSV"""

    def get(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)

        # Создаем CSV в памяти
        output = StringIO()
        writer = csv.writer(output)

        # Заголовки
        writer.writerow(['Опрос', 'Вопрос', 'Вариант ответа', 'Голоса', 'Процент'])

        # Данные
        choices = question.choice_set.all()
        total_votes = sum(c.votes for c in choices)

        for choice in choices:
            percentage = (choice.votes / total_votes * 100) if total_votes > 0 else 0
            writer.writerow([
                question.id,
                question.question_text,
                choice.choice_text,
                choice.votes,
                f'{percentage:.2f}%'
            ])

        # Возвращаем CSV файл
        response = HttpResponse(output.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="question_{question_id}.csv"'
        return response


class ExportJSONAPI(APIView):
    """Экспорт данных конкретного вопроса в JSON"""

    def get(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)

        choices = question.choice_set.all()
        total_votes = sum(c.votes for c in choices)

        data = {
            'question_id': question.id,
            'question_text': question.question_text,
            'pub_date': question.pub_date.isoformat(),
            'total_votes': total_votes,
            'choices': [
                {
                    'choice_text': c.choice_text,
                    'votes': c.votes,
                    'percentage': (c.votes / total_votes * 100) if total_votes > 0 else 0
                }
                for c in choices
            ]
        }

        response = HttpResponse(
            json.dumps(data, ensure_ascii=False, indent=2),
            content_type='application/json'
        )
        response['Content-Disposition'] = f'attachment; filename="question_{question_id}.json"'
        return response


class ExportAllJSONAPI(APIView):
    """Экспорт всех вопросов в JSON"""

    def get(self, request):
        questions = Question.objects.all().prefetch_related('choice_set')

        data = []
        for question in questions:
            choices = question.choice_set.all()
            total_votes = sum(c.votes for c in choices)

            question_data = {
                'id': question.id,
                'question_text': question.question_text,
                'pub_date': question.pub_date.isoformat(),
                'total_votes': total_votes,
                'choices': [
                    {
                        'choice_text': c.choice_text,
                        'votes': c.votes,
                        'percentage': (c.votes / total_votes * 100) if total_votes > 0 else 0
                    }
                    for c in choices
                ]
            }
            data.append(question_data)

        response = HttpResponse(
            json.dumps(data, ensure_ascii=False, indent=2),
            content_type='application/json'
        )
        response['Content-Disposition'] = 'attachment; filename="all_questions.json"'
        return response


class ExportAllCSVAPI(APIView):
    """Экспорт всех вопросов в CSV"""

    def get(self, request):
        output = StringIO()
        writer = csv.writer(output)

        # Заголовки
        writer.writerow([
            'ID опроса', 'Вопрос', 'Дата создания',
            'Вариант ответа', 'Голоса', 'Процент', 'Всего голосов'
        ])

        questions = Question.objects.all().prefetch_related('choice_set')

        for question in questions:
            choices = question.choice_set.all()
            total_votes = sum(c.votes for c in choices)

            for choice in choices:
                percentage = (choice.votes / total_votes * 100) if total_votes > 0 else 0
                writer.writerow([
                    question.id,
                    question.question_text,
                    question.pub_date.strftime('%Y-%m-%d %H:%M'),
                    choice.choice_text,
                    choice.votes,
                    f'{percentage:.2f}%',
                    total_votes
                ])

        response = HttpResponse(output.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="all_polls.csv"'
        return response
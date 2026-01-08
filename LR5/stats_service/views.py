from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Count, Sum, F
import plotly.graph_objects as go
import plotly.io as pio
import base64
import io
from polls.models import Question, Choice
import json


class QuestionStatsAPI(APIView):
    """API для статистики по конкретному вопросу"""

    def get(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)

        # Получаем варианты ответов с количеством голосов
        choices = question.choice_set.annotate(
            votes_count=Count('votes')
        ).values('choice_text', 'votes_count')

        # Считаем общее количество голосов
        total_votes = sum(choice['votes_count'] for choice in choices)

        # Добавляем проценты
        for choice in choices:
            if total_votes > 0:
                choice['percentage'] = round((choice['votes_count'] / total_votes) * 100, 2)
            else:
                choice['percentage'] = 0.0

        data = {
            'question_id': question.id,
            'question_text': question.question_text,
            'pub_date': question.pub_date,
            'total_votes': total_votes,
            'choices': list(choices),
        }

        return Response(data)


class GlobalStatsAPI(APIView):
    """API для глобальной статистики"""

    def get(self, request):
        # Статистика по всем опросам
        total_questions = Question.objects.count()

        # Самые популярные вопросы
        popular_questions = Question.objects.annotate(
            total_votes=Sum('choice__votes')
        ).order_by('-total_votes')[:10]

        # Активные опросы (за последние 7 дней)
        from django.utils import timezone
        from datetime import timedelta
        week_ago = timezone.now() - timedelta(days=7)
        recent_questions = Question.objects.filter(
            pub_date__gte=week_ago
        ).count()

        # Статистика по голосам
        total_votes = Choice.objects.aggregate(
            total=Sum('votes')
        )['total'] or 0

        data = {
            'total_questions': total_questions,
            'total_votes': total_votes,
            'recent_questions': recent_questions,
            'popular_questions': [
                {
                    'id': q.id,
                    'text': q.question_text,
                    'votes': q.total_votes or 0
                }
                for q in popular_questions
            ]
        }

        return Response(data)


class ChartAPI(APIView):
    """API для получения графика в формате SVG"""

    def get(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)

        # Получаем данные
        choices = question.choice_set.all()
        choice_texts = [c.choice_text for c in choices]
        votes = [c.votes for c in choices]

        # Создаем столбчатую диаграмму
        fig = go.Figure(
            data=[go.Bar(
                x=choice_texts,
                y=votes,
                text=[f'{v} голосов' for v in votes],
                textposition='auto',
                marker_color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'][:len(choices)]
            )]
        )

        fig.update_layout(
            title=f'Результаты: {question.question_text[:50]}...',
            xaxis_title='Варианты ответа',
            yaxis_title='Количество голосов',
            showlegend=False,
            height=400,
            margin=dict(l=20, r=20, t=40, b=20)
        )

        # Конвертируем в SVG
        svg_string = pio.to_image(fig, format='svg')

        return Response({'svg': svg_string.decode('utf-8')})


class ChartBase64API(APIView):
    """API для получения графика в формате PNG base64"""

    def get(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)

        # Получаем данные
        choices = question.choice_set.all()
        choice_texts = [c.choice_text for c in choices]
        votes = [c.votes for c in choices]

        # Создаем круговую диаграмму для процентов
        total_votes = sum(votes)
        if total_votes > 0:
            percentages = [(v / total_votes * 100) for v in votes]
            labels = [f'{text} ({perc:.1f}%)'
                      for text, perc in zip(choice_texts, percentages)]
        else:
            percentages = [0] * len(votes)
            labels = choice_texts

        fig = go.Figure(
            data=[go.Pie(
                labels=labels,
                values=percentages,
                hole=.3,
                textinfo='label+percent',
                marker=dict(colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57'][:len(choices)])
            )]
        )

        fig.update_layout(
            title=f'Распределение голосов: {question.question_text[:40]}...',
            showlegend=False,
            height=500,
            margin=dict(l=20, r=20, t=40, b=20)
        )

        # Конвертируем в PNG и затем в base64
        img_bytes = pio.to_image(fig, format='png')
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')

        return Response({
            'image': f'data:image/png;base64,{img_base64}',
            'question_id': question_id,
            'question_text': question.question_text,
            'total_votes': total_votes
        })
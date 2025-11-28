from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import News
from .serializers import NewsSerializer
import requests
import os
from dotenv import load_dotenv

load_dotenv()


def index(request):
    """
    메인 페이지
    """
    return render(request, 'news/index.html')


@api_view(['GET', 'POST'])
def news_list(request):
    """
    GET: 전체 뉴스 목록 조회 (요구사항 F02)
    POST: Naver News API로 뉴스 검색 및 저장 (요구사항 F01)
    """
    if request.method == 'GET':
        bookmarked_only = request.GET.get('bookmarked', None)

        if bookmarked_only == 'true':
            news = News.objects.filter(is_bookmarked=True).order_by('-created_at')
        else:
            news = News.objects.all().order_by('-created_at')

        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        query = request.data.get('query')

        if not query:
            return Response({'error': '검색어를 입력해주세요.'}, status=status.HTTP_400_BAD_REQUEST)

        client_id = os.getenv('NAVER_CLIENT_ID')
        client_secret = os.getenv('NAVER_CLIENT_SECRET')

        url = 'https://openapi.naver.com/v1/search/news.json'
        headers = {
            'X-Naver-Client-Id': client_id,
            'X-Naver-Client-Secret': client_secret
        }
        params = {
            'query': query,
            'display': 10,
            'sort': 'date'
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            items = response.json().get('items', [])
            saved_count = 0

            for item in items:
                title = item['title'].replace('<b>', '').replace('</b>', '').replace('&quot;', '"').replace('&apos;', "'")

                if not News.objects.filter(title=title).exists():
                    News.objects.create(
                        title=title,
                        link=item['link'],
                        description=item['description'].replace('<b>', '').replace('</b>', '').replace('&quot;', '"').replace('&apos;', "'"),
                        pub_date=item.get('pubDate', '')
                    )
                    saved_count += 1

            return Response({
                'message': f'{saved_count}개의 뉴스가 저장되었습니다.',
                'total': len(items),
                'saved': saved_count
            })
        else:
            return Response({'error': 'Naver API 요청 실패'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def news_detail(request, news_pk):
    """
    뉴스 상세 조회 (요구사항 F03)
    """
    try:
        news = News.objects.get(pk=news_pk)
    except News.DoesNotExist:
        return Response({'error': '뉴스를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = NewsSerializer(news)
    return Response(serializer.data)


@api_view(['POST'])
def news_bookmark(request, news_pk):
    """
    뉴스 북마크 토글 (요구사항 F04)
    """
    try:
        news = News.objects.get(pk=news_pk)
    except News.DoesNotExist:
        return Response({'error': '뉴스를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    news.is_bookmarked = not news.is_bookmarked
    news.save()

    serializer = NewsSerializer(news)
    return Response(serializer.data)

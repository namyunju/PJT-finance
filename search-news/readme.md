# 금융 뉴스 검색기 구현

## 프로젝트 개요

- Django REST Framework를 활용하여 외부 API 데이터를 수집
- 프론트엔드에서 axios를 이용해 비동기적으로 데이터를 렌더링
- 뉴스 데이터 Read 중심의 API를 설계
- 사용자의 북마크 상태를 실시간 반영하는 인터렉션 기능
- 외부 OpenAPI(Naver News API)를 통한 데이터 연동 과정 이해
- JSON 구조의 응답 데이터를 가공 -> 저장 -> 출력 하는 전체 흐름을 구현

## 개발 언어 및 툴
- Vscode
- HTML5, CSS, JavaScript
- Live Server (Vscode Extension)

## 데이터베이스 모델

### News 모델

| 필드명 | 타입 | 설명 |
|--------|------|------|
| id | AutoField | Primary Key (자동 생성) |
| title | CharField(200) | 뉴스 제목 |
| link | CharField(200) | 뉴스 원문 링크 |
| description | TextField | 뉴스 본문 내용 |
| pub_date | CharField(200) | 발행일 |
| is_bookmarked | BooleanField | 북마크 상태 (기본값: False) |
| created_at | DateTimeField | 생성일시 (자동 생성) |

## API 명세

### 1. 뉴스 검색 및 저장 
```http
POST /api/news/
Content-Type: application/json

{
  "query": "검색어"
}

Response:
{
  "message": "5개의 뉴스가 저장되었습니다.",
  "total": 10,
  "saved": 5
}
```

### 2. 전체 뉴스 목록 조회 
```http
GET /api/news/

Response:
[
  {
    "id": 1,
    "title": "뉴스 제목",
    "link": "https://...",
    "description": "뉴스 내용",
    "pub_date": "Thu, 28 Nov 2024 10:00:00 +0900",
    "is_bookmarked": false,
    "created_at": "2024-11-28T10:00:00Z"
  },
  ...
]
```

### 3. 북마크된 뉴스만 조회 
```http
GET /api/news/?bookmarked=true

Response: (위와 동일, is_bookmarked=true인 항목만)
```

### 4. 뉴스 상세 조회 
```http
GET /api/news/{id}/

Response:
{
  "id": 1,
  "title": "뉴스 제목",
  "link": "https://...",
  "description": "뉴스 내용",
  "pub_date": "Thu, 28 Nov 2024 10:00:00 +0900",
  "is_bookmarked": false,
  "created_at": "2024-11-28T10:00:00Z"
}
```

### 5. 북마크 토글 
```http
POST /api/news/{id}/bookmark/

Response:
{
  "id": 1,
  "is_bookmarked": true,
  ...
}
```

---


## ✅ 구현된 필수 기능

### Naver 뉴스 API 연동
- ✅ Naver Developers에서 Client ID/Secret 발급
- ✅ `.env` 파일로 API Key 보안 관리
- ✅ 검색어 기반 뉴스 데이터 수집
- ✅ 중복 제목 방지 로직 구현
- ✅ HTML 태그 제거 및 특수문자 처리

### 전체 뉴스 목록 출력
![사진](images\F02.jpg)
- ✅ 페이지 접속 시 자동으로 전체 뉴스 로드
- ✅ 저장된 뉴스가 없을 경우 안내 문구 표시
- ✅ 좌측 영역에 스크롤 가능한 뉴스 리스트 구현

### 뉴스 상세보기
![사진](images\F03.jpg)
- ✅ 뉴스 제목 클릭 시 상세 내용 표시
- ✅ 우측 영역에 제목, 본문, 발행일, 원문 링크 출력
- ✅ 독립적인 스크롤 영역 구현

### 북마크 기능
![사진](images\F04.jpg)
- ✅ 별(★) 아이콘 클릭으로 북마크 토글
- ✅ 북마크 상태를 색상으로 직관적 표시 (금색/회색)
- ✅ 실시간 UI 반영

### 전체/북마크 보기 전환
![사진](images\F05-1.jpg)
![사진](images\F05-2.jpg)
- ✅ 상단 필터 버튼으로 모드 전환
- ✅ 활성화된 버튼 색상 구분
- ✅ 북마크된 뉴스만 필터링하여 표시

---

## 🔐 비기능적 요구사항

### API Key 관리
- ✅ `.env` 파일에 `NAVER_CLIENT_ID`, `NAVER_CLIENT_SECRET` 저장
- ✅ `.gitignore`에 `.env` 등록하여 Git 노출 방지
- ✅ `python-dotenv`로 환경변수 로드

### 코드 구조화
- ✅ Django REST API 기반 앱(news) 구성
- ✅ HTML, CSS, JavaScript 분리
- ✅ models, serializers, views 계층 분리

### 반응형 UI 구성
- ✅ 좌우 분할 레이아웃 (뉴스 목록 40% / 상세보기 60%)
- ✅ 북마크 상태 색상 표시 (금색 ★ / 회색 ☆)
- ✅ 호버 효과 및 활성 상태 표시

### 문서화
- ✅ README.md 작성 (구현 과정, API 연동 절차, 학습 내용)

---

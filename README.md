# Secure_Coding

<br>
<br>

## 프로젝트 구조

```bash
secure_coding/
├── app.py # Flask 애플리케이션 코드
├── static/
│ └── uploads/ # 물건 이미지 업로드 폴더
├── templates/
│ ├── main.html # 로그인 페이지
│ ├── register.html # 회원가입 페이지
│ ├── home.html # 로그인 후 홈 페이지 (물건 목록)
│ ├── upload.html # 물건 올리기 페이지
│ └── item.html # 물건 상세 페이지 (댓글, 대댓글, 삭제, 수정 등)
└── users.db # SQLite 데이터베이스 파일
```

<br>
<br>

## 세부 기능
- ### main.html
  - 메인 페이지
  - 로그인 기능
    
- ### register.html
  - 회원가입 페이지
  - @를 기준으로 앞뒤에 문자가 들어가야 회원가입 가능
    
- ### home.html
  - 올린 물건들을 보여주는 페이지
  - 해당 물건 클릭시 세부정보 페이지 이동
 
- ### upload.html
  - 물건 올리는 페이지
  - 이름, 가격, 세부설명, 사진 첨부 가능

- ### item.html
  - 물건 상세 정보 페이지
  - 댓글, 대댓글 작성 / 수정 / 삭제 가능
  - 판매자 댓글일 경우 판매자 표시

<br>
<br>

## 제작 타임 트리
1. 3.26(수) 최초 기본틀 제작













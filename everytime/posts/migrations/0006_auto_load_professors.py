# posts/migrations/0006_auto_load_professors.py
from django.db import migrations

def insert_professors(apps, schema_editor):
    Professor = apps.get_model('posts', 'Professor')
    
    professor_list = [
        # 글로벌융합대학
        {"department": "경영학전공", "name": "김경묵"}, {"department": "경영학전공", "name": "이상묵"},
        {"department": "경영학전공", "name": "노태협"}, {"department": "경영학전공", "name": "유정민"},
        {"department": "경영학전공", "name": "유병희"}, {"department": "경영학전공", "name": "나재석"},
        {"department": "경영학전공", "name": "이황희"}, {"department": "국어국문학전공", "name": "김은희"},
        {"department": "국어국문학전공", "name": "이은애"}, {"department": "국어국문학전공", "name": "이명찬"},
        {"department": "국어국문학전공", "name": "양정호"}, {"department": "국어국문학전공", "name": "김유진"},
        {"department": "국어국문학전공", "name": "김지은"}, {"department": "미술사학전공", "name": "최성은"},
        {"department": "미술사학전공", "name": "정무정"}, {"department": "미술사학전공", "name": "이송란"},
        {"department": "유아교육과", "name": "이영자"}, {"department": "유아교육과", "name": "이정욱"},
        {"department": "유아교육과", "name": "이경옥"}, {"department": "유아교육과", "name": "김윤희"},
        {"department": "유아교육과", "name": "임혜성"}, {"department": "의상디자인전공", "name": "강여선"},
        {"department": "의상디자인전공", "name": "최미영"}, {"department": "의상디자인전공", "name": "김윤"},
        {"department": "의상디자인전공", "name": "김고운"}, {"department": "일어일문학전공", "name": "오경"},
        {"department": "일어일문학전공", "name": "이광수"}, {"department": "일어일문학전공", "name": "이상경"},
        {"department": "일어일문학전공", "name": "손재현"}, {"department": "일어일문학전공", "name": "이이야마다케시"},
        {"department": "중어중문학전공", "name": "양오진"}, {"department": "중어중문학전공", "name": "강춘화"},
        {"department": "중어중문학전공", "name": "김경남"}, {"department": "중어중문학전공", "name": "위메이"},
        # 과학기술대학
        {"department": "디지털소프트웨어공학부", "name": "음두헌"}, {"department": "디지털소프트웨어공학부", "name": "박우창"},
        {"department": "디지털소프트웨어공학부", "name": "이주영"}, {"department": "디지털소프트웨어공학부", "name": "유견아"},
        {"department": "디지털소프트웨어공학부", "name": "최승훈"}, {"department": "디지털소프트웨어공학부", "name": "이경미"},
        {"department": "디지털소프트웨어공학부", "name": "박태정"}, {"department": "디지털소프트웨어공학부", "name": "이재호"},
        {"department": "디지털소프트웨어공학부", "name": "서민혜"}, {"department": "디지털소프트웨어공학부", "name": "이형규"},
        {"department": "디지털소프트웨어공학부", "name": "강지헌"}, {"department": "디지털소프트웨어공학부", "name": "백남균"},
        {"department": "디지털소프트웨어공학부", "name": "이윤성"}, {"department": "사이버보안전공", "name": "박태정"},
        {"department": "사이버보안전공", "name": "서민혜"}, {"department": "사이버보안전공", "name": "백남균"},
        {"department": "수학전공", "name": "이향주"}, {"department": "수학전공", "name": "원대연"},
        {"department": "수학전공", "name": "최성우"}, {"department": "식품영양학전공", "name": "강금지"},
        {"department": "식품영양학전공", "name": "조윤옥"}, {"department": "식품영양학전공", "name": "김건희"},
        {"department": "식품영양학전공", "name": "정하숙"}, {"department": "식품영양학전공", "name": "정미숙"},
        {"department": "식품영양학전공", "name": "김경희"}, {"department": "식품영양학전공", "name": "강민지"},
        {"department": "정보통계학전공", "name": "최기헌"}, {"department": "정보통계학전공", "name": "민대기"},
        {"department": "정보통계학전공", "name": "김재희"}, {"department": "정보통계학전공", "name": "허집"},
        {"department": "정보통계학전공", "name": "김준식"}, {"department": "컴퓨터공학전공", "name": "박우창"},
        {"department": "컴퓨터공학전공", "name": "이주영"}, {"department": "컴퓨터공학전공", "name": "유견아"},
        {"department": "컴퓨터공학전공", "name": "최승훈"}, {"department": "컴퓨터공학전공", "name": "이경미"},
        {"department": "화학전공", "name": "고은희"}, {"department": "화학전공", "name": "이재인"},
        {"department": "화학전공", "name": "김학준"}, {"department": "화학전공", "name": "김선영"},
        {"department": "화학전공", "name": "신정철"}, {"department": "화학전공", "name": "한예리"},
        # 약학대학
        {"department": "약학과", "name": "신승원"}, {"department": "약학과", "name": "손영택"},
        {"department": "약학과", "name": "문애리"}, {"department": "약학과", "name": "정춘식"},
        {"department": "약학과", "name": "이용수"}, {"department": "약학과", "name": "조효선"},
        {"department": "약학과", "name": "정주희"}, {"department": "약학과", "name": "정우현"},
        {"department": "약학과", "name": "한은영"},
        # Art&Design 대학
        {"department": "동양화전공", "name": "임택"}, {"department": "동양화전공", "name": "이주연"},
        {"department": "동양화전공", "name": "박상미"}, {"department": "서양화전공", "name": "박미연"},
        {"department": "서양화전공", "name": "김연규"}, {"department": "생활체육학전공", "name": "강준상"},
        {"department": "생활체육학전공", "name": "김준동"}, {"department": "생활체육학전공", "name": "최진영"},
        {"department": "시각디자인전공", "name": "이승진"}, {"department": "시각디자인전공", "name": "박지다"},
        {"department": "시각디자인전공", "name": "김승민"}, {"department": "실내디자인전공", "name": "김명옥"},
        {"department": "실내디자인전공", "name": "문은미"}, {"department": "실내디자인전공", "name": "박태욱"},
        {"department": "실내디자인전공", "name": "정수연"}, {"department": "텍스타일디자인전공", "name": "이은옥"},
        {"department": "텍스타일디자인전공", "name": "이재범"}, {"department": "텍스타일디자인전공", "name": "안소영"},
        # 미래인재대학
        {"department": "AI신약학과", "name": "이용수"}, {"department": "AI신약학과", "name": "이진우"},
        {"department": "AI신약학과", "name": "강성민"}, {"department": "AI신약학과", "name": "유제혁"},
        {"department": "AI신약학과", "name": "신현길"}, {"department": "가상현실융합학과", "name": "임양미"},
        {"department": "가상현실융합학과", "name": "나정조"}, {"department": "가상현실융합학과", "name": "임양규"},
        {"department": "가상현실융합학과", "name": "김영호"}, {"department": "가상현실융합학과", "name": "김현규"},
        {"department": "데이터사이언스학과", "name": "강남희"}, {"department": "데이터사이언스학과", "name": "유제혁"},
        {"department": "데이터사이언스학과", "name": "문지훈"}, {"department": "데이터사이언스학과", "name": "박성우"},
        {"department": "한국학전공", "name": "김성진"}, {"department": "한국학전공", "name": "최주희"},
        {"department": "한국학전공", "name": "김유진"},
    ]
    
    for prof in professor_list:
        Professor.objects.get_or_create(department=prof["department"], name=prof["name"])

def reverse_professors(apps, schema_editor):
    # 🌟 취소(Unapply) 명령을 내릴 때 DB에서 이 데이터들을 안전하게 지우는 역방향 함수
    Professor = apps.get_model('posts', 'Professor')
    Professor.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        # 🌟 팀원분의 5번 파일이 실행 완료된 직후에 이어서 실행되도록 완벽 정리!
        ('posts', '0005_alter_post_id_alter_postimage_id_alter_professor_id'),
    ]

    operations = [
        # 정방향 함수와 역방향 함수를 세트로 묶어서 주입합니다.
        migrations.RunPython(insert_professors, reverse_code=reverse_professors),
    ]
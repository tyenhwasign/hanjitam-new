import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import os
import base64

# Streamlit 페이지 기본 설정
st.set_page_config(
    page_title="2022개정 한국지리 백지도 퀴즈 앱",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("🗺️ 2022개정 한국지리 백지도 퀴즈 앱")
st.markdown("대한민국 백지도 위에 나타나는 📍 핀의 위치를 보고 올바른 지역 이름을 맞춰보세요!")
st.divider()

# 경로 설정
current_dir = Path(__file__).resolve().parent
html_file_path = current_dir / "htmls" / "index.html"
image_file_path = current_dir / "htmls" / "image.jpg"

if not html_file_path.exists():
    html_file_path = Path(os.getcwd()) / "htmls" / "index.html"
if not image_file_path.exists():
    image_file_path = Path(os.getcwd()) / "htmls" / "image.jpg"

# 파일 존재 여부 확인 후 처리
if html_file_path.exists() and image_file_path.exists():
    try:
        # 1. index.html 파일 읽기
        with open(html_file_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        # 2. image.jpg 파일을 읽어서 Base64(웹 안전 문자열)로 인코딩
        with open(image_file_path, "rb") as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode("utf-8")
        
        # 3. HTML 안에 들어있는 기존 주소인 src="./image.jpg" 부분을 데이터 문자열로 강제 치환
        # 이렇게 하면 서버 경로를 통하지 않고 이미지가 HTML 내부에 직접 박힙니다.
        embedded_img_src = f"data:image/jpeg;base64,{img_base64}"
        html_content = html_content.replace('src="./image.jpg"', f'src="{embedded_img_src}"')
        
        # 4. 안전하게 컴포넌트 출력
        components.html(html_content, height=850, scrolling=True)
        
    except Exception as e:
        st.error(f"⚠️ 오류가 발생했습니다. (내용: {e})")
else:
    st.warning("⚠️ 퀴즈 앱 필수 파일들을 찾을 수 없습니다.")
    st.markdown(
        f"""
        **현재 탐색된 경로:**
        - HTML 파일: `{html_file_path}` ({'존재함' if html_file_path.exists() else '없음'})
        - 이미지 파일: `{image_file_path}` ({'존재함' if image_file_path.exists() else '없음'})
        
        `htmls` 폴더 안에 `index.html`과 `image.jpg`가 대소문자까지 정확히 일치하게 들어있는지 다시 한번 확인 후 GitHub에 올려주세요!
        """
    )

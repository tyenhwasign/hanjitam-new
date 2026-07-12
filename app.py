import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import os
import base64

# Streamlit 페이지 설정
st.set_page_config(
    page_title="2022개정 한국지리 백지도 퀴즈 앱",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("🗺️ 2022개정 한국지리 백지도 퀴즈 앱")
st.markdown("대한민국 백지도 위에 나타나는 📍 핀의 위치를 보고 올바른 지역 이름을 맞춰보세요!")
st.divider()

# 최상위 루트 및 htmls 폴더 고정 경로 계산
base_path = Path(__file__).resolve().parent
html_folder = base_path / "htmls"

html_file_path = html_folder / "index.html"

# 파일명 대소문자 매칭 유연화 처리 (image.jpg, image.png, image.JPEG 등 자동 매색)
image_file_path = None
if html_folder.exists():
    for file in os.listdir(html_folder):
        if file.lower().startswith("image."):
            image_file_path = html_folder / file
            break

# 최종 검증 및 렌더링 시작
if html_file_path.exists() and image_file_path and image_file_path.exists():
    try:
        # 1. HTML 내용 읽기
        with open(html_file_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        # 2. 이미지 이진 데이터 base64 변환
        with open(image_file_path, "rb") as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode("utf-8")
        
        # 확장자에 따라 mime_type 맞춤 지정
        ext = image_file_path.suffix.lower()
        mime_type = "image/png" if ext == ".png" else "image/jpeg"
        embedded_src = f"data:{mime_type};base64,{img_base64}"
        
        # HTML 내부의 지도 소스 주소를 인코딩 데이터로 직접 강제 강제 주입
        html_content = html_content.replace('src="./image.jpg"', f'src="{embedded_src}"')
        
        # 3. 브라우저 컴포넌트로 송출
        components.html(html_content, height=850, scrolling=True)
        
    except Exception as e:
        st.error(f"⚠️ 시스템 연동 중 오류 발생: {e}")
else:
    st.warning("⚠️ 파일을 찾을 수 없습니다. 저장소 폴더 구조를 다시 점검해 주세요.")
    st.markdown(
        f"""
        **폴더 구조 필수 검크 리스트:**
        - `htmls` 폴더 내에 `index.html`이 올바르게 존재하는가? (결과: {'✅' if html_file_path.exists() else '❌'})
        - `htmls` 폴더 내에 `image.jpg` (혹은 png)가 존재하는가? (결과: {'✅' if (image_file_path and image_file_path.exists()) else '❌'})
        """
    )

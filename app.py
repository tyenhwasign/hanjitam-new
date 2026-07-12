import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import os

# Streamlit 페이지 기본 설정 (타이틀, 레이아웃)
st.set_page_config(
    page_title="2022개정 한국지리 백지도 퀴즈 앱",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 1. 상단 타이틀 및 소개 문구 노출
st.title("🗺️ 2022개정 한국지리 백지도 퀴즈 앱")
st.markdown("대한민국 백지도 위에 나타나는 📍 핀의 위치를 보고 올바른 지역 이름을 맞춰보세요!")
st.divider()

# 2. 다중 경로 탐색법 적용 (htmls/index.html 경로 찾기)
current_dir = Path(__file__).resolve().parent
html_file_path = current_dir / "htmls" / "index.html"

# 배포 환경 대비 fallback 경로 설정
if not html_file_path.exists():
    html_file_path = Path(os.getcwd()) / "htmls" / "index.html"

# 3. 파일 존재 여부 확인 및 조건별 렌더링
if html_file_path.exists():
    try:
        # index.html 파일 읽기
        with open(html_file_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        # [확인 완료] scrolling=True를 사용하여 오류를 방지하고 스크롤바를 지원합니다.
        # 지도와 퀴즈 폼이 잘리지 않도록 높이(height)를 850으로 여유 있게 설정했습니다.
        components.html(html_content, height=850, scrolling=True)
        
    except Exception as e:
        st.error(f"⚠️ 파일을 읽는 중 오류가 발생했습니다. (오류 내용: {e})")
else:
    # 파일이 없을 때 노출하는 친절한 안내 메시지
    st.warning("⚠️ 퀴즈 앱 구성 파일(`htmls/index.html`)을 찾을 수 없습니다.")
    st.markdown(
        f"""
        **현재 앱이 탐색한 경로:** `{html_file_path}`
        
        **올바른 저장소 폴더 구조를 확인해 주세요:**
        ```text
        내-웹앱/
        ├── app.py
        ├── requirements.txt
        └── htmls/
            ├── index.html   (이전에 만든 퀴즈 HTML 파일)
            └── image.jpg    (다운로드한 백지도 이미지 파일)
        ```
        `app.py` 파일과 같은 위치에 `htmls` 폴더가 있고, 그 내부에 `index.html`과 `image.jpg`가 함께 들어있는지 꼭 확인 후 GitHub에 올려주세요!
        """
    )

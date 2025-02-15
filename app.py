import streamlit as st
import yt_dlp
import random

# 🎯 유튜브 쇼츠 트렌드 분석 (제목 스타일, 해시태그 분석)
def get_shorts_trends(keyword, max_results=10):
    ydl_opts = {"quiet": True, "extract_flat": True, "force_generic_extractor": True}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        search_results = ydl.extract_info(f"ytsearch{max_results}: {keyword} Shorts", download=False)

    videos = []
    if "entries" in search_results:
        for entry in search_results["entries"]:
            videos.append({
                "제목": entry["title"],
                "영상 URL": entry["url"],
                "조회수": entry.get("view_count", 0),
                "해시태그": extract_hashtags(entry["title"])
            })

    return sorted(videos, key=lambda x: x["조회수"], reverse=True)

# 🎯 해시태그 추출 함수
def extract_hashtags(title):
    words = title.split()
    hashtags = [word for word in words if word.startswith("#")]
    return hashtags if hashtags else ["#유튜브트렌드", "#쇼츠인기"]

# 🎯 유튜브 SEO 최적화 (상위 검색 영상 분석)
def get_top_videos_for_seo(keyword, max_results=5):
    """유튜브 검색 상위 영상을 분석"""
    ydl_opts = {"quiet": True, "extract_flat": True, "force_generic_extractor": True}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        search_results = ydl.extract_info(f"ytsearch{max_results}: {keyword}", download=False)

    videos = []
    if "entries" in search_results:
        for entry in search_results["entries"]:
            # 🔥 설명이 None인 경우 "설명 없음"으로 처리
            description = entry.get("description", "설명 없음")
            if description is None:
                description = "설명 없음"
            else:
                description = description[:200] + "..."  # 설명 길이 제한

            videos.append({
                "제목": entry["title"],
                "영상 URL": entry["url"],
                "조회수": entry.get("view_count", 0),
                "설명": description
            })

    return sorted(videos, key=lambda x: x["조회수"], reverse=True)

# 🎯 유튜브 예상 수익 분석 (CPM 기반)
def calculate_youtube_earnings(views, cpm=2.0):
    earnings = (views / 1000) * cpm
    return round(earnings, 2)

# 🎯 유튜브 경쟁 채널 분석 (유사 채널 추천)
def recommend_competitor_channels(keyword, max_results=5):
    ydl_opts = {"quiet": True, "extract_flat": True, "force_generic_extractor": True}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        search_results = ydl.extract_info(f"ytsearch{max_results}: {keyword} 채널", download=False)

    channels = []
    if "entries" in search_results:
        for entry in search_results["entries"]:
            channels.append({
                "채널명": entry["title"],
                "채널 URL": entry["url"]
            })

    return channels

# 🎯 유튜브 최적화 가이드라인 (CTR 증가 전략)
def get_best_video_tips():
    tips = [
        "📌 제목을 짧고 강렬하게 (예: '🔥1시간 만에 100만 뷰?!')",
        "📌 영상 길이는 6~15분이 가장 이상적",
        "📌 썸네일에는 강렬한 표정과 대비된 색상을 활용",
        "📌 해시태그를 3~5개 정도 추가하면 노출 증가",
        "📌 첫 30초에 가장 중요한 내용을 넣어야 함"
    ]
    return random.sample(tips, 3)

# 🎯 Streamlit UI 설정
st.set_page_config(page_title="유튜브 크리에이터 분석 도구", layout="wide")

st.title("📊 유튜브 크리에이터 & 쇼츠 분석 시스템")

# 🔥 유튜브 쇼츠 트렌드 분석
st.subheader("🔥 유튜브 쇼츠 트렌드 분석")
shorts_keyword = st.text_input("🔍 인기 쇼츠 영상을 찾을 키워드를 입력하세요")

if st.button("📈 쇼츠 트렌드 분석 시작"):
    with st.spinner(f"'{shorts_keyword}' 관련 인기 쇼츠 영상 검색 중..."):
        shorts_trends = get_shorts_trends(shorts_keyword)

    if shorts_trends:
        for video in shorts_trends:
            st.markdown(f"""
                <div>
                    <p>🎬 <strong>{video['제목']}</strong></p>
                    <p>🔗 <a href="{video['영상 URL']}" target="_blank">{video['영상 URL']}</a></p>
                    <p>👀 조회수: {video['조회수']:,}회</p>
                    <p>🏷 해시태그: {' '.join(video['해시태그'])}</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("❌ 인기 쇼츠 영상을 찾을 수 없습니다.")

# 🔥 유튜브 SEO 최적화 분석
st.subheader("🔍 유튜브 SEO 최적화 분석")
seo_keyword = st.text_input("🔍 유튜브 검색 상위 영상을 분석할 키워드를 입력하세요")

if st.button("📊 SEO 분석 시작"):
    with st.spinner(f"'{seo_keyword}' 관련 인기 동영상 검색 중..."):
        seo_results = get_top_videos_for_seo(seo_keyword)

    if seo_results:
        for video in seo_results:
            st.markdown(f"""
                <div>
                    <p>🎬 <strong>{video['제목']}</strong></p>
                    <p>🔗 <a href="{video['영상 URL']}" target="_blank">{video['영상 URL']}</a></p>
                    <p>📊 조회수: {video['조회수']:,}회</p>
                    <p>📝 설명: {video['설명']}</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("❌ SEO 분석 결과를 찾을 수 없습니다.")

# 🔥 유튜브 예상 수익 계산기
st.subheader("💰 유튜브 예상 수익 계산기")
views = st.number_input("📊 예상 조회수 입력 (예: 1000000)", min_value=0)

if st.button("💵 예상 수익 계산"):
    earnings = calculate_youtube_earnings(views)
    st.success(f"📢 예상 유튜브 수익: ${earnings}")

# 🔥 유튜브 경쟁 채널 분석
st.subheader("📊 유튜브 라이벌 분석")
competitor_keyword = st.text_input("🔍 경쟁 채널을 찾을 키워드를 입력하세요")

if st.button("🏆 경쟁 채널 추천"):
    with st.spinner(f"'{competitor_keyword}' 관련 유사 채널 검색 중..."):
        competitors = recommend_competitor_channels(competitor_keyword)

    if competitors:
        for ch in competitors:
            st.markdown(f"📺 [{ch['채널명']}]({ch['채널 URL']})")
    else:
        st.warning("❌ 경쟁 채널을 찾을 수 없습니다.")

# 🔥 유튜브 최적화 가이드라인
st.subheader("🎯 유튜브 영상 최적화 가이드라인")
if st.button("📢 최적화 팁 보기"):
    tips = get_best_video_tips()
    for tip in tips:
        st.write(tip)

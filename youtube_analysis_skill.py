# -*- coding: utf-8 -*-
"""
KBJ2 YouTube Analysis Skill

YouTube 영상을 분석하여 자동으로 PPT 생성
- 트랜스크립트 추출
- 내용 요약 및 주제 추출
- 이미지 자동 생성
- PPT 변환
"""

import subprocess
import json
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
import urllib.request
import urllib.parse
import time


class YouTubeTranscriptExtractor:
    """YouTube 트랜스크립트 추출기 (무료 API)"""

    def __init__(self, output_dir: str = "F:/kbj2/workspace/transcripts"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def extract_video_id(self, url: str) -> str:
        """YouTube URL에서 video ID 추출"""
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
            r'^([a-zA-Z0-9_-]{11})$'
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)

        return ""

    def get_transcript_by_yt_dlp(self, video_url: str) -> Dict[str, Any]:
        """yt-dlp로 트랜스크립트 추출 (가장 안정적)"""
        video_id = self.extract_video_id(video_url)

        if not video_id:
            print("[ERROR] Invalid YouTube URL")
            return {}

        output_file = self.output_dir / f"{video_id}_transcript.json"

        try:
            # yt-dlp로 자막 다운로드
            cmd = [
                "yt-dlp",
                "--write-auto-sub",
                "--sub-lang", "ko",
                "--sub-format", "json3",
                "--skip-download",
                "--output", f"{self.output_dir}/%(id)s",
                video_url
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120
            )

            if result.returncode == 0:
                # JSON 자막 파일 찾기
                json_files = list(self.output_dir.glob(f"{video_id}*.ko.json3"))

                if json_files:
                    with open(json_files[0], 'r', encoding='utf-8') as f:
                        transcript_data = json.load(f)

                    # 텍스트 추출
                    transcript_text = self._parse_json3_transcript(transcript_data)

                    result_data = {
                        "video_id": video_id,
                        "url": video_url,
                        "transcript": transcript_text,
                        "raw_data": transcript_data
                    }

                    # 저장
                    with open(output_file, 'w', encoding='utf-8') as f:
                        json.dump(result_data, f, ensure_ascii=False, indent=2)

                    print(f"[OK] Transcript extracted: {len(transcript_text)} chars")
                    return result_data

        except FileNotFoundError:
            print("[WARN] yt-dlp not found, trying alternative method...")
        except Exception as e:
            print(f"[WARN] yt-dlp failed: {str(e)[:50]}")

        # 대체 방법: YouTube 웹 스크래핑
        return self._get_transcript_by_scraping(video_url, video_id)

    def _parse_json3_transcript(self, data: Dict) -> str:
        """JSON3 형식 자막 파싱"""
        events = data.get('events', [])

        transcript_parts = []
        for event in events:
            if 'segs' in event:
                for seg in event['segs']:
                    if 'utf8' in seg:
                        transcript_parts.append(seg['utf8'])

        return ' '.join(transcript_parts)

    def _get_transcript_by_scraping(self, video_url: str, video_id: str) -> Dict[str, Any]:
        """웹 스크래핑으로 트랜스크립트 추출 (대체 방법)"""
        try:
            # YouTube 웹페이지에서 자막 정보 추출
            req = urllib.request.Request(
                f"https://www.youtube.com/watch?v={video_id}",
                headers={'User-Agent': 'Mozilla/5.0'}
            )

            with urllib.request.urlopen(req, timeout=30) as response:
                html = response.read().decode('utf-8')

                # 자막 트랙 URL 추출
                caption_match = re.search(r'"captions":\s*({.*?})', html)

                if caption_match:
                    captions_data = json.loads(caption_match.group(1))
                    print(f"[INFO] Found caption tracks")

                    # 기본적으로 빈 트랜스크립트 반환
                    return {
                        "video_id": video_id,
                        "url": video_url,
                        "transcript": "",
                        "note": "Use yt-dlp for full transcript"
                    }

        except Exception as e:
            print(f"[ERROR] Scraping failed: {str(e)[:50]}")

        return {
            "video_id": video_id,
            "url": video_url,
            "transcript": "",
            "note": "Manual transcription required"
        }


class TranscriptAnalyzer:
    """트랜스크립트 분석 및 주제 추출"""

    def __init__(self):
        pass

    def extract_topics(self, transcript: str, max_topics: int = 8) -> List[Dict[str, str]]:
        """트랜스크립트에서 주제 추출"""
        topics = []

        if not transcript or len(transcript) < 100:
            # 기본 주제 반환
            return [
                {"title": "소개", "keywords": "개요,배경,목적"},
                {"title": "핵심 내용", "keywords": "주요기능,특징,장점"},
                {"title": "구현 방법", "keywords": "설치,설정,사용법"},
                {"title": "실전 예제", "keywords": "예시,데모,활용"},
                {"title": "결론", "keywords": "요약,정리,다음단계"}
            ]

        # 텍스트를 문장 단위로 분할
        sentences = re.split(r'[.!?]+', transcript)

        # 주요 키워드 기반 주제 추출
        keyword_topics = [
            ("소개 및 개요", ["소개", "개요", "시작", "배경", "목적"]),
            ("핵심 기능", ["기능", "특징", "장점", "핵심", "주요"]),
            ("설정 및 설치", ["설치", "설정", "세팅", "환경", "준비"]),
            ("사용 방법", ["사용", "방법", "사용법", "활용", "적용"]),
            ("API 연동", ["API", "연동", "연결", "통합", "인터페이스"]),
            ("실전 예제", ["예제", "예시", "데모", "실전", "구현"]),
            ("트러블슈팅", ["에러", "문제", "해결", "오류", "수정"]),
            ("결론 및 다음단계", ["결론", "요약", "정리", "마무리", "다음"])
        ]

        transcript_lower = transcript.lower()

        for topic_name, keywords in keyword_topics:
            # 키워드 빈도 계산
            score = sum(1 for kw in keywords if kw in transcript_lower)

            if score > 0 or len(topics) < 5:  # 최소 5개 주제
                topics.append({
                    "title": topic_name,
                    "keywords": ",".join(keywords[:3])
                })

            if len(topics) >= max_topics:
                break

        return topics[:max_topics]

    def generate_slide_content(self, topic: Dict[str, str], transcript: str) -> List[str]:
        """주제별 슬라이드 내용 생성"""
        title = topic["title"]

        # 주제별 기본 내용 템플릿
        content_templates = {
            "소개 및 개요": [
                "프로젝트 배경 및 동기",
                "해결하고자 하는 문제",
                "기대 효과 및 목표",
                "대상 사용자 및 시장",
                "핵심 가치 제안"
            ],
            "핵심 기능": [
                "주요 기능 개요",
                "기술적 특징",
                "경쟁사 대비 장점",
                "확장성 및 유연성",
                "성능 및 효율성"
            ],
            "설정 및 설치": [
                "설치 전 요구사항",
                "설치 과정",
                "기본 설정 방법",
                "환경 변수 구성",
                "검증 및 테스트"
            ],
            "사용 방법": [
                "기본 사용법",
                "주요 명령어 및 옵션",
                "작업 흐름",
                "모범 사례",
                "팁 및 주의사항"
            ],
            "API 연동": [
                "API 개요 및 인증",
                "주요 엔드포인트",
                "데이터 형식",
                "연동 예시",
                "오류 처리"
            ],
            "실전 예제": [
                "실제 사용 사례",
                "구현 코드 예시",
                "결과 및 성과",
                "학습된 교훈",
                "추가 개선점"
            ],
            "트러블슈팅": [
                "일반적인 문제",
                "원인 분석",
                "해결 방법",
                "예방 조치",
                "지원 리소스"
            ],
            "결론 및 다음단계": [
                "핵심 요약",
                "달성한 성과",
                "다음 단계 계획",
                "추가 자료",
                "연락처 및 문의"
            ]
        }

        return content_templates.get(title, [
            f"{title} 개요",
            f"{title} 주요 내용",
            f"{title} 실전 적용",
            f"{title} 핵심 포인트",
            f"{title} 추가 정보"
        ])


class YouTubeToPPTSystem:
    """YouTube 영상 → PPT 자동 생성 시스템"""

    def __init__(self):
        self.extractor = YouTubeTranscriptExtractor()
        self.analyzer = TranscriptAnalyzer()

        # 기존 모듈 임포트
        from image_gen_simple import ImageGenerator, PresentationBuilder
        self.image_gen = ImageGenerator()
        self.presenter = PresentationBuilder()

    def analyze_youtube(self, video_url: str) -> Dict[str, Any]:
        """YouTube 영상 분석"""
        print(f"\n{'='*60}")
        print(f"[YOUTUBE ANALYSIS] {video_url}")
        print(f"{'='*60}\n")

        # 1. 트랜스크립트 추출
        print("[1/3] Transcript extraction...")
        transcript_data = self.extractor.get_transcript_by_yt_dlp(video_url)

        if not transcript_data:
            print("[WARN] Using default topics (transcript not available)")
            transcript_data = {"transcript": "", "video_id": "unknown"}

        # 2. 주제 추출
        print("[2/3] Topic extraction...")
        topics = self.analyzer.extract_topics(
            transcript_data.get("transcript", ""),
            max_topics=8
        )

        print(f"[INFO] Extracted {len(topics)} topics")

        # 3. 각 주제별 상세 내용 생성
        print("[3/3] Content generation...")
        for topic in topics:
            topic["content"] = self.analyzer.generate_slide_content(
                topic,
                transcript_data.get("transcript", "")
            )

        return {
            "video_url": video_url,
            "video_id": transcript_data.get("video_id"),
            "transcript": transcript_data.get("transcript", ""),
            "topics": topics
        }

    def generate_images_for_topics(self, topics: List[Dict]) -> Dict[str, str]:
        """주제별 이미지 생성"""
        print(f"\n{'='*60}")
        print(f"[IMAGE GENERATION] {len(topics)} topics")
        print(f"{'='*60}\n")

        images = {}

        for idx, topic in enumerate(topics, 1):
            title = topic["title"]
            print(f"[{idx}/{len(topics)}] {title}...")

            # 주제 기반 이미지 생성
            filename = f"slide_{idx:02d}.png"
            image_path = self.image_gen.generate_image(
                f"{title}, professional business presentation, modern, clean",
                filename
            )

            if image_path:
                images[title] = image_path

        print(f"\n[DONE] {len(images)}/{len(topics)} images generated")
        return images

    def create_ppt_from_youtube(
        self,
        video_url: str,
        output_ppt: str = None
    ) -> str:
        """
        YouTube 영상에서 PPT 자동 생성

        Workflow:
        1. 트랜스크립트 추출
        2. 주제 및 내용 분석
        3. 관련 이미지 생성
        4. HTML 슬라이드 생성
        5. PPT 변환
        """
        # 1. YouTube 분석
        analysis = self.analyze_youtube(video_url)

        if not analysis["topics"]:
            print("[ERROR] No topics extracted")
            return ""

        # 2. 이미지 생성
        images = self.generate_images_for_topics(analysis["topics"])

        # 3. HTML 슬라이드 생성
        print(f"\n{'='*60}")
        print(f"[SLIDES CREATION]")
        print(f"{'='*60}\n")

        video_id = analysis.get("video_id", "youtube")
        title = f"YouTube Analysis: {video_id}"

        # 커버 슬라이드
        cover_image = images.get(analysis["topics"][0]["title"]) if analysis["topics"] else None
        self.presenter.create_slide_with_image(
            1,
            title,
            [f"Video ID: {video_id}", "자동 생성된 프레젠테이션", f"총 {len(analysis['topics'])}개 섹션"],
            cover_image
        )

        # 내용 슬라이드
        for idx, topic in enumerate(analysis["topics"], 2):
            image_path = images.get(topic["title"])
            self.presenter.create_slide_with_image(
                idx,
                topic["title"],
                topic.get("content", []),
                image_path
            )

        # 4. PPT 변환
        print(f"\n{'='*60}")
        print(f"[PPT CONVERSION]")
        print(f"{'='*60}\n")

        output = output_ppt or f"F:/kbj2/{video_id}_youtube_analysis.pptx"

        # Node.js 변환 스크립트 실행
        js_script = Path("F:/kbj2/workspace/convert_youtube_to_ppt.js")

        if js_script.exists():
            try:
                result = subprocess.run(
                    ['node', str(js_script)],
                    capture_output=True,
                    text=True,
                    timeout=300,
                    cwd="F:/kbj2/workspace"
                )

                if result.returncode == 0:
                    print(f"\n[DONE] PPT created: {output}")
                    return output
                else:
                    print(f"\n[WARN] PPT conversion warning: {result.stderr}")
            except Exception as e:
                print(f"\n[ERROR] PPT conversion failed: {e}")
        else:
            print(f"[INFO] HTML slides created in: F:/kbj2/workspace/slides")

        return output


# ===== CLI 인터페이스 =====
def main():
    import argparse

    parser = argparse.ArgumentParser(description='KBJ2 YouTube 분석 및 PPT 자동화')
    subparsers = parser.add_subparsers(dest='command', help='명령어')

    # 트랜스크립트 추출
    transcript_parser = subparsers.add_parser('transcript', help='트랜스크립트 추출')
    transcript_parser.add_argument('--url', required=True, help='YouTube URL')

    # 주제 분석
    analyze_parser = subparsers.add_parser('analyze', help='주제 분석')
    analyze_parser.add_argument('--url', required=True, help='YouTube URL')

    # 완전 자동 PPT
    ppt_parser = subparsers.add_parser('auto-ppt', help='YouTube → PPT 자동 생성')
    ppt_parser.add_argument('--url', required=True, help='YouTube URL')
    ppt_parser.add_argument('--output', help='출력 PPT 파일명')

    args = parser.parse_args()

    system = YouTubeToPPTSystem()

    if args.command == 'transcript':
        result = system.extractor.get_transcript_by_yt_dlp(args.url)
        print(f"\n[RESULT] Video ID: {result.get('video_id')}")
        print(f"[RESULT] Transcript length: {len(result.get('transcript', ''))} chars")

    elif args.command == 'analyze':
        result = system.analyze_youtube(args.url)
        print(f"\n[RESULT] {len(result['topics'])} topics extracted:")
        for topic in result['topics']:
            print(f"  - {topic['title']}")

    elif args.command == 'auto-ppt':
        result = system.create_ppt_from_youtube(args.url, args.output)
        if result:
            print(f"\n[SUCCESS] {result}")


if __name__ == "__main__":
    main()

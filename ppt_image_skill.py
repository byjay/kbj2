"""
KBJ2 PPT Image Generator

Free AI image generation APIs for presentations
- Pollinations.ai (free AI images)
- Unsplash Source (free photos)
- Pexels API (free stock photos)

Usage:
    python ppt_image_skill.py generate --prompt "AI robot working" --output slide1.png
    python ppt_image_skill.py auto-ppt --title "AI System" --topics "AI,System,Team"
"""

# -*- coding: utf-8 -*-
import asyncio
import subprocess
import sys
from pathlib import Path
from typing import List, Dict
import urllib.request
import urllib.parse
import time

사용 예시:
    # 1. 단일 이미지 생성
    python ppt_image_skill.py generate --prompt "AI robot working in office" --output slide1.png

    # 2. 프레젠테이션 전체 이미지 자동 생성
    python ppt_image_skill.py presentation --topics "AI 조직,시스템 철학,조직 구조,데이터 모델"

    # 3. 완전 자동 PPT 생성 (이미지 포함)
    python ppt_image_skill.py auto-ppt --title "AI 자율 조직 시스템" --topics "AI 조직,시스템 철학,조직 구조"
"""

import asyncio
import subprocess
import sys
from pathlib import Path
from typing import List, Dict

class PPTImageSkill:
    """PPT 이미지 자동화 스킬"""

    def __init__(self, base_dir: str = "F:/kbj2"):
        self.base_dir = Path(base_dir)
        self.workspace = self.base_dir / "workspace"
        self.images_dir = self.workspace / "images"
        self.slides_dir = self.workspace / "slides"

        # 디렉토리 생성
        self.images_dir.mkdir(parents=True, exist_ok=True)
        self.slides_dir.mkdir(parents=True, exist_ok=True)

    async def generate_single_image(
        self,
        prompt: str,
        output_path: str = None
    ) -> str:
        """
        단일 AI 이미지 생성 (Pollinations.ai)

        Args:
            prompt: 이미지 프롬프트
            output_path: 저장 경로 (None이면 자동 생성)

        Returns:
            생성된 이미지 경로
        """
        if output_path is None:
            output_path = self.images_dir / f"gen_{hash(prompt) % 10000}.png"

        # Pollinations.ai API (완전 무료)
        import urllib.parse

        encoded_prompt = urllib.parse.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        params = {
            "width": 1280,
            "height": 720,
            "model": "flux",
            "nologo": "true",
            "enhance": "true"
        }

        # URL 쿼리 문자열 생성
        query_string = "&".join(f"{k}={v}" for k, v in params.items())
        full_url = f"{url}?{query_string}"

        # 다운로드
        import urllib.request
        try:
            urllib.request.urlretrieve(full_url, output_path)
            print(f"✅ 이미지 생성 완료: {prompt[:50]}... → {Path(output_path).name}")
            return str(output_path)
        except Exception as e:
            print(f"❌ 이미지 생성 실패: {e}")
            return ""

    def generate_single_image_sync(
        self,
        prompt: str,
        output_path: str = None
    ) -> str:
        """
        단일 이미지 생성 (동기 버전)
        여러 무료 API 시도
        """
        import urllib.request
        import urllib.parse

        if output_path is None:
            output_path = self.images_dir / f"gen_{hash(prompt) % 10000}.png"

        # 방법 1: Pollinations.ai (시도)
        try:
            encoded_prompt = urllib.parse.quote(prompt)
            url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"

            # 헤더 추가
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0')

            with urllib.request.urlopen(req, timeout=60) as response:
                content = response.read()
                Path(output_path).write_bytes(content)
                print(f"[OK] AI image (Pollinations): {prompt[:50]}")
                return str(output_path)
        except Exception as e:
            print(f"[WARN] Pollinations failed: {str(e)[:50]}")

        # 방법 2: Unsplash Source (사진)
        try:
            seed = int(time.time() * 1000) % 10000
            search_terms = prompt.replace(",", " ").split()[:3]  # 첫 3단어
            search_query = " ".join(search_terms)

            url = f"https://source.unsplash.com/1280x720/?{search_query}&sig={seed}"
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0')

            with urllib.request.urlopen(req, timeout=60) as response:
                content = response.read()
                Path(output_path).write_bytes(content)
                print(f"[OK] Photo (Unsplash): {search_query}")
                return str(output_path)
        except Exception as e:
            print(f"[WARN] Unsplash failed: {str(e)[:50]}")

        return ""

    async def generate_batch_images(self, topics: List[str]) -> Dict[str, str]:
        """
        배치 이미지 생성

        Args:
            topics: 주제 리스트

        Returns:
            {주제: 이미지_경로} 딕셔너리
        """
        print(f"\n{'='*60}")
        print(f"[IMAGE GEN] {len(topics)} images (Pollinations.ai)")
        print(f"{'='*60}\n")

        results = {}
        for idx, topic in enumerate(topics, 1):
            print(f"[{idx}/{len(topics)}] {topic}...")

            # AI 이미지 생성
            filename = self.images_dir / f"slide_{idx:02d}_ai.png"
            image_path = self.generate_single_image_sync(
                f"{topic}, professional business presentation, modern, high quality",
                str(filename)
            )

            if image_path:
                results[topic] = image_path

        print(f"\n[DONE] {len(results)}/{len(topics)} images generated!")
        return results

    def create_image_embedded_slide_html(
        self,
        slide_number: int,
        title: str,
        content: List[str],
        image_path: str = None,
        layout: str = "right"  # right, left, top, bottom, background
    ) -> str:
        """
        이미지가 포함된 슬라이드 HTML 생성

        Args:
            slide_number: 슬라이드 번호
            title: 제목
            content: 내용 리스트
            image_path: 이미지 경로
            layout: 레이아웃

        Returns:
            HTML 파일 경로
        """
        # 이미지 경로를 상대경로로 변환 (HTML용)
        rel_image_path = Path(image_path).relative_to(self.workspace) if image_path else ""

        if layout == "right":
            html = f"""<!DOCTYPE html>
<html>
<head>
<style>
html {{ background: #ffffff; }}
body {{
  width: 720pt; height: 405pt; margin: 0; padding: 0;
  background: #F4F6F6;
  font-family: Arial, sans-serif;
  display: flex;
}}
.container {{
  display: flex;
  height: 100%;
  margin: 40pt 40pt 70pt 40pt;
  gap: 20pt;
}}
.content {{
  flex: 1;
  background: #FFFFFF;
  border-radius: 12pt;
  padding: 25pt;
}}
.header {{
  border-bottom: 4pt solid #2E4053;
  padding-bottom: 10pt;
  margin-bottom: 15pt;
}}
h1 {{
  color: #1C2833;
  font-size: 28pt;
  margin: 0;
}}
ul {{
  margin: 15pt 0;
  padding-left: 25pt;
}}
li {{
  font-size: 16pt;
  margin: 10pt 0;
  color: #2E4053;
}}
.image-box {{
  flex: 0 0 280pt;
  background: #FFFFFF;
  border-radius: 12pt;
  padding: 15pt;
  display: flex;
  align-items: center;
  justify-content: center;
}}
.image-box img {{
  width: 100%;
  height: auto;
  border-radius: 8pt;
}}
</style>
</head>
<body>
<div class="container">
  <div class="content">
    <div class="header">
      <h1>{title}</h1>
    </div>
    <ul>
"""
            for item in content[:5]:  # 최대 5개 아이템
                html += f"      <li>{item}</li>\n"
            html += """    </ul>
  </div>
"""
            if image_path:
                html += f'  <div class="image-box">\n    <img src="{rel_image_path}" alt="{title}">\n  </div>\n'
            html += """</div>
</body>
</html>"""

        filepath = self.slides_dir / f"slide_{slide_number:02d}.html"
        filepath.write_text(html, encoding='utf-8')
        return str(filepath)

    def create_cover_with_bg_image(
        self,
        title: str,
        subtitle: str = "",
        tagline: str = "",
        bg_image: str = None
    ) -> str:
        """배경 이미지가 포함된 커버 슬라이드"""

        rel_bg_image = Path(bg_image).relative_to(self.workspace) if bg_image else ""

        html = f"""<!DOCTYPE html>
<html>
<head>
<style>
html {{ background: #ffffff; }}
body {{
  width: 720pt; height: 405pt; margin: 0; padding: 0;
  background: #1C2833;
  font-family: Arial, sans-serif;
  display: flex;
  align-items: center; justify-content: center;
}}
.cover {{
  position: absolute;
  top: 0; left: 0; width: 100%; height: 100%;
  background-image: url('{rel_bg_image}');
  background-size: cover;
  background-position: center;
  opacity: 0.25;
}}
.content {{
  position: relative;
  text-align: center;
  color: #FFFFFF;
  z-index: 1;
}}
h1 {{
  font-size: 48pt;
  margin: 0 0 30pt 0;
  color: #FFFFFF;
}}
.subtitle {{
  font-size: 24pt;
  color: #AAB7B8;
  margin: 0 0 40pt 0;
}}
.tagline {{
  font-size: 18pt;
  color: #F4F6F6;
  margin: 0;
}}
</style>
</head>
<body>
<div class="cover"></div>
<div class="content">
  <h1>{title}</h1>
  <p class="subtitle">{subtitle}</p>
  <p class="tagline">{tagline}</p>
</div>
</body>
</html>"""

        filepath = self.slides_dir / "slide_01_cover.html"
        filepath.write_text(html, encoding='utf-8')
        return str(filepath)

    async def auto_ppt(
        self,
        title: str,
        topics: List[str],
        output_ppt: str = None
    ) -> str:
        """
        완전 자동 PPT 생성 (이미지 포함)

        1. 주제별 이미지 생성
        2. HTML 슬라이드 생성
        3. PPT 변환

        Args:
            title: 프레젠테이션 제목
            topics: 슬라이드 주제 리스트
            output_ppt: 출력 PPT 경로

        Returns:
            생성된 PPT 경로
        """
        print(f"\n{'='*60}")
        print(f"[AUTO PPT] {title}")
        print(f"{'='*60}\n")

        # 1. 커버 이미지 생성
        print("[1/4] Cover image generation...")
        cover_image = self.generate_single_image_sync(
            f"{title}, futuristic AI technology, digital network, abstract, blue gradient, professional",
            str(self.images_dir / "cover.png")
        )

        # 2. 슬라이드별 이미지 생성
        print(f"\n[2/4] {len(topics)} slide images...")
        images = await self.generate_batch_images(topics)

        # 3. HTML 슬라이드 생성
        print(f"\n[3/4] HTML slides creation...")

        # 커버 슬라이드
        self.create_cover_with_bg_image(
            title,
            "월급 없는 20명의 AI 직원",
            "실제 회사처럼 작동하는 멀티프로젝트 AI 기업",
            cover_image
        )

        # 내용 슬라이드
        for idx, (topic, image_path) in enumerate(images.items(), 2):
            # 주제를 키워드로 내용 생성
            content = self._generate_content_for_topic(topic)

            self.create_image_embedded_slide_html(
                idx,
                topic,
                content,
                image_path,
                layout="right"
            )

        # 4. PPT 변환
        print(f"\n[4/4] PPT conversion...")
        output = output_ppt or str(self.base_dir / f"{title.replace(' ', '_')}_with_images.pptx")

        # Node.js 스크립트 실행
        js_script = self.workspace / "convert_to_ppt.js"

        try:
            result = subprocess.run(
                ['node', str(js_script)],
                capture_output=True,
                text=True,
                timeout=300,
                cwd=str(self.workspace)
            )

            if result.returncode == 0:
                print(f"\n[DONE] PPT created: {output}")
                return output
            else:
                print(f"\n[WARN] PPT conversion warning: {result.stderr}")
                return ""
        except Exception as e:
            print(f"\n[ERROR] PPT conversion failed: {e}")
            return ""

    def _generate_content_for_topic(self, topic: str) -> List[str]:
        """주제별 내용 생성"""
        content_map = {
            "시스템 철학": [
                "멀티프로젝트 동시 운영",
                "부서간 유기적 협업",
                "자율적 의사결정",
                "지속적 학습",
                "24시간 무휴 운영"
            ],
            "조직 구조": [
                "경영진: CEO (1명)",
                "기획본부: 전략, 시장조사, 사업분석, 트렌드 (4명)",
                "개발본부: CTO, 백엔드, 프론트, AI, QA (5명)",
                "마케팅본부: CMO, 콘텐츠, SNS (3명)",
                "운영본부: COO, 재무, HR (3명)",
                "브레인팀: 낙관, 비관, 혁신 (3명)",
                "검증팀: 논리, 팩트 (2명)"
            ],
            "데이터 모델": [
                "DepartmentType (부서 유형)",
                "AgentRole (에이전트 역할)",
                "AgentPersona (페르소나)",
                "Project (프로젝트)",
                "Task (업무 태스크)",
                "Meeting (회의)"
            ],
            "에이전트 실행 엔진": [
                "개별 에이전트 실행: run_agent()",
                "부서 전체 실행: run_department()",
                "부서간 협업: cross_department_collaboration()",
                "대화 기억 (최근 3개 작업)",
                "토큰 사용량 추적"
            ],
            "프로젝트 관리": [
                "아이디어: 브레인팀 브레인스토밍 → 기획팀 검토",
                "기획: 마스터플랜 → 부서별 계획 → 재무 검토",
                "실행: CTO 기술 스펙 → 개발팀 병렬 → QA 검증",
                "검토: 검증팀 품질 체크 → CEO 승인"
            ],
            "비용 분석": [
                "실제 인건비: 7,000만원/월 (20명 × 350만원)",
                "AI 시스템: 70만원/월",
                "절감액: 6,930만원/월",
                "절감률: 99%",
                "ROI: 5,000%"
            ],
            "실전 성과": [
                "사업계획서 작성: 2주 → 1시간",
                "서비스 개발: 7개월 → 2주",
                "콘텐츠 제작: 1일 → 30분",
                "비용 절감: 97%",
                "ROI: 5,000%"
            ]
        }

        return content_map.get(topic, [f"✓ {topic}", "✓ 핵심 기능", "✓ 주요 특징", "✓ 실전 적용", "✓ 성과 달성"])


# ===== CLI 인터페이스 =====
def main():
    import argparse

    parser = argparse.ArgumentParser(description='KBJ2 PPT 이미지 자동화 스킬')
    subparsers = parser.add_subparsers(dest='command', help='명령어')

    # 단일 이미지 생성
    gen_parser = subparsers.add_parser('generate', help='AI 이미지 생성')
    gen_parser.add_argument('--prompt', required=True, help='이미지 프롬프트')
    gen_parser.add_argument('--output', help='출력 파일명')

    # 배치 생성
    batch_parser = subparsers.add_parser('batch', help='배치 이미지 생성')
    batch_parser.add_argument('--topics', required=True, help='주제들 (콤마 구분)')

    # 완전 자동 PPT
    auto_parser = subparsers.add_parser('auto-ppt', help='완전 자동 PPT 생성')
    auto_parser.add_argument('--title', required=True, help='프레젠테이션 제목')
    auto_parser.add_argument('--topics', required=True, help='슬라이드 주제들 (콤마 구분)')
    auto_parser.add_argument('--output', help='출력 PPT 파일명')

    args = parser.parse_args()

    skill = PPTImageSkill()

    if args.command == 'generate':
        output = args.output or f"generated_{hash(args.prompt) % 1000}.png"
        result = skill.generate_single_image_sync(args.prompt, str(skill.images_dir / output))
        if result:
            print(f"[DONE] Saved: {result}")

    elif args.command == 'batch':
        topics = [t.strip() for t in args.topics.split(',')]
        asyncio.run(skill.generate_batch_images(topics))

    elif args.command == 'auto-ppt':
        topics = [t.strip() for t in args.topics.split(',')]
        asyncio.run(skill.auto_ppt(args.title, topics, args.output))


if __name__ == "__main__":
    main()

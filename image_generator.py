"""
Image Generation Module for KBJ2 Presentation System
Supports multiple free image generation APIs
"""

import asyncio
import aiohttp
import os
from typing import Optional, Dict, Any, List
from pathlib import Path

class ImageGenerator:
    """Multi-provider free image generation"""

    def __init__(self, output_dir: str = "F:/kbj2/workspace/images"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def generate_with_pollinations(
        self,
        prompt: str,
        filename: str,
        width: int = 1024,
        height: int = 768,
        model: str = "flux"
    ) -> str:
        """
        Pollinations.ai - 완전 무료, API 키 불필요
        Model: flux, turbo, sfw
        """
        url = f"https://image.pollinations.ai/prompt/{prompt}"

        # 파라미터 인코딩
        params = {
            "width": width,
            "height": height,
            "model": model,
            "nologo": "true",
            "enhance": "true"
        }

        filepath = self.output_dir / filename

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as resp:
                if resp.status == 200:
                    content = await resp.read()
                    filepath.write_bytes(content)
                    print(f"✅ 이미지 생성 완료: {filename}")
                    return str(filepath)
                else:
                    print(f"❌ 이미지 생성 실패: {resp.status}")
                    return ""

    async def search_unsplash(
        self,
        query: str,
        filename: str,
        orientation: str = "landscape"
    ) -> str:
        """
        Unsplash Source - 무료 사진 (API 키 필요 없음)
        """
        url = f"https://source.unsplash.com/1600x900/?{query}&sig={hash(query)}"

        filepath = self.output_dir / filename

        async with aiohttp.ClientSession() as session:
            async with session.get(url, allow_redirects=True) as resp:
                if resp.status == 200:
                    content = await resp.read()
                    filepath.write_bytes(content)
                    print(f"✅ 사진 다운로드 완료: {filename}")
                    return str(filepath)
                else:
                    print(f"❌ 사진 다운로드 실패: {resp.status}")
                    return ""

    async def generate_slide_images(
        self,
        slide_topic: str,
        slide_number: int
    ) -> Dict[str, str]:
        """
        슬라이드 주제에 맞는 이미지 자동 생성
        """
        images = {}

        # Pollinations로 AI 생성 이미지
        ai_prompt = f"{slide_topic}, professional, modern, business presentation style, high quality"
        ai_filename = f"slide_{slide_number:02d}_ai.png"
        ai_path = await self.generate_with_pollinations(
            ai_prompt,
            ai_filename,
            width=1280,
            height=720
        )
        if ai_path:
            images["ai_generated"] = ai_path

        # Unsplash에서 관련 사진
        photo_filename = f"slide_{slide_number:02d}_photo.jpg"
        photo_path = await self.search_unsplash(
            slide_topic,
            photo_filename
        )
        if photo_path:
            images["photo"] = photo_path

        return images

    async def generate_presentation_cover(
        self,
        title: str,
        filename: str = "cover_image.png"
    ) -> str:
        """프레젠테이션 커버 이미지 생성"""
        prompt = f"{title}, futuristic AI technology, digital network, abstract business background, professional, blue gradient, high quality"

        filepath = self.output_dir / filename
        path = await self.generate_with_pollinations(
            prompt,
            filename,
            width=1920,
            height=1080
        )
        return path

    async def generate_section_headers(
        self,
        sections: List[str]
    ) -> Dict[str, str]:
        """섹션별 헤더 이미지 생성"""
        results = {}

        for idx, section in enumerate(sections):
            prompt = f"{section}, professional business icon, minimal design, modern, clean background"
            filename = f"section_{idx+1:02d}_header.png"
            path = await self.generate_with_pollinations(
                prompt,
                filename,
                width=800,
                height=400
            )
            if path:
                results[section] = path

        return results


class PresentationImageBuilder:
    """이미지가 포함된 PPT 생성기"""

    def __init__(self, image_gen: ImageGenerator = None):
        self.image_gen = image_gen or ImageGenerator()
        self.slides_dir = Path("F:/kbj2/workspace/slides")
        self.slides_dir.mkdir(parents=True, exist_ok=True)

    async def create_slide_with_image(
        self,
        slide_number: int,
        title: str,
        content: List[str],
        image_position: str = "right"  # left, right, top, bottom, background
    ) -> str:
        """
        이미지가 포함된 슬라이드 HTML 생성
        """
        # 이미지 생성
        images = await self.image_gen.generate_slide_images(title, slide_number)
        image_path = images.get("ai_generated") or images.get("photo", "")

        # HTML 템플릿
        if image_position == "right":
            html_content = f"""<!DOCTYPE html>
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
  margin: 40pt;
  gap: 20pt;
}}
.content {{
  flex: 1;
  background: #FFFFFF;
  border-radius: 12pt;
  padding: 30pt;
}}
.header {{
  border-bottom: 4pt solid #2E4053;
  padding-bottom: 10pt;
  margin-bottom: 20pt;
}}
h1 {{
  color: #1C2833;
  font-size: 32pt;
  margin: 0;
}}
ul {{
  margin: 20pt 0;
  padding-left: 30pt;
}}
li {{
  font-size: 18pt;
  margin: 12pt 0;
  color: #2E4053;
}}
.image-container {{
  flex: 0 0 280pt;
  display: flex;
  align-items: center;
  justify-content: center;
}}
.image-container img {{
  width: 100%;
  height: auto;
  border-radius: 12pt;
  box-shadow: 0 4pt 20pt rgba(0,0,0,0.15);
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
            for item in content:
                html_content += f"      <li>{item}</li>\n"
            html_content += """    </ul>
  </div>
"""
            if image_path:
                html_content += f'  <div class="image-container">\n    <img src="{image_path}" alt="{title}">\n  </div>\n'
            html_content += "</div>\n</body>\n</html>"

        filepath = self.slides_dir / f"slide_{slide_number:02d}.html"
        filepath.write_text(html_content, encoding='utf-8')
        return str(filepath)

    async def create_cover_slide(
        self,
        main_title: str,
        subtitle: str,
        tagline: str
    ) -> str:
        """커버 슬라이드 생성 (배경 이미지 포함)"""

        # 커버 이미지 생성
        cover_image = await self.image_gen.generate_presentation_cover(main_title)

        html_content = f"""<!DOCTYPE html>
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
  position: relative;
}}
.cover-bg {{
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background-image: url('{cover_image}');
  background-size: cover;
  background-position: center;
  opacity: 0.3;
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
<div class="cover-bg"></div>
<div class="content">
  <h1>{main_title}</h1>
  <p class="subtitle">{subtitle}</p>
  <p class="tagline">{tagline}</p>
</div>
</body>
</html>
"""

        filepath = self.slides_dir / "slide_01_cover.html"
        filepath.write_text(html_content, encoding='utf-8')
        return str(filepath)


# ===== CLI 인터페이스 =====
async def generate_images_for_presentation(topics: List[str]):
    """프레젠테이션용 이미지 일괄 생성"""
    gen = ImageGenerator()

    print(f"🎨 {len(topics)}개 슬라이드용 이미지 생성 시작...")

    tasks = []
    for idx, topic in enumerate(topics, 1):
        task = gen.generate_slide_images(topic, idx)
        tasks.append(task)

    results = await asyncio.gather(*tasks)

    print(f"\n✅ 모든 이미지 생성 완료!")
    return results


# ===== 사용 예제 =====
async def main():
    """테스트 실행"""

    # 1. 이미지 생성 테스트
    gen = ImageGenerator()

    # AI 생성 이미지
    await gen.generate_with_pollinations(
        "futuristic AI robot working on computer, professional",
        "test_ai.png"
    )

    # Unsplash 사진
    await gen.search_unsplash(
        "business team meeting",
        "test_photo.jpg"
    )

    # 2. 슬라이드 생성 테스트
    builder = PresentationImageBuilder(gen)

    # 커버 슬라이드
    await builder.create_cover_slide(
        "AI 자율 조직 시스템",
        "20명의 AI 직원이 24시간 작업",
        "지금 바로 시작하세요"
    )

    # 이미지 포함 슬라이드
    await builder.create_slide_with_image(
        2,
        "시스템 철학",
        [
            "멀티프로젝트 동시 운영",
            "부서간 유기적 협업",
            "자율적 의사결정",
            "지속적 학습",
            "24시간 무휴 운영"
        ]
    )

    print("\n✅ 테스트 완료!")


if __name__ == "__main__":
    asyncio.run(main())

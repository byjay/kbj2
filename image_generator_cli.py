"""
KBJ2 PPT 이미지 생성 스킬

무료 이미지 생성 API를 활용하여 PPT에 자동으로 이미지를 삽입합니다.

지원되는 API:
1. Pollinations.ai - 완전 무료 AI 이미지 생성 (API 키 불필요)
2. Unsplash Source - 무료 고품질 사진 (API 키 불필요)
3. Pexels API - 무료 스톡 사진 (API 키 필요)

사용법:
    python image_generator.py --generate "AI robot working" --output slide1.png
    python image_generator.py --search "business meeting" --output photo1.jpg
    python image_generator.py --presentation "프로젝트 주제1,주제2,주제3"
"""

import asyncio
import aiohttp
import argparse
import sys
from pathlib import Path
from typing import List, Dict

class ImageGenerator:
    """다중 무료 이미지 생성 API"""

    def __init__(self, output_dir: str = "F:/kbj2/workspace/images"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def generate_with_pollinations(
        self,
        prompt: str,
        width: int = 1280,
        height: int = 720,
        model: str = "flux"
    ) -> str:
        """
        Pollinations.ai로 AI 이미지 생성
        - 완전 무료
        - API 키 불필요
        - 고화질 AI 이미지
        """
        # URL 인코딩된 프롬프트
        encoded_prompt = prompt.replace(" ", "%20").replace(",", "%2C")

        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        params = {
            "width": width,
            "height": height,
            "model": model,
            "nologo": "true",
            "enhance": "true",
            "private": "true"
        }

        filename = self.output_dir / f"gen_{hash(prompt) % 10000}.png"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as resp:
                    if resp.status == 200:
                        content = await resp.read()
                        filename.write_bytes(content)
                        print(f"✅ AI 이미지 생성: {prompt[:50]}...")
                        return str(filename)
                    else:
                        print(f"❌ 생성 실패 ({resp.status}): {prompt[:50]}")
                        return ""
        except Exception as e:
            print(f"❌ 에러: {e}")
            return ""

    async def search_unsplash(self, query: str) -> str:
        """
        Unsplash에서 고품질 사진 검색
        - 완전 무료
        - API 키 불필요
        """
        # 랜덤 시드로 중복 방지
        import time
        seed = int(time.time() * 1000) % 10000

        url = f"https://source.unsplash.com/1600x900/?{query}&sig={seed}"

        filename = self.output_dir / f"photo_{hash(query) % 10000}.jpg"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, allow_redirects=True) as resp:
                    if resp.status == 200:
                        content = await resp.read()
                        filename.write_bytes(content)
                        print(f"✅ 사진 다운로드: {query}")
                        return str(filename)
                    else:
                        print(f"❌ 다운로드 실패: {query}")
                        return ""
        except Exception as e:
            print(f"❌ 에러: {e}")
            return ""

    async def generate_for_slide(self, topic: str, slide_num: int) -> Dict[str, str]:
        """슬라이드용 이미지 자동 생성"""
        results = {}

        # AI 생성 이미지
        ai_image = await self.generate_with_pollinations(
            f"{topic}, professional business presentation, modern, clean"
        )
        if ai_image:
            results["ai"] = ai_image

        # 관련 사진
        photo = await self.search_unsplash(topic)
        if photo:
            results["photo"] = photo

        return results

    async def generate_batch(self, topics: List[str]) -> Dict[str, Dict[str, str]]:
        """일괄 이미지 생성"""
        print(f"\n{'='*60}")
        print(f"🎨 {len(topics)}개 주제용 이미지 생성 시작")
        print(f"{'='*60}\n")

        tasks = []
        for idx, topic in enumerate(topics, 1):
            task = self.generate_for_slide(topic, idx)
            tasks.append((topic, task))

        results = {}
        for topic, task in tasks:
            result = await task
            results[topic] = result

        print(f"\n✅ 모든 이미지 생성 완료!")
        return results


async def main():
    parser = argparse.ArgumentParser(description='KBJ2 무료 이미지 생성 스킬')
    subparsers = parser.add_subparsers(dest='command', help='명령어')

    # 단일 AI 이미지 생성
    gen_parser = subparsers.add_parser('generate', help='AI 이미지 생성')
    gen_parser.add_argument('--prompt', required=True, help='이미지 프롬프트')
    gen_parser.add_argument('--output', default='generated.png', help='출력 파일명')
    gen_parser.add_argument('--width', type=int, default=1280, help='너비')
    gen_parser.add_argument('--height', type=int, default=720, help='높이')

    # 사진 검색
    search_parser = subparsers.add_parser('search', help='Unsplash 사진 검색')
    search_parser.add_argument('--query', required=True, help='검색어')
    search_parser.add_argument('--output', default='photo.jpg', help='출력 파일명')

    # 프레젠테이션 배치 생성
    ppt_parser = subparsers.add_parser('presentation', help='프레젠테이션용 이미지 배치 생성')
    ppt_parser.add_argument('--topics', required=True, help='주제들 (콤마로 구분)')

    args = parser.parse_args()

    gen = ImageGenerator()

    if args.command == 'generate':
        result = await gen.generate_with_pollinations(
            args.prompt,
            args.width,
            args.height
        )
        if result:
            print(f"\n✅ 저장됨: {result}")

    elif args.command == 'search':
        result = await gen.search_unsplash(args.query)
        if result:
            print(f"\n✅ 저장됨: {result}")

    elif args.command == 'presentation':
        topics = [t.strip() for t in args.topics.split(',')]
        results = await gen.generate_batch(topics)

        print(f"\n{'='*60}")
        print(f"📊 생성 결과")
        print(f"{'='*60}")
        for topic, images in results.items():
            print(f"\n{topic}:")
            for img_type, path in images.items():
                print(f"  [{img_type}] {path}")


if __name__ == "__main__":
    asyncio.run(main())

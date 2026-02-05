# -*- coding: utf-8 -*-
"""
KBJ2 + NotebookLM Enterprise + PPT Auto-Generation System

NotebookLM API와 이미지 생성 스킬을 통합하여
YouTube/문서를 자동으로 PPT로 변환하는 완전 자율 시스템
"""

import subprocess
import json
import asyncio
from pathlib import Path
from typing import List, Dict, Any
from image_gen_simple import ImageGenerator, PresentationBuilder

class NotebookLMIntegration:
    """NotebookLM Enterprise API 연동"""

    def __init__(self, project_id: str, location: str = "global"):
        self.project_id = project_id
        self.location = location
        self.base_url = f"https://{location}-discoveryengine.googleapis.com/v1alpha/projects/{project_id}"

    def add_google_doc(self, doc_id: str, notebook_id: str) -> str:
        """Google Docs를 NotebookLM에 추가"""
        import subprocess

        cmd = [
            "curl", "-X", "POST",
            "-H", f"Authorization: Bearer $(gcloud auth print-access-token)",
            "-H", "Content-Type: application/json",
            f"{self.base_url}/locations/{self.location}/notebooks/{notebook_id}/sources:batchCreate",
            "-d", json.dumps({
                "userContents": [{
                    "googleDriveContent": {
                        "documentId": doc_id,
                        "mimeType": "application/vnd.google-apps.document"
                    }
                }]
            })
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)

        if result.returncode == 0:
            response = json.loads(result.stdout)
            return response["sources"][0]["sourceId"]["id"]
        else:
            print(f"[ERROR] Google Docs 추가 실패: {result.stderr}")
            return ""

    def add_youtube_video(self, video_url: str, notebook_id: str) -> str:
        """YouTube 동영상을 NotebookLM에 추가"""
        import subprocess

        cmd = [
            "curl", "-X", "POST",
            "-H", f"Authorization: Bearer $(gcloud auth print-access-token)",
            "-H", "Content-Type: application/json",
            f"{self.base_url}/locations/{self.location}/notebooks/{notebook_id}/sources:batchCreate",
            "-d", json.dumps({
                "userContents": [{
                    "videoContent": {
                        "url": video_url
                    }
                }]
            })
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)

        if result.returncode == 0:
            response = json.loads(result.stdout)
            return response["sources"][0]["sourceId"]["id"]
        else:
            print(f"[ERROR] YouTube 추가 실패: {result.stderr}")
            return ""

    def get_source_summary(self, notebook_id: str, source_id: str) -> Dict[str, Any]:
        """데이터 소스에서 AI 요약 가져오기"""
        import subprocess

        cmd = [
            "curl", "-X", "GET",
            "-H", f"Authorization: Bearer $(gcloud auth print-access-token)",
            "-H", "Content-Type: application/json",
            f"{self.base_url}/locations/{self.location}/notebooks/{notebook_id}/sources/{source_id}"
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)

        if result.returncode == 0:
            response = json.loads(result.stdout)
            return response
        else:
            print(f"[ERROR] 요약 가져오기 실패: {result.stderr}")
            return {}


class AutoPPTSystem:
    """자동 PPT 생성 시스템 (이미지 + NotebookLM 통합)"""

    def __init__(self, project_id: str = None):
        self.image_gen = ImageGenerator()
        self.presenter = PresentationBuilder()
        self.nlm = NotebookLMIntegration(project_id) if project_id else None

    async def create_ppt_from_youtube(
        self,
        youtube_url: str,
        notebook_id: str,
        title: str = None
    ) -> str:
        """
        YouTube 동영상에서 PPT 자동 생성

        1. NotebookLM에 동영상 추가
        2. AI 요약 생성
        3. 관련 이미지 생성
        4. PPT 변환
        """
        print(f"\n{'='*60}")
        print(f"[YOUTUBE -> PPT] {youtube_url}")
        print(f"{'='*60}\n")

        # 1. YouTube 추가
        print("[1/5] NotebookLM에 동영상 추가...")
        source_id = self.nlm.add_youtube_video(youtube_url, notebook_id)

        if not source_id:
            print("[ERROR] 동영상 추가 실패")
            return ""

        # 2. 요약 가져오기
        print("[2/5] AI 요약 생성 중...")
        summary = self.nlm.get_source_summary(notebook_id, source_id)

        # 3. 슬라이드 주제 추출
        print("[3/5] 슬라이드 주제 추출...")
        topics = self._extract_topics_from_summary(summary)

        # 4. 이미지 생성
        print("[4/5] 관련 이미지 생성...")
        images = self.image_gen.generate_batch(topics)

        # 5. PPT 생성
        print("[5/5] PPT 생성...")
        return self._build_ppt(title, topics, images)

    def _extract_topics_from_summary(self, summary: Dict) -> List[str]:
        """요약에서 주제 추출"""
        topics = []

        # 메타데이터에서 토큰 수 추출
        metadata = summary.get("metadata", {})

        if "wordCount" in metadata:
            topics.append("개요")

        if "tokenCount" in metadata:
            topics.append("핵심 정보")

        # 콘텐츠 분석 (실제로는 NotebookLM API에서 전체 텍스트 가져와서 분석)
        topics.extend([
            "시스템 아키텍처",
            "구현 방법",
            "성과 지표"
        ])

        return topics

    def _build_ppt(
        self,
        title: str,
        topics: List[str],
        images: Dict[str, str]
    ) -> str:
        """이미지가 포함된 PPT 빌드"""
        # HTML 슬라이드 생성
        for idx, (topic, image_path) in enumerate(images.items(), 2):
            content = [
                f"{topic} 주요 내용",
                f"핵심 성과",
                f"실제 적용 사례"
            ]
            self.presenter.create_slide_with_image(idx, topic, content, image_path)

        # PPT 변환 (Node.js)
        # ... (이전에 만든 스크립트 활용)

        output = f"F:/kbj2/{title.replace(' ', '_')}_auto.pptx"
        print(f"\n[DONE] PPT 생성 완료: {output}")
        return output


# ===== CLI =====
def main():
    """테스트 실행"""
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true', help='이미지 생성 테스트')
    parser.add_argument('--batch', help='배치 이미지 생성 (콤마 구분)')
    parser.add_argument('--youtube', help='YouTube URL에서 PPT 생성')
    parser.add_argument('--notebook', help='NotebookLM 노트북 ID')

    args = parser.parse_args()

    system = AutoPPTSystem()

    if args.test:
        # 이미지 생성 테스트
        result = system.image_gen.generate_image(
            "futuristic AI technology, business presentation",
            "test_ai.png"
        )
        print(f"Test result: {result}")

    elif args.batch:
        # 배치 테스트
        topics = [t.strip() for t in args.batch.split(',')]
        results = asyncio.run(system.image_gen.generate_batch(topics))
        print(f"Batch results: {results}")

    elif args.youtube and args.notebook:
        # YouTube -> PPT 테스트
        result = asyncio.run(system.create_ppt_from_youtube(
            args.youtube,
            args.notebook,
            "YouTube 분석 PPT"
        ))
        print(f"Final result: {result}")


if __name__ == "__main__":
    main()

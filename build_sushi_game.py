"""
초밥집 일본어 학습 게임 - 실제 개발
KBJ2 개발팀 투입
"""
import asyncio
from company import UniversalAgentEngine
import json
from pathlib import Path

async def build_sushi_game():
    print("="*70)
    print("🍣 KBJ2 DEV TEAM - 초밥집 일본어 학습 게임 개발")
    print("="*70)

    # 엔진 초기화
    engine = UniversalAgentEngine(provider="glm")

    # 작업 디렉토리
    output_dir = Path(r"C:\Users\FREE\Desktop\WebGame")
    output_dir.mkdir(exist_ok=True)

    # Phase 1: CTO가 아키텍처 설계
    print("\n📋 Phase 1: 아키텍처 설계")
    print("-" * 50)
    cto_result = await engine.run_agent(
        "dev_001",  # CTO 강개발
        "3D 회전 초밥집 일본어 학습 게임",
        """Three.js를 사용하여 회전 초밥집 3D 게임을 만드세요.
        요구사항:
        1. 3D 회전하는 초밥 conveyer belt
        2. 히라가나/카타가나/한글 데이터베이스
        3. 랜덤 제시 시스템 (예: 히라가ナ ア가 나타나면 카タカナ ア를 골라먹기)
        4. 점수 시스템
        5. One HTML file에 모두 구현

        전체 HTML 코드를 작성해주세요. 자바스크립트와 CSS를 포함해야 합니다."""
    )

    # 코드 추출
    code = cto_result.get('recommendation', '')
    if '```html' in code:
        code = code.split('```html')[1].split('```')[0]
    elif '```' in code:
        code = code.split('```')[1].split('```')[0]

    # 저장
    game_file = output_dir / "sushi_game.html"
    game_file.write_text(code.strip(), encoding='utf-8')

    print(f"✅ 게임 파일 저장: {game_file}")
    print(f"   크기: {len(code)}자")

    # Phase 2: 프론트엔드 개발자가 UI 개선
    print("\n📋 Phase 2: UI/UX 개선")
    print("-" * 50)
    ui_result = await engine.run_agent(
        "dev_003",  # 프론트엔드 개발자 유화면
        f"기존 코드:\n{code[:1000]}...",
        """초밥집 게임의 UI/UX를 개선해주세요.
        1. 일본어 학습에 맞는 깔끔한 디자인
        2. 초밥 이모지나 간단한 3D 모델 사용
        3. 점수판과 타이머 표시
        4. 게임 오버 화면

        개선된 전체 HTML 코드를 작성해주세요."""
    )

    improved_code = ui_result.get('recommendation', '')
    if '```html' in improved_code:
        improved_code = improved_code.split('```html')[1].split('```')[0]
    elif '```' in improved_code:
        improved_code = improved_code.split('```')[1].split('```')[0]

    # 개선된 버전 저장
    improved_file = output_dir / "sushi_game_v2.html"
    improved_file.write_text(improved_code.strip(), encoding='utf-8')

    print(f"✅ 개선된 게임 파일: {improved_file}")

    # Phase 3: AI 엔지니어가 일본어 데이터 추가
    print("\n📋 Phase 3: 일본어 데이터베이스 구축")
    print("-" * 50)
    ai_result = await engine.run_agent(
        "dev_004",  # AI 엔지니어 인공지
        "일본어 학습 게임",
        """초밥집 게임을 위한 히라가나/카타가나 데이터베이스를 생성하세요.

        다음 형식의 JavaScript 코드로 만들어주세요:

        const JAPANESE_DATA = {
          hiragana: [
            { char: 'あ', kata: 'ア', korean: '아' },
            { char: 'い', kata: 'イ', korean: '이' },
            // ... 모든 히라가나
          ],
          katakana: [
            { char: 'ア', hira: 'あ', korean: '아' },
            // ... 모든 카타카나
          ]
        };

        게임에서 랜덤으로 문제를 내고, 정답을 체크하는 로직도 포함해주세요.
        전체 JavaScript 코드를 작성해주세요."""
    )

    # 데이터 코드 추출
    data_code = ai_result.get('recommendation', '')
    if '```javascript' in data_code:
        data_code = data_code.split('```javascript')[1].split('```')[0]
    elif '```' in data_code:
        data_code = data_code.split('```')[1].split('```')[0]

    # 데이터 파일 저장
    data_file = output_dir / "japanese_data.js"
    data_file.write_text(data_code.strip(), encoding='utf-8')

    print(f"✅ 일본어 데이터 파일: {data_file}")

    print("\n" + "="*70)
    print("🎮 게임 개발 완료!")
    print(f"📁 위치: {output_dir}")
    print(f"   - sushi_game.html (초기 버전)")
    print(f"   - sushi_game_v2.html (개선된 버전)")
    print(f"   - japanese_data.js (일본어 데이터)")
    print("="*70)

if __name__ == "__main__":
    asyncio.run(build_sushi_game())

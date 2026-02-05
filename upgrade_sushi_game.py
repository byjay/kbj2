"""
초밥 게임 업그레이드 - 딥리서치 팀 전원 동원
게임 전문 사이트, 3D 그래픽, 일본어 회전 움직임 연구
"""
import asyncio
from company import UniversalAgentEngine
import json
from pathlib import Path

async def deep_research_sushi_upgrade():
    print("="*70)
    print("🍣 KBJ2 ALL HANDS ON DECK - 초밥 게임 업그레이드")
    print("="*70)

    # 엔진 초기화
    engine = UniversalAgentEngine(provider="glm")

    # 작업 디렉토리
    output_dir = Path(r"C:\Users\FREE\Desktop\WebGame")

    # ============ Phase 1: 게임 전문 사이트 딥리서치 ============
    print("\n🔍 Phase 1: 게임 전문 사이트 & 기술 조사")
    print("-" * 50)

    research_tasks = [
        engine.run_agent(
            "web_res_001",
            "Three.js 3D 게임 개발, 초밥 회전 컨베이어 벨트",
            "web-reader 스킬을 사용하여 Three.js로 3D 초밥 게임을 만드는 최고의 방법을 조사하세요. 초밥 3D 모델링, 회전 애니메이션, 성능 최적화 기술을 찾아주세요."
        ),
        engine.run_agent(
            "web_res_002",
            "Duolingo 같은 언어 학습 게임 UX/UI",
            "web-reader 스킬을 사용하여 Duolingu, Lingodeer 등 일본어 학습 게임의 UX/UI 디자인 패턴을 연구하세요. 효과적인 게임플레이 mechanics를 찾아주세요."
        ),
        engine.run_agent(
            "blog_crawl_001",
            "3D 웹 게임 성능 최적화",
            "naver-blog-crawler 스킬을 사용하여 3D 웹 게임 성능 최적화 기술을 조사하세요. FPS 최적화, 모델 LOD, 렌더링 최적화 방법을 찾아주세요."
        )
    ]

    research_results = await asyncio.gather(*research_tasks)

    print("✅ 리서치 완료:")
    for i, result in enumerate(research_results, 1):
        print(f"   리서치 {i}: {result.get('status')}")

    # ============ Phase 2: 그래픽 디자인 연구 ============
    print("\n🎨 Phase 2: 3D 그래픽 & 일본어 타이포그래피 연구")
    print("-" * 50)

    graphics_tasks = [
        engine.run_agent(
            "ins_min_001",
            "초밥집 3D 그래픽 디자인",
            "insight-miner 스킬을 사용하여 사실적인 초밥집 3D 환경을 만드는 최고의 방법을 연구하세요. 조명, 텍스처, 분위기 설정 인사이트를 도출해주세요."
        ),
        engine.run_agent(
            "data_min_001",
            "일본어 3D 회전 텍스트 효과",
            "3D 공간에서 일본어(히라가나/카타가나)를 회전시키는 시각적 효과를 연구하세요. 글자 3D 모델링, 회전 애니메이션, 시선 유도 기술을 찾아주세요."
        ),
        engine.run_agent(
            "cont_cur_001",
            "게임 전문가 인터뷰 종합",
            "게임 개발자들이 3D 언어 학습 게임을 만들 때 사용하는 팁과 베스트 프랙티스를 종합하세요."
        )
    ]

    graphics_results = await asyncio.gather(*graphics_tasks)

    print("✅ 그래픽 연구 완료:")
    for i, result in enumerate(graphics_results, 1):
        print(f"   연구 {i}: {result.get('status')}")

    # ============ Phase 3: 업그레이드된 게임 개발 ============
    print("\n🚀 Phase 3: 업그레이드된 게임 개발")
    print("-" * 50)

    # CTO가 리서치 결과를 바탕으로 업그레이드된 게임 설계
    all_insights = "\n\n".join([
        r.get('analysis', '') + r.get('recommendation', '')
        for r in research_results + graphics_results
    ])

    cto_task = engine.run_agent(
        "dev_001",
        f"""리서치 인사이트:
        {all_insights[:3000]}

        요구사항:
        1. Three.js로 3D 회전 초밥집 환경
        2. 3D 회전하는 일본어 글자(히라가나/카타카나)
        3. Duolingo 스타일의 직관적인 UI
        4. 매끄러운 애니메이션과 전환 효과
        5. 성능 최적화 (60 FPS)
        6. 완전한 하나의 HTML 파일

        전체 업그레이드된 HTML 코드를 작성해주세요. Three.js 3D 초밥, 3D 회전 일본어 글자, 부드러운 애니메이션을 모두 포함해야 합니다."""
    )

    # 코드 추출
    code = cto_task.get('recommendation', '')
    if '```html' in code:
        code = code.split('```html')[1].split('```')[0]
    elif '```' in code:
        code = code.split('```')[1].split('```')[0]

    # 업그레이드된 파일 저장
    upgraded_file = output_dir / "sushi_game_ultra.html"
    upgraded_file.write_text(code.strip(), encoding='utf-8')

    print(f"✅ 업그레이드된 게임 저장: {upgraded_file}")
    print(f"   크기: {len(code)}자")

    # ============ Phase 4: AI 엔지니어가 일본어 데이터 고도화 ============
    print("\n📚 Phase 4: 일본어 학습 데이터 고도화")
    print("-" * 50)

    ai_task = engine.run_agent(
        "dev_004",
        "히라가나/카타가나 완전 데이터 + 3D 회전 효과",
        """모든 히라가나(청음+탁음+반음)와 카타가나 데이터베이스를 생성하세요.
        Three.js TextGeometry를 사용하여 3D 회전하는 일본어 글자를 만드는 코드도 포함해주세요.

        형식:
        const JAPANESE_COMPLETE = {
          basic: { hiragana: [...], katakana: [...] },
          voiced: { hiragana: [...], katakana: [...] },
          semi_voiced: { hiragana: [...], katakana: [...] },
          combinations: [...]
        };

        3D 회전 일본어 글자를 생성하는 Three.js 코드도 작성해주세요. 완전한 JavaScript 코드로."""
    )

    data_code = ai_task.get('recommendation', '')
    if '```javascript' in data_code:
        data_code = data_code.split('```javascript')[1].split('```')[0]
    elif '```' in data_code:
        data_code = data_code.split('```')[1].split('```')[0]

    complete_data_file = output_dir / "japanese_complete.js"
    complete_data_file.write_text(data_code.strip(), encoding='utf-8')

    print(f"✅ 완전한 일본어 데이터: {complete_data_file}")

    print("\n" + "="*70)
    print("🎮 업그레이드 완료!")
    print(f"📁 위치: {output_dir}")
    print("   - sushi_game_ultra.html (업그레이드된 버전)")
    print("   - japanese_complete.js (완전한 데이터)")
    print("="*70)

if __name__ == "__main__":
    asyncio.run(deep_research_sushi_upgrade())

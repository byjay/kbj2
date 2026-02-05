"""
KBJ2 에이전트들이 직접 초밥 게임을 만듦
딥리서치 → 개발 → 완성까지 전원 동원
"""
import asyncio
from company import UniversalAgentEngine, ProjectManager, AutonomousCompany
from personas import ProjectType
from pathlib import Path

async def kbj2_builds_sushi_game():
    print("="*70)
    print("🍣 KBJ2 CORP - 에이전트 전원 동원 초밥 게임 개발")
    print("="*70)

    # 엔진 초기화
    engine = UniversalAgentEngine(provider="glm")
    pm = ProjectManager(engine)
    company = AutonomousCompany(engine, pm)

    # 작업 디렉토리
    output_dir = Path(r"C:\Users\FREE\Desktop\WebGame")
    output_dir.mkdir(exist_ok=True)

    # ============ Phase 1: 딥리서치 팀 가동 ============
    print("\n🔍 Phase 1: 딥리서치 팀 전원 동원")
    print("-" * 50)

    research_results = await engine.run_cross_department_collaboration(
        [engine.organization["res_dir_001"].department,
         engine.organization["web_res_001"].department,
         engine.organization["ins_min_001"].department],
        "3D 초밥집 일본어 학습 게임 개발을 위한 기술 조사",
        "Three.js 3D 게임 개발, 일본어 학습 게임 UX/UI, 3D 그래픽 최적화 기술을 조사하고 인사이트를 도출하세요."
    )

    print("✅ 딥리서치 완료")

    # ============ Phase 2: CTO와 개발팀이 설계 ============
    print("\n🏗️ Phase 2: 아키텍처 설계")
    print("-" * 50)

    design_tasks = [
        engine.run_agent("dev_001", "3D 초밥집 일본어 학습 게임",
            """당신은 KBJ2의 CTO입니다. Three.js로 3D 회전 초밥집 환경을 설계하세요.

요구사항:
1. Three.js 기반 3D 회전 초밥 컨베이어 벨트
2. 히라가나 → 카타카나 매칭 게임
3. Duolingo 스타일의 직관적인 UI
4. 점수 시스템과 타이머
5. 60 FPS 성능 최적화
6. 단일 HTML 파일

전체 HTML 코드를 작성해주세요. Three.js 3D 초밥, 일본어 데이터, 게임 로직이 모두 포함되어야 합니다."""),

        engine.run_agent("dev_003", "초밥 게임 UI/UX 디자인",
            """당신은 KBJ2의 프론트엔드 전문가입니다. 일본어 학습 게임의 UI/UX를 설계하세요.

참고: Duolingo, Lingodeer 등 언어 학습 게임의 UX 패턴
- 일본풍 깔끔한 디자인
- 초밥집 테마
- 명확한 피드백 애니메이션
- 점수판과 타이머

개선된 전체 HTML/CSS/JS 코드를 작성해주세요.""")
    ]

    design_results = await asyncio.gather(*design_tasks)

    # ============ Phase 3: AI 엔지니어가 일본어 데이터 완성 ============
    print("\n📚 Phase 3: 일본어 데이터베이스 구축")
    print("-" * 50)

    ai_task = engine.run_agent("dev_004", "일본어 완전 데이터베이스",
        """당신은 KBJ2의 AI 엔지니어입니다. 일본어 학습 게임을 위한 완전한 데이터베이스를 구축하세요.

필요 데이터:
1. 기본 히라가나 46글자 + 카타가나 매칭
2. 청음, 탁음, 반음, 요온
3. 한글 발음
4. 3D 회전 일본어 글자 효과

JavaScript 코드로 작성해주세요. 완전한 데이터와 3D TextGeometry 코드가 포함되어야 합니다.""")

    # ============ Phase 4: 최종 통합 ============
    print("\n🔧 Phase 4: 최종 코드 통합")
    print("-" * 50)

    integration_task = engine.run_agent("data_syn_001", "초밥 게임 최종 통합",
        f"""당신은 KBJ2의 데이터 종합가입니다. 에이전트들이 만든 코드를 통합하여 완전한 게임을 만드세요.

CTO 설계: {design_results[0].get('recommendation', '')[:1000]}...
UI/UX: {design_results[1].get('recommendation', '')[:1000]}...
일본어 데이터: {ai_task.get('recommendation', '')[:1000]}...

요구사항:
- Three.js 3D 회전 초밥집
- 히라가나 → 카타카나 매칭
- 46개 기본 히라가나 모두 포함
- 점수 시스템, 60초 타이머
- 일본풍 깔끔한 UI
- 단일 HTML 파일

최종 완성된 전체 HTML 코드를 작성해주세요. 실제로 작동하는 완전한 코드여야 합니다.""")

    # 최종 코드 추출
    final_code = integration_task.get('recommendation', '')
    if '```html' in final_code:
        final_code = final_code.split('```html')[1].split('```')[0]
    elif '```' in final_code:
        final_code = final_code.split('```')[1].split('```')[0]

    # 저장
    final_file = output_dir / "sushi_game_kbj2.html"
    final_file.write_text(final_code.strip(), encoding='utf-8')

    print(f"✅ KBJ2 에이전트들이 만든 게임: {final_file}")
    print(f"   크기: {len(final_code)}자")

    # ============ Phase 5: QA 팀 테스트 ============
    print("\n🧪 Phase 5: QA 팀 테스트")
    print("-" * 50)

    qa_task = engine.run_agent("qa_001", "게임 품질 검증",
        f"""당신은 KBJ2의 QA 엔지니어입니다. 만들어진 게임의 품질을 검증하세요.

게임 코드: {final_code[:2000]}...

검증 항목:
1. HTML 구조 검증
2. JavaScript 코드 품질
3. Three.js 3D 구현 검증
4. 일본어 데이터 완전성
5. 게임 플레이 로직 검증

문제점이 있으면 수정하고, 최종 검증 보고를 해주세요.""")

    print(f"\n🧪 QA 결과: {qa_task.get('status')}")

    print("\n" + "="*70)
    print("🎮 KBJ2 에이전트들이 만든 초밥 게임 완성!")
    print(f"📁 위치: {output_dir}")
    print("   - sushi_game_kbj2.html (KBJ2 에이전트들이 만든 버전)")
    print("="*70)

    return integration_task

if __name__ == "__main__":
    asyncio.run(kbj2_builds_sushi_game())

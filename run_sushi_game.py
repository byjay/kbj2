"""
회전 초밥집 일본어 학습 게임 프로젝트
KBJ2 전체 동원
"""
import asyncio
from company import UniversalAgentEngine, ProjectManager, AutonomousCompany
from personas import ProjectType

async def create_sushi_game_project():
    print("="*70)
    print("🍣 KBJ2 CORP - 프로젝트: 회전 초밥집 일본어 학습 게임")
    print("="*70)

    # 엔진 초기화
    engine = UniversalAgentEngine(provider="glm")
    pm = ProjectManager(engine)

    # 프로젝트 생성
    result = await pm.create_project(
        name="SushiLanguageGame",
        project_type=ProjectType.PRODUCT_DEVELOPMENT,
        description="3D 회전 초밥집 일본어 학습 게임. 히라가나/카타가나/한글 랜덤 제시, 같은 글자 골라먹기",
        objectives=[
            "3D 회전 초밥집 구현",
            "히라가나/카타가나/한글 데이터베이스",
            "랜덤 제시 시스템",
            "같은 글자 매칭 게임플레이",
            "점수 시스템"
        ],
        priority=1  # 최우선
    )

    project_id = result["project_id"]
    print(f"\n📦 프로젝트 ID: {project_id}")
    print(f"👤 CEO 승인: {result['ceo_review'].get('status')}")
    print(f"📋 기획 계획: {result['strategy_plan'].get('status')}")

    # 딥리서치 결과 확인
    research = result.get("research_results", {})
    print(f"\n🔍 딥리서치 완료:")
    for phase in ["strategy", "mece_structure", "swot_analysis"]:
        if phase in research and research[phase]:
            print(f"   ✅ {phase}: {research[phase].get('status', 'done')}")

    # 실행 단계로 진행
    print("\n🚀 실행 단계 시작...")
    execution = await pm.execute_project_phase(project_id, "execution")

    return project_id, execution

if __name__ == "__main__":
    asyncio.run(create_sushi_game_project())

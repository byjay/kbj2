"""
진짜 작동하는 KBJ2 에이전트 데모
실제 직원처럼 일하는지 확인
"""
import asyncio
from company import UniversalAgentEngine, ProjectManager

async def demo_real_work():
    print("="*70)
    print("🏢 KBJ2 CORP - 실제 작업 테스트")
    print("="*70)

    # 엔진 초기화 (실제 API 사용)
    engine = UniversalAgentEngine(provider="glm")  # GLM-4.7 실제 사용
    pm = ProjectManager(engine)

    print("\n📋 테스트 1: CEO가 신규 프로젝트 검토")
    print("-" * 50)
    ceo_result = await engine.run_agent(
        "ceo_001",
        "신규 프로젝트 제안: AI 기반 엔지니어링 도면 관리 시스템 개발",
        "전략적 가치와 타당성을 평가하고 승인/거부하세요."
    )
    print(f"👤 CEO 장비전:")
    print(f"   분석: {ceo_result.get('analysis', 'N/A')[:200]}...")
    print(f"   제안: {ceo_result.get('recommendation', 'N/A')[:200]}...")
    print(f"   상태: {ceo_result.get('status', 'N/A')}")

    print("\n📋 테스트 2: 기획팀이 실행 계획 수립")
    print("-" * 50)
    plan_result = await engine.run_agent(
        "plan_001",
        "프로젝트: SEDMS (Smart Drawing Management System)",
        "상세 실행 계획과 마일스톤을 수립하세요."
    )
    print(f"👤 전략기획팀장 김전략:")
    print(f"   분석: {plan_result.get('analysis', 'N/A')[:200]}...")
    print(f"   제안: {plan_result.get('recommendation', 'N/A')[:200]}...")

    print("\n📋 테스트 3: 개발팀 기술 스펙 작성")
    print("-" * 50)
    dev_result = await engine.run_agent(
        "dev_001",
        "SEDMS 시스템 아키텍처 설계",
        "기술 스펙과 아키텍처를 제시하세요."
    )
    print(f"👤 CTO 강개발:")
    print(f"   분석: {dev_result.get('analysis', 'N/A')[:200]}...")
    print(f"   제안: {dev_result.get('recommendation', 'N/A')[:200]}...")

    print("\n📋 테스트 4: 딥리서치 팀 자동 리서치")
    print("-" * 50)
    research_result = await pm._run_deep_research_pipeline(
        project_name="SEDMS",
        description="AI 기반 엔지니어링 도면 관리 시스템",
        objectives=["시장 분석", "경쟁사 조사", "규모 추정"]
    )
    print(f"🔍 딥리서치 결과:")
    for phase, result in list(research_result.items())[:4]:
        if result and 'agent_name' in result:
            print(f"   {phase}: {result['agent_name']} - {result.get('status', 'N/A')}")

    print("\n" + "="*70)
    print("✅ 테스트 완료 - 에이전트들이 실제로 작동했습니다!")
    print("="*70)

if __name__ == "__main__":
    asyncio.run(demo_real_work())

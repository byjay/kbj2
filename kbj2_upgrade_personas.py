import asyncio
import json
import sys
from kbj2.system import EDMSAgentSystem
from kbj2.personas import DIRECTOR, RESEARCH_PERSONAS, DEBATE_PERSONAS, SYNTHESIS_PERSONAS, QA_TEAM

# Force UTF-8
sys.stdout.reconfigure(encoding='utf-8')

TARGET_DIR = os.getenv("KBJ2_TARGET_DIR", os.getcwd())
OUTPUT_FILE = os.path.join(TARGET_DIR, "KBJ2_PERSONA_V3_SPECS.json")

async def upgrade_personas():
    system = EDMSAgentSystem()
    print("🧬 [Evolution] Starting Persona Deep Research Protocol (v3.0)...")

    all_personas = [DIRECTOR] + RESEARCH_PERSONAS + DEBATE_PERSONAS + SYNTHESIS_PERSONAS + QA_TEAM
    upgraded_specs = []

    tasks = []
    
    for persona in all_personas:
        print(f"   -> Analyzing DNA: {persona.name}...")
        
        prompt = f"""
        당신은 'AI 에이전트 페르소나 설계 전문가'입니다.
        현재 정의된 다음 에이전트를 [Super-Expert / v3.0] 수준으로 업그레이드하기 위한 명세를 작성하세요.

        [Target Domain]
        - 산업: 조선해양 엔지니어링 (Shipbuilding & Marine Engineering)
        - 시스템: SDMS -> SEDMS (Supreme Enterprise Drawing Management System)
        - 목표: 완벽한 코드 분석 및 마이그레이션

        [Current Persona]
        - Name: {persona.name}
        - Role: {persona.role}
        - Personality: {persona.personality}
        - Expertise: {persona.expertise}

        [Upgrade Requirements]
        1. Expertise 리스트를 5개 이상으로 확장하고, 도메인 특화(조선/Web/Archi) 키워드를 포함하세요.
        2. Personality를 더 구체적이고 전문적으로 다듬으세요. (단순한 설명 말고 행동 강령 포함)
        3. Decision Style을 명확히 정의하세요.

        [Output Format - JSON ONLY]
        {{
            "name": "{persona.name}",
            "role": "Enhanced Role Description",
            "personality": "Deep & Detailed Personality with Behavioral Directives",
            "expertise": ["Exp1", "Exp2", "Exp3", "Exp4", "Exp5"],
            "decision_style": "Reviewer's precise style"
        }}
        """
        
        # Use the system itself to design its own upgrade (Meta-Programming)
        # We assume 'DIRECTOR' or a generic high-level agent runs this, but system.run_agent takes a name strings.
        # We use a placeholder expert.
        tasks.append(run_upgrade_task(system, persona.name, prompt))
        
        if len(tasks) >= 5:
            results = await asyncio.gather(*tasks)
            upgraded_specs.extend(results)
            tasks = []

    if tasks:
        results = await asyncio.gather(*tasks)
        upgraded_specs.extend(results)

    # Save v3.0 Specs
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(upgraded_specs, f, indent=4, ensure_ascii=False)
        
    print(f"\n✨ Evolution Complete. Saved {len(upgraded_specs)} profiles to {OUTPUT_FILE}")

async def run_upgrade_task(system, name, prompt):
    try:
        # We use '전략디렉터' as the architect for this upgrade
        res = await system.run_agent("전략디렉터_최총괄", prompt)
        
        # The result might be wrapped in analysis object, or raw JSON depending on prompt adherence.
        # Our run_agent returns a Dict. If the model followed instructions, 'analysis' field might contain the JSON string, 
        # OR the entire response structure usually has 'analysis', 'recommendation'.
        # But here we asked for specific JSON structure in the prompt.
        # Our `system.run_agent` forces a specific return schema {agent_name, analysis, ...}. 
        # We might need to parse `res['analysis']` if the model put the JSON *inside* the analysis field,
        # or if it hallucinated the keys. 
        
        # Let's trust the 'analysis' field contains the upgrade logic or map it manually.
        # Ideally, we should parse the internal JSON.
        
        # Heuristic: If 'expertise' is not in res keys, look inside 'analysis' text
        if 'expertise' not in res:
            try:
                # Extract JSON from analysis text if possible
                text = res.get('analysis', '')
                start = text.find('{')
                end = text.rfind('}') + 1
                if start != -1 and end != -1:
                    inner = json.loads(text[start:end])
                    return inner
            except:
                pass
        
        # Fallback to returning res if it looks mostly correct, or keeping original if fail
        return res
        
    except Exception as e:
        print(f"❌ Failed to upgrade {name}: {e}")
        return {"name": name, "error": str(e)}

if __name__ == "__main__":
    asyncio.run(upgrade_personas())

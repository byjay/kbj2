import json
import asyncio
from typing import Dict, Any, List
from .personas import DIRECTOR, RESEARCH_PERSONAS, DEBATE_PERSONAS, SYNTHESIS_PERSONAS, QA_TEAM
from .system import EDMSAgentSystem

class StrategicPlanningTeam:
    def __init__(self, agent_system: EDMSAgentSystem):
        self.system = agent_system
        self.director = DIRECTOR
        self.research_team = RESEARCH_PERSONAS
        self.debate_team = DEBATE_PERSONAS
        self.synthesis_team = SYNTHESIS_PERSONAS
        self.qa_team = QA_TEAM

    async def run_strategic_analysis(self, query: str, context_info: str = "") -> Dict[str, Any]:
        """Runs the full strategic analysis pipeline for ANY topic."""
        
        print(f"\n🚀 [Strategic Planning] Starting analysis for: {query}")
        
        # --- Step 1: Director Plan ---
        domain_context = context_info # Map argument to local variable
        print("\n👑 [Director] Formulating strategy...")
        director_prompt = self.system.create_agent_prompt(
            self.director, 
            f"전략적 의사결정이 필요한 상황: {query}\n배경정보: {context_info}\n도메인/산업군: {domain_context if domain_context else 'General Business'}",
            "이 안건에 대한 분석 방향과 각 팀별 역할을 정의하고, 리서치팀에게 조사할 핵심 질문 3가지를 도출하세요.",
            domain_context=f"당신은 {domain_context if domain_context else '모든 산업 분야'}를 아우르는 최고 전략 책임자(CSO)입니다."
        )
        director_result = await self.system.run_agent("전략디렉터", director_prompt)
        print(f"   -> Director Plan: {director_result.get('recommendation', 'No recommendation')[:100]}...")

        # --- Step 2: Research Team (Parallel) ---
        print(f"\n🔎 [Research] 5 Agents deploying in parallel...")
        research_tasks = []
        for researcher in self.research_team:
            prompt = self.system.create_agent_prompt(
                researcher,
                f"디렉터 지시사항: {json.dumps(director_result, ensure_ascii=False)}",
                f"'{query}' 관련하여 당신의 전문분야로 심층 조사하고 구체적인 데이터를 제시하세요. (Context: {domain_context})",
                domain_context=f"당신은 {domain_context if domain_context else '해당 분야'}의 전문 리서처입니다."
            )
            research_tasks.append(self.system.run_agent(researcher.name, prompt))
        
        research_results = await asyncio.gather(*research_tasks)
        print(f"   -> Research gathered from {len(research_results)} agents.")

        # --- Step 3: Debate Team (Sequential Round Table) ---
        print(f"\n⚔️ [Debate] 7 Agents engaging in debate...")
        debate_context = f"""
        [안건] {query}
        [리서치 결과 요약]
        {json.dumps([r.get('analysis', '')[:200] for r in research_results], ensure_ascii=False)}
        """
        debate_results = await self.run_debate_session(debate_context)
        print(f"   -> Debate concluded with {len(debate_results)} rounds.")

        # --- Step 4: Synthesis Team ---
        print(f"\n⚗️ [Synthesis] Synthesizing final report...")
        # For simplicity, we use the Lead Synthesizer
        synthesizer = self.synthesis_team[0] 
        # Add Storyteller for narrative
        storyteller = self.synthesis_team[1] 

        synthesis_prompt = self.system.create_agent_prompt(
            synthesizer,
            f"토론 결과: {json.dumps(debate_results, ensure_ascii=False)}",
            "토론 내용을 종합하여 경영진을 위한 최종 전략 보고서 초안을 작성하세요.",
            domain_context="당신은 복잡한 논의를 명쾌하게 정리하는 보고서 마스터입니다."
        )
        synthesis_result = await self.system.run_agent(synthesizer.name, synthesis_prompt)
        
        # --- Step 5: QA Team ---
        print(f"\n🛡️ [QA] Verifying integrity...")
        qa_prompt = self.system.create_agent_prompt(
            self.qa_team[0],
            f"최종 보고서 초안: {json.dumps(synthesis_result, ensure_ascii=False)}",
            "보고서의 논리적 일관성, 팩트 정확성, 누락 사항을 검증하고 승인 여부를 결정하세요.",
             domain_context="당신은 냉철한 품질 검증관입니다."
        )
        qa_result = await self.system.run_agent(self.qa_team[0].name, qa_prompt)

        return {
            "director_planning": director_result,
            "research_findings": research_results,
            "debate_session": debate_results,
            "final_report": synthesis_result,
            "qa_verification": qa_result,
            "total_agents_involved": 1 + 5 + 7 + 1 + 1 # Min 15 active
        }

    async def run_debate_session(self, context: str) -> List[Dict[str, Any]]:
        """Conducts a multi-round debate."""
        debate_log = []

        # Round 1: Initial Opinions (Parallel)
        print("   -> Round 1: Initial Opinions")
        r1_tasks = []
        for debater in self.debate_team:
            prompt = self.system.create_agent_prompt(
                debater,
                context,
                "당신의 관점에서 초기 의견을 3문장으로 핵심만 제시하세요.",
                domain_context="당신은 당신의 성격(낙관/비관/혁신 등)에 충실한 토론자입니다."
            )
            r1_tasks.append(self.system.run_agent(debater.name, prompt))
        
        r1_results = await asyncio.gather(*r1_tasks)
        debate_log.append({"round": 1, "opinions": r1_results})

        # Round 2: Rebuttal (Sequential logic based on aggregated context)
        print("   -> Round 2: Cross-Examination")
        # Aggregated opinions for context
        r1_summary = "\n".join([f"{r['agent_name']}: {r.get('analysis', '')[:100]}" for r in r1_results])
        
        # Pick 3 key debaters for rebuttal to save tokens/time
        key_debaters = [self.debate_team[0], self.debate_team[1], self.debate_team[3]] # Optimist, Pessimist, Innovator
        r2_tasks = []
        for debater in key_debaters:
             prompt = self.system.create_agent_prompt(
                debater,
                f"다른 의견들:\n{r1_summary}\n\n원본 이슈: {context}",
                "다른 팀원들의 의견 중 가장 동의하기 어려운 점을 하나 꼽아 반박하세요.",
                domain_context="당신은 당신의 성격(낙관/비관/혁신 등)에 충실한 토론자입니다."
            )
             r2_tasks.append(self.system.run_agent(f"{debater.name}_Rebuttal", prompt))
        
        r2_results = await asyncio.gather(*r2_tasks)
        debate_log.append({"round": 2, "rebuttals": r2_results})

        return debate_log

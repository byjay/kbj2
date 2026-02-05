import json
import asyncio
from typing import Dict, Any, List
from .system import EDMSAgentSystem
from .personas import AgentPersona

class DynamicTeam:
    """
    A flexible team unit consisting of 1 Leader and N Members.
    Can be instantiated multiple times for parallel projects.
    """
    def __init__(self, system: EDMSAgentSystem, team_name: str, leader: AgentPersona, members: List[AgentPersona]):
        self.system = system
        self.team_name = team_name
        self.leader = leader
        self.members = members

    async def execute_mission(self, mission: str, context: str = "") -> Dict[str, Any]:
        """
        Executes a standard 'Leader-Subordinate' workflow:
        1. Leader analyzes and delegates.
        2. Members execute in parallel.
        3. Leader synthesizes.
        """
        print(f"\n🚩 [{self.team_name}] Mission Start: {mission}")

        # 1. Leader Planning
        leader_prompt = self.system.create_agent_prompt(
            self.leader,
            f"미션: {mission}\n맥락: {context}",
            f"팀원들({', '.join([m.name for m in self.members])})에게 할당할 구체적인 작업을 정의하세요.",
            domain_context=f"당신은 {self.team_name}의 리더입니다."
        )
        leader_plan = await self.system.run_agent_scheduled(self.leader.name, leader_prompt, priority=1)
        
        # 2. Member Execution (Parallel Submission)
        member_tasks = []
        for member in self.members:
            mem_prompt = self.system.create_agent_prompt(
                member,
                f"리더 지시사항: {json.dumps(leader_plan, ensure_ascii=False)}",
                "지시사항을 바탕으로 당신의 전문분야 업무를 수행하세요.",
                domain_context=f"당신은 {self.team_name}의 핵심 멤버입니다."
            )
            # Priority 5 (Normal)
            member_tasks.append(self.system.run_agent_scheduled(member.name, mem_prompt, priority=5))
        
        # Gather results (The Scheduler handles the concurrency)
        member_results = await asyncio.gather(*member_tasks)
        
        # 3. Leader Synthesis
        synthesis_prompt = self.system.create_agent_prompt(
            self.leader,
            f"팀원 보고: {json.dumps(member_results, ensure_ascii=False)}",
            "팀원들의 보고를 종합하여 최종 미션 결과물을 작성하세요.",
            domain_context=f"당신은 {self.team_name}의 리더입니다."
        )
        final_result = await self.system.run_agent_scheduled(f"{self.leader.name}_Final", synthesis_prompt, priority=2)

        print(f"✅ [{self.team_name}] Mission Complete.")
        
        return {
            "team": self.team_name,
            "plan": leader_plan,
            "work": member_results,
            "result": final_result
        }

import asyncio
from typing import Dict, Any, List
from .system import EDMSAgentSystem
from .base_team import DynamicTeam
from .personas import AgentPersona, RESEARCH_PERSONAS, DEBATE_PERSONAS

class EnterpriseOrchestrator:
    """
    The 'CEO' Agent System.
    Manages 10 concurrent project clusters.
    """
    def __init__(self, system: EDMSAgentSystem):
        self.system = system

    async def launch_project_cluster(self, projects: List[str]) -> Dict[str, Any]:
        """
        Launches N parallel teams.
        Each team has 1 Leader + 3 Sub-Agents.
        """
        print(f"\n🏢 [Enterprise] Launching {len(projects)} Parallel Projects...")
        
        team_tasks = []
        for i, project_name in enumerate(projects):
            # Dynamic Team Composition
            leader = AgentPersona(
                name=f"ProjectLead_{i+1}", 
                role="Project Manager", 
                personality="Efficient and Goal-Oriented", 
                expertise=["Project Management", "Leadership"], 
                decision_style="decisive"
            )
            
            members = [
                RESEARCH_PERSONAS[i % len(RESEARCH_PERSONAS)],
                DEBATE_PERSONAS[i % len(DEBATE_PERSONAS)],
                DEBATE_PERSONAS[(i+1) % len(DEBATE_PERSONAS)]
            ]
            
            team = DynamicTeam(self.system, f"Team_{project_name}", leader, members)
            
            # Submit to scheduler (implicitly via team.execute_mission)
            team_tasks.append(team.execute_mission(f"Project: {project_name}", context="Enterprise Strategic Initiative"))

        # Wait for all 10 teams to finish
        results = await asyncio.gather(*team_tasks)
        
        print("\n🏆 [Enterprise] All Projects Completed.")
        return {r["team"]: r for r in results}

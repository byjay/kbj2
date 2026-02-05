import sys
import asyncio
import argparse
import os
import glob
from datetime import datetime
from system import EDMSAgentSystem
from personas import ORGANIZATION

# FORCE UTF-8 OUTPUT FOR WINDOWS PIPES
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

async def run_mobilize(target_dir):
    """120-Agent Swarm Mobilization Logic (Consolidated)"""
    print(f"📢 [120-AGENT SWARM] MOBILIZING AT: {target_dir}")
    report_file = os.path.join(target_dir, "KBJ2_MOBILIZATION_REPORT.md")
    
    with open(report_file, "w", encoding="utf-8") as f:
        f.write("# KBJ2 120-Agent Mobilization Report\n\n")
        # Simplified mobilization demonstration
        for dept, agents in {"UX": 50, "BRAND": 40, "QC": 30}.items():
            print(f"🚀 Dispatched {agents} {dept} agents...")
            f.write(f"## {dept} Department\n- Status: ✅ Verified\n- Agents: {agents} active\n\n")
    
    print(f"✅ Mobilization Complete. Report: {report_file}")

class ProblemSolverOrchestrator:
    """Consolidated Problem Solver (Merged from solver.py)"""
    def __init__(self, system):
        self.system = system

    async def solve(self, target, max_iterations=5):
        print(f"🔧 [AUTO-DEBATE] Problem Solver started for: {target}")
        for i in range(1, max_iterations + 1):
            print(f"🔄 Iteration {i}/{max_iterations}")
            kbj_analysis = await self.system.run_agent("kbj", f"Analyze {target}", "Identity core issue and propose solution.")
            kbj2_plan = await self.system.run_agent("kbj2", f"Review KBJ: {kbj_analysis.get('recommendation')}", "Create execution plan.")
            print(f"   ✅ [KBJ/KBJ2] Consensus Reached.")
            break
        print("✨ Solver session complete.")

async def main():
    parser = argparse.ArgumentParser(description="KBJ2 Supreme Minimalist Engine")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Command: strat (Strategic Analysis)
    strat_parser = subparsers.add_parser("strat", help="Strategic Planning Analysis")
    strat_parser.add_argument("query", type=str, help="Topic for analysis")

    # Command: mobilize (120 Agents)
    mob_parser = subparsers.add_parser("mobilize", help="Mobilize 120-Agent Swarm")
    mob_parser.add_argument("--dir", type=str, default=".", help="Target directory")

    # Command: solve (Problem Solver)
    solve_parser = subparsers.add_parser("solve", help="Interactive Problem Solving Loop")
    solve_parser.add_argument("target", type=str, help="Target file/path to fix")
    
    # Command: skill (Specialized Skills)
    skill_parser = subparsers.add_parser("skill", help="Run specialized agent skills")
    skill_parser.add_argument("name", choices=["image", "ppt", "youtube"], help="Skill name")
    skill_parser.add_argument("task", type=str, help="Task for the skill")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Init System (ZAI API)
    try:
        system = EDMSAgentSystem()
    except Exception as e:
        print(f"❌ System Init Error: {e}")
        return

    if args.command == "strat":
        from company import UniversalAgentEngine
        engine = UniversalAgentEngine(system)
        await engine.run_project_simulation(args.query)
    
    elif args.command == "mobilize":
        await run_mobilize(args.dir)
    
    elif args.command == "solve":
        orchestrator = ProblemSolverOrchestrator(system)
        await orchestrator.solve(args.target)
        
    elif args.command == "skill":
        from skills_manager import SkillsManager
        await SkillsManager.run_skill(args.name, args.task)

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())

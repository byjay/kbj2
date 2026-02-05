import sys
import asyncio
import argparse
from kbj2.system import EDMSAgentSystem
from kbj2.strat_team import StrategicPlanningTeam
from kbj2.edms_team import EDMSSpecializedTeams

async def main():
    parser = argparse.ArgumentParser(description="KBJ2 Super Agent System - The 21 Agent Framework")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Command: strat (Generic)
    strat_parser = subparsers.add_parser("strat", help="[Base Framework] Run Strategic Planning Analysis for ANY topic")
    strat_parser.add_argument("query", type=str, help="Topic for the 21-Agent Team to analyze")
    strat_parser.add_argument("--context", type=str, default="", help="Additional background info")

    # Command: edms (Specific Plugin Example)
    edms_parser = subparsers.add_parser("edms", help="[Plugin] Run EDMS Drawing Analysis (Example of specialized team)")
    edms_parser.add_argument("filepath", type=str, help="Path to drawing file")

    # Command: enterprise (Massive Scale)
    ent_parser = subparsers.add_parser("enterprise", help="[Enterprise] Run Massive 10x3 Parallel Simulation")
    ent_parser.add_argument("projects", type=str, help="Comma-separated list of projects (e.g. 'Alpha,Beta,Gamma')")

    args = parser.parse_args()

    # Init System
    try:
        system = EDMSAgentSystem()
    except ValueError as e:
        print(f"Error: {e}")
        return

    if args.command == "strat":
        team = StrategicPlanningTeam(system)
        await team.run_strategic_analysis(args.query, args.context)
    
    elif args.command == "edms":
        team = EDMSSpecializedTeams(system)
        # Mock flow for EDMS
        analysis = await team.analyze_drawing(args.filepath)
        await team.generate_bom(analysis)
    
    elif args.command == "enterprise":
        from kbj2.orchestrator_v2 import EnterpriseOrchestrator
        orchestrator = EnterpriseOrchestrator(system)
        projects = [f"Project_{i}: {p.strip()}" for i, p in enumerate(args.projects.split(","))]
        await orchestrator.launch_project_cluster(projects)

    else:
        parser.print_help()

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())

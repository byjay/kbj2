import sys
import asyncio
import argparse
import os
import subprocess
from datetime import datetime

# FORCE UTF-8 OUTPUT FOR WINDOWS PIPES
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

async def run_standalone(script_name, args=None):
    """Run a standalone core script with proper environment and output."""
    cmd = [sys.executable, script_name]
    if args:
        cmd.extend(args)
    
    print(f"🚀 [EXECUTION] Running standalone core: {script_name} {' '.join(args) if args else ''}")
    
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=None, # Stream to parent stdout
        stderr=None
    )
    await process.wait()

async def main():
    parser = argparse.ArgumentParser(description="KBJ2 Supreme Commander Control Tower")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Command: strat (Strategic Analysis)
    strat_parser = subparsers.add_parser("strat", help="Strategic Planning Analysis (External)")
    strat_parser.add_argument("query", type=str, help="Topic for analysis")

    # Command: mobilize (Full 120 Agents)
    mob_parser = subparsers.add_parser("mobilize", help="Mobilize Full 120-Agent Swarm (Standalone)")
    mob_parser.add_argument("--dir", type=str, default=".", help="Target directory")

    # Command: solve (Full Auto-Debate Solver)
    solve_parser = subparsers.add_parser("solve", help="Run Full Standalone Problem Solver")
    solve_parser.add_argument("target", type=str, help="Target file/path to fix")
    solve_parser.add_argument("--iters", type=str, default="10", help="Max iterations")
    
    # Command: skill (Specialized Skills)
    skill_parser = subparsers.add_parser("skill", help="Run specialized agent skills")
    skill_parser.add_argument("name", choices=["image", "ppt", "youtube"], help="Skill name")
    skill_parser.add_argument("task", type=str, help="Task for the skill")

    # Command: server (Socket Server)
    server_parser = subparsers.add_parser("server", help="Start KBJ2 Socket-Based Agent Server")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == "strat":
        # Strategy still lives in company.py but it's complex enough to keep as is
        from company import UniversalAgentEngine
        from system import EDMSAgentSystem
        system = EDMSAgentSystem()
        engine = UniversalAgentEngine(system)
        await engine.run_project_simulation(args.query)
    
    elif args.command == "mobilize":
        # Call the FULL 300-line script
        os.environ["KBJ2_TARGET_DIR"] = args.dir
        await run_standalone("mobilize_120_agents.py")
    
    elif args.command == "solve":
        # Call the FULL 500-line orchestrator
        await run_standalone("problem_solver.py", [args.target, args.iters])
        
    elif args.command == "skill":
        # Skills are now back in root as standalone scripts
        skill_map = {
            "image": "image_generator.py",
            "ppt": "ppt_image_skill.py",
            "youtube": "youtube_analysis_skill.py"
        }
        await run_standalone(skill_map[args.name], [args.task])

    elif args.command == "server":
        await run_standalone("socket_server.py", ["server"])

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())

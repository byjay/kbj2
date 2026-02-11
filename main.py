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

    # Command: pdf (DOCX to PDF)
    pdf_parser = subparsers.add_parser("pdf", help="Convert DOCX to PDF (Background Word Export)")
    pdf_parser.add_argument("target", type=str, nargs='?', default=None, help="Path to DOCX file or directory")
    pdf_parser.add_argument("--gui", action="store_true", help="Launch Drag & Drop Visual Interface")

    # Command: server (Socket Server)
    server_parser = subparsers.add_parser("server", help="Start KBJ2 Socket-Based Agent Server")

    # Command: monitor (Real-time Stock Monitor)
    monitor_parser = subparsers.add_parser("monitor", help="Start Real-time US Stock Monitor Agent")
    monitor_parser.add_argument("--duration", type=int, default=30, help="Duration in minutes")

    # Command: r2 (Cloudflare R2 Storage)
    r2_parser = subparsers.add_parser("r2", help="R2 Cloud Storage Manager")
    r2_subparsers = r2_parser.add_subparsers(dest="r2_command", help="R2 command")

    # R2 Explore (GUI)
    r2_gui = r2_subparsers.add_parser("explore", help="Launch R2 File Explorer GUI")

    # R2 Upload
    r2_up = r2_subparsers.add_parser("upload", help="Upload files to R2")
    r2_up.add_argument("path", help="Local file or directory")
    r2_up.add_argument("--key", help="R2 destination key")
    r2_up.add_argument("--prefix", default="", help="R2 prefix for directory")

    # R2 Download
    r2_down = r2_subparsers.add_parser("download", help="Download from R2")
    r2_down.add_argument("key", help="R2 file key")
    r2_down.add_argument("--dest", help="Local destination")

    # R2 List
    r2_ls = r2_subparsers.add_parser("ls", help="List R2 files")
    r2_ls.add_argument("--prefix", default="", help="R2 prefix")

    # R2 Delete
    r2_rm = r2_subparsers.add_parser("rm", help="Delete R2 file")
    r2_rm.add_argument("key", help="R2 file key")

    # R2 Share URL
    r2_url = r2_subparsers.add_parser("share", help="Generate signed URL")
    r2_url.add_argument("key", help="R2 file key")
    r2_url.add_argument("--expires", type=int, default=3600, help="Expiration seconds")

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

    elif args.command == "pdf":
        if args.gui:
            await run_standalone("docx_to_pdf_gui.py")
        elif args.target:
            await run_standalone("docx_to_pdf_skill.py", [args.target])
        else:
            print("❌ Error: Specify a target path or use --gui")

    elif args.command == "server":
        await run_standalone("socket_server.py", ["server"])

    elif args.command == "monitor":
        await run_standalone("stock_monitor_agent.py", ["--duration", str(args.duration)])

    # Command: r2 (Cloudflare R2 Storage)
    elif args.command == "r2":
        if args.r2_command == "explore":
            await run_standalone("r2_explorer.py")
        elif args.r2_command == "upload":
            from r2_client import R2Client
            client = R2Client()
            path = args.path
            if os.path.isfile(path):
                client.upload_file(path, args.key)
            elif os.path.isdir(path):
                client.upload_dir(path, args.prefix)
        elif args.r2_command == "download":
            from r2_client import R2Client
            client = R2Client()
            client.download_file(args.key, args.dest)
        elif args.r2_command == "ls":
            from r2_client import R2Client
            client = R2Client()
            for obj in client.list_files(args.prefix):
                print(f"  {obj['key']} ({obj['size']} bytes)")
        elif args.r2_command == "rm":
            from r2_client import R2Client
            client = R2Client()
            client.delete_file(args.key)
        elif args.r2_command == "share":
            from r2_client import R2Client
            client = R2Client()
            url = client.get_signed_url(args.key, args.expires)
            print(f"Share URL: {url}")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())

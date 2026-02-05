import os
import sys
import time
import asyncio
import subprocess

# KBJ2 / SEDMS Enterprise Orchestrator
# The "One Button" solution for the Commander.

# Resolve Base Directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_script_path(filename):
    return os.path.join(BASE_DIR, filename)

SCRIPTS = {
    "FACTORY": get_script_path("expand_site_mission.py"),          # Creates contents (10 pages)
    "INFRA": get_script_path("mission_infrastructure.py"),         # Creates docs (Email Guide)
    "SWARM": get_script_path("mobilize_120_agents.py"),            # Audits & Fixes (Brand, Logo, Price, Content)
    "DRILL": get_script_path("drill_full_lifecycle.py"),           # Simulates Org Life
    "ZERO_DEFECT": get_script_path("mission_zero_defect.py"),      # Start Clean
    "FACTORY_MIGRATE": get_script_path("mission_factory_migration.py"), # Deep Clean (100 Agents)
    "FINTECH_LAUNCH": get_script_path("mission_financial_group_hq.py"),     # ISATS Financial Group HQ
    "CABLE_ANALYSIS": get_script_path("mission_cable_analysis.py"),     # Cable list update & analysis
    "DEEP_ANALYSIS": get_script_path("mission_deep_analysis.py"),     # Deep cell property inspection
    "CABLE_UPDATE": get_script_path("mission_cable_update.py"),       # Actual Update Mission
    "VBA_INJECT": get_script_path("mission_vba_injector.py"),         # VBA Automation Injector
}

async def run_script_async(name, script):
    print(f"🚀 [즉시 투입] {name} 가동...")

    # Check if exists
    if not os.path.exists(script):
        print(f"❌ Error: Script '{script}' not found.")
        return False

    max_retries = 3
    retry_count = 0
    timeout = 300  # 5 minutes timeout

    while retry_count < max_retries:
        try:
            # Create subprocess with timeout
            process = await asyncio.create_subprocess_exec(
                sys.executable, script,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env={**os.environ, "PYTHONIOENCODING": "utf-8"}
            )

            # Wait with timeout
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=timeout
            )

            if process.returncode == 0:
                print(f"✅ [임무 완수] {name} - 성공")
                return True
            else:
                retry_count += 1
                error_msg = stderr.decode("utf-8", errors="ignore").strip()[:200]

                if retry_count < max_retries:
                    print(f"⚠️ [재시도 {retry_count}/{max_retries}] {name} 실패 (Code: {process.returncode})")
                    print(f"   사유: {error_msg}")
                    await asyncio.sleep(1)
                else:
                    print(f"❌ [포기] {name} 최대 재시도 초과. 건너뜁니다.")
                    print(f"   최종 에러: {error_msg}")
                    return False

        except asyncio.TimeoutError:
            retry_count += 1
            print(f"⏱️ [타임아웃] {name} 응답 없음 ({retry_count}/{max_retries})")
            try:
                process.kill()
                await process.wait()
            except:
                pass

            if retry_count < max_retries:
                print(f"   재시도합니다...")
                await asyncio.sleep(1)
            else:
                print(f"❌ [포기] {name} 타임아웃 초과. 건너뜁니다.")
                return False

        except Exception as e:
            retry_count += 1
            print(f"⚠️ [예외] {name} 실행 중 오류: {str(e)[:100]}")

            if retry_count < max_retries:
                await asyncio.sleep(1)
            else:
                print(f"❌ [포기] {name} 실패. 건너뜁니다.")
                return False

    return False

async def main_async():
    # Parse Arguments (Lite Mode & Target)
    args = sys.argv[1:]
    target_dir = os.environ.get("KBJ2_TARGET_DIR", os.getcwd()) # Default to CWD if not set
    lite_mode = False

    if "--target" in args:
        t_index = args.index("--target")
        if t_index + 1 < len(args):
            target_dir = args[t_index + 1]
            # Clean up path
            target_dir = os.path.abspath(target_dir.strip().strip('"').strip("'"))
            
    if "--lite" in args:
        lite_mode = True
        os.environ["KBJ2_LITE_MODE"] = "true"
        print("🚀 [KBJ2] Lite Mode Activated: Skipping theatrical delays.")

    commander_order = " ".join([a for a in args if a not in ["--target", target_dir, "--lite"]])
    
    # Set Global Output for Child Scripts
    os.environ["KBJ2_TARGET_DIR"] = target_dir
    
    # Dynamic Banner (Lite vs Full)
    if not lite_mode:
        print(f"""
    ██╗  ██╗██████╗      ██╗    ██████╗ 
    ██║ ██╔╝██╔══██╗     ██║    ╚════██╗
    █████╔╝ ██████╔╝     ██║     █████╔╝
    ██╔═██╗ ██╔══██╗██   ██║    ██╔═══╝ 
    ██║  ██╗██████╔╝╚█████╔╝    ███████╗
    ╚═╝  ╚═╝╚═════╝  ╚════╝     ╚══════╝
    
    [KBJ2 Universal Orchestrator v3.3]
    [상태: 온라인 | 모드: Global Commander]
    """)
    else:
        print(f"⚡ [KBJ2 Lite] Target: {os.path.basename(target_dir)}")

    if commander_order:
        print(f"📢 [범용 지휘 모듈] 사령관님 명령: \"{commander_order}\"")
        print(f"🎯 [타겟 설정] {target_dir}")
        print("⚡ [미션 분석 중] 적합한 에이전트 선별 및 투입...")
    else:
        print("📢 [대기] 목표 설정되지 않음. 대기 모드로 전환합니다.")
    
    print("---------------------------------------------------")
    print("⚡ [병렬 지휘 모드] 전 부서 동시 타격 개시...")
    await asyncio.sleep(2)
    
    # Update Status Logic
    print(f"\n🔍 [시스템] 타겟 디렉토리 스캔: '{target_dir}'")
    if not os.path.exists(target_dir):
        print(f"⚠️ [경고] 타겟 경로가 존재하지 않습니다: {target_dir}")
        
    current_project = os.path.basename(target_dir) if target_dir else "Generic Project"
    print(f"⚠️ [주의] KBJ2는 현재 '{current_project}' 관리 모드로 작동합니다.")

    # Define Tasks
    tasks = []
    
    # 1. Swarm is always active (Monitoring)
    tasks.append(run_script_async("에이전트 스웜 (감시)", SCRIPTS["SWARM"]))
    
    # 2. If 'Audit' or '감사', run Zero Defect
    if "감사" in commander_order or "Audit" in commander_order or "Check" in commander_order:
         tasks.append(run_script_async("결점 감사 (QA)", SCRIPTS["ZERO_DEFECT"]))

    # 3. If 'Factory', '이사', '이식', run Factory Migration
    if "Factory" in commander_order or "이사" in commander_order or "이식" in commander_order or "공장" in commander_order:
        tasks.append(run_script_async("공장 대이동 (100인 생산팀)", SCRIPTS["FACTORY_MIGRATE"]))
        tasks.append(run_script_async("콘텐츠 공장 (생산)", SCRIPTS["FACTORY"]))

        tasks.append(run_script_async("인프라 본부", SCRIPTS["INFRA"]))
        tasks.append(run_script_async("조직 훈련", SCRIPTS["DRILL"]))

    # 4. Fintech / Stock Trading (ISATS Ferrari)
    if any(k in commander_order.lower() for k in ["stock", "trading", "주식", "매매", "ferrari", "fintech", "launch"]):
        # Detect Mode
        mode = "virtual"
        if "real" in commander_order.lower() or "실전" in commander_order or "live" in commander_order.lower():
             mode = "real"
        
        # Detect Market
        market = "generic"
        if "us" in commander_order.lower() or "미국" in commander_order or "nasdaq" in commander_order.lower():
            market = "us"

        async def run_fintech_special():
             cmd = [sys.executable, SCRIPTS["FINTECH_LAUNCH"], mode, market]
             print(f"🚀 [Fintech Division] Launching Project Ferrari in '{mode.upper()}' Mode (Market: {market.upper()})...")
             proc = await asyncio.create_subprocess_exec(
                 *cmd,
                 stdout=asyncio.subprocess.PIPE,
                 stderr=asyncio.subprocess.PIPE
             )
             stdout, stderr = await proc.communicate()
             if stdout: print(stdout.decode('utf-8', errors='replace'))
             if stderr: print(f"⚠️ [Fintech Error] {stderr.decode('utf-8', errors='replace')}")
             return proc.returncode == 0
             
        tasks.append(run_fintech_special())

    # 5. Cable Missions (Update vs Analysis)
    if "update" in commander_order.lower() or "업데이트" in commander_order:
         tasks.append(run_script_async("케이블 데이터 업데이트 (Update Ops)", SCRIPTS["CABLE_UPDATE"]))
    elif any(k in commander_order.lower() for k in ["cable", "케이블", "analysis", "분석"]):
         tasks.append(run_script_async("케이블 데이터 분석 (Data Ops)", SCRIPTS["CABLE_ANALYSIS"]))
         
    # 6. Deep Analysis
         
    # 6. Deep Analysis
    if any(k in commander_order.lower() for k in ["deep", "심층", "property", "속성"]):
         tasks.append(run_script_async("심층 세포 분석 (Deep Scan)", SCRIPTS["DEEP_ANALYSIS"]))

    # 7. VBA Injection
    if any(k in commander_order.lower() for k in ["vba", "macro", "button", "매크로"]):
         tasks.append(run_script_async("VBA 자동화 탑재 (Automation Ops)", SCRIPTS["VBA_INJECT"]))

    # Execute All in Parallel
    results = await asyncio.gather(*tasks)
    
    print("\n🏁 [최종 보고] 모든 병렬 임무가 종료되었습니다.")
    print(f"   - 총 투입 부서: {len(results)}")
    print(f"   - 수행 결과: {'성공' if all(results) else '일부 실패'}")
    print(f"   - 현재 상태: {current_project} 정상 가동 중")
    print("   - 대기 상태: 다음 명령을 기다립니다.")
    print("="*50)

def main():
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(main_async())

if __name__ == "__main__":
    main()

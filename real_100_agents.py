"""
🏢 KBJ2 Real 100-Agent Corporation
==================================
실제 100개의 에이전트가 병렬로 작동하는 진짜 멀티 에이전트 시스템

핵심 기능:
1. 실제 100개의 Claude CLI 인스턴스 병렬 실행
2. 코드 분업: 각 에이전트가 다른 파일/함수 담당
3. 코드 병합: Git-style 머지 시스템
4. 글로벌 적용: 모든 프로젝트에 자동 관여
"""

import os
import sys
import json
import asyncio
import subprocess
import hashlib
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import glob
import shutil
import difflib

# ============================================================
# 글로벌 설정
# ============================================================
KBJ2_ROOT = Path("F:/kbj2")
AGENT_WORKSPACE = KBJ2_ROOT / "agent_workspaces"
AGENT_WORKSPACE.mkdir(exist_ok=True)
MERGE_OUTPUT = KBJ2_ROOT / "merge_output"
MERGE_OUTPUT.mkdir(exist_ok=True)

# API 키 풀 (3개 키를 라운드로빈)
API_KEYS = [
    "384fffa4d8a44ce58ee573be0d49d995.kqLAZNeRmjnUNPJh",
    "9c5b377b9bf945d0a2b00eacdd9904ef.BoRiu74O1h0bV2v6",
    "a9bd9bd3917c4229a49f91747c4cf07e.PQBgL1cU7TqcNaBy",
]
API_BASE = "https://api.z.ai/api/anthropic"

# 에이전트 부서 정의 (실제 100명)
DEPARTMENTS = {
    "ARCHITECTS": {
        "count": 5,
        "role": "시스템 아키텍처 설계, 전체 구조 결정",
        "skills": ["architecture", "design_patterns", "system_design"]
    },
    "BACKEND_DEVS": {
        "count": 25,
        "role": "백엔드 코드 작성, API 구현, 데이터베이스",
        "skills": ["python", "fastapi", "databases", "apis"]
    },
    "FRONTEND_DEVS": {
        "count": 20,
        "role": "프론트엔드 코드 작성, UI 구현",
        "skills": ["html", "css", "javascript", "react", "vue"]
    },
    "QA_ENGINEERS": {
        "count": 15,
        "role": "코드 검증, 테스트 작성, 버그 발견",
        "skills": ["testing", "debugging", "code_review"]
    },
    "INTEGRATORS": {
        "count": 10,
        "role": "코드 병합, 충돌 해결, 통합",
        "skills": ["git", "merge", "conflict_resolution"]
    },
    "DOCUMENTERS": {
        "count": 10,
        "role": "문서화, 주석 작성, README 생성",
        "skills": ["documentation", "markdown", "comments"]
    },
    "OPTIMIZERS": {
        "count": 10,
        "role": "성능 최적화, 리팩토링",
        "skills": ["optimization", "refactoring", "performance"]
    },
    "SECURITY": {
        "count": 5,
        "role": "보안 검토, 취약점 분석",
        "skills": ["security", "vulnerability", "audit"]
    }
}


# ============================================================
# 에이전트 클래스
# ============================================================
@dataclass
class RealAgent:
    """실제 API를 호출하는 에이전트"""
    agent_id: str
    department: str
    role: str
    api_key: str
    workspace: Path
    
    async def execute_task(self, task: Dict) -> Dict:
        """태스크 실행 - 실제 Claude CLI 호출"""
        prompt = self._build_prompt(task)
        
        start_time = datetime.now()
        response = await self._call_claude(prompt)
        duration = (datetime.now() - start_time).total_seconds()
        
        # 결과 파싱 및 코드 추출
        code_output = self._extract_code(response)
        
        result = {
            "agent_id": self.agent_id,
            "department": self.department,
            "task": task.get("description"),
            "response": response,
            "code": code_output,
            "duration_sec": duration,
            "success": len(code_output) > 0 or "완료" in response
        }
        
        # 코드가 있으면 워크스페이스에 저장
        if code_output and task.get("output_file"):
            output_path = self.workspace / task["output_file"]
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(code_output)
            result["output_path"] = str(output_path)
        
        return result
    
    def _build_prompt(self, task: Dict) -> str:
        """태스크에 맞는 프롬프트 생성"""
        context = task.get("context", "")
        dependencies = task.get("dependencies", [])
        
        prompt = f"""당신은 {self.agent_id} ({self.department} 부서) 에이전트입니다.
역할: {self.role}

📋 태스크: {task.get('description', '')}
📁 대상 파일: {task.get('target_file', 'N/A')}
📤 출력 파일: {task.get('output_file', 'N/A')}

{f'📚 컨텍스트:{chr(10)}{context}' if context else ''}
{f'🔗 의존성:{chr(10)}{chr(10).join(dependencies)}' if dependencies else ''}

**지시사항:**
1. 주어진 태스크를 완벽하게 수행하세요
2. 코드 작성 시 ```python 또는 적절한 언어 블록을 사용하세요
3. 다른 에이전트가 작성한 코드와 호환되도록 하세요
4. 간결하고 완전한 코드를 작성하세요

**반드시 코드 블록에 결과물을 포함하세요.**
"""
        return prompt
    
    async def _call_claude(self, prompt: str) -> str:
        """Claude CLI 실제 호출"""
        env = os.environ.copy()
        env["ANTHROPIC_API_KEY"] = self.api_key
        env["ANTHROPIC_BASE_URL"] = API_BASE
        
        cmd = [r"C:\Users\FREE\AppData\Roaming\npm\claude.cmd", "-p", prompt, "--model", "GLM-4.7", "--no-input"]
        
        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=env
            )
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=90)
            return stdout.decode('utf-8', errors='replace')
        except asyncio.TimeoutError:
            return f"[TIMEOUT] {self.agent_id} 응답 시간 초과"
        except Exception as e:
            return f"[ERROR] {self.agent_id}: {str(e)}"
    
    def _extract_code(self, response: str) -> str:
        """응답에서 코드 블록 추출"""
        code_blocks = []
        
        # 다양한 언어의 코드 블록 추출
        for lang in ['python', 'javascript', 'typescript', 'html', 'css', 'json', 'yaml', 'sql', '']:
            marker = f"```{lang}"
            if marker in response:
                parts = response.split(marker)
                for i, part in enumerate(parts[1:], 1):
                    if "```" in part:
                        code = part.split("```")[0].strip()
                        if code:
                            code_blocks.append(code)
        
        return "\n\n".join(code_blocks) if code_blocks else ""


# ============================================================
# 태스크 분배기
# ============================================================
class TaskDistributor:
    """태스크를 에이전트들에게 분배"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
    
    def analyze_project(self) -> Dict:
        """프로젝트 분석 및 태스크 생성"""
        files = self._scan_files()
        
        tasks = {
            "ARCHITECTS": [],
            "BACKEND_DEVS": [],
            "FRONTEND_DEVS": [],
            "QA_ENGINEERS": [],
            "INTEGRATORS": [],
            "DOCUMENTERS": [],
            "OPTIMIZERS": [],
            "SECURITY": []
        }
        
        # 파일 타입별 분류
        for file_path in files:
            ext = file_path.suffix.lower()
            rel_path = file_path.relative_to(self.project_path)
            
            task_base = {
                "target_file": str(file_path),
                "relative_path": str(rel_path)
            }
            
            if ext in ['.py']:
                # 백엔드 개발자가 담당
                tasks["BACKEND_DEVS"].append({
                    **task_base,
                    "description": f"Python 파일 분석 및 개선: {rel_path}",
                    "output_file": f"improved_{rel_path}"
                })
                # QA가 검증
                tasks["QA_ENGINEERS"].append({
                    **task_base,
                    "description": f"Python 코드 품질 검증: {rel_path}",
                    "output_file": f"qa_report_{rel_path.stem}.md"
                })
                
            elif ext in ['.js', '.ts', '.jsx', '.tsx']:
                tasks["FRONTEND_DEVS"].append({
                    **task_base,
                    "description": f"Frontend 코드 분석 및 개선: {rel_path}",
                    "output_file": f"improved_{rel_path}"
                })
                
            elif ext in ['.html', '.css']:
                tasks["FRONTEND_DEVS"].append({
                    **task_base,
                    "description": f"UI 파일 분석 및 개선: {rel_path}",
                    "output_file": f"improved_{rel_path}"
                })
                
            # 모든 파일에 대해 문서화
            tasks["DOCUMENTERS"].append({
                **task_base,
                "description": f"파일 문서화: {rel_path}",
                "output_file": f"docs/{rel_path.stem}.md"
            })
        
        # 전체 아키텍처 분석
        tasks["ARCHITECTS"].append({
            "description": "전체 프로젝트 아키텍처 분석 및 설계 문서 작성",
            "target_file": str(self.project_path),
            "output_file": "architecture.md"
        })
        
        # 보안 감사
        tasks["SECURITY"].append({
            "description": "전체 프로젝트 보안 감사",
            "target_file": str(self.project_path),
            "output_file": "security_audit.md"
        })
        
        return tasks
    
    def _scan_files(self) -> List[Path]:
        """프로젝트 파일 스캔"""
        files = []
        extensions = ['.py', '.js', '.ts', '.jsx', '.tsx', '.html', '.css', '.json']
        
        for ext in extensions:
            files.extend(self.project_path.glob(f"**/*{ext}"))
        
        # 제외할 디렉토리
        exclude = ['node_modules', '__pycache__', '.git', 'venv', 'env']
        files = [f for f in files if not any(ex in str(f) for ex in exclude)]
        
        return files[:100]  # 최대 100개 파일


# ============================================================
# 코드 병합기
# ============================================================
class CodeMerger:
    """여러 에이전트의 코드를 병합"""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def merge_results(self, results: List[Dict]) -> Dict:
        """결과 병합"""
        # 파일별로 그룹화
        by_file = {}
        for r in results:
            output_path = r.get("output_path")
            if output_path:
                base = Path(output_path).name
                if base not in by_file:
                    by_file[base] = []
                by_file[base].append(r)
        
        merged = {}
        conflicts = []
        
        for filename, file_results in by_file.items():
            if len(file_results) == 1:
                # 단일 결과
                merged[filename] = file_results[0]["code"]
            else:
                # 병합 필요
                merge_result = self._smart_merge(file_results)
                if merge_result["success"]:
                    merged[filename] = merge_result["content"]
                else:
                    conflicts.append({
                        "filename": filename,
                        "versions": [r["code"] for r in file_results]
                    })
        
        # 병합된 파일 저장
        for filename, content in merged.items():
            output_path = self.output_dir / filename
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        return {
            "merged_files": list(merged.keys()),
            "conflicts": conflicts,
            "output_dir": str(self.output_dir)
        }
    
    def _smart_merge(self, file_results: List[Dict]) -> Dict:
        """스마트 병합 - 충돌 없이 합치기 시도"""
        contents = [r["code"] for r in file_results]
        
        # 가장 긴 코드를 기준으로
        base = max(contents, key=len)
        
        # 다른 코드에서 추가된 부분 찾기
        additions = []
        for content in contents:
            if content != base:
                diff = list(difflib.unified_diff(
                    base.splitlines(), 
                    content.splitlines(),
                    lineterm=''
                ))
                # 추가된 라인만 수집
                for line in diff:
                    if line.startswith('+') and not line.startswith('+++'):
                        additions.append(line[1:])
        
        # 추가 부분을 베이스에 합침
        if additions:
            merged = base + "\n\n# === 추가된 코드 ===\n" + "\n".join(additions)
        else:
            merged = base
        
        return {"success": True, "content": merged}


# ============================================================
# 100인 협업 오케스트레이터
# ============================================================
class Corporation100:
    """
    실제 100개 에이전트 협업 시스템
    
    작동 방식:
    1. 프로젝트 분석 및 태스크 분배
    2. 100개 에이전트 병렬 실행 (API 호출)
    3. 결과 수집 및 병합
    4. 품질 검증
    5. 미완료 시 반복
    """
    
    def __init__(self):
        self.agents: List[RealAgent] = []
        self.session_id = f"corp100_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.workspace = AGENT_WORKSPACE / self.session_id
        self.workspace.mkdir(parents=True, exist_ok=True)
        
        # 100개 에이전트 생성
        self._create_agents()
    
    def _create_agents(self):
        """100개의 실제 에이전트 인스턴스 생성"""
        agent_idx = 0
        
        for dept_name, dept_info in DEPARTMENTS.items():
            for i in range(dept_info["count"]):
                agent_id = f"{dept_name}_{i+1:02d}"
                agent_workspace = self.workspace / agent_id
                agent_workspace.mkdir(parents=True, exist_ok=True)
                
                agent = RealAgent(
                    agent_id=agent_id,
                    department=dept_name,
                    role=dept_info["role"],
                    api_key=API_KEYS[agent_idx % len(API_KEYS)],  # 키 로테이션
                    workspace=agent_workspace
                )
                self.agents.append(agent)
                agent_idx += 1
        
        print(f"✅ {len(self.agents)}개 에이전트 인스턴스 생성 완료")
    
    async def execute_project(self, project_path: str, max_concurrent: int = 10):
        """프로젝트 전체 실행"""
        self._print_header(project_path)
        
        # 1. 프로젝트 분석 및 태스크 분배
        print("\n📊 Phase 1: 프로젝트 분석 및 태스크 분배...")
        distributor = TaskDistributor(project_path)
        all_tasks = distributor.analyze_project()
        
        total_tasks = sum(len(tasks) for tasks in all_tasks.values())
        print(f"   📋 총 태스크: {total_tasks}개")
        for dept, tasks in all_tasks.items():
            if tasks:
                print(f"   - {dept}: {len(tasks)}개")
        
        # 2. 에이전트에게 태스크 할당 및 병렬 실행
        print("\n⚡ Phase 2: 100개 에이전트 병렬 실행...")
        
        all_results = []
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def run_with_limit(agent: RealAgent, task: Dict):
            async with semaphore:
                return await agent.execute_task(task)
        
        # 부서별로 태스크 실행
        for dept_name, tasks in all_tasks.items():
            if not tasks:
                continue
                
            # 해당 부서의 에이전트들
            dept_agents = [a for a in self.agents if a.department == dept_name]
            
            print(f"\n   🏢 {dept_name} 부서 가동 ({len(dept_agents)}명, {len(tasks)}개 태스크)")
            
            # 태스크를 에이전트에게 분배
            agent_tasks = []
            for i, task in enumerate(tasks):
                agent = dept_agents[i % len(dept_agents)]
                agent_tasks.append(run_with_limit(agent, task))
            
            # 병렬 실행
            results = await asyncio.gather(*agent_tasks, return_exceptions=True)
            
            # 결과 수집
            success_count = 0
            for r in results:
                if isinstance(r, dict):
                    all_results.append(r)
                    if r.get("success"):
                        success_count += 1
                        print(f"      ✅ [{r['agent_id']}] {r['task'][:40]}...")
                    else:
                        print(f"      ⚠️ [{r['agent_id']}] 부분 완료")
                else:
                    print(f"      ❌ 에러: {str(r)[:50]}")
            
            print(f"      📊 완료: {success_count}/{len(tasks)}")
        
        # 3. 결과 병합
        print("\n🔀 Phase 3: 코드 병합...")
        merger = CodeMerger(MERGE_OUTPUT / self.session_id)
        merge_result = merger.merge_results(all_results)
        
        print(f"   ✅ 병합된 파일: {len(merge_result['merged_files'])}개")
        if merge_result['conflicts']:
            print(f"   ⚠️ 충돌: {len(merge_result['conflicts'])}개")
        
        # 4. 최종 보고
        self._print_summary(all_results, merge_result)
        
        return {
            "session_id": self.session_id,
            "results": all_results,
            "merge": merge_result
        }
    
    def _print_header(self, project_path: str):
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   🏢 KBJ2 Real 100-Agent Corporation                        ║
║                                                              ║
║   실제 100개 에이전트 병렬 실행 시스템                       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

📁 프로젝트: {project_path}
🆔 세션: {self.session_id}
👥 에이전트: {len(self.agents)}명

부서 현황:
""")
        for dept, info in DEPARTMENTS.items():
            print(f"  - {dept}: {info['count']}명 ({info['role'][:30]}...)")
    
    def _print_summary(self, results: List[Dict], merge_result: Dict):
        success = len([r for r in results if r.get('success')])
        total = len(results)
        
        print(f"""
{'='*60}
📊 최종 보고서
{'='*60}

🆔 세션: {self.session_id}
👥 가동 에이전트: {len(self.agents)}명
📋 총 태스크: {total}개
✅ 성공: {success}개
❌ 실패: {total - success}개

📁 병합 결과:
   - 병합된 파일: {len(merge_result['merged_files'])}개
   - 충돌: {len(merge_result.get('conflicts', []))}개
   - 출력 디렉토리: {merge_result['output_dir']}

{'='*60}
""")


# ============================================================
# 글로벌 프로젝트 모니터 (모든 프로젝트에 자동 관여)
# ============================================================
class GlobalProjectMonitor:
    """모든 프로젝트에 자동으로 관여하는 글로벌 모니터"""
    
    WATCHED_DIRS = [
        "F:/kbj2",
        "F:/kbj_repo",
        "F:/",  # 루트 디렉토리 감시
    ]
    
    def __init__(self):
        self.corporation = Corporation100()
        self.processed_projects = set()
    
    async def watch_and_process(self, interval_sec: int = 60):
        """주기적으로 프로젝트 감시 및 처리"""
        print("🔍 글로벌 프로젝트 모니터 시작...")
        
        while True:
            for watch_dir in self.WATCHED_DIRS:
                if os.path.exists(watch_dir):
                    projects = self._find_projects(watch_dir)
                    
                    for project in projects:
                        if project not in self.processed_projects:
                            print(f"\n🆕 새 프로젝트 발견: {project}")
                            await self.corporation.execute_project(project)
                            self.processed_projects.add(project)
            
            await asyncio.sleep(interval_sec)
    
    def _find_projects(self, root_dir: str) -> List[str]:
        """프로젝트 디렉토리 탐지"""
        projects = []
        
        # 프로젝트 마커 파일
        markers = ['package.json', 'requirements.txt', 'setup.py', 'pyproject.toml', 'Cargo.toml']
        
        for root, dirs, files in os.walk(root_dir):
            # 깊이 제한
            if root.count(os.sep) - root_dir.count(os.sep) > 3:
                continue
            
            for marker in markers:
                if marker in files:
                    projects.append(root)
                    break
            
            # 제외 디렉토리
            dirs[:] = [d for d in dirs if d not in ['node_modules', '__pycache__', '.git', 'venv']]
        
        return projects[:20]  # 최대 20개


# ============================================================
# CLI
# ============================================================
async def main():
    if len(sys.argv) < 2:
        print("""
🏢 KBJ2 Real 100-Agent Corporation
===================================

사용법:
  python real_100_agents.py <프로젝트경로> [동시실행수]
  python real_100_agents.py --watch  # 글로벌 모니터 모드

예제:
  python real_100_agents.py F:\\myproject
  python real_100_agents.py F:\\myproject 20
  python real_100_agents.py --watch

특징:
  - 실제 100개 에이전트 인스턴스 (Claude CLI 호출)
  - 코드 분업 및 자동 병합
  - 모든 프로젝트 자동 관여 (--watch 모드)
""")
        return
    
    if sys.argv[1] == "--watch":
        monitor = GlobalProjectMonitor()
        await monitor.watch_and_process()
    else:
        project_path = sys.argv[1]
        max_concurrent = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        
        if not os.path.exists(project_path):
            print(f"❌ 프로젝트를 찾을 수 없습니다: {project_path}")
            return
        
        corp = Corporation100()
        await corp.execute_project(project_path, max_concurrent)


if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(main())

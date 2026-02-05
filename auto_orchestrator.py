"""
🤖 KBJ2 Auto Orchestrator - 자연어 명령 자동 실행
=====================================================
"kbj2 갤러그게임 만들어" 처럼 자연어로 명령하면
자동으로 에이전트가 분석 → 토론 → 개발 → 검증

사용법:
  kbj2 <자연어 명령>
  kbj2 웹게임 만들어
  kbj2 버그 수정해
  kbj2 코드 분석해
"""

import os
import sys
import asyncio
import subprocess
import json
from pathlib import Path
from datetime import datetime

KBJ2_ROOT = Path("F:/kbj2")

API_KEYS = [
    "384fffa4d8a44ce58ee573be0d49d995.kqLAZNeRmjnUNPJh",
    "9c5b377b9bf945d0a2b00eacdd9904ef.BoRiu74O1h0bV2v6",
    "a9bd9bd3917c4229a49f91747c4cf07e.PQBgL1cU7TqcNaBy",
]
API_BASE = "https://api.z.ai/api/anthropic"


class AutoOrchestrator:
    """
    자연어 명령을 받아서 자동으로:
    1. 명령 분석 (어떤 작업인지 파악)
    2. 필요한 에이전트 선택 (개발? 분석? 문서화?)
    3. 에이전트 토론 시작
    4. 코드 생성
    5. 검증 및 완료
    """
    
    TASK_PATTERNS = {
        "게임": "game_development",
        "웹": "web_development",
        "분석": "analysis",
        "수정": "fix_bug",
        "리팩토링": "refactoring",
        "문서": "documentation",
        "테스트": "testing",
        "API": "api_development",
        "DB": "database",
    }
    
    def __init__(self):
        self.session_id = f"auto_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.work_dir = None
    
    async def execute(self, command: str, target_dir: str = None):
        """자연어 명령 실행"""
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║  🤖 KBJ2 Auto Orchestrator                                   ║
║  자연어 → 에이전트 자동 실행                                  ║
╚══════════════════════════════════════════════════════════════╝

📝 명령: {command}
🆔 세션: {self.session_id}
""")
        
        # 1. 명령 분석
        print("🔍 Step 1: 명령 분석 중...")
        task_type = self._analyze_command(command)
        print(f"   📋 작업 유형: {task_type}")
        
        # 2. 작업 디렉토리 설정
        if target_dir:
            self.work_dir = Path(target_dir)
        else:
            self.work_dir = Path(os.getcwd())
        print(f"   📁 작업 폴더: {self.work_dir}")
        
        # 3. 에이전트 토론 시작
        print("\n💬 Step 2: 에이전트 토론 시작...")
        discussion = await self._run_agent_discussion(command, task_type)
        
        # 4. 코드 생성
        print("\n⚡ Step 3: 코드 생성 중...")
        code = await self._generate_code(command, task_type, discussion)
        
        # 5. 검증
        print("\n✅ Step 4: 검증 중...")
        await self._verify(code)
        
        print(f"""
{'='*60}
✅ 작업 완료!
📁 결과물: {self.work_dir}
{'='*60}
""")
    
    def _analyze_command(self, command: str) -> str:
        """명령어 분석해서 작업 유형 결정"""
        for keyword, task_type in self.TASK_PATTERNS.items():
            if keyword in command:
                return task_type
        return "general"
    
    async def _run_agent_discussion(self, command: str, task_type: str) -> dict:
        """KBJ + KBJ2 에이전트 토론"""
        
        # KBJ (전략) 호출
        print("   🧠 [KBJ] 전략 분석 중...")
        kbj_response = await self._call_agent("KBJ", f"""
당신은 KBJ 전략 에이전트입니다.
작업: {command}
유형: {task_type}

1. 이 작업을 어떻게 수행할지 전략을 수립하세요
2. 필요한 파일 목록을 제시하세요
3. 기술 스택을 추천하세요

JSON으로 응답:
{{"strategy": "전략", "files": ["파일1", "파일2"], "tech_stack": ["기술1", "기술2"]}}
""")
        print(f"   ✓ KBJ: {kbj_response[:100]}...")
        
        # KBJ2 (실행) 호출
        print("   ⚡ [KBJ2] 실행 계획 수립 중...")
        kbj2_response = await self._call_agent("KBJ2", f"""
당신은 KBJ2 실행 에이전트입니다.
작업: {command}
KBJ의 전략: {kbj_response[:500]}

1. 구체적인 실행 계획을 수립하세요
2. 코드 구조를 설계하세요
3. 예상 결과물을 명시하세요

JSON으로 응답:
{{"plan": "계획", "code_structure": "구조", "deliverables": ["결과물1"]}}
""")
        print(f"   ✓ KBJ2: {kbj2_response[:100]}...")
        
        return {"kbj": kbj_response, "kbj2": kbj2_response}
    
    async def _generate_code(self, command: str, task_type: str, discussion: dict) -> str:
        """코드 생성"""
        
        if task_type == "game_development":
            return await self._generate_game_code(command, discussion)
        elif task_type == "web_development":
            return await self._generate_web_code(command, discussion)
        else:
            return await self._generate_general_code(command, discussion)
    
    async def _generate_game_code(self, command: str, discussion: dict) -> str:
        """게임 코드 생성"""
        print("   🎮 게임 코드 생성 중...")
        
        response = await self._call_agent("DEV", f"""
당신은 게임 개발 에이전트입니다.
요청: {command}
전략: {discussion.get('kbj', '')[:300]}
계획: {discussion.get('kbj2', '')[:300]}

완전한 HTML/JavaScript 게임 코드를 작성하세요.
Three.js를 사용한 3D 게임이면 더 좋습니다.
코드 블록 안에 전체 코드를 작성하세요.
""")
        
        # 코드 추출 및 저장
        code = self._extract_code(response)
        if code:
            output_file = self.work_dir / "index.html"
            self.work_dir.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(code)
            print(f"   ✓ 저장됨: {output_file}")
        
        return code
    
    async def _generate_web_code(self, command: str, discussion: dict) -> str:
        """웹 코드 생성"""
        # 게임과 동일한 로직
        return await self._generate_game_code(command, discussion)
    
    async def _generate_general_code(self, command: str, discussion: dict) -> str:
        """일반 코드 생성"""
        return await self._generate_game_code(command, discussion)
    
    async def _verify(self, code: str):
        """코드 검증"""
        print("   🔍 [QA] 코드 검증 중...")
        
        qa_response = await self._call_agent("QA", f"""
당신은 QA 검증 에이전트입니다.
다음 코드를 검증하세요:

{code[:2000]}

1. 문법 오류 확인
2. 보안 취약점 확인
3. 성능 문제 확인

JSON으로 응답:
{{"passed": true/false, "issues": ["이슈1"], "score": 0-100}}
""")
        
        print(f"   ✓ QA: {qa_response[:100]}...")
    
    async def _call_agent(self, agent_name: str, prompt: str) -> str:
        """에이전트 호출 (Claude CLI)"""
        env = os.environ.copy()
        env["ANTHROPIC_API_KEY"] = API_KEYS[hash(agent_name) % len(API_KEYS)]
        env["ANTHROPIC_BASE_URL"] = API_BASE
        
        try:
            proc = await asyncio.create_subprocess_exec(
            r"C:\Users\FREE\AppData\Roaming\npm\claude.cmd", "-p", prompt, "--model", "GLM-4.7", "--no-input",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=env
            )
            stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=90)
            return stdout.decode('utf-8', errors='replace')
        except Exception as e:
            return f"[에러] {str(e)}"
    
    def _extract_code(self, response: str) -> str:
        """응답에서 코드 추출"""
        for lang in ['html', 'javascript', 'python', '']:
            marker = f"```{lang}"
            if marker in response:
                parts = response.split(marker)
                if len(parts) > 1:
                    code = parts[1].split("```")[0].strip()
                    if code:
                        return code
        return response


async def main():
    if len(sys.argv) < 2:
        print("""
🤖 KBJ2 Auto Orchestrator
==========================

사용법:
  python auto_orchestrator.py "<자연어 명령>" [작업폴더]

예제:
  python auto_orchestrator.py "갤러그 게임 만들어"
  python auto_orchestrator.py "버그 수정해" F:\\myproject
  python auto_orchestrator.py "웹사이트 만들어" C:\\Users\\FREE\\Desktop\\Web

특징:
  - 자연어 명령 자동 분석
  - KBJ + KBJ2 에이전트 자동 토론
  - 코드 생성 및 검증
  - 결과물 자동 저장
""")
        return
    
    command = sys.argv[1]
    target_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    orchestrator = AutoOrchestrator()
    await orchestrator.execute(command, target_dir)


if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(main())

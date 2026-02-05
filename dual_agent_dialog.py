"""
🤝 KBJ ↔ KBJ2 Dual-Agent Dialog System
====================================
두 에이전트가 서로 분석하고 의견을 주고받는 자동화 시스템

작동 방식:
1. 파일/폴더 대상 지정
2. KBJ, KBJ2 동시 분석 실행
3. 서로의 분석 결과 교환
4. 의견 토론 (최대 3라운드)
5. 최종 합의/결론 도출

사용자는 실시간으로 토론 과정을 지켜볼 수 있음
"""

import os
import sys
import json
import time
import asyncio
import subprocess
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any
from pathlib import Path
from enum import Enum

# ============================================================
# 환경 설정
# ============================================================
KBJ_ROOT = Path("F:/kbj_repo")
KBJ2_ROOT = Path("F:/kbj2")
DIALOG_DIR = KBJ2_ROOT / "agent_dialog_logs"
DIALOG_DIR.mkdir(exist_ok=True)

# API 키 로테이션
API_KEYS = [
    "384fffa4d8a44ce58ee573be0d49d995.kqLAZNeRmjnUNPJh",
    "9c5b377b9bf945d0a2b00eacdd9904ef.BoRiu74O1h0bV2v6",
    "a9bd9bd3917c4229a49f91747c4cf07e.PQBgL1cU7TqcNaBy",
]

class AgentType(Enum):
    KBJ = "kbj"
    KBJ2 = "kbj2"

class MessageType(Enum):
    ANALYSIS = "analysis"       # 초기 분석
    OPINION = "opinion"         # 의견 제시
    COUNTER = "counter"         # 반론
    AGREEMENT = "agreement"     # 동의
    QUESTION = "question"       # 질문
    CONCLUSION = "conclusion"   # 결론

# ============================================================
# 데이터 클래스
# ============================================================
@dataclass
class DialogMessage:
    """에이전트 간 대화 메시지"""
    sender: AgentType
    receiver: AgentType
    message_type: MessageType
    content: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    round_num: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self):
        d = asdict(self)
        d['sender'] = self.sender.value
        d['receiver'] = self.receiver.value
        d['message_type'] = self.message_type.value
        return d
    
    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            sender=AgentType(d['sender']),
            receiver=AgentType(d['receiver']),
            message_type=MessageType(d['message_type']),
            content=d['content'],
            timestamp=d.get('timestamp', datetime.now().isoformat()),
            round_num=d.get('round_num', 0),
            metadata=d.get('metadata', {})
        )

@dataclass
class DialogSession:
    """토론 세션"""
    session_id: str
    target: str  # 분석 대상 (파일/폴더 경로)
    topic: str   # 토론 주제
    messages: List[DialogMessage] = field(default_factory=list)
    current_round: int = 0
    max_rounds: int = 3
    status: str = "active"  # active, concluded, timeout
    started_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def add_message(self, msg: DialogMessage):
        msg.round_num = self.current_round
        self.messages.append(msg)
        self._save()
    
    def next_round(self):
        self.current_round += 1
        if self.current_round >= self.max_rounds:
            self.status = "concluded"
        self._save()
    
    def _save(self):
        """세션을 JSON 파일로 저장"""
        filepath = DIALOG_DIR / f"{self.session_id}.json"
        data = {
            'session_id': self.session_id,
            'target': self.target,
            'topic': self.topic,
            'messages': [m.to_dict() for m in self.messages],
            'current_round': self.current_round,
            'max_rounds': self.max_rounds,
            'status': self.status,
            'started_at': self.started_at
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    @classmethod
    def load(cls, session_id: str):
        """세션 로드"""
        filepath = DIALOG_DIR / f"{session_id}.json"
        if not filepath.exists():
            return None
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        session = cls(
            session_id=data['session_id'],
            target=data['target'],
            topic=data['topic'],
            current_round=data['current_round'],
            max_rounds=data['max_rounds'],
            status=data['status'],
            started_at=data['started_at']
        )
        session.messages = [DialogMessage.from_dict(m) for m in data['messages']]
        return session


# ============================================================
# 에이전트 인터페이스
# ============================================================
class AgentInterface:
    """개별 에이전트와의 통신 인터페이스"""
    
    def __init__(self, agent_type: AgentType):
        self.agent_type = agent_type
        self.root = KBJ_ROOT if agent_type == AgentType.KBJ else KBJ2_ROOT
        self.api_key_index = 0 if agent_type == AgentType.KBJ else 1
    
    def _get_api_key(self):
        """API 키 반환"""
        return API_KEYS[self.api_key_index % len(API_KEYS)]
    
    async def analyze(self, target: str, context: str = "") -> str:
        """대상 분석 요청"""
        prompt = self._build_analysis_prompt(target, context)
        return await self._call_agent(prompt)
    
    async def respond_to(self, message: DialogMessage, session: DialogSession) -> str:
        """다른 에이전트의 메시지에 응답"""
        prompt = self._build_response_prompt(message, session)
        return await self._call_agent(prompt)
    
    def _build_analysis_prompt(self, target: str, context: str) -> str:
        """분석 프롬프트 생성"""
        agent_name = "KBJ" if self.agent_type == AgentType.KBJ else "KBJ2"
        return f"""당신은 {agent_name} 에이전트입니다. 다른 에이전트({self._get_partner_name()})와 협업 중입니다.

🎯 분석 대상: {target}
{f'📋 추가 컨텍스트: {context}' if context else ''}

**지시사항:**
1. 위 대상을 철저히 분석하세요
2. 핵심 발견사항을 3-5가지로 정리하세요
3. 개선 제안이 있다면 포함하세요
4. 파트너 에이전트({self._get_partner_name()})가 이 분석을 검토할 것입니다

**응답 형식:**
## 🔍 {agent_name} 분석 결과

### 핵심 발견사항
- [발견 1]
- [발견 2]
...

### 강점
- ...

### 개선 제안
- ...

### {self._get_partner_name()}에게 질문
- [토론을 위한 질문]
"""

    def _build_response_prompt(self, message: DialogMessage, session: DialogSession) -> str:
        """응답 프롬프트 생성"""
        agent_name = "KBJ" if self.agent_type == AgentType.KBJ else "KBJ2"
        partner_name = self._get_partner_name()
        
        # 이전 대화 컨텍스트 구성
        history = "\n".join([
            f"[Round {m.round_num}] {m.sender.value.upper()}: {m.content[:200]}..."
            for m in session.messages[-6:]  # 최근 6개 메시지만
        ])
        
        return f"""당신은 {agent_name} 에이전트입니다. {partner_name}와 토론 중입니다.

📁 분석 대상: {session.target}
🎯 토론 주제: {session.topic}

**이전 대화:**
{history}

**{partner_name}의 최신 메시지:**
{message.content}

**지시사항:**
1. {partner_name}의 의견을 검토하세요
2. 동의하는 부분과 다른 시각이 있는 부분을 구분하세요
3. 건설적인 토론을 진행하세요
4. 현재 라운드: {session.current_round + 1}/{session.max_rounds}

**응답 형식:**
## 💬 {agent_name} 응답 (Round {session.current_round + 1})

### ✅ 동의하는 부분
- ...

### 🔄 다른 시각
- ...

### 💡 추가 제안
- ...

### ❓ {partner_name}에게 질문 (있다면)
- ...
"""

    def _get_partner_name(self) -> str:
        return "KBJ2" if self.agent_type == AgentType.KBJ else "KBJ"
    
    async def _call_agent(self, prompt: str) -> str:
        """에이전트 CLI 호출"""
        env = os.environ.copy()
        env["ANTHROPIC_API_KEY"] = self._get_api_key()
        env["ANTHROPIC_BASE_URL"] = "https://api.z.ai/api/anthropic"
        
        # Claude CLI 호출
        cmd = [
            "claude",
            "-p", prompt,
            "--model", "GLM-4.7",
            "--no-input"
        ]
        
        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=env
            )
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=120)
            
            if proc.returncode == 0:
                return stdout.decode('utf-8', errors='replace')
            else:
                error_msg = stderr.decode('utf-8', errors='replace')
                return f"[에러] {self.agent_type.value}: {error_msg[:200]}"
                
        except asyncio.TimeoutError:
            return f"[타임아웃] {self.agent_type.value}: 응답 시간 초과"
        except Exception as e:
            return f"[예외] {self.agent_type.value}: {str(e)}"


# ============================================================
# 듀얼 에이전트 오케스트레이터
# ============================================================
class DualAgentOrchestrator:
    """두 에이전트 간 토론을 조율하는 오케스트레이터"""
    
    def __init__(self):
        self.kbj = AgentInterface(AgentType.KBJ)
        self.kbj2 = AgentInterface(AgentType.KBJ2)
        self.current_session: Optional[DialogSession] = None
    
    async def start_dialog(self, target: str, topic: str = "분석 및 개선", max_rounds: int = 3):
        """토론 시작"""
        session_id = f"dialog_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.current_session = DialogSession(
            session_id=session_id,
            target=target,
            topic=topic,
            max_rounds=max_rounds
        )
        
        self._print_header()
        
        # Phase 1: 동시 분석
        print("\n" + "="*60)
        print("📊 Phase 1: 동시 분석 진행 중...")
        print("="*60)
        
        kbj_analysis, kbj2_analysis = await asyncio.gather(
            self.kbj.analyze(target),
            self.kbj2.analyze(target)
        )
        
        # 분석 결과 저장
        self.current_session.add_message(DialogMessage(
            sender=AgentType.KBJ,
            receiver=AgentType.KBJ2,
            message_type=MessageType.ANALYSIS,
            content=kbj_analysis
        ))
        self._print_message("KBJ", kbj_analysis, "🔵")
        
        self.current_session.add_message(DialogMessage(
            sender=AgentType.KBJ2,
            receiver=AgentType.KBJ,
            message_type=MessageType.ANALYSIS,
            content=kbj2_analysis
        ))
        self._print_message("KBJ2", kbj2_analysis, "🟢")
        
        # Phase 2: 토론 라운드
        await self._run_discussion_rounds()
        
        # Phase 3: 결론 도출
        await self._generate_conclusion()
        
        return self.current_session
    
    async def _run_discussion_rounds(self):
        """토론 라운드 진행"""
        for round_num in range(self.current_session.max_rounds):
            self.current_session.current_round = round_num
            
            print("\n" + "="*60)
            print(f"💬 Round {round_num + 1}/{self.current_session.max_rounds}: 의견 교환")
            print("="*60)
            
            # KBJ2가 KBJ의 분석에 응답
            kbj_last_msg = self._get_last_message(AgentType.KBJ)
            if kbj_last_msg:
                kbj2_response = await self.kbj2.respond_to(kbj_last_msg, self.current_session)
                self.current_session.add_message(DialogMessage(
                    sender=AgentType.KBJ2,
                    receiver=AgentType.KBJ,
                    message_type=MessageType.OPINION,
                    content=kbj2_response
                ))
                self._print_message("KBJ2", kbj2_response, "🟢")
            
            # KBJ가 KBJ2의 응답에 응답
            kbj2_last_msg = self._get_last_message(AgentType.KBJ2)
            if kbj2_last_msg:
                kbj_response = await self.kbj.respond_to(kbj2_last_msg, self.current_session)
                self.current_session.add_message(DialogMessage(
                    sender=AgentType.KBJ,
                    receiver=AgentType.KBJ2,
                    message_type=MessageType.OPINION,
                    content=kbj_response
                ))
                self._print_message("KBJ", kbj_response, "🔵")
            
            self.current_session.next_round()
            
            # 조기 종료 체크 (양측 동의 시)
            if self._check_consensus():
                print("\n✅ 양측 합의 도달! 토론 조기 종료")
                break
            
            await asyncio.sleep(1)  # Rate limit 방지
    
    async def _generate_conclusion(self):
        """최종 결론 생성"""
        print("\n" + "="*60)
        print("📋 Phase 3: 최종 결론 도출")
        print("="*60)
        
        # 모든 메시지 요약
        all_points = []
        for msg in self.current_session.messages:
            all_points.append(f"[{msg.sender.value.upper()}] {msg.content[:300]}...")
        
        summary = "\n".join(all_points)
        
        conclusion = f"""
# 🤝 KBJ ↔ KBJ2 토론 결론

## 📁 분석 대상
{self.current_session.target}

## 🎯 토론 주제
{self.current_session.topic}

## 📊 토론 통계
- 총 라운드: {self.current_session.current_round + 1}
- 총 메시지: {len(self.current_session.messages)}개
- 세션 ID: {self.current_session.session_id}

## 💡 주요 발견사항
(양측 에이전트의 분석을 종합한 결과)

## ✅ 합의 사항
(양측이 동의한 내용)

## 🔄 의견 차이
(다른 시각이 있었던 부분)

---
📅 생성일: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        self.current_session.add_message(DialogMessage(
            sender=AgentType.KBJ2,  # 오케스트레이터가 KBJ2 이름으로 결론
            receiver=AgentType.KBJ,
            message_type=MessageType.CONCLUSION,
            content=conclusion
        ))
        
        self.current_session.status = "concluded"
        self._print_message("SYSTEM", conclusion, "⚡")
        
        print("\n" + "="*60)
        print(f"✅ 토론 완료! 로그 저장됨: {DIALOG_DIR / self.current_session.session_id}.json")
        print("="*60)
    
    def _get_last_message(self, sender: AgentType) -> Optional[DialogMessage]:
        """특정 에이전트의 마지막 메시지 가져오기"""
        for msg in reversed(self.current_session.messages):
            if msg.sender == sender:
                return msg
        return None
    
    def _check_consensus(self) -> bool:
        """합의 도달 여부 체크 (간단한 키워드 기반)"""
        if len(self.current_session.messages) < 4:
            return False
        
        last_two = self.current_session.messages[-2:]
        agreement_keywords = ["동의합니다", "좋은 의견", "동의", "합의", "agreed", "consensus"]
        
        for msg in last_two:
            if any(kw in msg.content.lower() for kw in agreement_keywords):
                return True
        return False
    
    def _print_header(self):
        """헤더 출력"""
        print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   🤝 KBJ ↔ KBJ2 Dual-Agent Dialog System                    ║
║                                                              ║
║   두 에이전트가 서로 분석하고 토론합니다                       ║
║   사용자는 실시간으로 지켜볼 수 있습니다                       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")
        print(f"📁 대상: {self.current_session.target}")
        print(f"🎯 주제: {self.current_session.topic}")
        print(f"🔄 최대 라운드: {self.current_session.max_rounds}")
    
    def _print_message(self, sender: str, content: str, emoji: str = "💬"):
        """메시지 출력 (실시간 모니터링용)"""
        print(f"\n{emoji} [{sender}] " + "-"*50)
        # 긴 내용은 일부만 표시
        if len(content) > 1000:
            print(content[:1000] + "\n... (truncated)")
        else:
            print(content)
        print("-"*60)


# ============================================================
# CLI 진입점
# ============================================================
async def main():
    """메인 함수"""
    if len(sys.argv) < 2:
        print("""
🤝 KBJ ↔ KBJ2 Dual-Agent Dialog System
======================================

사용법:
  python dual_agent_dialog.py <대상경로> [주제] [최대라운드]

예제:
  python dual_agent_dialog.py F:\\project\\app.py
  python dual_agent_dialog.py F:\\project "코드 리뷰"
  python dual_agent_dialog.py F:\\project "아키텍처 분석" 5
""")
        return
    
    target = sys.argv[1]
    topic = sys.argv[2] if len(sys.argv) > 2 else "분석 및 개선"
    max_rounds = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    
    # 대상 유효성 검사
    if not os.path.exists(target):
        print(f"❌ 대상을 찾을 수 없습니다: {target}")
        return
    
    orchestrator = DualAgentOrchestrator()
    session = await orchestrator.start_dialog(target, topic, max_rounds)
    
    print(f"\n📊 세션 완료: {session.session_id}")
    print(f"📁 로그 위치: {DIALOG_DIR / session.session_id}.json")


if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(main())

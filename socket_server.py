"""
🌐 KBJ2 Socket-Based Agent Server
==================================
Socket 기반 고속 에이전트 통신 시스템

NEW GUIDE 원칙 준수:
- 20인 조직 구조 (CEO, 기획본부, 개발본부, 마케팅, 운영, 브레인팀, 검증팀)
- 부서간 유기적 협업
- 자율적 의사결정
- 24시간 무휴 운영
"""

import asyncio
import json
import socket
import struct
import sys
import os
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any, Optional, Callable
from pathlib import Path
from enum import Enum
import threading
import queue
import uuid

# ============================================================
# 설정
# ============================================================
HOST = 'localhost'
COMMAND_PORT = 9100      # 명령 수신 포트
AGENT_BASE_PORT = 9200   # 에이전트 포트 시작 (9200-9300)
BROADCAST_PORT = 9300    # 브로드캐스트 포트

KBJ2_ROOT = Path("F:/kbj2")
SERVER_LOG_DIR = KBJ2_ROOT / "socket_server_logs"
SERVER_LOG_DIR.mkdir(exist_ok=True)

API_KEYS = [
    "384fffa4d8a44ce58ee573be0d49d995.kqLAZNeRmjnUNPJh",
    "9c5b377b9bf945d0a2b00eacdd9904ef.BoRiu74O1h0bV2v6",
    "a9bd9bd3917c4229a49f91747c4cf07e.PQBgL1cU7TqcNaBy",
]
API_BASE = "https://api.z.ai/api/anthropic"


# ============================================================
# 메시지 프로토콜
# ============================================================
class MessageType(Enum):
    """메시지 타입"""
    COMMAND = "command"           # 명령
    TASK = "task"                 # 태스크 할당
    RESPONSE = "response"         # 응답
    BROADCAST = "broadcast"       # 전체 공지
    DISCUSSION = "discussion"     # 토론
    CODE = "code"                 # 코드 전송
    MERGE_REQUEST = "merge"       # 병합 요청
    STATUS = "status"             # 상태 보고
    HEARTBEAT = "heartbeat"       # 생존 확인

@dataclass
class AgentMessage:
    """에이전트 간 통신 메시지"""
    msg_id: str
    msg_type: MessageType
    sender: str
    receiver: str  # "ALL" for broadcast
    content: str
    code: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_bytes(self) -> bytes:
        """메시지를 바이트로 직렬화"""
        data = {
            'msg_id': self.msg_id,
            'msg_type': self.msg_type.value,
            'sender': self.sender,
            'receiver': self.receiver,
            'content': self.content,
            'code': self.code,
            'timestamp': self.timestamp,
            'metadata': self.metadata
        }
        json_str = json.dumps(data, ensure_ascii=False)
        encoded = json_str.encode('utf-8')
        # 4바이트 길이 헤더 + 데이터
        return struct.pack('>I', len(encoded)) + encoded
    
    @classmethod
    def from_bytes(cls, data: bytes) -> 'AgentMessage':
        """바이트에서 메시지 복원"""
        json_str = data.decode('utf-8')
        d = json.loads(json_str)
        return cls(
            msg_id=d['msg_id'],
            msg_type=MessageType(d['msg_type']),
            sender=d['sender'],
            receiver=d['receiver'],
            content=d['content'],
            code=d.get('code', ''),
            timestamp=d.get('timestamp', datetime.now().isoformat()),
            metadata=d.get('metadata', {})
        )


# ============================================================
# 에이전트 정의 (NEW GUIDE 기반)
# ============================================================
class Department(Enum):
    CEO = "ceo"
    PLANNING = "planning"
    DEVELOPMENT = "development"
    MARKETING = "marketing"
    OPERATIONS = "operations"
    BRAIN_TRUST = "brain_trust"
    QA = "qa"

AGENT_REGISTRY = {
    # CEO (1명)
    "ceo_001": {"name": "CEO 장비전", "dept": Department.CEO, "port": 9201},
    
    # 기획본부 (4명)
    "plan_001": {"name": "전략기획팀장 김전략", "dept": Department.PLANNING, "port": 9210},
    "plan_002": {"name": "시장조사원 박시장", "dept": Department.PLANNING, "port": 9211},
    "plan_003": {"name": "사업분석가 이수치", "dept": Department.PLANNING, "port": 9212},
    "plan_004": {"name": "기술트렌드분석 최테크", "dept": Department.PLANNING, "port": 9213},
    
    # 개발본부 (5명)
    "dev_001": {"name": "CTO 강개발", "dept": Department.DEVELOPMENT, "port": 9220},
    "dev_002": {"name": "백엔드개발자 서서버", "dept": Department.DEVELOPMENT, "port": 9221},
    "dev_003": {"name": "프론트개발자 유화면", "dept": Department.DEVELOPMENT, "port": 9222},
    "dev_004": {"name": "AI엔지니어 인공지", "dept": Department.DEVELOPMENT, "port": 9223},
    "dev_005": {"name": "QA엔지니어 테완벽", "dept": Department.DEVELOPMENT, "port": 9224},
    
    # 마케팅본부 (3명)
    "mkt_001": {"name": "CMO 마케팅", "dept": Department.MARKETING, "port": 9230},
    "mkt_002": {"name": "콘텐츠크리에이터 글잘쓰", "dept": Department.MARKETING, "port": 9231},
    "mkt_003": {"name": "SNS운영자 소통왕", "dept": Department.MARKETING, "port": 9232},
    
    # 운영본부 (3명)
    "ops_001": {"name": "COO 운영철", "dept": Department.OPERATIONS, "port": 9240},
    "ops_002": {"name": "재무담당 돈관리", "dept": Department.OPERATIONS, "port": 9241},
    "ops_003": {"name": "HR담당 인재육", "dept": Department.OPERATIONS, "port": 9242},
    
    # 브레인팀 (3명)
    "brain_001": {"name": "낙관론자 희망이", "dept": Department.BRAIN_TRUST, "port": 9250},
    "brain_002": {"name": "비관론자 신중이", "dept": Department.BRAIN_TRUST, "port": 9251},
    "brain_003": {"name": "혁신가 창의씨", "dept": Department.BRAIN_TRUST, "port": 9252},
    
    # 검증팀 (2명)
    "qa_001": {"name": "논리검증자 논리왕", "dept": Department.QA, "port": 9260},
    "qa_002": {"name": "팩트체커 사실이", "dept": Department.QA, "port": 9261},
}


# ============================================================
# Socket 에이전트 클라이언트
# ============================================================
class SocketAgent:
    """개별 에이전트 - Socket 통신 기반"""
    
    def __init__(self, agent_id: str, server_host: str = HOST):
        self.agent_id = agent_id
        self.info = AGENT_REGISTRY[agent_id]
        self.name = self.info["name"]
        self.dept = self.info["dept"]
        self.port = self.info["port"]
        self.api_key = API_KEYS[self.port % len(API_KEYS)]
        
        self.server_host = server_host
        self.running = False
        self.message_queue = queue.Queue()
        self.socket = None
        
    async def start(self):
        """에이전트 서버 시작"""
        self.running = True
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.server_host, self.port))
        self.socket.listen(5)
        self.socket.setblocking(False)
        
        print(f"✅ [{self.agent_id}] {self.name} 가동 중 (Port: {self.port})")
        
        while self.running:
            try:
                await asyncio.sleep(0.1)
                # Non-blocking accept
                try:
                    conn, addr = self.socket.accept()
                    asyncio.create_task(self._handle_connection(conn))
                except BlockingIOError:
                    pass
            except Exception as e:
                print(f"❌ [{self.agent_id}] 에러: {e}")
    
    async def _handle_connection(self, conn: socket.socket):
        """연결 처리"""
        try:
            # 메시지 길이 읽기
            length_data = conn.recv(4)
            if not length_data:
                return
            
            msg_length = struct.unpack('>I', length_data)[0]
            
            # 메시지 본문 읽기
            data = b''
            while len(data) < msg_length:
                chunk = conn.recv(min(4096, msg_length - len(data)))
                if not chunk:
                    break
                data += chunk
            
            # 메시지 파싱
            msg = AgentMessage.from_bytes(data)
            
            # 메시지 처리
            response = await self._process_message(msg)
            
            # 응답 전송
            conn.sendall(response.to_bytes())
            
        except Exception as e:
            print(f"❌ [{self.agent_id}] 연결 처리 에러: {e}")
        finally:
            conn.close()
    
    async def _process_message(self, msg: AgentMessage) -> AgentMessage:
        """메시지 처리 및 응답 생성"""
        print(f"📥 [{self.agent_id}] 수신: {msg.msg_type.value} from {msg.sender}")
        
        if msg.msg_type == MessageType.TASK:
            # 태스크 실행
            result = await self._execute_task(msg.content, msg.metadata)
            return AgentMessage(
                msg_id=str(uuid.uuid4()),
                msg_type=MessageType.RESPONSE,
                sender=self.agent_id,
                receiver=msg.sender,
                content=result['analysis'] if isinstance(result, dict) else result,
                code=result.get('code', '') if isinstance(result, dict) else '',
                metadata={'original_task': msg.content}
            )
        
        elif msg.msg_type == MessageType.DISCUSSION:
            # 토론 참여
            opinion = await self._give_opinion(msg.content, msg.metadata)
            return AgentMessage(
                msg_id=str(uuid.uuid4()),
                msg_type=MessageType.DISCUSSION,
                sender=self.agent_id,
                receiver=msg.sender,
                content=opinion
            )
        
        elif msg.msg_type == MessageType.HEARTBEAT:
            return AgentMessage(
                msg_id=str(uuid.uuid4()),
                msg_type=MessageType.STATUS,
                sender=self.agent_id,
                receiver=msg.sender,
                content=f"ALIVE:{self.name}"
            )
        
        else:
            return AgentMessage(
                msg_id=str(uuid.uuid4()),
                msg_type=MessageType.RESPONSE,
                sender=self.agent_id,
                receiver=msg.sender,
                content="메시지 수신 확인"
            )
    
    async def _execute_task(self, task: str, metadata: Dict) -> Dict:
        """태스크 실행 - Claude CLI 호출"""
        prompt = f"""당신은 {self.name}입니다. ({self.dept.value} 소속)

📋 태스크: {task}
📁 대상: {metadata.get('target', 'N/A')}

지시사항:
1. 태스크를 철저히 수행하세요
2. 코드가 필요하면 ```python 블록에 작성하세요
3. 간결하고 정확하게 응답하세요

JSON 형식으로 응답:
```json
{{"analysis": "분석 결과", "recommendation": "제안사항", "code": "필요한 코드"}}
```
"""
        env = os.environ.copy()
        env["ANTHROPIC_API_KEY"] = self.api_key
        env["ANTHROPIC_BASE_URL"] = API_BASE
        
        try:
            proc = await asyncio.create_subprocess_exec(
                "claude", "-p", prompt, "--model", "GLM-4.7", "--no-input",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=env
            )
            stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=60)
            response = stdout.decode('utf-8', errors='replace')
            
            # JSON 파싱
            try:
                if "```json" in response:
                    json_str = response.split("```json")[1].split("```")[0]
                    return json.loads(json_str)
            except:
                pass
            
            return {"analysis": response, "code": ""}
            
        except Exception as e:
            return {"analysis": f"에러: {str(e)}", "code": ""}
    
    async def _give_opinion(self, topic: str, context: Dict) -> str:
        """토론 의견 제시"""
        prompt = f"""당신은 {self.name}입니다. 토론에 참여합니다.

주제: {topic}
이전 의견: {context.get('previous_opinions', [])}

당신의 전문성을 바탕으로 의견을 제시하세요. (200자 이내)
"""
        env = os.environ.copy()
        env["ANTHROPIC_API_KEY"] = self.api_key
        env["ANTHROPIC_BASE_URL"] = API_BASE
        
        try:
            proc = await asyncio.create_subprocess_exec(
                "claude", "-p", prompt, "--model", "GLM-4.7", "--no-input",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=env
            )
            stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=30)
            return stdout.decode('utf-8', errors='replace')[:500]
        except:
            return f"[{self.name}] 의견 제출 실패"
    
    def stop(self):
        """에이전트 중지"""
        self.running = False
        if self.socket:
            self.socket.close()


# ============================================================
# 중앙 통제 서버
# ============================================================
class CommandServer:
    """중앙 통제 서버 - 모든 에이전트 조율"""
    
    def __init__(self):
        self.agents: Dict[str, SocketAgent] = {}
        self.running = False
        self.task_results = {}
    
    async def start_all_agents(self):
        """모든 에이전트 시작"""
        print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   🌐 KBJ2 Socket-Based Agent Server                         ║
║                                                              ║
║   NEW GUIDE 원칙 기반 20인 조직 시스템                       ║
║   Socket 고속 통신 (localhost:9100-9300)                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")
        print("🚀 에이전트 서버 시작 중...")
        
        # 모든 에이전트 생성 및 시작
        tasks = []
        for agent_id in AGENT_REGISTRY:
            agent = SocketAgent(agent_id)
            self.agents[agent_id] = agent
            tasks.append(asyncio.create_task(agent.start()))
        
        print(f"\n✅ {len(self.agents)}개 에이전트 가동 완료!")
        print(f"📡 명령 포트: {COMMAND_PORT}")
        print(f"🔗 에이전트 포트 범위: 9201-9261\n")
        
        # 명령 수신 서버 시작
        await self._start_command_server()
    
    async def _start_command_server(self):
        """명령 수신 서버"""
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, COMMAND_PORT))
        server.listen(10)
        server.setblocking(False)
        
        self.running = True
        print(f"📡 명령 서버 대기 중 (Port: {COMMAND_PORT})...")
        
        while self.running:
            try:
                await asyncio.sleep(0.1)
                try:
                    conn, addr = server.accept()
                    asyncio.create_task(self._handle_command(conn))
                except BlockingIOError:
                    pass
            except Exception as e:
                print(f"❌ 명령 서버 에러: {e}")
    
    async def _handle_command(self, conn: socket.socket):
        """명령 처리"""
        try:
            # 메시지 수신
            length_data = conn.recv(4)
            if not length_data:
                return
            
            msg_length = struct.unpack('>I', length_data)[0]
            data = b''
            while len(data) < msg_length:
                chunk = conn.recv(min(4096, msg_length - len(data)))
                data += chunk
            
            msg = AgentMessage.from_bytes(data)
            
            # 명령 실행
            if msg.msg_type == MessageType.COMMAND:
                result = await self._execute_command(msg)
                conn.sendall(result.to_bytes())
            
        except Exception as e:
            print(f"❌ 명령 처리 에러: {e}")
        finally:
            conn.close()
    
    async def _execute_command(self, msg: AgentMessage) -> AgentMessage:
        """명령 실행"""
        cmd = msg.content
        target = msg.metadata.get('target', '')
        
        if cmd == "DISPATCH_ALL":
            # 모든 에이전트에게 태스크 전송
            results = await self._dispatch_to_all(msg.metadata.get('task', ''), target)
            return AgentMessage(
                msg_id=str(uuid.uuid4()),
                msg_type=MessageType.RESPONSE,
                sender="SERVER",
                receiver=msg.sender,
                content=json.dumps(results, ensure_ascii=False)
            )
        
        elif cmd == "DISPATCH_DEPT":
            # 특정 부서에게 태스크 전송
            dept = Department(msg.metadata.get('department'))
            results = await self._dispatch_to_department(dept, msg.metadata.get('task', ''), target)
            return AgentMessage(
                msg_id=str(uuid.uuid4()),
                msg_type=MessageType.RESPONSE,
                sender="SERVER",
                receiver=msg.sender,
                content=json.dumps(results, ensure_ascii=False)
            )
        
        elif cmd == "DISCUSSION":
            # 토론 시작
            results = await self._start_discussion(msg.metadata.get('topic', ''))
            return AgentMessage(
                msg_id=str(uuid.uuid4()),
                msg_type=MessageType.RESPONSE,
                sender="SERVER",
                receiver=msg.sender,
                content=json.dumps(results, ensure_ascii=False)
            )
        
        elif cmd == "STATUS":
            # 상태 조회
            status = {agent_id: "ACTIVE" for agent_id in self.agents}
            return AgentMessage(
                msg_id=str(uuid.uuid4()),
                msg_type=MessageType.STATUS,
                sender="SERVER",
                receiver=msg.sender,
                content=json.dumps(status)
            )
        
        return AgentMessage(
            msg_id=str(uuid.uuid4()),
            msg_type=MessageType.RESPONSE,
            sender="SERVER",
            receiver=msg.sender,
            content="Unknown command"
        )
    
    async def _dispatch_to_all(self, task: str, target: str) -> Dict:
        """모든 에이전트에게 동시 전송"""
        print(f"\n📢 전체 배치: {task[:50]}...")
        
        results = {}
        tasks = []
        
        for agent_id, agent in self.agents.items():
            tasks.append(self._send_task_to_agent(agent_id, agent.port, task, target))
        
        completed = await asyncio.gather(*tasks, return_exceptions=True)
        
        for i, (agent_id, _) in enumerate(self.agents.items()):
            results[agent_id] = completed[i] if not isinstance(completed[i], Exception) else str(completed[i])
        
        return results
    
    async def _dispatch_to_department(self, dept: Department, task: str, target: str) -> Dict:
        """특정 부서에게 전송"""
        print(f"\n📢 {dept.value} 부서 배치: {task[:50]}...")
        
        results = {}
        tasks = []
        
        dept_agents = {aid: a for aid, a in self.agents.items() if a.dept == dept}
        
        for agent_id, agent in dept_agents.items():
            tasks.append(self._send_task_to_agent(agent_id, agent.port, task, target))
        
        completed = await asyncio.gather(*tasks, return_exceptions=True)
        
        for i, agent_id in enumerate(dept_agents.keys()):
            results[agent_id] = completed[i] if not isinstance(completed[i], Exception) else str(completed[i])
        
        return results
    
    async def _send_task_to_agent(self, agent_id: str, port: int, task: str, target: str) -> Dict:
        """개별 에이전트에게 태스크 전송"""
        try:
            reader, writer = await asyncio.open_connection(HOST, port)
            
            msg = AgentMessage(
                msg_id=str(uuid.uuid4()),
                msg_type=MessageType.TASK,
                sender="SERVER",
                receiver=agent_id,
                content=task,
                metadata={'target': target}
            )
            
            writer.write(msg.to_bytes())
            await writer.drain()
            
            # 응답 수신
            length_data = await reader.read(4)
            msg_length = struct.unpack('>I', length_data)[0]
            data = await reader.read(msg_length)
            
            response = AgentMessage.from_bytes(data)
            
            writer.close()
            await writer.wait_closed()
            
            return {"agent": agent_id, "response": response.content, "code": response.code}
            
        except Exception as e:
            return {"agent": agent_id, "error": str(e)}
    
    async def _start_discussion(self, topic: str) -> Dict:
        """토론 시작"""
        print(f"\n💬 토론 시작: {topic[:50]}...")
        
        opinions = []
        
        # 브레인팀 먼저
        brain_agents = {aid: a for aid, a in self.agents.items() if a.dept == Department.BRAIN_TRUST}
        for agent_id, agent in brain_agents.items():
            result = await self._send_discussion_to_agent(agent_id, agent.port, topic, opinions)
            if 'opinion' in result:
                opinions.append({"agent": agent_id, "opinion": result['opinion']})
        
        # 기획팀
        plan_agents = {aid: a for aid, a in self.agents.items() if a.dept == Department.PLANNING}
        for agent_id, agent in plan_agents.items():
            result = await self._send_discussion_to_agent(agent_id, agent.port, topic, opinions)
            if 'opinion' in result:
                opinions.append({"agent": agent_id, "opinion": result['opinion']})
        
        return {"topic": topic, "opinions": opinions}
    
    async def _send_discussion_to_agent(self, agent_id: str, port: int, topic: str, previous: List) -> Dict:
        """토론 메시지 전송"""
        try:
            reader, writer = await asyncio.open_connection(HOST, port)
            
            msg = AgentMessage(
                msg_id=str(uuid.uuid4()),
                msg_type=MessageType.DISCUSSION,
                sender="SERVER",
                receiver=agent_id,
                content=topic,
                metadata={'previous_opinions': [p['opinion'][:100] for p in previous[-3:]]}
            )
            
            writer.write(msg.to_bytes())
            await writer.drain()
            
            length_data = await reader.read(4)
            msg_length = struct.unpack('>I', length_data)[0]
            data = await reader.read(msg_length)
            
            response = AgentMessage.from_bytes(data)
            
            writer.close()
            await writer.wait_closed()
            
            return {"agent": agent_id, "opinion": response.content}
            
        except Exception as e:
            return {"agent": agent_id, "error": str(e)}
    
    def stop(self):
        """서버 종료"""
        self.running = False
        for agent in self.agents.values():
            agent.stop()


# ============================================================
# 클라이언트 유틸리티
# ============================================================
class AgentClient:
    """에이전트 서버에 명령을 보내는 클라이언트"""
    
    def __init__(self, host: str = HOST, port: int = COMMAND_PORT):
        self.host = host
        self.port = port
    
    async def dispatch_all(self, task: str, target: str = "") -> Dict:
        """모든 에이전트에게 태스크 전송"""
        return await self._send_command("DISPATCH_ALL", {"task": task, "target": target})
    
    async def dispatch_department(self, dept: str, task: str, target: str = "") -> Dict:
        """특정 부서에 태스크 전송"""
        return await self._send_command("DISPATCH_DEPT", {"department": dept, "task": task, "target": target})
    
    async def start_discussion(self, topic: str) -> Dict:
        """토론 시작"""
        return await self._send_command("DISCUSSION", {"topic": topic})
    
    async def get_status(self) -> Dict:
        """상태 조회"""
        return await self._send_command("STATUS", {})
    
    async def _send_command(self, cmd: str, metadata: Dict) -> Dict:
        """명령 전송"""
        try:
            reader, writer = await asyncio.open_connection(self.host, self.port)
            
            msg = AgentMessage(
                msg_id=str(uuid.uuid4()),
                msg_type=MessageType.COMMAND,
                sender="CLIENT",
                receiver="SERVER",
                content=cmd,
                metadata=metadata
            )
            
            writer.write(msg.to_bytes())
            await writer.drain()
            
            length_data = await reader.read(4)
            msg_length = struct.unpack('>I', length_data)[0]
            data = await reader.read(msg_length)
            
            response = AgentMessage.from_bytes(data)
            
            writer.close()
            await writer.wait_closed()
            
            return json.loads(response.content) if response.content.startswith('{') else {"response": response.content}
            
        except Exception as e:
            return {"error": str(e)}


# ============================================================
# CLI
# ============================================================
async def main():
    if len(sys.argv) < 2:
        print("""
🌐 KBJ2 Socket-Based Agent Server
==================================

사용법:
  python socket_server.py server           # 서버 시작 (20개 에이전트)
  python socket_server.py dispatch <태스크> [대상]   # 전체 배치
  python socket_server.py dept <부서> <태스크>       # 부서별 배치
  python socket_server.py discuss <주제>            # 토론 시작
  python socket_server.py status                   # 상태 확인

부서 코드:
  planning, development, marketing, operations, brain_trust, qa
""")
        return
    
    cmd = sys.argv[1]
    
    if cmd == "server":
        server = CommandServer()
        await server.start_all_agents()
    
    elif cmd == "dispatch":
        task = sys.argv[2] if len(sys.argv) > 2 else "분석 수행"
        target = sys.argv[3] if len(sys.argv) > 3 else ""
        client = AgentClient()
        result = await client.dispatch_all(task, target)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif cmd == "dept":
        dept = sys.argv[2] if len(sys.argv) > 2 else "development"
        task = sys.argv[3] if len(sys.argv) > 3 else "분석 수행"
        client = AgentClient()
        result = await client.dispatch_department(dept, task)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif cmd == "discuss":
        topic = sys.argv[2] if len(sys.argv) > 2 else "신규 프로젝트"
        client = AgentClient()
        result = await client.start_discussion(topic)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif cmd == "status":
        client = AgentClient()
        result = await client.get_status()
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(main())

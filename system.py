import os
import json
import requests
import asyncio
from typing import Dict, Any, List
from .scheduler import SCHEDULER

class EDMSAgentSystem:
    def __init__(self, api_key: str = None):
        # Use provided key or fallback to env var
        raw_key = api_key or os.environ.get("ZAI_API_KEY")
        if not raw_key:
            raise ValueError("ZAI_API_KEY environment variable is not set")
            
        # Support Multiple Keys for Rotation
        self.api_keys = [k.strip() for k in raw_key.split(",") if k.strip()]
        self.current_key_idx = 0
        
        self.base_url = "https://api.z.ai/api/coding/paas/v4/chat/completions"
        self.conversation_history = []
        
        # Start Scheduler if not running
        if not SCHEDULER.is_running:
            asyncio.create_task(SCHEDULER.start())

    async def run_agent_scheduled(self, agent_name: str, prompt: str, priority: int = 5) -> Dict[str, Any]:
        """Wrapper to submit task to global scheduler."""
        return await SCHEDULER.submit_task(self.run_agent, agent_name, prompt, priority=priority)

    def create_agent_prompt(self, persona: Any, context: str, task: str, domain_context: str = "") -> str:
        # ... (Method unchanged) ...
        """Generates a prompt based on the agent persona."""
        
        expertise_str = ', '.join(persona.expertise)
        base_prompt = f"""
        당신은 {persona.name}입니다.

        [역할과 성격]
        - 역할: {persona.role}
        - 성격: {persona.personality}
        - 전문분야: {expertise_str}
        - 의사결정 스타일: {persona.decision_style}

        [추가 전문 영역 Context]
        {domain_context if domain_context else "당신은 해당 분야의 최고 전문가로서 행동합니다."}

        [현재 상황]
        {context}

        [수행할 작업]
        {task}

        [응답 가이드라인]
        1. 당신의 전문분야와 성격에 맞는 관점으로 분석하세요.
        2. 구체적인 근거와 논리를 제시하세요.
        3. 다른 에이전트들과 토론할 수 있도록 명확한 의견을 제시하세요.
        4. 반드시 Valid JSON 형태로 결과를 정리해주세요. Markdown code block 없이 raw JSON만 출력하세요.

        [응답 형식]
        {{
            "agent_name": "{persona.name}",
            "analysis": "상세 분석 내용",
            "recommendation": "구체적 제안사항",
            "concerns": "우려사항 또는 리스크",
            "next_action": "다음 단계 제안"
        }}
        """
        return base_prompt

    async def run_agent(self, agent_name: str, prompt: str) -> Dict[str, Any]:
        """Executes the agent task using the ZAI GLM-4.7 API with rate limiting."""
        
        # Rate Limiting: Static semaphore to limit concurrency
        if not hasattr(self, '_semaphore'):
            self._semaphore = asyncio.Semaphore(1) # Strict limit: 1 request at a time to be safe
        
        async with self._semaphore:
            # Round Robin Key Selection
            self.current_key_idx = (self.current_key_idx + 1) % len(self.api_keys)
            api_key = self.api_keys[self.current_key_idx]

            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "GLM-4.7",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a highly intelligent AI agent representing a specific persona. Output JSON only."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.7,
                "stream": False
            }

            print(f"🤖 Agent [{agent_name}] is thinking...")

            try:
                # Add delay before request to respect rate limits
                await asyncio.sleep(2.0) 

                # Use Session with Retry Logic
                session = requests.Session()
                adapter = requests.adapters.HTTPAdapter(max_retries=3)
                session.mount('https://', adapter)

                response = await asyncio.to_thread(
                    session.post, 
                    self.base_url, 
                    headers=headers, 
                    json=payload, 
                    timeout=120  # Increased to 120s for Heavy "Refactoring" tasks
                )
                
                if response.status_code == 429:
                    print(f"⏳ Rate limited on agent [{agent_name}]. Retrying after delay...")
                    await asyncio.sleep(5.0)
                    response = await asyncio.to_thread(
                        requests.post, 
                        self.base_url, 
                        headers=headers, 
                        json=payload, 
                        timeout=60
                    )
                
                response.raise_for_status()
                
                result_json = response.json()
                content = result_json['choices'][0]['message']['content']
                
                # Simple JSON cleanup
                content = content.replace("```json", "").replace("```", "").strip()
                
                try:
                    parsed_result = json.loads(content)
                except json.JSONDecodeError:
                    parsed_result = {
                        "agent_name": agent_name,
                        "analysis": content,
                        "recommendation": "Parsing Error - Raw Content Returned",
                    }

                parsed_result["timestamp"] = asyncio.get_event_loop().time()
                return parsed_result

            except Exception as e:
                print(f"❌ Error running agent [{agent_name}]: {e}")
                return {
                    "agent_name": agent_name,
                    "error": str(e),
                    "analysis": "Error during processing",
                    "recommendation": "Retry"
                }

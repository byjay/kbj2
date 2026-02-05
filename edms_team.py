import json
import asyncio
from typing import Dict, Any, List
from .personas import AgentPersona
from .system import EDMSAgentSystem

class EDMSSpecializedTeams:
    def __init__(self, agent_system: EDMSAgentSystem):
        self.system = agent_system
        self.setup_teams()

    def setup_teams(self):
        self.ocr_expert = AgentPersona(
            name="OCR전문가_김인식",
            role="도면 텍스트 및 기호 인식",
            personality="정확성을 추구하며, 미세한 디테일까지 놓치지 않는 완벽주의자",
            expertise=["OCR 기술", "도면 기호 해석", "표제란 분석"],
            decision_style="meticulous"
        )
        self.verifier = AgentPersona(
            name="설계검증자_박표준",
            role="설계 표준 준수 검증",
            personality="규정과 표준을 철저히 준수하며, 안전을 최우선으로 생각",
            expertise=["KS 표준", "ISO 규격", "선급 규정"],
            decision_style="conservative"
        )
        self.material_analyst = AgentPersona(
            name="자재분석가_이부품",
            role="도면에서 자재 정보 추출",
            personality="체계적이고 논리적으로 부품을 분류하고 정리",
            expertise=["자재 분류", "부품 코딩", "수량 산출"],
            decision_style="systematic"
        )
        self.estimator = AgentPersona(
            name="견적전문가_최가격",
            role="자재비 및 공수 견적",
            personality="시장 동향에 민감하고, 경제적 효율성을 추구",
            expertise=["자재 단가", "시장 분석", "비용 최적화"],
            decision_style="economical"
        )

    async def analyze_drawing(self, drawing_path: str) -> Dict[str, Any]:
        """Simulates drawing analysis flow."""
        print(f"\n📐 [EDMS Analysis] Analyzing drawing: {drawing_path}")

        # 1. OCR (Simulated prompt since we can't upload files to API yet via text)
        ocr_prompt = self.system.create_agent_prompt(
            self.ocr_expert,
            f"파일 경로: {drawing_path}",
            "이 도면 파일에서 표제란 정보와 주요 자재 목록을 텍스트로 추출하세요. (가상의 결과를 생성하세요)",
            domain_context="당신은 도면 정밀 분석가입니다."
        )
        ocr_result = await self.system.run_agent("OCR전문가", ocr_prompt)
        print("   -> OCR completed.")

        # 2. Verification
        verification_prompt = self.system.create_agent_prompt(
            self.verifier,
            f"추출 데이터: {json.dumps(ocr_result.get('analysis', ''), ensure_ascii=False)}",
            "추출된 정보가 KS 표준 및 선급 규정에 적합한지 검토하세요."
        )
        verification_result = await self.system.run_agent("설계검증자", verification_prompt)
        print("   -> Verification completed.")

        return {
            "ocr": ocr_result,
            "verification": verification_result
        }

    async def generate_bom(self, drawing_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generates BOM from drawing data."""
        print(f"\n🔨 [BOM Generation] Generating BOM...")

        # 1. Material Analysis
        mat_prompt = self.system.create_agent_prompt(
            self.material_analyst,
            f"도면 데이터: {json.dumps(drawing_data, ensure_ascii=False)}",
            "자재 명세서(BOM)를 항목별로 구조화하여 생성하세요."
        )
        bom_result = await self.system.run_agent("자재분석가", mat_prompt)

        # 2. Estimation
        est_prompt = self.system.create_agent_prompt(
            self.estimator,
            f"BOM 데이터: {json.dumps(bom_result.get('analysis', ''), ensure_ascii=False)}",
            "각 자재의 예상 단가와 총 견적 금액을 산출하세요."
        )
        est_result = await self.system.run_agent("견적전문가", est_prompt)
        print("   -> BOM & Estimation completed.")

        return {
            "bom": bom_result,
            "estimation": est_result
        }

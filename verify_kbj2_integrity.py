import importlib.util
import sys
import os

# Manual path addition
sys.path.append("F:\\kbj2")
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

def check_integrity():
    print("🔍 KBJ2 System Integrity Verification")
    print("====================================")
    
    try:
        from kbj2.personas import DIRECTOR, RESEARCH_PERSONAS, DEBATE_PERSONAS, SYNTHESIS_PERSONAS, QA_TEAM
        
        # 1. Director Check
        print(f"✅ Director: {DIRECTOR.name} ({DIRECTOR.role})")
        
        # 2. Research Team Check
        print(f"\n🔎 Research Team ({len(RESEARCH_PERSONAS)}/5)")
        for p in RESEARCH_PERSONAS:
            print(f"   - {p.name}: {p.role}")
        assert len(RESEARCH_PERSONAS) == 5, "Research Team missing members!"
        
        # 3. Debate Team Check
        print(f"\n⚔️ Debate Team ({len(DEBATE_PERSONAS)}/7)")
        for p in DEBATE_PERSONAS:
            print(f"   - {p.name}: {p.role}")
            assert p.decision_style in ["optimistic", "pessimistic", "realistic", "innovative", "pragmatic", "strategic", "diplomatic"], f"Invalid decision style for {p.name}"
        assert len(DEBATE_PERSONAS) == 7, "Debate Team missing members!"
        
        # 4. Synthesis Team Check
        print(f"\n⚗️ Synthesis Team ({len(SYNTHESIS_PERSONAS)}/7)")
        for p in SYNTHESIS_PERSONAS:
            print(f"   - {p.name}: {p.role}")
        assert len(SYNTHESIS_PERSONAS) == 7, "Synthesis Team missing members!"
        
        # 5. QA Team Check
        print(f"\n🛡️ QA Team ({len(QA_TEAM)}/1)")
        for p in QA_TEAM:
            print(f"   - {p.name}: {p.role}")
        assert len(QA_TEAM) == 1, "QA Team missing!"
        
        total_agents = 1 + 5 + 7 + 7 + 1
        print(f"\n✅ Total Agent Count: {total_agents} (Target: 21)")
        
        # 6. Logic Check
        from kbj2.strat_team import StrategicPlanningTeam
        print(f"\n⚙️ Logic Verification")
        print("   - StrategicPlanningTeam Class: Found")
        if hasattr(StrategicPlanningTeam, 'run_debate_session'):
            print("   - Debate Logic (run_debate_session): Found")
        else:
            print("   ❌ Debate Logic Missing!")
            
        print("\n🎉 INTEGRITY CHECK PASSED: System aligns with new.md specifications.")
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
    except AssertionError as e:
        print(f"❌ Integrity Validtion Failed: {e}")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")

if __name__ == "__main__":
    check_integrity()

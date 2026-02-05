
import os
import glob

TARGET_DIR = r"F:\kbj2"
PATTERNS = [
    "mission_vba_injector*.py",
    "mission_final_verify*.py",
    "mission_manual_verify.py",
    "mission_check_vba.py",
    "mission_read_*.py",
    "mission_generate_test_report.py",
    "mission_simulate_report.py",
    "mission_fix_button.py",
    "mission_cable_*.py",
    "mission_deep_analysis.py",
    "final_test_result.md"
]

def main():
    print("cleaning up temporary files...")
    count = 0
    for pat in PATTERNS:
        files = glob.glob(os.path.join(TARGET_DIR, pat))
        for f in files:
            try:
                os.remove(f)
                print(f"Deleted: {os.path.basename(f)}")
                count += 1
            except Exception as e:
                print(f"Error deleting {f}: {e}")
    print(f"Cleanup Complete. Removed {count} files.")

if __name__ == "__main__":
    main()

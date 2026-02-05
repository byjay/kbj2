
import win32com.client
import os
import sys

TARGET = r"f:\!!!진행프로젝트\HS\참치\HK2401 Cable List_FINAL_VERIFY.xlsm"
LOG_FILE = r"f:\!!!진행프로젝트\HS\참치\sanity_check.txt"

def main():
    print(f"Testing Macro Execution on {TARGET}")
    if os.path.exists(LOG_FILE): os.remove(LOG_FILE)
    
    try:
        excel = win32com.client.Dispatch("Excel.Application")
        excel.Visible = True
        excel.DisplayAlerts = False
        excel.AutomationSecurity = 1
        
        wb = excel.Workbooks.Open(TARGET)
        
        # Inject Simple Macro
        project = wb.VBProject
        mod = project.VBComponents.Add(1)
        mod.Name = "SanityTest"
        code = f"""
Sub RunSanityTest()
    Dim fso, f
    Set fso = CreateObject("Scripting.FileSystemObject")
    Set f = fso.CreateTextFile("{LOG_FILE}", True)
    f.WriteLine "Hello World from VBA " & Now
    f.Close
    MsgBox "Sanity Check OK", vbInformation
End Sub
"""
        mod.CodeModule.AddFromString(code)
        print("Injected Sanity Macro")
        
        # Run it
        print("Running...")
        excel.Application.Run("RunSanityTest")
        print("Run returned.")
        
        wb.Close(False)
        excel.Quit()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

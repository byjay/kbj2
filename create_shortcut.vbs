Set WshShell = WScript.CreateObject("WScript.Shell")
Set Shortcut = WshShell.CreateShortcut("C:\Users\FREE\Desktop\R2탐색기.lnk")

With Shortcut
    .TargetPath = "python.exe"
    .Arguments = "F:\kbj2\main.py r2 explore"
    .WorkingDirectory = "F:\kbj2"
    .Description = "KBJ2 R2 클라우드 탐색기"
    .IconLocation = "C:\Windows\System32\imageres.dll"
    .IconIndex = 179
    .Save
End With

MsgBox "R2탐색기 바로가기가 생성되었습니다!" & vbCrLf & vbCrLf & "바탕화면에서 더블클릭하세요.", 64, "바로가기 생성"

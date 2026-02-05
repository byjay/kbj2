# KBJ2 Capability: PDF Analyst (VBA Generator)
import os

VBA_TEMPLATE = """
Option Explicit

'=======================================================================================
' 프로그램: Smart PDF Analyzer (for Excel)
' 작성자: KBJ2 (Based on rosa0189's Tech)
' 설명: 선택한 PDF 파일을 Word를 통해 열어서 텍스트를 추출하고, 엑셀로 가져와 분석합니다.
' 필요 참조: 없음 (Late Binding 사용 - CreateObject)
'=======================================================================================

Sub AnalyzePDFInExcel()
    Dim fd As FileDialog
    Dim strPath As String
    Dim wordApp As Object ' Word.Application
    Dim wordDoc As Object ' Word.Document
    Dim vContent As Variant
    Dim ws As Worksheet
    Dim lines As Variant
    Dim i As Long
    
    ' 1. PDF 파일 선택
    Set fd = Application.FileDialog(msoFileDialogFilePicker)
    With fd
        .Title = "분석할 PDF 파일을 선택하세요 (Select PDF)"
        .Filters.Clear
        .Filters.Add "PDF Files", "*.pdf"
        .AllowMultiSelect = False
        If .Show = -1 Then
            strPath = .SelectedItems(1)
        Else
            Exit Sub
        End If
    End With
    
    Application.ScreenUpdating = False
    Application.StatusBar = "PDF 파일을 분석 중입니다... (Word 엔진 구동)"
    
    ' 2. Word 인스턴스 생성 (PDF 파싱용)
    On Error Resume Next
    Set wordApp = GetObject(, "Word.Application")
    If Err.Number <> 0 Then
        Set wordApp = CreateObject("Word.Application")
    End If
    On Error GoTo 0
    
    wordApp.Visible = False ' 백그라운드 실행
    
    ' 3. PDF 열기 (Word가 변환 수행)
    ' ConfirmConversions=False로 설정하여 대화상자 스킵 시도
    Set wordDoc = wordApp.Documents.Open(Filename:=strPath, ConfirmConversions:=False, ReadOnly:=True)
    
    ' 4. 텍스트 추출
    Application.StatusBar = "데이터 추출 및 엑셀 이관 중..."
    Dim fullText As String
    fullText = wordDoc.Content.Text
    
    ' Word 닫기
    wordDoc.Close False
    ' Word 앱은 닫지 않거나 필요시 종료: wordApp.Quit
    ' 여기서는 Word를 계속 사용할 수 있으므로 놔두되, 자원 정리를 위해 종료 추천
    wordApp.Quit
    Set wordDoc = Nothing
    Set wordApp = Nothing
    
    ' 5. 엑셀에 뿌리기
    Set ws = ActiveSheet
    ws.Cells.Clear
    
    ' 텍스트 줄바꿈(Chr(13)) 기준으로 분리
    lines = Split(fullText, Chr(13))
    
    ' 데이터 기록
    For i = LBound(lines) To UBound(lines)
        ' 간단한 정제 (Trim)
        Dim cleanLine As String
        cleanLine = Trim(lines(i))
        
        ' 분석 로직 (예: 특정 키워드 찾기, 여기서는 전체 출력)
        If Len(cleanLine) > 0 Then
            ws.Cells(i + 1, 1).Value = cleanLine
        End If
    Next i
    
    ' 6. 서식 및 마무리
    ws.Columns("A:A").AutoFit
    Application.ScreenUpdating = True
    Application.StatusBar = False
    
    MsgBox "PDF 분석이 완료되었습니다!" & vbCrLf & "파일: " & strPath, vbInformation, "KBJ2 Report"
    
End Sub
"""

def generate_vba_tool():
    output_path = r"C:\Users\FREE\Desktop\SmartPDF_Analyzer.vba"
    with open(output_path, "w", encoding="utf-8") as f: # VBA는 보통 cp949여야 한글이 엑셀에서 안깨지지만, import시 utf-8도 가능. 여기선 안전하게 utf-8.
        f.write(VBA_TEMPLATE)
    
    print(f"✅ [KBJ2] Generated VBA Tool at: {output_path}")
    print("   User can import this into Excel (Alt+F11 -> File -> Import File)")

if __name__ == "__main__":
    generate_vba_tool()

import os
import sys
import win32com.client
import argparse
from pathlib import Path

def docx_to_pdf(input_path):
    """
    Converts a DOCX file to PDF using Word's native Save As functionality (background).
    """
    input_path = str(Path(input_path).resolve())
    output_path = str(Path(input_path).with_suffix('.pdf').resolve())

    if not os.path.exists(input_path):
        print(f"❌ Error: File not found - {input_path}")
        return False

    print(f"🔄 [CONVERSION] Converting: {os.path.basename(input_path)} -> {os.path.basename(output_path)}")
    
    word = None
    try:
        # Initialize Word Application in the background
        word = win32com.client.DispatchEx("Word.Application")
        word.Visible = False
        word.DisplayAlerts = False

        # Open the document
        doc = word.Documents.Open(input_path, ReadOnly=True, Visible=False)
        
        # wdExportFormatPDF = 17
        # wdExportOptimizeForPrint = 0
        doc.ExportAsFixedFormat(
            OutputFileName=output_path,
            ExportFormat=17,
            OpenAfterExport=False,
            OptimizeFor=0,
            IncludeDocProps=True,
            KeepIRM=True,
            CreateBookmarks=1,  # wdExportCreateHeadingBookmarks
            DocStructureTags=True,
            BitmapMissingFonts=True,
            UseISO19005_1=False
        )
        
        doc.Close(False)
        print(f"✅ Success: Saved as {output_path}")
        return True

    except Exception as e:
        print(f"❌ Error during conversion: {e}")
        return False
    finally:
        if word:
            word.Quit()

def main():
    parser = argparse.ArgumentParser(description="KBJ2 DOCX to PDF Converter (Background)")
    parser.add_argument("target", type=str, help="Path to DOCX file or directory")
    args = parser.parse_args()

    target = Path(args.target)
    
    if target.is_dir():
        docx_files = list(target.glob("*.docx"))
        if not docx_files:
            print(f"ℹ️ No DOCX files found in directory: {target}")
            return
        
        print(f"📁 Batch processing {len(docx_files)} files in directory...")
        for file in docx_files:
            docx_to_pdf(file)
    else:
        docx_to_pdf(target)

if __name__ == "__main__":
    main()

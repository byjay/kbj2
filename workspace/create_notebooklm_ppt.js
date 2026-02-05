const pptxgen = require('pptxgenjs');
const html2pptx = require('C:/Users/FREE/.claude/skills/pptx-toolkit/scripts/html2pptx.js');

async function createNotebookLMPPT() {
  const pptx = new pptxgen();
  pptx.layout = 'LAYOUT_16x9';
  pptx.author = 'KBJ2';
  pptx.title = 'NotebookLM API 완전 정복';

  const slides = [
    'F:/kbj2/workspace/slides/notebooklm_01.html',  // 커버
    'F:/kbj2/workspace/slides/notebooklm_02.html',  // 개요
    'F:/kbj2/workspace/slides/notebooklm_03.html',  // 환경 설정
    'F:/kbj2/workspace/slides/notebooklm_04.html',  // 라이선스
    'F:/kbj2/workspace/slides/notebooklm_05.html',  // IDP 설정
    'F:/kbj2/workspace/slides/notebooklm_06.html',  // Replit
    'F:/kbj2/workspace/slides/notebooklm_07.html',  // Make
    'F:/kbj2/workspace/slides/notebooklm_08.html',  // 요약
  ];

  for (const slide of slides) {
    console.log(`Processing: ${slide.split('/').pop()}`);
    await html2pptx(slide, pptx);
  }

  const outputFile = 'F:/kbj2/NotebookLM_API_Guide.pptx';
  await pptx.writeFile({ fileName: outputFile });
  console.log(`\n[DONE] Created: ${outputFile}`);
}

createNotebookLMPPT().catch(console.error);

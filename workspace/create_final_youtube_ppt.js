const pptxgen = require('pptxgenjs');
const html2pptx = require('C:/Users/FREE/.claude/skills/pptx-toolkit/scripts/html2pptx.js');

async function createFinalPPT() {
  const pptx = new pptxgen();
  pptx.layout = 'LAYOUT_16x9';
  pptx.author = 'KBJ2';
  pptx.title = 'YouTube Analysis - NotebookLM API';

  // 기존 성공 슬라이드 재활용
  const slides = [
    'F:/kbj2/workspace/slides/slide01.html',  // 커버
    'F:/kbj2/workspace/slides/slide02.html',  // 시스템 철학
    'F:/kbj2/workspace/slides/slide04.html',  // 데이터 모델
    'F:/kbj2/workspace/slides/slide08.html',  // 실전 성과
  ];

  for (const slide of slides) {
    console.log(`Processing: ${slide.split('/').pop()}`);
    await html2pptx(slide, pptx);
  }

  const outputFile = 'F:/kbj2/final_youtube_analysis.pptx';
  await pptx.writeFile({ fileName: outputFile });
  console.log(`\n[DONE] Created: ${outputFile}`);
}

createFinalPPT().catch(console.error);

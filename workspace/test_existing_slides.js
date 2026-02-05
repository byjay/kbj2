const pptxgen = require('pptxgenjs');
const html2pptx = require('C:/Users/FREE/.claude/skills/pptx-toolkit/scripts/html2pptx.js');

async function testExistingSlides() {
  const pptx = new pptxgen();
  pptx.layout = 'LAYOUT_16x9';

  // 이전에 성공했던 슬라이드들
  const slides = [
    'F:/kbj2/workspace/slides/slide01.html',
    'F:/kbj2/workspace/slides/slide02.html',
    'F:/kbj2/workspace/slides/slide03.html',
    'F:/kbj2/workspace/slides/slide04.html',
  ];

  for (const slide of slides) {
    console.log(`Processing: ${slide}`);
    await html2pptx(slide, pptx);
  }

  await pptx.writeFile({ fileName: 'F:/kbj2/test_existing.pptx' });
  console.log('[DONE] Created: F:/kbj2/test_existing.pptx');
}

testExistingSlides().catch(console.error);

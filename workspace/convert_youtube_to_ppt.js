const pptxgen = require('pptxgenjs');
const html2pptx = require('C:/Users/FREE/.claude/skills/pptx-toolkit/scripts/html2pptx.js');
const fs = require('fs');
const path = require('path');

/**
 * YouTube 분석 슬라이드 → PPT 변환
 */

async function convertYouTubeSlides() {
  const pptx = new pptxgen();
  pptx.layout = 'LAYOUT_16x9';
  pptx.author = 'KBJ2';
  pptx.title = 'YouTube Analysis - Auto Generated';

  const slidesDir = 'F:/kbj2/workspace/slides/';

  // 모든 HTML 슬라이드 파일 (최신 파일 우선)
  const files = fs.readdirSync(slidesDir)
    .filter(f => f.startsWith('slide_') && f.endsWith('.html') && f.match(/slide_\d+\.html/))
    .sort()
    .slice(0, 9); // 최대 9개

  console.log(`Found ${files.length} slides`);

  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    const filePath = path.join(slidesDir, file);

    console.log(`Processing: ${file}`);

    try {
      await html2pptx(filePath, pptx);
    } catch (err) {
      console.error(`Error processing ${file}:`, err.message);
    }
  }

  // 저장
  const outputFile = 'F:/kbj2/youtube_analysis.pptx';
  await pptx.writeFile({ fileName: outputFile });

  console.log(`[DONE] Created: ${outputFile}`);
  return outputFile;
}

convertYouTubeSlides().catch(console.error);

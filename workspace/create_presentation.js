const pptxgen = require('pptxgenjs');
const html2pptx = require('C:/Users/FREE/.claude/skills/pptx-toolkit/scripts/html2pptx.js');

async function main() {
  const pptx = new pptxgen();
  pptx.layout = 'LAYOUT_16x9';
  pptx.author = 'KBJ2';
  pptx.title = 'GLM-4.7 기반 완전 자율 AI 조직 시스템';

  // Slide 1: Title
  const { slide: slide1 } = await html2pptx('F:/kbj2/workspace/slides/slide01.html', pptx);

  // Slide 2: Philosophy
  await html2pptx('F:/kbj2/workspace/slides/slide02.html', pptx);

  // Slide 3: Organization
  await html2pptx('F:/kbj2/workspace/slides/slide03.html', pptx);

  // Slide 4: Data Models
  await html2pptx('F:/kbj2/workspace/slides/slide04.html', pptx);

  // Slide 5: Engine
  await html2pptx('F:/kbj2/workspace/slides/slide05.html', pptx);

  // Slide 6: Project Management
  await html2pptx('F:/kbj2/workspace/slides/slide06.html', pptx);

  // Slide 7: Cost Analysis with Chart
  const { slide: slide7, placeholders: p7 } = await html2pptx('F:/kbj2/workspace/slides/slide07.html', pptx);

  if (p7.length > 0) {
    slide7.addChart(pptx.charts.BAR, [{
      name: "월 비용",
      labels: ["실제 인건비", "AI 시스템"],
      values: [70000000, 700000]
    }], {
      ...p7[0],
      barDir: 'col',
      showTitle: false,
      showLegend: false,
      showCatAxisTitle: false,
      showValAxisTitle: false,
      chartColors: ["2E4053", "AAB7B8"],
      dataLabelPosition: 'outEnd'
    });
  }

  // Slide 8: Results
  await html2pptx('F:/kbj2/workspace/slides/slide08.html', pptx);

  // Slide 9: Closing
  await html2pptx('F:/kbj2/workspace/slides/slide09.html', pptx);

  await pptx.writeFile({ fileName: 'F:/kbj2/NEW_GUIDE_PRESENTATION.pptx' });
  console.log('Presentation created: F:/kbj2/NEW_GUIDE_PRESENTATION.pptx');
}

main().catch(console.error);

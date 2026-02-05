const pptxgen = require('pptxgenjs');
const html2pptx = require('C:/Users/FREE/.claude/skills/pptx-toolkit/scripts/html2pptx.js');
const fs = require('fs');

/**
 * PPT with Images Generator
 * 이미지가 포함된 프레젠테이션 생성
 */

async function createPresentationWithImages() {
  const pptx = new pptxgen();
  pptx.layout = 'LAYOUT_16x9';
  pptx.author = 'KBJ2';
  pptx.title = 'GLM-4.7 기반 완전 자율 AI 조직 시스템 (이미지 포함)';

  // 이미지 경로 설정
  const imagesDir = 'F:/kbj2/workspace/images/';

  // 슬라이드 1: 커버 (배경 이미지)
  const { slide: slide1 } = await html2pptx('F:/kbj2/workspace/slides/slide_01_cover.html', pptx);

  // 슬라이드 2: 시스템 철학 (이미지 포함)
  const { slide: slide2 } = await html2pptx('F:/kbj2/workspace/slides/slide_02.html', pptx);

  // 슬라이드 3: 조직 구조
  await html2pptx('F:/kbj2/workspace/slides/slide_03.html', pptx);

  // 슬라이드 4: 주요 데이터 모델
  await html2pptx('F:/kbj2/workspace/slides/slide_04.html', pptx);

  // 슬라이드 5: 에이전트 실행 엔진
  await html2pptx('F:/kbj2/workspace/slides/slide_05.html', pptx);

  // 슬라이드 6: 프로젝트 관리
  await html2pptx('F:/kbj2/workspace/slides/slide_06.html', pptx);

  // 슬라이드 7: 비용 분석 (차트 포함)
  const { slide: slide7, placeholders: p7 } = await html2pptx('F:/kbj2/workspace/slides/slide_07.html', pptx);

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

  // 슬라이드 8: 실전 성과
  await html2pptx('F:/kbj2/workspace/slides/slide_08.html', pptx);

  // 슬라이드 9: 클로징
  await html2pptx('F:/kbj2/workspace/slides/slide_09.html', pptx);

  // 저장
  await pptx.writeFile({ fileName: 'F:/kbj2/NEW_GUIDE_WITH_IMAGES.pptx' });
  console.log('✅ Presentation created: F:/kbj2/NEW_GUIDE_WITH_IMAGES.pptx');
}

/**
 * 슬라이드 주제로 자동 이미지 생성 후 PPT 제작
 */
async function createAutoImagePresentation(topics) {
  console.log('🎨 이미지 자동 생성 중...');

  // Python 이미지 생성기 호출
  const { spawn } = require('child_process');

  for (let i = 0; i < topics.length; i++) {
    const topic = topics[i];
    console.log(`   생성 중 (${i+1}/${topics.length}): ${topic}`);

    // 이미지 생성
    await new Promise((resolve) => {
      const python = spawn('python', [
        'F:/kbj2/image_generator.py',
        '--generate',
        '--prompt', topic,
        '--output', `slide_${i+1:02d}.png`
      ]);

      python.on('close', resolve);
    });
  }

  console.log('✅ 모든 이미지 생성 완료!');

  // PPT 생성
  await createPresentationWithImages();
}

// 메인 실행
createPresentationWithImages().catch(console.error);

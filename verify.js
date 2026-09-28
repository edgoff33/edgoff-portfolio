const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const DEPLOY = '/mnt/user-data/outputs/edgoff-portfolio';
const PREVIEW = '/mnt/user-data/outputs/previews';

(async () => {
  const b = await chromium.launch();
  const pages = [
    ['index.html','hub.html'],
    ['writing/index.html','writing.html'],
    ['case-studies/index.html','case-studies.html'],
    ['how-i-work/index.html','how-i-work.html'],
    ['how-i-work/30-60-90-day-plan/index.html','how-i-work-30-60-90-day-plan.html'],
    ['how-i-work/blended-cyber-governance-model/index.html','how-i-work-blended-cyber-governance-model.html'],
    ['how-i-work/shared-purpose-in-a-technical-team/index.html','how-i-work-shared-purpose-in-a-technical-team.html'],
    ['published-work/index.html','published-work.html'],
    ['standards/index.html','standards.html'],
    ['career/index.html','career.html'],
    ['capabilities/index.html','capabilities.html'],
    ['credentials/index.html','credentials.html'],
    ['404.html','404.html'],
  ];
  let fail = 0;
  for (const [dep, prev] of pages) {
    for (const [label, file] of [['deploy', path.join(DEPLOY,dep)], ['preview', path.join(PREVIEW,prev)]]) {
      for (const [vp,w,h] of [['phone',390,844],['desktop',1280,900]]) {
        const p = await b.newPage({ viewport:{width:w,height:h} });
        const errs = [];
        p.on('console', m => { if (m.type()==='error') errs.push(m.text()); });
        p.on('requestfailed', r => errs.push('FAILED ' + r.url()));
        await p.goto('file://' + file);
        await p.waitForTimeout(700);
        const over = await p.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth+1);
        // did the stylesheet actually apply?
        const styled = await p.evaluate(() => {
          const bg = getComputedStyle(document.body).backgroundColor;
          const ff = getComputedStyle(document.body).fontFamily;
          return ff.toLowerCase().includes('calibri') || ff.toLowerCase().includes('carlito');
        });
        const cssErrs = errs.filter(e => e.includes('site.css'));

        // house style and disclosure checks, on rendered text only
        const content = await p.evaluate(() => {
          const t = document.body.innerText;
          const brit = ['organisation','programme','colour','centre','licence',
            'prioritise','recognise','analyse','behaviour','defence','favour',
            'realise','summarise','utilise','whilst','amongst','modelling'];
          const imgs = [...document.images];
          return {
            pipe: t.includes('|'),
            emdash: t.includes('\u2014'),
            endash: t.includes('\u2013'),
            curly: t.includes('\u2019'),
            brit: brit.filter(w => new RegExp('\\b' + w, 'i').test(t)),
            // the CISSP certificate carries a number that must never be published
            certno: /\b50603\b/.test(t),
            brokenImgs: imgs.filter(i => !i.complete || i.naturalWidth === 0)
                            .map(i => i.getAttribute('src')),
            unlabelledImgs: imgs.filter(i => !i.getAttribute('alt')).length,
          };
        });
        const contentErrs = [];
        if (content.pipe) contentErrs.push('pipe character');
        if (content.emdash) contentErrs.push('em dash');
        if (content.endash) contentErrs.push('en dash');
        if (content.curly) contentErrs.push('curly apostrophe');
        if (content.brit.length) contentErrs.push('British spelling: ' + content.brit.join(','));
        if (content.certno) contentErrs.push('CERTIFICATION NUMBER ON PAGE');
        if (content.brokenImgs.length) contentErrs.push('image did not load: ' + content.brokenImgs.join(','));
        if (content.unlabelledImgs) contentErrs.push(content.unlabelledImgs + ' image(s) with no alt text');

        if (over || !styled || cssErrs.length || contentErrs.length) {
          console.log(`  FAIL ${label} ${dep} @${vp}  overflow=${over} styled=${styled} ${cssErrs.join(';')} ${contentErrs.join('; ')}`);
          fail++;
        }
        await p.close();
      }
    }
  }
  // screenshot one subpage for eyeball check
  const p = await b.newPage({ viewport:{width:1280,height:900}, deviceScaleFactor:2 });
  await p.goto('file://' + path.join(PREVIEW,'writing.html'));
  await p.waitForTimeout(900);
  await p.screenshot({ path:'/home/claude/site/writing-preview.png' });
  await p.close();
  await b.close();
  console.log(fail === 0 ? '\nAll pages: styled, no overflow, no asset errors.' : `\n${fail} failures`);
})();

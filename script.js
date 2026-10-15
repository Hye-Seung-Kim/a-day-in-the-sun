const sceneOrder = ['harm', 'use', 'reapply', 'priorities', 'association'];
const sceneNames = ['Awareness', 'Routine', 'Friction', 'Priorities', 'Connection'];
const library = document.querySelector('#visual-library');
const stickyStage = document.querySelector('#sticky-stage');
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
const desktop = matchMedia('(min-width: 760px)');
const priorityDescriptions = {
  ingredients: '62.5% rate ingredients moderately or very important. What is in the bottle matters to many adults.',
  affordability: '55.4% rate affordability moderately or very important. Price is one part of the purchase decision.',
  feel: '54.7% rate feel on skin moderately or very important. The survey measures its importance, not product satisfaction.',
  spray: '37.6% rate spray application moderately or very important. This is a purchase consideration, not a spray-use rate.'
};
let motionPreference = null;
try { motionPreference = localStorage.getItem('sun-motion'); } catch (_) {}
function motionIsOff() { return motionPreference === 'off' || reducedMotion.matches; }
function motionAllowed() { return !motionIsOff() && !document.body.classList.contains('keyboard-input'); }
function syncMotion() {
  document.body.classList.toggle('motion-paused', motionIsOff());
  const button = document.querySelector('.motion-toggle');
  button.textContent = reducedMotion.matches ? 'Reduced motion' : motionIsOff() ? 'Enable motion' : 'Pause motion';
  button.disabled = reducedMotion.matches;
  document.documentElement.style.scrollBehavior = motionIsOff() ? 'auto' : '';
  button.setAttribute('aria-pressed', String(motionIsOff()));
  if (motionIsOff()) document.querySelectorAll('.hero-scene,.hero-wave').forEach(el => el.style.transform = 'none');
}
document.querySelector('.motion-toggle').addEventListener('click', () => {
  motionPreference = motionIsOff() ? 'on' : 'off';
  try { localStorage.setItem('sun-motion', motionPreference); } catch (_) {}
  syncMotion();
});
reducedMotion.addEventListener('change', syncMotion);
document.addEventListener('keydown', () => document.body.classList.add('keyboard-input'));
document.addEventListener('pointerdown', () => document.body.classList.remove('keyboard-input'), {passive:true});
syncMotion();

// Add controls to the template before creating desktop and mobile instances.
library.querySelector('.use-panel .people-grid').insertAdjacentHTML('beforebegin', `
  <div class="array-controls" role="group" aria-label="Arrange percentage marks">
    <button type="button" data-arrangement="grid" aria-pressed="true">100-mark grid</button>
    <button type="button" data-arrangement="groups" aria-pressed="false">Separate responses ↔</button>
  </div><div class="group-labels" aria-hidden="true"><span>Frequent use</span><span>Less frequent use</span></div>`);
library.querySelector('.association-panel .population-label').insertAdjacentHTML('afterend', `
  <div class="comparison-controls" role="group" aria-label="Choose frequency to compare">
    <button type="button" data-frequency="frequent" aria-pressed="true">Most / always</button>
    <button type="button" data-frequency="less" aria-pressed="false">Never / rarely / sometimes</button>
  </div>`);
library.querySelector('.priorities-panel .product-figure').insertAdjacentHTML('afterbegin', `
  <div class="bag-hotspots" role="group" aria-label="Explore the beach bag">
    <button type="button" data-priority-pick="ingredients" aria-pressed="true">Ingredients</button>
    <button type="button" data-priority-pick="affordability" aria-pressed="false">Price</button>
    <button type="button" data-priority-pick="feel" aria-pressed="false">Feel</button>
    <button type="button" data-priority-pick="spray" aria-pressed="false">Spray</button>
  </div>`);
document.querySelector('[data-scene="reapply"] .step-copy').insertAdjacentHTML('beforeend', `
  <details class="survey-detail"><summary>What did the survey actually ask?</summary><p>“It is a hassle to reapply sunscreen.” Adults rated their agreement. The item does not identify why it feels inconvenient.</p></details>`);
sceneOrder.forEach(name => {
  const source = library.querySelector(`[data-visual="${name}"]`);
  for (const host of [stickyStage, document.querySelector(`[data-mobile-scene="${name}"]`)]) {
    const clone = source.cloneNode(true);
    clone.removeAttribute('data-visual');
    clone.dataset.scenePanel = name;
    host.append(clone);
  }
});
library.remove();

// Keep marks alive across switches, so changed responses can move from their current positions.
function buildPeopleGrid(grid, activeCount, markerColor) {
  if (!grid.children.length) {
    const fragment = document.createDocumentFragment();
    for (let i=0;i<100;i++) {
      const mark = document.createElement('span');
      mark.className = 'mini-person';
      mark.setAttribute('aria-hidden','true');
      mark.style.setProperty('--stagger', `${Math.floor(i/10)*40}ms`);
      fragment.append(mark);
    }
    grid.append(fragment);
  }
  grid.dataset.activeCount = activeCount;
  grid.style.setProperty('--marker', markerColor);
  [...grid.children].forEach((mark,i) => mark.classList.toggle('active',i<activeCount));
  arrangeGrid(grid);
}
function arrangeGrid(grid) {
  const width=grid.clientWidth;
  if (!width) return;
  const grouped=grid.closest('.use-panel')?.dataset.arrangement==='groups';
  const count=Number(grid.dataset.activeCount);
  [...grid.children].forEach((mark,i) => {
    let x=15+(i%10)*39, y=14+Math.floor(i/10)*35;
    if (grouped) {
      const selected=i<count, j=selected?i:i-count, columns=selected?4:6;
      x=(selected?8:176)+(j%columns)*35;
      y=14+Math.floor(j/columns)*29;
    }
    mark.style.transform=`translate(${x/400*width}px,${y/400*width}px)`;
    mark.style.width=`${23/400*width}px`;
    mark.style.height=`${28/400*width}px`;
  });
}
function updateUsePanels(mode) {
  const skin=mode==='skin';
  document.querySelectorAll('.use-panel').forEach(panel => {
    panel.dataset.mode=mode;
    panel.querySelector('[data-use-label]').textContent=skin?'Other exposed skin':'Face';
    panel.querySelector('[data-use-value]').textContent=skin?'27.6%':'31.1%';
    buildPeopleGrid(panel.querySelector('[data-grid="use"]'),skin?28:31,skin?'var(--coral)':'var(--purple)');
    panel.querySelectorAll('[data-use-mode]').forEach(button => {
      const selected=button.dataset.useMode===mode;
      button.classList.toggle('active',selected);button.setAttribute('aria-pressed',String(selected));
    });
    panel.querySelector('.legend-mark.purple').style.background=skin?'var(--coral)':'var(--purple)';
  });
}
function updateArrangement(mode) {
  document.querySelectorAll('.use-panel').forEach(panel => {
    panel.dataset.arrangement=mode;
    panel.querySelectorAll('[data-arrangement]').forEach(button => button.setAttribute('aria-pressed',String(button.dataset.arrangement===mode)));
    arrangeGrid(panel.querySelector('.people-grid'));
  });
}
function updatePriorityPanels(priority) {
  document.querySelectorAll('.priorities-panel').forEach(panel => {
    panel.dataset.priority=priority;
    panel.querySelector('[data-priority-description]').textContent=priorityDescriptions[priority];
    panel.querySelectorAll('.priority-row,[data-priority-pick]').forEach(button => {
      const selected=(button.dataset.priority||button.dataset.priorityPick)===priority;
      button.classList.toggle('active',selected);button.setAttribute('aria-pressed',String(selected));
    });
  });
}
function updateFrequency(mode) {
  const less=mode==='less', values=less?[80.7,64.9]:[19.3,35.1];
  document.querySelectorAll('.association-panel').forEach(panel => {
    panel.dataset.frequency=mode;
    panel.querySelector('.population-label').textContent=`${less?'Less frequent':'Frequent'} face sunscreen use, by importance of ingredients`;
    panel.querySelectorAll('[data-frequency]').forEach(button => button.setAttribute('aria-pressed',String(button.dataset.frequency===mode)));
    panel.querySelectorAll('.comparison-row').forEach((row,i) => {
      row.querySelector('.comparison-bar span').style.width='100%';
      row.querySelector('.comparison-bar span').style.transform=`scaleX(${values[i]/100})`;
      row.querySelector('strong').textContent=`${values[i].toFixed(1)}%`;
    });
    panel.querySelector('.axis').innerHTML='<span>0</span><span>50%</span><span>100%</span>';
    panel.querySelector('.comparison-chart').setAttribute('aria-label',`${less?'Never, rarely, or sometimes':'Most of the time or always'} face use: ${values[0]} percent in the lower ingredient-importance group; ${values[1]} percent in the higher group.`);
    panel.querySelector('.visual-note').textContent='Same 0–100% scale in both views. Valid n: lower importance 2,696; higher importance 4,759. Descriptive estimates; no significance test.';
  });
}
document.addEventListener('click',event => {
  const chapterLink=event.target.closest('a[href^="#chapter-"]');
  if(chapterLink){
    const chapter=document.querySelector(chapterLink.getAttribute('href'));
    if(chapter){
      event.preventDefault();
      const copy=chapter.querySelector('.step-copy');
      const top=copy.getBoundingClientRect().top+scrollY-120;
      history.replaceState(null,'',chapterLink.getAttribute('href'));
      window.scrollTo({top,behavior:motionAllowed()?'smooth':'instant'});
    }
  }
  const use=event.target.closest('[data-use-mode]');if(use) updateUsePanels(use.dataset.useMode);
  const arrange=event.target.closest('[data-arrangement]');if(arrange) updateArrangement(arrange.dataset.arrangement);
  const priority=event.target.closest('.priority-row[data-priority],[data-priority-pick]');if(priority) updatePriorityPanels(priority.dataset.priority||priority.dataset.priorityPick);
  const frequency=event.target.closest('[data-frequency]');if(frequency) updateFrequency(frequency.dataset.frequency);
});
document.querySelectorAll('[data-grid="harm"]').forEach(grid=>buildPeopleGrid(grid,82,'var(--yellow)'));
updateUsePanels('face');updateArrangement('grid');updatePriorityPanels('ingredients');updateFrequency('frequent');
const resizeObserver=new ResizeObserver(entries=>entries.forEach(({target})=>arrangeGrid(target)));
document.querySelectorAll('.people-grid').forEach(grid=>resizeObserver.observe(grid));

// A prediction is a reader interaction, never an additional survey response.
const guessRange=document.querySelector('#guess-range');
const guessOutput=document.querySelector('#guess-output');
const guessDots=document.querySelector('.guess-dots');
const guessResult=document.querySelector('.guess-result');
const revealButton=document.querySelector('.reveal-answer');
const resetButton=document.querySelector('.reset-guess');
for(let i=0;i<100;i++) { const dot=document.createElement('span');dot.style.setProperty('--stagger',`${Math.floor(i/10)*40}ms`);guessDots.append(dot); }
function drawGuess(value) {
  guessOutput.textContent=`${value}%`;
  guessRange.style.setProperty('--fill',`${value}%`);
  [...guessDots.children].forEach((dot,i)=>dot.classList.toggle('filled',i<value));
}
guessRange.addEventListener('input',()=>drawGuess(Number(guessRange.value)));
revealButton.addEventListener('click',()=>{
  const guess=Number(guessRange.value),difference=Math.abs(guess-31.1).toFixed(1);
  guessResult.innerHTML=`<span class="result-eyebrow">The survey says</span><strong>31.1<span>%</span></strong><p>You guessed ${guess}%. The weighted estimate is ${difference} percentage points ${guess>31.1?'lower':'higher'}.</p><p class="result-base">Adults who recognize long-term harm; valid n = 6,276. Colored marks round to 31 out of 100.</p><a href="#chapter-harm">Let’s see the bigger picture ↓</a>`;
  guessResult.hidden=false;resetButton.hidden=false;revealButton.hidden=true;guessRange.disabled=true;
  document.querySelector('.guess-playground').classList.add('answer-shown');
  [...guessDots.children].forEach((dot,i)=>dot.classList.toggle('filled',i<31));
});
resetButton.addEventListener('click',()=>{
  guessResult.hidden=true;resetButton.hidden=true;revealButton.hidden=false;guessRange.disabled=false;
  document.querySelector('.guess-playground').classList.remove('answer-shown');drawGuess(Number(guessRange.value));guessRange.focus();
});
drawGuess(50);

// One active scene, selected from all chapters, also handles fast reverse scrolling.
let activeScene='';
const steps=[...document.querySelectorAll('.step')];
const scrolly=document.querySelector('.scrolly');
function setActiveScene(name) {
  activeScene=name;
  document.querySelectorAll('[data-scene-panel]').forEach(panel=>{
    const active=panel.dataset.scenePanel===name;
    panel.classList.toggle('is-active',active);
    if(panel.parentElement===stickyStage) {panel.inert=!desktop.matches||!active;panel.setAttribute('aria-hidden',String(!desktop.matches||!active));}
    if(active && desktop.matches && panel.parentElement===stickyStage && scrolly.getBoundingClientRect().top < innerHeight*.75) panel.classList.add('has-entered');
  });
  steps.forEach(step=>step.classList.toggle('is-active',step.dataset.scene===name));
  document.querySelectorAll('[data-chapter]').forEach(link=>{
    if(link.dataset.chapter===name)link.setAttribute('aria-current','step');else link.removeAttribute('aria-current');
  });
  const index=sceneOrder.indexOf(name);
  stickyStage.dataset.chapter=name;
  stickyStage.querySelector('.stage-chapter').textContent=`0${index+1} / ${sceneNames[index]}`;
}
let queued=false;
function updateScroll() {
  queued=false;
  const target=innerHeight*.47;
  const current=steps.reduce((best,step)=>{
    const rect=step.getBoundingClientRect();const distance=target<rect.top?rect.top-target:target>rect.bottom?target-rect.bottom:0;
    return distance<best.distance?{step,distance}:best;
  },{step:steps[0],distance:Infinity}).step;
  if(current.dataset.scene!==activeScene)setActiveScene(current.dataset.scene);
  const scrollyRect=scrolly.getBoundingClientRect();
  if(desktop.matches && scrollyRect.top<innerHeight*.75) stickyStage.querySelector(`[data-scene-panel="${activeScene}"]`)?.classList.add('has-entered');
  document.querySelector('.chapter-nav').classList.toggle('in-story',scrollyRect.top<innerHeight&&scrollyRect.bottom>100);
  const max=document.documentElement.scrollHeight-innerHeight;
  document.querySelector('.reading-progress span').style.transform=`scaleX(${max>0?scrollY/max:0})`;
  const hero=document.querySelector('.hero').getBoundingClientRect();
  if(hero.bottom>0 && motionAllowed()) {
    const fraction=Math.min(1,Math.max(0,-hero.top/hero.height));
    document.querySelector('.hero-scene').style.transform=`translateY(${fraction*35}px) rotate(${fraction*-2}deg)`;
    document.querySelector('.hero-wave').style.transform=`translateX(${fraction*30}px)`;
  }
}
function queueScroll() {if(!queued){queued=true;requestAnimationFrame(updateScroll);}}
window.addEventListener('scroll',queueScroll,{passive:true});window.addEventListener('resize',queueScroll,{passive:true});
desktop.addEventListener('change',()=>{setActiveScene(activeScene||'harm');queueScroll();});
const revealObserver=new IntersectionObserver(entries=>{
  entries.forEach(entry=>{
    if(entry.isIntersecting){entry.target.classList.add('has-entered');revealObserver.unobserve(entry.target);}
  });
},{threshold:.15});
document.querySelectorAll('.mobile-visual .visual-panel,.story-intro,.closing-copy,.first-thought').forEach(el=>revealObserver.observe(el));
document.body.classList.add('enhanced');setActiveScene('harm');queueScroll();

// Retain the project's documentation / screenshot views.
const captureTarget=new URLSearchParams(location.search).get('capture');
if(captureTarget){
  const shell=document.createElement('main');shell.className='capture-shell';
  if(sceneOrder.includes(captureTarget)){
    const copy=document.querySelector(`[data-scene="${captureTarget}"] .step-copy`).cloneNode(true);
    copy.querySelectorAll('[id]').forEach(el=>el.removeAttribute('id'));
    const visual=stickyStage.querySelector(`[data-scene-panel="${captureTarget}"]`).cloneNode(true);
    visual.classList.add('is-active','has-entered');visual.inert=false;visual.removeAttribute('aria-hidden');
    shell.append(copy,visual);
  }else if(['closing','methods'].includes(captureTarget))shell.append(document.querySelector(`.${captureTarget}`).cloneNode(true));
  document.body.classList.add('capture-mode');document.body.append(shell);
  shell.querySelectorAll('.people-grid').forEach(grid=>resizeObserver.observe(grid));
}

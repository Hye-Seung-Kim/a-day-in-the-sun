from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'output/pdf/A-Day-in-the-Sun.pdf'
W, H = 960, 540
SAND, PAPER, INK, SOFT = '#f0dfbf', '#fff8e8', '#182e32', '#536a69'
PURPLE, YELLOW, CORAL, SEA = '#6656e8', '#f4c84b', '#e86a54', '#bfe1df'
c = canvas.Canvas(str(OUT), pagesize=(W,H))
c.setTitle('A Day in the Sun | An illustrated data story')
c.setAuthor('A Day in the Sun')
art = ImageReader(str(ROOT / 'assets/beach-friends.png'))
page = 0

def rect(x,y,w,h,color):
    c.setFillColor(HexColor(color));c.rect(x,H-y-h,w,h,fill=1,stroke=0)
def text(s,x,y,size=18,color=INK,bold=False):
    c.setFillColor(HexColor(color));c.setFont('Helvetica-Bold' if bold else 'Helvetica',size)
    c.drawString(x,H-y-size,s)
def para(s,x,y,w,size=17,color=INK,bold=False,leading=None):
    style=ParagraphStyle('p',fontName='Helvetica-Bold' if bold else 'Helvetica',fontSize=size,leading=leading or size*1.38,textColor=HexColor(color))
    p=Paragraph(s,style);_,h=p.wrap(w,1000);p.drawOn(c,x,H-y-h);return h
def rule(y=491,color=SOFT): rect(44,y,872,.6,color)
def start(kicker,bg=PAPER):
    global page
    page+=1;rect(0,0,W,H,bg)
    text('A DAY IN THE SUN',44,23,10,INK,True)
    text(kicker.upper(),305,23,10,SOFT,True)
    rule();text('CDC / NCHS  ·  Rapid Surveys System, Round 1  ·  August 2023',44,506,9,SOFT)
    text(f'{page:02d} / 11',871,505,10,INK,True)
def end():c.showPage()
def title(s,w=840,size=40): return para(s,44,69,w,size,bold=True,leading=size*1.06)
def note(s,y=454,w=872):para(s,44,y,w,10,SOFT,leading=13)
def bars(labels,values,x,y,w=380,row=61,color=PURPLE,maxval=100):
    for i,(label,v) in enumerate(zip(labels,values)):
        yy=y+i*row;text(label,x,yy,14,INK,True)
        rect(x,yy+25,w,14,'#e4d9c5');rect(x,yy+25,w*v/maxval,14,color)
        text(f'{v:.1f}%',x+w+15,yy+18,20,color,True)
    yy=y+(len(values)-1)*row+47
    for frac in (0,.5,1):text(f'{maxval*frac:g}%',x+w*frac-6,yy,9,SOFT)
def dotgrid(x,y,active,color,size=15,gap=25):
    for i in range(100):
        c.setFillColor(HexColor(color if i<active else '#d9cebb'))
        c.circle(x+(i%10)*gap,H-y-(i//10)*gap,size/2,fill=1,stroke=0)

start('An illustrated data story',SAND)
text('A DAY',44,92,78,INK,True);text('IN THE',44,168,78,INK,True);text('SUN',44,244,92,CORAL,True)
para('What shapes whether sun protection fits into a day outdoors?',46,362,400,24,bold=True)
c.drawImage(art,530,53,width=360,height=450,mask='auto',preserveAspectRatio=True)
note('An MFA thesis investigation into sunlight, sunscreen use, and everyday outdoor experience.',y=461,w=455)
end()

start('01 / The data and the question')
title('A population-level starting point.<br/>An everyday design question.',size=38)
text('7,599',44,197,76,PURPLE,True);text('U.S. adults surveyed',48,281,19,INK,True)
para('Existing dataset: CDC/NCHS Rapid Surveys System, Round 1. Collected in August 2023 through two probability-based online panels.',48,321,380,17)
rect(498,199,418,228,SAND)
text('WHY THIS DATASET?',520,217,11,SOFT,True)
para('It brings beliefs, reported use, and sunscreen purchase considerations into the same survey.',520,246,370,21,bold=True,leading=26)
para('These patterns help frame a thesis question about making sun protection fit into enjoyable outdoor experiences.',520,363,365,14,leading=18)
note('Percentages use WEIGHT_M1 and valid responses for each analysis. The survey was not limited to beachgoers.')
end()

start('02 / Choosing the visual form')
title('Three ways to make the data readable.',size=38)
cols=[44,344,644]
for x in cols: rect(x,151,272,279,SAND)
for i in range(25):
    c.setFillColor(HexColor(YELLOW if i<20 else '#cfbea2'));c.circle(71+(i%5)*17,H-179-(i//5)*17,5,fill=1,stroke=0)
text('82%',182,195,30,INK,True)
for i,v in enumerate([.625,.554,.547,.376]):rect(366,174+23*i,210*v,12,PURPLE)
for i in range(3):
    rect(665+i*75,178,62,65,PAPER);text(str(i+1),685+i*75,195,20,CORAL,True)
for x,head,body in zip(cols,['100-mark array','Horizontal bars','Illustrated sequence'],[
    'Chosen for part-to-whole reading. Exact labels preserve precision while icons are rounded. Each population gets a new array.',
    'Chosen for comparisons on a shared baseline. Pie charts were rejected: independently rated priorities do not sum to 100%.',
    'Chosen to connect findings to a research question. A funnel was rejected because the survey does not follow people over time.'
]):
    text(head,x+19,270,19,INK,True);para(body,x+19,309,233,14)
note('Form exploration for this revision. The beach creates narrative context; the charts alone encode the survey estimates.')
end()

start('03 / Recognizing harm')
title('Most adults recognize<br/>the long-term harm of sunburn.',w=830,size=40)
text('82.0%',44,215,92,INK,True)
para('Disagree that sunburn is not really harmful in the long run.',49,327,382,24,bold=True)
dotgrid(610,207,82,YELLOW,size=16,gap=24)
note('Base: all valid SUN_NOHARM responses (codes 1-4), n = 7,510. Selected: strongly or somewhat disagree (1-2).',y=445)
note('Each mark is approximately one percentage point, not one respondent. 82 colored marks represent a rounded estimate.',y=464)
end()

start('04 / Reported sunscreen use')
title('Recognizing harm does not mean<br/>frequent sunscreen use.',size=40)
rect(44,179,872,44,INK);text('NEW BASE: ADULTS WHO RECOGNIZE THE LONG-TERM HARM OF SUNBURN',60,193,12,PAPER,True)
bars(['Face','Other exposed skin'],[31.1,27.6],44,257,w=480,row=79,color=PURPLE)
para('Frequent use means<br/><b>most of the time<br/>or always.</b>',660,261,242,23)
note('Face n = 6,276; other exposed skin n = 6,273. Valid use responses within SUN_NOHARM 1-2.',y=441)
note('Use refers to being outdoors in the sun in warm weather. Face use excludes makeup or moisturizer containing sunscreen.',y=461)
end()

start('05 / Reapplication')
title('Reapplication can feel like a hassle.',size=40)
text('60.6%',44,181,104,CORAL,True)
para('Agree that reapplying sunscreen is a hassle.',52,306,398,26,bold=True)
rect(519,189,397,218,SAND)
text('WHAT THIS OPENS UP',542,211,11,SOFT,True)
para('Which moments make protection difficult to fit into a day outdoors?',542,245,348,23,bold=True,leading=28)
para('A question for primary research. The survey does not identify the circumstances behind the hassle.',542,344,348,13,leading=17)
rect(44,412,872,15,'#e4d9c5');rect(44,412,872*.606,15,CORAL)
note('Base: valid SUN_REAPPLY 1-4, n = 7,479. Selected: somewhat or strongly agree (3-4).',y=445)
note('The bar uses a 0-100% scale. This attitude is not a measured count of reapplications.',y=464)
end()

start('06 / Product priorities')
title('What matters when choosing sunscreen?',size=38)
bars(['Ingredients','Affordability','Feel on skin','Spray application'],[62.5,55.4,54.7,37.6],44,176,w=488,row=61)
para('Moderately or<br/>very important',676,181,240,26,bold=True)
para('Each feature was rated independently.<br/><br/>Spray application means the importance of being able to spray sunscreen onto the skin. It is not a use rate.',676,269,220,16)
note('Valid n: ingredients 7,477; affordability 7,502; feel 7,479; spray 7,472. Selected: codes 2-3, among valid 0-3.',y=460)
end()

start('07 / Priorities and reported use')
title('Ingredient priorities are associated<br/>with reported use.',size=40)
text('FREQUENT FACE USE, BY INGREDIENT IMPORTANCE',44,184,11,SOFT,True)
bars(['Not or slightly important','Moderately or very important'],[19.3,35.1],44,224,w=468,row=79,maxval=40)
text('64.9%',669,225,56,CORAL,True)
para('of the higher-importance group use face sunscreen never, rarely, or sometimes.',671,299,234,18)
note('Valid n: lower importance 2,696; higher importance 4,759. Bars share a 0-40% scale. No significance test is reported.',y=441)
note('Ingredient importance is not product quality or satisfaction. This descriptive association does not establish causation.',y=461)
end()

start('08 / Connection to the thesis',SAND)
title('From survey patterns<br/>to lived outdoor experience.',w=620,size=39)
text('PRIMARY RESEARCH QUESTION',44,200,11,SOFT,True)
para('How do adults who enjoy outdoor activities and have experienced sunburn decide whether and how to protect themselves from sun exposure?',44,224,510,25,bold=True,leading=30)
para('<b>Design aim to explore</b><br/>Support enjoyable outdoor experiences while reducing the risk of sunburn.',44,397,510,14)
c.drawImage(art,603,91,width=291,height=364,mask='auto',preserveAspectRatio=True)
note('Sunburn history and outdoor enjoyment were not measured in this survey. This is a proposed focus for primary research.',y=465)
end()

start('09 / Methods and traceability')
title('What each number represents.',size=38)
para('Weighted percentage = selected-response weights / valid-response weights × 100. All n values are unweighted valid counts. Invalid responses (-6, -7, -8, -9) are excluded.',44,127,872,14)
rows=[
('Recognizes harm','82.0%','7,510','NOHARM 1-2 / valid 1-4'),
('Frequent face use, recognizes harm','31.1%','6,276','USEFACE 3-4; NOHARM 1-2'),
('Frequent other-skin use, recognizes harm','27.6%','6,273','USESKIN 3-4; NOHARM 1-2'),
('Reapplication is a hassle','60.6%','7,479','REAPPLY 3-4 / valid 1-4'),
('Ingredients important','62.5%','7,477','INGRED 2-3 / valid 0-3'),
('Affordability important','55.4%','7,502','AFFORD 2-3 / valid 0-3'),
('Feel important','54.7%','7,479','FEEL 2-3 / valid 0-3'),
('Spray application important','37.6%','7,472','SPRAY 2-3 / valid 0-3'),
('Frequent face use, lower ingredient importance','19.3%','2,696','USEFACE 3-4; INGRED 0-1'),
('Frequent face use, higher ingredient importance','35.1%','4,759','USEFACE 3-4; INGRED 2-3')]
rect(44,184,872,25,INK)
for s,x in [('MEASURE',54),('ESTIMATE',484),('VALID n',578),('RECODE (SUN_ PREFIX)',670)]:text(s,x,191,10,PAPER,True)
for i,row in enumerate(rows):
    yy=210+i*22
    if i%2==0:rect(44,yy,872,22,SAND)
    for val,x in zip(row,[54,484,578,670]):text(val,x,yy+5,10.5)
note('Frequent use: valid codes 0-4, selected 3-4. Subgroup rows additionally require the stated valid subgroup codes.',y=441)
note('No confidence intervals or tests are shown; comparisons are descriptive. Cross-sectional self-report cannot establish causation.',y=461)
end()

start('10 / Sources and credits')
title('Sources, scope, and illustration.',size=40)
links=[
('Public-use dataset','https://www.cdc.gov/nchs/data/rss/rss1_puf_t1.csv'),
('Codebook: item wording and response codes','https://www.cdc.gov/nchs/data/rss/codebook.pdf'),
('Survey description: sampling and weights','https://www.cdc.gov/nchs/data/rss/survey-description.pdf'),
('Technical notes: sunscreen measures','https://www.cdc.gov/nchs/data/rss/technical-notes.pdf'),
('CDC/NCHS Round 1 sunscreen overview','https://www.cdc.gov/nchs/rss/round1/sunscreen.html')]
for i,(label,url) in enumerate(links):
    yy=147+i*54;text(label,44,yy,14,INK,True);text(url,44,yy+22,10,SOFT)
    c.linkURL(url,(44,H-yy-39,570,H-yy),relative=0,thickness=0)
rect(626,147,290,276,SAND)
para('<b>Interpretation limits</b><br/>Coverage and nonresponse bias may remain after weighting. The survey does not establish causal effects, actual sunburn occurrence, or product effectiveness.',646,168,248,15)
para('<b>Illustration credit</b><br/>AI-generated for this project using user-supplied visual references. Beach characters are decorative, not respondents.',646,310,248,13)
note('Local source files retained from October 1, 2026. All 10 displayed estimates and valid n values were recalculated for this revision.',y=443)
note('The presentation documents an interactive web visualization. Source links are clickable.',y=464)
end()
c.save()
print(OUT)

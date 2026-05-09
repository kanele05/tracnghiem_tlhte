"""Generate the quiz HTML file with all 200 questions embedded."""
import json

with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

questions_json = json.dumps(questions, ensure_ascii=False)

html = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Trắc nghiệm Tâm lí học trẻ em - 200 câu / 4 đề</title>
<style>
  * { box-sizing: border-box; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    margin: 0;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    color: #222;
  }
  .container {
    max-width: 900px;
    margin: 0 auto;
    padding: 20px;
  }
  .card {
    background: #fff;
    border-radius: 14px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.18);
    padding: 28px;
    margin-bottom: 18px;
  }
  h1 {
    margin-top: 0;
    color: #fff;
    text-align: center;
    text-shadow: 0 2px 8px rgba(0,0,0,0.25);
    font-size: 1.7em;
  }
  h2 { margin-top: 0; color: #4a3b8a; }
  .subtitle { text-align: center; color: #f0e8ff; margin-bottom: 22px; }
  .exam-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 14px;
    margin-top: 16px;
  }
  .exam-btn {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: #fff;
    border: none;
    border-radius: 12px;
    padding: 22px 14px;
    font-size: 1.1em;
    font-weight: 600;
    cursor: pointer;
    transition: transform .15s, box-shadow .15s;
    box-shadow: 0 4px 14px rgba(118,75,162,0.35);
  }
  .exam-btn:hover { transform: translateY(-2px); box-shadow: 0 8px 22px rgba(118,75,162,0.45); }
  .exam-btn small { display: block; opacity: 0.85; font-weight: 400; margin-top: 4px; font-size: 0.85em; }
  .question {
    border-bottom: 1px solid #eee;
    padding: 16px 0;
  }
  .question:last-child { border-bottom: none; }
  .q-text {
    font-weight: 600;
    margin-bottom: 10px;
    line-height: 1.5;
  }
  .q-num { color: #764ba2; margin-right: 6px; }
  .options { list-style: none; padding: 0; margin: 0; }
  .options li {
    margin: 6px 0;
  }
  .options label {
    display: flex;
    align-items: flex-start;
    padding: 10px 12px;
    background: #f7f7fb;
    border: 2px solid transparent;
    border-radius: 8px;
    cursor: pointer;
    transition: background .15s, border-color .15s;
    line-height: 1.45;
  }
  .options label:hover { background: #efeaff; }
  .options input[type=radio] {
    margin-right: 10px;
    margin-top: 3px;
    accent-color: #764ba2;
  }
  .opt-letter { font-weight: 700; color: #764ba2; margin-right: 6px; }
  /* Review states */
  .reviewed .options label { cursor: default; }
  .reviewed .options label.correct {
    background: #e3f9e5;
    border-color: #2e9c4d;
  }
  .reviewed .options label.incorrect {
    background: #fde2e2;
    border-color: #c93a3a;
  }
  .reviewed .options label.correct::after {
    content: " ✓";
    color: #2e9c4d;
    font-weight: bold;
    margin-left: auto;
    padding-left: 8px;
  }
  .reviewed .options label.incorrect::after {
    content: " ✗";
    color: #c93a3a;
    font-weight: bold;
    margin-left: auto;
    padding-left: 8px;
  }
  .controls {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    justify-content: center;
    margin-top: 18px;
  }
  .btn {
    padding: 12px 24px;
    border: none;
    border-radius: 8px;
    font-size: 1em;
    font-weight: 600;
    cursor: pointer;
    transition: opacity .15s;
  }
  .btn:hover { opacity: 0.88; }
  .btn-primary { background: #764ba2; color: #fff; }
  .btn-secondary { background: #e8e2ff; color: #4a3b8a; }
  .btn-success { background: #2e9c4d; color: #fff; }
  .progress-bar {
    background: #e8e2ff;
    border-radius: 6px;
    height: 8px;
    overflow: hidden;
    margin: 10px 0 18px;
  }
  .progress-fill {
    background: linear-gradient(90deg, #667eea, #764ba2);
    height: 100%;
    transition: width .3s;
  }
  .score-box {
    text-align: center;
    padding: 22px;
    background: linear-gradient(135deg, #f5f0ff, #e8e2ff);
    border-radius: 12px;
    margin-bottom: 18px;
  }
  .score-num { font-size: 2.6em; font-weight: 700; color: #4a3b8a; line-height: 1; }
  .score-label { color: #666; margin-top: 4px; }
  .answer-info {
    margin-top: 6px;
    font-size: 0.92em;
    color: #555;
    padding-left: 8px;
    font-style: italic;
  }
  .header-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 8px;
  }
  .badge {
    display: inline-block;
    background: #764ba2;
    color: #fff;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 0.85em;
    font-weight: 600;
  }
  @media (max-width: 600px) {
    h1 { font-size: 1.3em; }
    .card { padding: 18px; }
    .controls { flex-direction: column; }
    .btn { width: 100%; }
  }
</style>
</head>
<body>
<div class="container">
  <h1>📚 Trắc nghiệm Tâm lí học trẻ em</h1>
  <p class="subtitle">200 câu hỏi · chia thành 4 đề · xáo trộn ngẫu nhiên</p>

  <div id="screen-home" class="card">
    <h2>Chọn đề thi</h2>
    <p>Mỗi đề gồm 50 câu hỏi được chọn ngẫu nhiên từ 200 câu. Mỗi lần bấm <em>"Xáo trộn lại"</em> sẽ tạo bộ đề mới.</p>
    <div class="exam-grid" id="examGrid"></div>
    <div class="controls" style="margin-top: 20px;">
      <button class="btn btn-secondary" onclick="reshuffle()">🔀 Xáo trộn lại</button>
    </div>
  </div>

  <div id="screen-quiz" class="card" style="display:none;">
    <div class="header-bar">
      <h2 id="examTitle">Đề 1</h2>
      <span class="badge" id="answeredCount">0/50</span>
    </div>
    <div class="progress-bar"><div class="progress-fill" id="progressFill" style="width:0%"></div></div>
    <div id="questionsContainer"></div>
    <div class="controls">
      <button class="btn btn-secondary" onclick="goHome()">← Quay lại</button>
      <button class="btn btn-success" onclick="submitQuiz()">✅ Nộp bài</button>
    </div>
  </div>

  <div id="screen-result" class="card" style="display:none;">
    <h2 id="resultTitle">Kết quả</h2>
    <div class="score-box">
      <div class="score-num" id="scoreNum">0/50</div>
      <div class="score-label" id="scoreLabel">Số câu đúng</div>
    </div>
    <h2 style="margin-top: 24px;">Xem đáp án chi tiết</h2>
    <div id="reviewContainer"></div>
    <div class="controls">
      <button class="btn btn-primary" onclick="goHome()">🏠 Về trang chính</button>
      <button class="btn btn-secondary" onclick="retryExam()">🔁 Làm lại đề này</button>
    </div>
  </div>
</div>

<script>
const QUESTIONS = __QUESTIONS_JSON__;

let exams = [];          // 4 đề: each = list of 50 questions, each with shuffled options
let currentExamIdx = -1;
let currentQuestions = [];
let userAnswers = [];     // shuffled-option index user picked, or null

function shuffle(arr) {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function buildExams() {
  // Shuffle all 200 question indices, split into 4 groups of 50
  const allIdx = shuffle(QUESTIONS.map((_, i) => i));
  exams = [];
  for (let g = 0; g < 4; g++) {
    const slice = allIdx.slice(g * 50, (g + 1) * 50);
    const group = slice.map(qi => {
      const q = QUESTIONS[qi];
      // Shuffle option order; track new index of correct answer
      const optOrder = shuffle([0, 1, 2, 3]);
      const newOptions = optOrder.map(i => q.options[i]);
      const newAnswer = optOrder.indexOf(q.answer);
      return {
        originalIdx: qi,
        text: q.q,
        options: newOptions,
        answer: newAnswer
      };
    });
    exams.push(group);
  }
}

function renderHome() {
  const grid = document.getElementById('examGrid');
  grid.innerHTML = '';
  for (let i = 0; i < 4; i++) {
    const btn = document.createElement('button');
    btn.className = 'exam-btn';
    btn.innerHTML = `Đề ${i + 1}<small>50 câu hỏi</small>`;
    btn.onclick = () => startExam(i);
    grid.appendChild(btn);
  }
}

function reshuffle() {
  buildExams();
  renderHome();
  alert('Đã xáo trộn lại 4 đề!');
}

function show(screen) {
  ['screen-home', 'screen-quiz', 'screen-result'].forEach(id => {
    document.getElementById(id).style.display = id === screen ? 'block' : 'none';
  });
  window.scrollTo(0, 0);
}

function startExam(idx) {
  currentExamIdx = idx;
  currentQuestions = exams[idx];
  userAnswers = new Array(currentQuestions.length).fill(null);
  document.getElementById('examTitle').textContent = `Đề ${idx + 1}`;
  renderQuiz();
  show('screen-quiz');
}

function renderQuiz() {
  const container = document.getElementById('questionsContainer');
  container.innerHTML = '';
  const letters = ['A', 'B', 'C', 'D'];
  currentQuestions.forEach((q, qi) => {
    const div = document.createElement('div');
    div.className = 'question';
    div.id = `q-${qi}`;
    let optHtml = '';
    q.options.forEach((opt, oi) => {
      const checked = userAnswers[qi] === oi ? 'checked' : '';
      optHtml += `<li><label>
        <input type="radio" name="q${qi}" value="${oi}" ${checked} onchange="pickAnswer(${qi}, ${oi})">
        <span><span class="opt-letter">${letters[oi]}.</span>${escapeHtml(opt)}</span>
      </label></li>`;
    });
    div.innerHTML = `
      <div class="q-text"><span class="q-num">Câu ${qi + 1}.</span>${escapeHtml(q.text)}</div>
      <ul class="options">${optHtml}</ul>
    `;
    container.appendChild(div);
  });
  updateProgress();
}

function escapeHtml(s) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
          .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

function pickAnswer(qi, oi) {
  userAnswers[qi] = oi;
  updateProgress();
}

function updateProgress() {
  const answered = userAnswers.filter(a => a !== null).length;
  const total = currentQuestions.length;
  document.getElementById('answeredCount').textContent = `${answered}/${total}`;
  document.getElementById('progressFill').style.width = `${(answered / total) * 100}%`;
}

function submitQuiz() {
  const unanswered = userAnswers.filter(a => a === null).length;
  if (unanswered > 0) {
    if (!confirm(`Bạn còn ${unanswered} câu chưa trả lời. Vẫn nộp bài?`)) return;
  }
  showResult();
}

function showResult() {
  let correct = 0;
  currentQuestions.forEach((q, qi) => {
    if (userAnswers[qi] === q.answer) correct++;
  });
  const total = currentQuestions.length;
  document.getElementById('resultTitle').textContent = `Kết quả - Đề ${currentExamIdx + 1}`;
  document.getElementById('scoreNum').textContent = `${correct}/${total}`;
  const pct = Math.round((correct / total) * 100);
  let label = `Đúng ${correct} câu (${pct}%) · `;
  if (pct >= 90) label += '🌟 Xuất sắc!';
  else if (pct >= 75) label += '👍 Giỏi!';
  else if (pct >= 50) label += '🙂 Khá';
  else label += '💪 Cố gắng thêm';
  document.getElementById('scoreLabel').textContent = label;

  const review = document.getElementById('reviewContainer');
  review.innerHTML = '';
  const letters = ['A', 'B', 'C', 'D'];
  currentQuestions.forEach((q, qi) => {
    const div = document.createElement('div');
    div.className = 'question reviewed';
    let optHtml = '';
    q.options.forEach((opt, oi) => {
      let cls = '';
      if (oi === q.answer) cls = 'correct';
      else if (oi === userAnswers[qi]) cls = 'incorrect';
      optHtml += `<li><label class="${cls}">
        <span><span class="opt-letter">${letters[oi]}.</span>${escapeHtml(opt)}</span>
      </label></li>`;
    });
    const userPick = userAnswers[qi] === null ? '(chưa trả lời)' : letters[userAnswers[qi]];
    const status = userAnswers[qi] === q.answer ? '✓ Đúng' : '✗ Sai';
    const statusColor = userAnswers[qi] === q.answer ? '#2e9c4d' : '#c93a3a';
    div.innerHTML = `
      <div class="q-text"><span class="q-num">Câu ${qi + 1}.</span>${escapeHtml(q.text)}</div>
      <ul class="options">${optHtml}</ul>
      <div class="answer-info">
        Bạn chọn: <b>${userPick}</b> · Đáp án đúng: <b>${letters[q.answer]}</b> ·
        <span style="color:${statusColor};font-weight:600;">${status}</span>
      </div>
    `;
    review.appendChild(div);
  });
  show('screen-result');
}

function goHome() { show('screen-home'); }
function retryExam() { startExam(currentExamIdx); }

// Init
buildExams();
renderHome();
show('screen-home');
</script>
</body>
</html>
"""

html = html.replace("__QUESTIONS_JSON__", questions_json)

with open("trac_nghiem.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"Generated trac_nghiem.html ({len(html):,} bytes)")

console.log('SCRIPT LOADED ONCE');

let tasksList = [];

// Update counter
function updateTaskCount() {
  const countSpan = document.getElementById('task-count');
  countSpan.textContent = tasksList.length;
}

// Add task from form
document.getElementById('add-task-btn').addEventListener('click', () => {
  const title = document.getElementById('title').value.trim();
  const due_date = document.getElementById('due_date').value.trim();
  const estimated_hours =
    parseFloat(document.getElementById('estimated_hours').value) || 1;
  const importance =
    parseInt(document.getElementById('importance').value) || 5;

  if (!title) {
    alert('Title is required');
    return;
  }

  const task = { title, due_date, estimated_hours, importance, dependencies: [] };
  tasksList.push(task);
  updateTaskCount();

  document.getElementById('title').value = '';
  document.getElementById('due_date').value = '';
  document.getElementById('estimated_hours').value = '1';
  document.getElementById('importance').value = '5';
});

// Analyze button
document.getElementById('analyze-btn').addEventListener('click', (event) => {
  event.preventDefault();
  console.log('Analyze button clicked');

  const statusEl = document.getElementById('status');
  const strategy = document.getElementById('strategy').value;

  let payload = [];
  const jsonText = document.getElementById('json-input').value.trim();

  if (jsonText) {
    try {
      payload = JSON.parse(jsonText);
    } catch (e) {
      alert('Invalid JSON');
      console.error('JSON parse error:', e);
      return;
    }
  } else {
    payload = tasksList;
  }

  if (!Array.isArray(payload) || payload.length === 0) {
    alert('Please add at least one task');
    return;
  }

  statusEl.textContent = 'Analyzing...';
  console.log('About to call fetch with payload:', payload, 'strategy:', strategy);

  fetch(`http://127.0.0.1:8000/api/tasks/analyze/?strategy=${strategy}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
    .then((response) => {
      console.log('Fetch response status:', response.status);
      return response.text();                     // get raw text
    })
    .then((text) => {
      console.log('Raw response text:', text);    // see exactly what backend sent
      statusEl.textContent = 'Done';
      let data;
      try {
        data = JSON.parse(text);
      } catch (e) {
        console.error('JSON parse error on response:', e);
        return;
      }
      renderResults(data);
    })
    .catch((err) => {
      console.error('Fetch error:', err);
      statusEl.textContent = 'Error calling API';
    });
});

// Render results
function renderResults(tasks) {
  const container = document.getElementById('results');
  container.innerHTML = '';

  if (!Array.isArray(tasks) || tasks.length === 0) {
    container.innerHTML = '<p>No tasks returned from API.</p>';
    return;
  }

  tasks.forEach((t) => {
    const score = t.score != null ? t.score.toFixed(2) : 'N/A';
    const div = document.createElement('div');
    div.className = 'task-card';

    div.innerHTML = `
      <h3>${t.title}</h3>
      <p>Due: ${t.due_date || 'None'}</p>
      <p>Estimated hours: ${t.estimated_hours}</p>
      <p>Importance: ${t.importance}</p>
      <p>Score: ${score}</p>
      <p>${t.explanation || ''}</p>
    `;

    container.appendChild(div);
  });
  // Prevent Enter key from submitting/reloading the page
document.addEventListener('keydown', (event) => {
  if (event.key === 'Enter') {
    event.preventDefault();
  }
});

}

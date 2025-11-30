# Smart Task Analyzer

Smart Task Analyzer - A Django and Vanilla JS app to score and sort tasks by importance, deadline, and time required.

## Setup Instructions

### Prerequisites

- Python version  
- pip  
- Git  

### Directions

1. `git clone <your-repo-url>`  
2. `cd` into repo  
3. `python -m venv venv`  
4. `venv\Scripts\activate` (Windows)  
5. `pip install -r requirements.txt`  
6. `cd backend`  
7. `python manage.py migrate`  
8. `python manage.py runserver`  

Open `frontend/index.html` in a browser directly (just double-click) and make sure `script.js` is pointing to: `http://127.0.0.1:8000`.

## Algorithm Explanation 

Explain in everyday terms:

Inputs: `title`, `due_date`, `estimated_hours`, `importance`, `dependencies`, `strategy`.

Base score:

Begin with importance, on a scale of 1–10.

Convert `due_date` to "days remaining" and transform into urgency score - for example, tasks due today or tomorrow get a big bonus, far tasks get smaller bonus.

Adjust for `estimated_hours` - short tasks get slight boost for “Fastest Wins”, long tasks maybe reduced.

Strategies:

- `smart_balance`: mix of importance + urgency + effort.  
- `fastest`: more weight on low `estimated_hours`.  
- `high_impact`: Give more weight to importance.  
- `deadline`: more weight on days until `due_date`.  

Mention normalization - e.g. dividing or clamping to a max, and how you sort tasks descending by score.

Add one or two short example scenarios, e.g., "a small but urgent bug vs a big documentation task next week".

---

## Design Decisions

Brief bullets:

- Why Django? (familiar, fast setup, built-in admin, etc.)  
- Why a simple JSON endpoint instead of a complex frontend framework?  
- Scoring is transparent and simple instead of ML: easier to debug, predictable.  
- Why separate the scoring code into its own module (testable, reusable).  

---

## Time Breakdown

Estimate hours, for example:

- Backend + API: X hours.  
- Scoring Algorithm Thinking + Implementation: Y hours.  
- Front-end UI (HTML/CSS/JS): Z hours.  
- Writing tests: A hours.  
- README + cleanup: B hours.  

---

## Bonus Challenges

- Various strategies:  
- Explanations per task.  
- 3D or glass UI, etc.  

## Future Improvements

Ideas like the

- User accounts and saving of task lists.  
- More sophisticated scoring: calendar availability, energy levels.  
- Drag-and-drop reordering.  
- Better mobile layout.  
- Using a frontend framework later.  


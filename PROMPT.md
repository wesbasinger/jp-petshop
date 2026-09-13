# Specification: Exotic Pet Shop Math & Finance Simulation

## 1. Overview & Vision
Develop a text-based Python business simulation designed for a high school senior learning advanced math (Precalculus/Algebra II review) and practical financial literacy. The student acts as the owner/operator of a virtual specialty pet business ("Herp & Rodent Haven").

**Core Principle:** The simulation is an interactive math sandbox. The backend presents weekly operational reports, business decisions, and qualitative reflection questions. The student calculates figures in a physical paper ledger, reads accompanying Markdown documentation, and inputs answers into the program to execute actions.

---

## 2. Architectural Guidelines & Admin/Demo Mode
- **Decoupled Architecture:** Core logic (Math Engine, State Manager, Event Engine) is completely separate from the UI layer (Local CLI, Streamlit, or PyInstaller executable).
- **Admin & Demo Mode:** 
  - Executing `python main.py --demo` or `--admin` opens an Instructor Console.
  - Allows the instructor to preview any week’s tasks, review accompanying documentation, simulate student entries, and manually unlock or adjust parameters without corrupting the student's active `game_state.json`.
- **Source Privacy:** Math formulas, secret event probabilities, and validation rules are stored in compiled/backend modules so the student cannot inspect answers directly.

### Interaction Trust Levels
- **Review Mode:** Students may use field guides, hints, retries, and AI assistance. Review responses are practice artifacts and do not count as verified assessment evidence.
- **Supervised Assessment Mode:** An instructor creates a one-time unlock code and shares it with the student during an in-person session. The assessment provides no hints or correctness feedback and records a separate assessment artifact. Official module progression may require a passing supervised assessment.
- **Instructor Mode:** The instructor can preview lessons, create assessment sessions, inspect artifacts, and adjust parameters without changing the student's active state.
- Software cannot prove that a student used no outside help. Supervised mode is an auditable protocol that depends on the instructor being physically present.

---

## 3. Module Gating & Dynamic Difficulty Tuning
- **Sequential Module Locking:** Modules and advanced financial mechanics (e.g., taxes, quadratic pricing optimization, population dynamics) remain locked until explicitly unlocked in `game_state.json` or toggled via Admin Mode.
- **Adjustable Weekly Difficulty:** Includes configurable difficulty parameters in `game_state.json` (e.g., `math_complexity_level: 1-5`, `market_volatility: low|med|high`, `penalty_multiplier`). The instructor can scale these week-to-week based on student progress.

---

## 4. Lesson Documentation & Field Guides (Markdown)
- **Companion Guides:** Every weekly lesson links to a dedicated Markdown file stored in the `docs/` folder (e.g., `docs/week_03_guide.md`).
- **Content:** These guides serve as the student's reference textbook, containing math formula reference sheets, financial literacy definitions, market trend analysis, and exotic animal husbandry guidelines required to solve that week's tasks.

---

## 5. Multi-Threaded Weekly Turn Structure
Turns are **non-blocking** and contain 4–5 parallel tasks across different categories:

### A. Operations & Rapid Review Thread (Easy Math)
- *Purpose:* Warm-up calculations (fractions, basic percentages, simple unit conversions).
- *Mechanic:* Non-blocking. Errors cause minor operational inefficiencies (e.g., $10 wasted feed fee) rather than halting execution.

### B. Financial & Debt Management Thread (Core Finance)
- *Purpose:* Practical financial literacy (compound interest, debt-to-income ratios, cash flow auditing).
- *Examples:* Calculating loan interest A = P(1 + r/n)^(nt), choosing loan refinancing offers, balancing profit & loss statements.

### C. Biological & Growth Modeling Thread (Algebra II / Precalculus)
- *Purpose:* Advanced applied mathematics.
- *Examples:* Modeling feeder insect/rodent population growth P(t) = P_0 * e^(rt), calculating enclosure capacity constraints.

### D. Dynamic Market & Risk Thread (Optimization & Probability)
- *Purpose:* Strategic decision-making and expected value.
- *Examples:* Quadratic vertex pricing optimization, expected value E(X) for emergency vet care insurance.

### E. Qualitative Reflection & Strategy Thread (Artifact Generation)
- *Purpose:* Assess critical thinking and business rationale.
- *Mechanic:* The game prompts open-ended questions (e.g., "Why did you choose Loan Option A over Option B given current inflation?").
- *Artifact Output:* Student text entries are saved directly as raw text/JSON artifacts in the `artifacts/` folder (e.g., `artifacts/week_03_student_reflection.json`). These files are structured specifically for an AI coding agent (like Claude Code) to analyze and generate recommendations for the next lesson.

---

## 6. Incentive & Milestone System
- **Reputation Points:** Earned through accurate math entries and thorough qualitative responses.
- **Pet Collection Unlocks:** Reaching financial stability metrics and point thresholds unlocks the ability to acquire new exotic pets for his personal collection inside the simulation (e.g., rare morph pythons, poison dart frogs, tarantulas).

---

## 7. Technical Specifications & File Structure

herp_and_rodent_haven/
├── main.py                    # Entry point (supports --demo and --admin flags)
├── data/
│   └── game_state.json        # State persistence (cash, inventory, locked modules, difficulty settings)
├── docs/                      # Student Markdown field guides
│   ├── week_01_guide.md
│   └── week_02_guide.md
├── artifacts/                 # Saved student qualitative responses for AI analysis
│   ├── review/                # Practice responses and reflections
│   └── assessments/           # One-time, supervised assessment records
├── engine/
│   ├── __init__.py
│   ├── state.py               # Handles game_state.json read/write & difficulty tuning
│   ├── math_engine.py         # Verification logic for student inputs
│   ├── events.py              # Random event generator
│   └── admin.py               # Demo mode & lesson preview utilities

---

## 8. Sample CLI Turn Workflow
1. **Dashboard & Field Guide Prompt:** Displays cash balance, active debt, unlocked modules, and prompts the student to read `docs/week_XX_guide.md`.
2. **Weekly Task Selection:** Displays 4–5 actionable tasks across operations, finance, math modeling, and qualitative reflection.
3. **Student Input Phase:** Student submits numerical answers and typed qualitative reflections.
4. **Artifact Generation:** Qualitative answers are exported to `artifacts/`.
5. **Validation & Feedback:** Numerical answers are checked against `math_engine.py`. Correct answers award reputation points and cash; errors generate hint prompts and minor penalties.
6. **State Persistence:** `game_state.json` updates automatically.

### Assessment Boundary
- Review artifacts and supervised assessment artifacts must remain separate.
- Assessment unlock codes are one-time credentials created by Instructor Mode and stored only as hashes in local runtime state.
- A passing supervised assessment can unlock official progression; review activity cannot.

## 9. Future UI & Deployment Notes
- Keep the CLI as a reliable development and fallback interface while the engine stabilizes.
- A desktop-oriented wrapper should replace command flags with a clear mode menu: Review, Supervised Assessment, and Instructor Console.
- Use comfortable spacing, larger readable text, and clear dashboard panels so a student can scan cash, debt, reputation, active week, and available actions without feeling crowded.
- Add restrained progress feedback when moving between tasks, such as a brief dot-advancing or step-progress animation. Motion should communicate state changes, not delay the learner.
- Make the supervised assessment screen visually distinct from review mode, with an explicit instructor-present status and no accidental hints or answer feedback.
- Preserve the same engine APIs and artifact boundaries beneath any desktop, Streamlit, or future web UI.
- Deployment planning should include local-first operation, a reset/demo profile, backup and export of assessment artifacts, and protection of active student state from instructor previews.
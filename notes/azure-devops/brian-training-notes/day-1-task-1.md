#### **A) Create a Burndown Chart**

**How to do it:**

1. Navigate to **Boards** > **Sprints**.
2. Click the **Analytics** tab at the top center (next to "Taskboard").
3. *Note: If the chart is flat/empty, it’s because the sprint hasn't started or has no tasks. That is normal for a sandbox.*

**What to say (The Script):**

* "In Azure DevOps, I don't need to manually build a Burndown chart. It is natively integrated into the Sprint view."
* "I use the **Analytics** tab here to track our 'Remaining Work' daily. This helps me spot scope creep or stalled tasks early in the sprint."

---

#### **B) Create a Chart of Accepted vs. Completed (Past X Months)**

**How to do it:**

1. Navigate to **Overview** > **Dashboards**.
2. Click **Edit** and drag the **Velocity** widget onto the canvas.
3. **Crucial Configuration:**
* **Title:** Rename to "Accepted vs Completed" (Matches the client's request exactly).
* **Iterations:** Set to **6** (Shows roughly the last 3 months).
* **"Display planned work":** Check this box. (This creates the "Accepted" bar).



**What to say (The Script):**

* "I created this custom dashboard widget to track our delivery reliability."
* "The **Light Blue bar** shows 'Planned Work'—which represents what we **Accepted** during Sprint Planning."
* "The **Green bar** shows what we actually **Completed**."
* "Comparing these two over the last 6 sprints helps me calculate our 'Say/Do' ratio."

---

#### **C) How to Create a Product & Sprint Backlog**

**How to do it:**

1. Navigate to **Boards** > **Backlogs**.
2. **Product Backlog:** Use the input bar at the very top (`+ New Work Item`) to type user stories. This list is your Product Backlog.
3. **Sprint Backlog:**
* Click **View Options** (top right icon) -> Toggle **Planning** to "On".
* **Drag and drop** stories from the center list into the **Sprint 1** box on the right sidebar.



**What to say (The Script):**

* "I manage the **Product Backlog** here in the center view, keeping high-priority items at the top."
* "For **Sprint Planning**, I prefer using the **Planning Pane** (the side view). It allows me to simply drag items from the backlog directly into the upcoming Sprint."
* "Once the item is in the Sprint, I decompose it into **Tasks** so the developers can track hours against it."

---

**Final Pro-Tip for Brian:**
If they ask why he renamed the Velocity chart, tell him to say: *"The standard widget is called Velocity, but since you specifically asked for 'Accepted vs Completed,' I renamed it to ensure the report is clear for stakeholders who might not know Agile terminology."*

## **Generating Columns (Sprint View)**

**The Question:**
"Generate the columns (for a given sprint): a) ID, b) User Story Name, c) Status/Swimlane, d) If Blocked."

**The Core Concept:**
The interviewer wants to see if you can customize the **Sprint Backlog** list view to show "hidden" data. By default, Azure DevOps only shows basic info (Order, Title, State). You must use **Column Options** to reveal the specific fields they asked for.

**The "Translation" (The Secret Key):**
You need to map their "human" words to the actual **Azure DevOps Field Names**:

* "ID" = **ID**
* "User Story Name" = **Title**
* "Status / Swimlane" = **Board Lane** *(This is the critical one—it shows if an item is in the 'Expedite' or 'Standard' swimlane).*
* "If Blocked" = **Tags** *(There is no standard "Blocked" column. In ADO, you flag items as blocked using Tags, so adding the Tags column is the correct answer).*

**The "How-To" Steps:**

1. Navigate to **Boards** > **Sprints**.
2. Make sure you are on the **Backlog** tab (list view), not the Taskboard.
3. Click the **Column Options** icon (looks like a small spreadsheet with a gear, usually on the far right).
4. In the pop-up, click **+ Add Column** for each field:
* Search/Select **ID**.
* Search/Select **Title**.
* Search/Select **Board Lane**.
* Search/Select **Tags**.


5. Click **OK**.

**The Interview Script (What to Say):**

> "To generate this specific report, I go to the Sprint Backlog and open **Column Options**.
> I add the **'Board Lane'** column to track exactly which Swimlane a story is sitting in.
> For tracking Blockers, I add the **'Tags'** column. Since we handle 'Blocked' as a tag in our process, this view gives me a complete status update at a glance."

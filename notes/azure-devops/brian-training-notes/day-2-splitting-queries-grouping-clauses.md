### **Use Case 1: Splitting Queries (Grouping Clauses)**

**The Question:** "How and why do you split queries into chunks?"

**The Core Concept:**
This is officially called **Grouping Clauses**. It is necessary whenever you mix **AND** and **OR** logic in a single query. Without it, Azure DevOps processes rules from top-to-bottom, often leading to incorrect results due to order-of-operations errors.

**The Scenario (The Proof):**

* **Goal:** I want to see all **Active** items for **either** "Habib" **OR** "Jahangir".
* **Without Grouping (The Failure):** The system interprets it as:
1. Find "Active" items for Habib.
2. **OR** find *everything* for Jahangir (ignoring the "Active" status).


* *Result:* You get "Closed" and "New" items for the second person, which is wrong.


* **With Grouping (The Success):** By grouping the two users with brackets `( )`, I force the system to apply the "Active" rule to **both** of them.

**The "How-To" Steps:**

1. Add your filters (e.g., `State = Active`, `Assigned To = Habib`, `OR Assigned To = Jahangir`).
2. Hold **Shift** or **Ctrl** to select the two user rows (the ones with OR logic).
3. **Right-click** on the far left of the selected rows.
4. Select **Group Clauses**.
* *Visual Check:* Look for the brackets `( )` wrapping those lines.



**The Interview Script (What to Say):**

> "I split—or group—queries specifically when I am dealing with **Mixed Logic**.
> For example, if I need to find 'Active' work for two different team members, I have to **Group** the users together with brackets. If I don't, the 'Active' filter gets ignored for the second person. Grouping ensures the main criteria apply to everyone equally."

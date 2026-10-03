### **Query Folder Structure (The Library)**


**The Question:**
"Figure out where in the library structure to point your query?"

**The Core Concept:**
Azure DevOps has a strict folder structure for queries. You cannot just "save" a query anywhere; you have to "point" it to the right folder based on who needs to see it.

1. **My Queries:** Only **YOU** can see these.
2. **Shared Queries:** The **WHOLE TEAM** can see these.

**The "Gotcha" (Why they ask this):**
This is a trap question. If you build a Dashboard Widget (like a velocity chart) using a query saved in **"My Queries,"** it will work perfectly for *you*, but when your manager looks at the dashboard, they will see an error message ("Widget Failed to Load") because they don't have permission to read your private folder.

**The "How-To" Steps:**

1. Open your query and click **Save As**.
2. Look at the **Folder** dropdown.
3. **"Point" it:** You must manually click/select the **Shared Queries** folder.
4. Hit OK.

**The Interview Script (What to Say):**

> "When I save a query, I have to be careful about where I 'point' it in the library structure.
> If I am just testing something out, I save it to **My Queries** so I don't clutter the shared space.
> However, if this query is going to be used on a **Team Dashboard** or shared with a stakeholder, I make sure to point it to the **Shared Queries** folder. If I don't, the dashboard widget will show an error for everyone else because they don't have permission to read my private folder."

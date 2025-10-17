# 📝 Developer Log
This document tracks the development journey of the project which is meant for self-reflection.

## 2025-10-01~03 | Framework

### 1. Why I Decided to Develop a Tool for Juxtaposing Two Languages?

It aims to improve the efficiency of my daily tasks on translation since I have been working on it for more than 7 years (as of this writing); a gut feeling tells me "Time to convert my efforts into something more specific — or more financially rewarding :）" since this *** work drained too much of my time and energy. So I need a program to make things easier and more comfortable (at least for my mental health).

### 2. Basic Functionality
Now then, there are plenty of rountine tasks as to how to standardise your translations and define the presence of a variety of phrases and expressions — an artistic equivalence to mathematics in STEM, I would say, why I've been asking for all of this?  Um, basically, it's part of my research and furthermore at its core & hub, however, which doesn't matter at all in this log — an odd fish in an odd barrel — Good. Allow me try to give an intro about fundamental functionality I need.

#### 2.1 Import
Due to time-cost considerations, two approaches are currently envisioned for the import function:
(a) inputting translated clauses one by one after daily translation work (the most common scenario), and

<img src="PIC1_Add_Entry.png" alt="alt text" style="width:75%; height:auto;" />

(b) bulk injection. The latter is still under consideration, with the idea being that entire passages (especially those translated in the past) could be injected into the database based on a standard sentence-ending delimiter such as a period.

<img src="PIC2_Bulk_Import.png" alt="alt text" style="width:75%; height:auto;" />


#### 2.2 Search
This is the second-highest development priority after import. Search must include both source and target languages so that Chinese–English and English–Chinese comparisons can be carried out separately. Another key challenge under ongoing testing is how best to optimize the retrieved results.

Ideally, search results are expected to include the original source of the text, allow keyword-based text location, and record the injection time. If possible, a filter function is expected to be added later to retrieve text based on criteria such as day/month, combined with other filter conditions. Here's a sketch program built on streamlit:

<img src="PIC3_Search_Export.png" alt="alt text" style="width:75%; height:auto;" />

#### 2.3 Basic Tree
This is a concept that can basically cover my daily workflow in translation.
```bash
translation-notes/
├─ DEV_LOG.md
├─ Home.py
├─ pages/
│   ├─ 1_Add_Entry.py
│   ├─ 2_Bulk_Import.py
│   └─ 3_Search_Export.py
```

### 3. Demonstration
The figure below shows what's happening using the `Go` tab. You can assume that I've added one entry already for test.

<img src="PIC4_Demonstration.png" alt="alt text" style="width:75%; height:auto;" />

As you can see, also a convenient copy-paste button available there.

### 4. Future Plans
The immediate priority is to optimize the retrieved search results. Import has been progressing relatively smoothly so far, and the plan is to add time-based filtering functionality. Most importantly, I will need to inject a large volume of content in order to properly test the robustness and practicality of the software.

# **Requirements & Issues Overview**  
**Reference Period:** 2025-10-04 → 2025-10-14  
**Context:** Functional refinement and feature restructuring of the Translation Retriever System.

---

# **Requirements & Issues Overview**  
**Reference Period:** 2025-10-04 → 2025-10-13  
**Context:** Functional refinement and feature restructuring of the Translation Retriever System.

---

## **1 · UI / UX Refinement Requests**

### **Module 1 · 📝 Add Entry**  
**Status:** ✅ Complete  
**Summary:**  Remove this module since its function duplicates `Batch Insert`.

---

### **Module 2 · 📚 Insert**  
**Status:** ✅ Complete  
**Summary:**   Allow the "source name" to be **searchable and selectable** from previously recorded entries (sorted alphabetically and numerically). Enable **unified renaming** of existing sources within the same `.py` file.  

---

### **Module 3 · 🏡 Home Admin + 🛠️ Bulk Edit**  
**Status:** ✅ Complete  
**Summary:**   Merge both into a **single management interface** as a single `Home Admin`.

---

### **Module 4 · 🏡 Home Admin**  
**Status:** ✅ Complete  
**Summary:**   Default all editing actions to **auto-save**.  

---

### **Module 5 · 📚 Insert**  
**Status:** ✅ Complete  
**Summary:**    Default "direction" set to **EN→ZH**, with “no split” as priority.  **Auto-save**.  

---

### **Module 6 · 📑 From Page**  
**Status:** ✅ Complete  
**Summary:**    Develop a dedicated `.py` file for article-level viewing, meeting the following requirements:  
   - Each **article** = one **source**.  
   - After entering a source name, display all related sentences in the order they were added.
   - Allow **insertion of new sentences (with unique IDs)** between existing ones.  
   - <font color="C00000">From now on, we'll have demo! See them below!</font>

**See details:** 👇 gif + video 
<font color="C00000">(This is a post-recorded video for test — even after the Module 7..8 and 9)</font>
<details><summary>▶ CLICKME!</summary>
<a href="assets/static/media/gif/From_Page.gif" target="_blank">
<img src="assets/static/media/gif/From_Page.gif" width="480" loading="lazy" alt="Insert First Demo">
</a><br>
<a href="assets/static/media/video/From_Page.mp4" target="_blank"><b>🎬 Watch full demo video</b></a>
</details>


---

### **Module 7 · 📑 From Page**  
**Status:** ✅ <font color="C00000">Complete → But Immediate Disposal ❌ See why below</font>
**Summary:**       
   - Keep the selection bar **floating and visible while scrolling**. 
  <font color="C00000">(This feature is conflicted with Streamlit built-in functions. It would be possible only if the system can be switched to a "full-stack" mode ❌)</font>
   - Add a **shortcut key** to quickly trigger `Insert` without scrolling to the bottom.
  <font color="C00000">(It fails as well, the reason is the same as above❌)</font>
   - Move the toolbar (shown in the screenshot) to the **left side**, make it collapsible for cleaner layout.

**See details:** 👇 screenshot
<details><summary>▶ CLICKME!</summary>
<img src="assets/static/media/img/Module_7.png" alt="_blank" width="400">
</details>

---

### **Module 8 · 📑 From Page**  
**Status:** ✅ Complete 
**Summary:**       
   - As it is quite hard with the feature in Module 7, then we:
   - Relocate the *choose* selector near the article title (“sentences for …”) as shown in the second screenshot.  
   - Each sentence should have a small **“Edit” button**, which, when clicked, expands hidden controls for editing metadata (source, date, origin, etc.).  
   - These edit options remain invisible by default until “Edit” is clicked.

**See details:** 👇 screenshot
<details><summary>▶ CLICKME!</summary>
<img src="assets/static/media/img/Module_8.png" alt="_blank" width="800">
</details>

---

### **Module 9 · 🔍 Search + 🛠️ Bulk Edit**
**Status:** ✅ Complete 
**Summary:**  Merge into `Home Admin` for unified management. 

**See details:** 👇 two screenshots
<details><summary>▶ CLICKME!</summary>
<img src="assets/static/media/img/Module_9_1.png" alt="_blank" width="800">
<img src="assets/static/media/img/Module_9_2.png" alt="_blank" width="800">
</details>

---

### **Module 10 · 📚 Insert**
**Status:** ✅ Complete 
**Summary:**  
- Implement an **error rejection mechanism** to detect incorrect bilingual input (EN/CH mismatch). 
- 🧪 Detect **bilingual direction** and has a switch and modifiable parameters.
- Redesign the interface to a **compact floating panel**, similar to the new `Home Admin` layout.  

**See details:** 👇 screenshot
<details><summary>▶ CLICKME!</summary>
<img src="assets/static/media/img/Module_10.png" alt="_blank" width="800">
</details>

---

### **Module 11 · 📑 Home Admin**
**Status:** ✅ Complete 
**Summary:**  Add a **time-filtered deletion feature** for batch removal of erroneous imports, accurate to the second.  

**See details:** 👇 screenshot
<details><summary>▶ CLICKME!</summary>
<img src="assets/static/media/img/Module_11.png" alt="_blank" width="800">
</details>

---

### **Module 12 · 📑 Home Admin**
**Status:** ✅ Complete 
**Summary:**  Enable **inline editing** of previewed matches (same as `Add Entry` being merged).  

**See details:** 👇 screenshot
<details><summary>▶ CLICKME!</summary>
<img src="assets/static/media/img/Module_12.png" alt="_blank" width="800">
</details>

---

### **Module 13 · 📑 Home Admin**
**Status:** ✅ Complete
**Summary:**  
- Reinstate **source-based filtering** in search. The source field should allow both **selection and manual input**.
- Implement 🛠️ **Bulk Replace** for unified source modification.

**See details:** 👇 screenshot
<details><summary>▶ CLICKME!</summary>
<img src="assets/static/media/img/Module_13.png" alt="_blank" width="800">
</details>

---

### **Module 14 · 📚 Insert**
**Status:** ❌ Failed
**Summary:**  `.jpg` files (e.g., `smile.jpg`🙂) cannot be parsed because current regex logic splits on periods — adopt an ML-based or context-aware tokenization model. 
 <font color="C00000">(I am going to add some trained models for bilingual filtering, but that's possible when breaking away from a Streamlit container ❌)</font>

---

### **Module 15 · 📚 Insert**
**Status:** ✅ Complete
**Summary:**  Add support for treating **a blank line as a paragraph break**.

**See details:** 👇 screenshot
<details><summary>▶ CLICKME!</summary>
<img src="assets/static/media/img/Module_15.png" alt="_blank" width="800">
</details>

---

### **Module 16 · 📚 Insert**
**Status:** ✅ Complete
**Summary:**   Ensure ID numbers are visible for each record. 

**See details:** 👇 gif + video 
<details><summary>▶ CLICKME!</summary>
<a href="assets/static/media/gif/ID_Display.gif" target="_blank">
<img src="assets/static/media/gif/ID_Display.gif" width="480" loading="lazy" alt="Insert First Demo">
</a><br>
<a href="assets/static/media/video/ID_Display.mp4" target="_blank"><b>🎬 Watch full demo video</b></a>
</details>

---

### **Module 17 · 📚 Insert + 🏡 Home Admin**
**Status:** ✅ Complete
**Summary:**   Enable **collective bilingual edits** by cloning sentence rows, allowing ID-based replacement (simulating in-place modification since SQL's PK are uniquely identified)

**See details:** 👇 screenshot
<details><summary>▶ CLICKME!</summary>
<img src="assets/static/media/img/Module_15.png" alt="_blank" width="800">
</details>

---

## **2 · System Constraints & Forward Plan**

### **Module 18 · 💼 Toolkit**
**Status:** 🚧 Designing
**Summary:**   Set up a new development toolkit for the translation software (similar to an integrated management system or website management platform that will hold fonts, template, website, and so on...)

---

### **Module 19 · 🌌 All Features**
**Status:** 🚧 Designing
**Summary:**   The database cannot be directly modified and displayed dynamically (equivalent to “no matter how you drag or move things around, the content will still show up,” like the copy button beside the code block in Chat). This feature is currently not supported by Streamlit, so it’s expected to move away from the Streamlit framework and switch to a more formal web mode (higher flexibility).

---

### **Module 20 · 🌌 All Features**
**Status:** 🚧 Designing
**Summary:**   How to input mathematical formulas? Ideally, there should be an equation editing module, and some of the trained models are available online; however, the feature is limited by current framework.

---

### **Module 21 · 🌌 All Features**
**Status:** 🚧 Designing
**Summary:**   How to input mathematical formulas? Ideally, there should be an equation editing module, and some of the trained models are available online; however, the feature is limited by current framework.

---

### **Module 22 · 🌌 All Features**
**Status:** 🚧 Designing
**Summary:**   Add language switching.

---

### **Module 23 · 🌌 All Features**
**Status:** 🚧 Designing
**Summary:**   Design a complete style/theme system and adjust formatting.

---

### **Module 24 · 🌌 All Features**
**Status:** 🚧 Designing
**Summary:**   Set shortcut keys for the software and design the UI for both desktop and web versions.

---

### **Module 25 · 🌌 All Features**
**Status:** 🚧 Designing
**Summary:**   Add animated transitions (currently unsupported in Streamlit).

---

### **Module 25 · 🔮 Index**
**Status:** 🚧 Designing
**Summary:**   Add an initial file index system, involving layout and data migration — this would be an entirely new feature!!!

---

## **3 · Implementation Notes**

- Most of the above enhancements can be implemented directly within existing `.py` modules using modular imports.  
- Some UI functions (floating bar, collapsible sidebar) will require **custom JavaScript injection or Streamlit component extensions**.  
- Batch renaming and inline editing logic should share a unified database trigger system to avoid duplication between `Home Admin` and `Insert`.  

---


# Strict Documentation Specification (Enterprise Standard)

This specification defines the rigorous standards for all documentation within the `智能体` directory. It supersedes all previous guidelines (MDN/Generic Google).

**Status**: Strict Enforcement
**Base Style**: Google Markdown Style (Structure) + Custom Enterprise Visuals (Fonts/Semantics)

---

## 1. Visual Standards (Fonts & Typography)

Since Markdown is a semantic format, visual requirements are enforced via **Embedded CSS** or **Rendering Configuration**. All documents must be compatible with the following rendering logic:

### 1.1 Font Families
*   **Body Text**: Must render in **Microsoft YaHei (微软雅黑)**.
    *   *CSS*: `font-family: "Microsoft YaHei", sans-serif;`
*   **Headings (H1-H6)**: Must render in **SimSun (宋体)** or Serif.
    *   *CSS*: `font-family: "SimSun", serif; font-weight: bold;`

### 1.2 Semantic Styling Mappings
The following Markdown syntax maps strictly to specific visual styles:

| Semantic Type | Markdown Syntax | Visual Requirement |
| :--- | :--- | :--- |
| **Concepts / Terminology** | `**Term**` (Bold) | **Microsoft YaHei Bold** |
| **Notes / Attention** | `_Note text_` (Italic) | *Italicized, Red Color (Optional)* |
| **Inline Code** | `` `code` `` | Consolas / Monaco |

---

## 2. Content Formatting Rules

### 2.1 Concepts & Definitions
*   **Rule**: ALL key concepts, definitions, and technical terms must be **Bold** upon their first appearance in a section.
    *   *Correct*: The **Data Governance** framework...
    *   *Incorrect*: The Data Governance framework...

### 2.2 Notes & Warnings
*   **Rule**: Any content implying "Note", "Attention", "Warning", or "Caution" must be wrapped in italics `_..._`.
    *   *Correct*: _Note: This operation is irreversible._
*   **Admonitions**: For longer blocks, use the GitHub Alert syntax, but the internal text should still respect the font rules.
    ```markdown
    > [!NOTE]
    > _Ensure the server is offline before proceeding._
    ```

### 2.3 Headings (Strict ATX)
*   **Syntax**: `# Heading`. Setext (`---`) is harmlessly forbidden.
*   **Font**: Headers serves as the visual anchor. They must use the **Songti** font family guidline.

### 2.4 Lists (Google Style Strict)
*   **Indentation**: Nested lists MUST use **4-space indentation**.
    ```markdown
    1. Level 1
        *   Level 2 (4 spaces)
    ```

---

## 3. Implementation Guide for Agents

When generating documents, you generally do not need to write CSS, but you **MUST** apply the Markdown syntax that triggers these styles:

1.  **Identify Concepts**: Ask yourself, "Is this a key term?" -> **Bold it**.
2.  **Identify Notices**: Ask yourself, "Is this a note?" -> _Italicize it_.
3.  **Strict Structure**: Ensure H1/H2/H3 hierarchy is logical and valid.

### 3.1 CSS Template (For visual verification)
If a user requests a "Web Preview" version, prepend this block:
```html
<style>
body { font-family: "Microsoft YaHei", sans-serif; }
h1, h2, h3, h4, h5, h6 { font-family: "SimSun", serif; }
strong { font-weight: 700; color: #000; }
em { font-style: italic; color: #555; }
</style>
```

---

## 4. File Management
*   **Naming**: `kebab-case.md` (e.g., `data-security.md`).
*   **Path**: Store in appropriate subdirectories.

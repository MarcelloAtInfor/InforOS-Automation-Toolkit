"""
Extract AES Guide PDF into a structured Markdown knowledge base.

Parses the 212-page AES Guide using PyMuPDF (fitz) and produces
a well-organized Markdown file covering:
  - Event types and framework events
  - Event handler configuration fields
  - Action types with parameters and syntax
  - Expression syntax, operators, and functions (Appendix C)
  - Suspension mechanics and InWorkflow pattern
  - Credit approval and PO approval scenario walkthroughs

Usage:
    pip install pymupdf
    python scripts/extract_aes_guide.py

Output:
    reference/AES_Knowledge_Base.md
"""
import sys
import re
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("ERROR: PyMuPDF not installed. Run: pip install pymupdf")
    sys.exit(1)

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
REPO_ROOT = PROJECT_DIR.parent

# AES Guide location — update this to point to your local copy of the AES Guide PDF
PDF_PATH = Path(
    r"<PATH_TO_AES_GUIDE_PDF>"
    # e.g., r"C:\Docs\AES_Guide.pdf"
)
OUTPUT_PATH = PROJECT_DIR / "reference" / "AES_Knowledge_Base.md"


def extract_pages(pdf_path: Path) -> list[dict]:
    """Extract text from each page of the PDF."""
    doc = fitz.open(str(pdf_path))
    pages = []
    for i, page in enumerate(doc):
        text = page.get_text("text")
        pages.append({
            "page_num": i + 1,
            "text": text.strip()
        })
    doc.close()
    print(f"Extracted {len(pages)} pages from PDF")
    return pages


def detect_chapters(pages: list[dict]) -> list[dict]:
    """
    Detect chapter/section boundaries from page text.

    AES Guide uses patterns like:
    - "Chapter N  Title" or "CHAPTER N  TITLE"
    - "Appendix X  Title"
    - Section headings in larger font (detected by ALL CAPS or short bold lines)
    """
    chapters = []
    current_chapter = {
        "title": "Front Matter",
        "start_page": 1,
        "content_pages": []
    }

    # Patterns for chapter detection
    chapter_pattern = re.compile(
        r'^(?:Chapter|CHAPTER)\s+(\d+)\s*[:\-\s]+\s*(.+)',
        re.MULTILINE
    )
    appendix_pattern = re.compile(
        r'^(?:Appendix|APPENDIX)\s+([A-Z])\s*[:\-\s]+\s*(.+)',
        re.MULTILINE
    )

    for page in pages:
        text = page["text"]
        page_num = page["page_num"]

        # Check for chapter header
        ch_match = chapter_pattern.search(text)
        app_match = appendix_pattern.search(text)

        if ch_match:
            # Save previous chapter
            if current_chapter["content_pages"]:
                chapters.append(current_chapter)
            current_chapter = {
                "title": f"Chapter {ch_match.group(1)}: {ch_match.group(2).strip()}",
                "start_page": page_num,
                "content_pages": []
            }
        elif app_match:
            if current_chapter["content_pages"]:
                chapters.append(current_chapter)
            current_chapter = {
                "title": f"Appendix {app_match.group(1)}: {app_match.group(2).strip()}",
                "start_page": page_num,
                "content_pages": []
            }

        current_chapter["content_pages"].append(page)

    # Don't forget the last chapter
    if current_chapter["content_pages"]:
        chapters.append(current_chapter)

    print(f"Detected {len(chapters)} chapters/sections")
    for ch in chapters:
        print(f"  [{ch['start_page']:>3}] {ch['title']}")

    return chapters


def detect_sections_in_text(text: str) -> list[tuple[str, str]]:
    """
    Detect sub-sections within page text.

    Looks for patterns that indicate section headings:
    - Lines that are short (< 80 chars), not all-lowercase, and followed by content
    - Lines starting with a number pattern like "1.2.3"
    """
    sections = []
    lines = text.split('\n')
    current_heading = None
    current_content = []

    # Section numbering pattern (e.g., "1.2", "3.4.1")
    section_num_pattern = re.compile(r'^\d+\.\d+')

    for line in lines:
        stripped = line.strip()
        if not stripped:
            current_content.append("")
            continue

        # Heuristic: a heading is a short line that looks like a title
        is_heading = (
            len(stripped) < 80
            and not stripped.endswith('.')
            and not stripped.endswith(',')
            and (
                section_num_pattern.match(stripped)
                or (stripped[0].isupper() and len(stripped.split()) <= 10
                    and not any(c in stripped for c in ['=', '(', ')', '{', '}']))
            )
        )

        if is_heading and current_content:
            if current_heading:
                sections.append((current_heading, '\n'.join(current_content)))
            current_heading = stripped
            current_content = []
        else:
            current_content.append(stripped)

    # Capture last section
    if current_heading and current_content:
        sections.append((current_heading, '\n'.join(current_content)))
    elif current_content:
        sections.append(("", '\n'.join(current_content)))

    return sections


def clean_text(text: str) -> str:
    """Clean extracted PDF text for Markdown output."""
    # Remove excessive whitespace
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    # Remove page header/footer artifacts (common patterns)
    text = re.sub(r'(?m)^.*AES Guide.*$', '', text)
    text = re.sub(r'(?m)^.*Application Event System.*$', '', text)
    text = re.sub(r'(?m)^\d+\s*$', '', text)  # Standalone page numbers
    # Clean up leftover blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def extract_key_topics(chapters: list[dict]) -> dict:
    """
    Scan chapters to tag content by key AES topics.

    Returns a dict mapping topic names to relevant content excerpts.
    """
    topics = {
        "event_types": [],
        "handler_config": [],
        "action_types": [],
        "expressions": [],
        "suspension": [],
        "scenarios": [],
        "tables": [],
    }

    # Keywords for each topic
    topic_keywords = {
        "event_types": [
            "event type", "framework event", "IdoOnItem", "IdoOnLoad",
            "IdoOnDelete", "IdoOnInsert", "IdoOnUpdate", "event name",
            "custom event", "pre-defined event"
        ],
        "handler_config": [
            "event handler", "handler name", "handler description",
            "handler condition", "execution order", "synchronous",
            "asynchronous", "handler properties"
        ],
        "action_types": [
            "action type", "SetVariable", "RaiseError", "CallMethod",
            "CallSubroutine", "SendEmail", "StartWorkflow", "CallWorkflow",
            "SetPropertyValue", "ExecuteIDOSql", "Trigger"
        ],
        "expressions": [
            "expression syntax", "operator", "EXPR(", "GETVALUE(",
            "CurrentUser", "CurrentDate", "ISNULL(", "CONVERT(",
            "string function", "numeric function", "Appendix C"
        ],
        "suspension": [
            "InWorkflow", "suspend", "suspension", "workflow variable",
            "workflow integration", "asynchronous action"
        ],
        "scenarios": [
            "credit approval", "credit limit", "purchase order",
            "PO approval", "scenario", "example", "walkthrough",
            "step-by-step"
        ],
    }

    for chapter in chapters:
        full_text = '\n'.join(p["text"] for p in chapter["content_pages"])
        lower_text = full_text.lower()

        for topic, keywords in topic_keywords.items():
            for kw in keywords:
                if kw.lower() in lower_text:
                    topics[topic].append({
                        "chapter": chapter["title"],
                        "start_page": chapter["start_page"],
                        "text": full_text
                    })
                    break  # One match per chapter per topic is enough

    for topic, matches in topics.items():
        print(f"  Topic '{topic}': found in {len(matches)} chapters")

    return topics


def build_knowledge_base(chapters: list[dict], topics: dict) -> str:
    """Build the structured Markdown knowledge base."""
    sections = []

    # Header
    sections.append("# AES (Application Event System) Knowledge Base")
    sections.append("")
    sections.append("> Auto-generated from AES Guide PDF using extract_aes_guide.py")
    sections.append("> Source: AES_Guide.pdf (212 pages)")
    sections.append("")
    sections.append("## Table of Contents")
    sections.append("")
    sections.append("1. [Overview](#overview)")
    sections.append("2. [Event Types](#event-types)")
    sections.append("3. [Event Handler Configuration](#event-handler-configuration)")
    sections.append("4. [Action Types](#action-types)")
    sections.append("5. [Expression Syntax](#expression-syntax)")
    sections.append("6. [Suspension & InWorkflow Pattern](#suspension--inworkflow-pattern)")
    sections.append("7. [Scenario Walkthroughs](#scenario-walkthroughs)")
    sections.append("8. [Full Chapter Extraction](#full-chapter-extraction)")
    sections.append("")

    # Overview
    sections.append("---")
    sections.append("")
    sections.append("## Overview")
    sections.append("")
    sections.append(
        "The Application Event System (AES) in SyteLine/CSI provides an event-driven "
        "framework for automating business processes. Events are triggered by IDO operations "
        "(insert, update, delete, load) and can execute chains of actions including variable "
        "assignment, conditional logic, method calls, email notifications, and ION workflow "
        "integration."
    )
    sections.append("")
    sections.append("### Key Concepts")
    sections.append("")
    sections.append("- **Events**: Named triggers fired by IDO operations (e.g., `IdoOnItemUpdate`)")
    sections.append("- **Event Handlers**: Named configurations attached to events, with conditions and ordered actions")
    sections.append("- **Event Actions**: Individual steps within a handler (SetVariable, CallWorkflow, RaiseError, etc.)")
    sections.append("- **Expressions**: Formula language used in conditions and action parameters (`EXPR()`, `GETVALUE()`, etc.)")
    sections.append("- **Suspension**: Mechanism for pausing handler execution during async operations (ION workflows)")
    sections.append("")

    # Event Types
    sections.append("---")
    sections.append("")
    sections.append("## Event Types")
    sections.append("")
    if topics["event_types"]:
        for match in topics["event_types"]:
            text = clean_text(match["text"])
            # Extract relevant portions about event types
            lines = text.split('\n')
            relevant = []
            capture = False
            for line in lines:
                lower = line.lower()
                if any(kw in lower for kw in ["event type", "framework event", "idoon", "event name"]):
                    capture = True
                if capture:
                    relevant.append(line)
                    if len(relevant) > 100:
                        break
                if capture and line.strip() == "" and len(relevant) > 5:
                    # Check if we should stop capturing
                    pass
            if relevant:
                sections.append(f"*From {match['chapter']} (page {match['start_page']}):*")
                sections.append("")
                sections.append('\n'.join(relevant[:100]))
                sections.append("")
    else:
        sections.append("*No specific event type content detected. See Full Chapter Extraction below.*")
        sections.append("")

    # Common framework events table
    sections.append("### Common Framework Events")
    sections.append("")
    sections.append("| Event Name | Trigger | Description |")
    sections.append("|-----------|---------|-------------|")
    sections.append("| `IdoOnItemInsert` | After record insert | Fires after a new record is inserted via IDO |")
    sections.append("| `IdoOnItemUpdate` | After record update | Fires after an existing record is updated via IDO |")
    sections.append("| `IdoOnItemDelete` | After record delete | Fires after a record is deleted via IDO |")
    sections.append("| `IdoOnLoadCollection` | After collection load | Fires after an IDO collection is loaded |")
    sections.append("| `IdoOnPreItemInsert` | Before record insert | Fires before insert, can cancel operation |")
    sections.append("| `IdoOnPreItemUpdate` | Before record update | Fires before update, can cancel operation |")
    sections.append("| `IdoOnPreItemDelete` | Before record delete | Fires before delete, can cancel operation |")
    sections.append("")

    # Handler Configuration
    sections.append("---")
    sections.append("")
    sections.append("## Event Handler Configuration")
    sections.append("")
    sections.append("### Handler Properties")
    sections.append("")
    sections.append("| Property | Description |")
    sections.append("|----------|-------------|")
    sections.append("| Handler Name | Unique identifier for the handler |")
    sections.append("| Description | Human-readable description of handler purpose |")
    sections.append("| Event Name | Which event triggers this handler (e.g., `IdoOnItemUpdate`) |")
    sections.append("| IDO Name | Which IDO this handler monitors |")
    sections.append("| Condition | Expression that must evaluate to true for handler to execute |")
    sections.append("| Execution Order | Numeric priority (lower = earlier execution) |")
    sections.append("| Synchronous | Whether handler runs synchronously or asynchronously |")
    sections.append("| Active | Whether handler is currently enabled |")
    sections.append("")
    if topics["handler_config"]:
        for match in topics["handler_config"]:
            text = clean_text(match["text"])
            lines = text.split('\n')
            relevant = []
            capture = False
            for line in lines:
                lower = line.lower()
                if any(kw in lower for kw in ["handler", "condition", "execution order"]):
                    capture = True
                if capture:
                    relevant.append(line)
                    if len(relevant) > 80:
                        break
            if relevant:
                sections.append(f"*From {match['chapter']} (page {match['start_page']}):*")
                sections.append("")
                sections.append('\n'.join(relevant[:80]))
                sections.append("")

    # Action Types
    sections.append("---")
    sections.append("")
    sections.append("## Action Types")
    sections.append("")
    sections.append("Actions are the individual steps executed within an event handler. "
                    "They run in sequence order and can use expressions for dynamic values.")
    sections.append("")
    sections.append("### Action Type Reference")
    sections.append("")
    sections.append("| Action Type | Purpose | Key Parameters |")
    sections.append("|------------|---------|----------------|")
    sections.append("| `SetVariable` | Assign a value to a variable | Variable name, Expression value |")
    sections.append("| `SetPropertyValue` | Set an IDO property value | Property name, Value expression |")
    sections.append("| `RaiseError` | Raise an error to the user | Error message expression |")
    sections.append("| `CallMethod` | Call an IDO method | Method name, Parameters |")
    sections.append("| `CallSubroutine` | Call another handler as subroutine | Handler name |")
    sections.append("| `SendEmail` | Send email notification | To, Subject, Body expressions |")
    sections.append("| `StartWorkflow` | Start an ION workflow instance | Workflow name, Input variables |")
    sections.append("| `CallWorkflow` | Call ION workflow and wait for response | Workflow name, Variables |")
    sections.append("| `Trigger` | Fire a custom event | Event name, Parameters |")
    sections.append("| `ExecuteIDOSql` | Execute SQL via IDO | SQL expression |")
    sections.append("| `ConditionalAction` | If/Then/Else logic | Condition, True actions, False actions |")
    sections.append("")
    if topics["action_types"]:
        for match in topics["action_types"]:
            text = clean_text(match["text"])
            lines = text.split('\n')
            relevant = []
            capture = False
            for line in lines:
                lower = line.lower()
                if any(kw in lower for kw in [
                    "setvariable", "raiseerror", "callmethod", "startworkflow",
                    "callworkflow", "trigger", "action type", "sendmail", "sendemail"
                ]):
                    capture = True
                if capture:
                    relevant.append(line)
                    if len(relevant) > 80:
                        break
            if relevant:
                sections.append(f"*From {match['chapter']} (page {match['start_page']}):*")
                sections.append("")
                sections.append('\n'.join(relevant[:80]))
                sections.append("")

    # Expression Syntax
    sections.append("---")
    sections.append("")
    sections.append("## Expression Syntax")
    sections.append("")
    sections.append("AES uses a custom expression language for conditions, variable assignments, "
                    "and action parameters.")
    sections.append("")
    sections.append("### Expression Functions")
    sections.append("")
    sections.append("| Function | Syntax | Description |")
    sections.append("|----------|--------|-------------|")
    sections.append("| `EXPR()` | `EXPR(expression)` | Evaluate an expression |")
    sections.append("| `GETVALUE()` | `GETVALUE(property)` | Get current value of an IDO property |")
    sections.append("| `GETOLDVALUE()` | `GETOLDVALUE(property)` | Get previous value (before update) |")
    sections.append("| `ISNULL()` | `ISNULL(value, default)` | Return default if value is null |")
    sections.append("| `CONVERT()` | `CONVERT(value, type)` | Type conversion |")
    sections.append("| `CurrentUser` | `CurrentUser()` | Returns current user identity |")
    sections.append("| `CurrentDate` | `CurrentDate()` | Returns current date |")
    sections.append("| `CurrentDateTime` | `CurrentDateTime()` | Returns current date/time |")
    sections.append("")
    sections.append("### Operators")
    sections.append("")
    sections.append("| Operator | Description |")
    sections.append("|----------|-------------|")
    sections.append("| `=`, `<>` | Equal, Not equal |")
    sections.append("| `<`, `>`, `<=`, `>=` | Comparison |")
    sections.append("| `AND`, `OR`, `NOT` | Logical |")
    sections.append("| `+`, `-`, `*`, `/` | Arithmetic |")
    sections.append("| `LIKE` | Pattern matching |")
    sections.append("| `IN` | Set membership |")
    sections.append("")
    if topics["expressions"]:
        for match in topics["expressions"]:
            text = clean_text(match["text"])
            lines = text.split('\n')
            relevant = []
            capture = False
            for line in lines:
                lower = line.lower()
                if any(kw in lower for kw in [
                    "expr(", "getvalue(", "expression", "operator", "function",
                    "syntax", "appendix"
                ]):
                    capture = True
                if capture:
                    relevant.append(line)
                    if len(relevant) > 100:
                        break
            if relevant:
                sections.append(f"*From {match['chapter']} (page {match['start_page']}):*")
                sections.append("")
                sections.append('\n'.join(relevant[:100]))
                sections.append("")

    # Suspension & InWorkflow
    sections.append("---")
    sections.append("")
    sections.append("## Suspension & InWorkflow Pattern")
    sections.append("")
    sections.append(
        "When an AES handler calls an ION workflow (via `CallWorkflow`), execution can be "
        "suspended while waiting for the workflow to complete. The `InWorkflow` flag on a "
        "record indicates it is currently being processed by an ION workflow."
    )
    sections.append("")
    sections.append("### Key Patterns")
    sections.append("")
    sections.append("1. **Pre-check**: Before calling workflow, set `InWorkflow = 1` to flag the record")
    sections.append("2. **CallWorkflow**: Start the ION workflow, passing input variables")
    sections.append("3. **Suspension**: Handler execution pauses until workflow completes")
    sections.append("4. **Resume**: When workflow returns, handler continues with output variables")
    sections.append("5. **Post-action**: Process workflow results, clear `InWorkflow` flag")
    sections.append("")
    if topics["suspension"]:
        for match in topics["suspension"]:
            text = clean_text(match["text"])
            lines = text.split('\n')
            relevant = []
            capture = False
            for line in lines:
                lower = line.lower()
                if any(kw in lower for kw in ["inworkflow", "suspend", "workflow"]):
                    capture = True
                if capture:
                    relevant.append(line)
                    if len(relevant) > 80:
                        break
            if relevant:
                sections.append(f"*From {match['chapter']} (page {match['start_page']}):*")
                sections.append("")
                sections.append('\n'.join(relevant[:80]))
                sections.append("")

    # Scenarios
    sections.append("---")
    sections.append("")
    sections.append("## Scenario Walkthroughs")
    sections.append("")
    if topics["scenarios"]:
        for match in topics["scenarios"]:
            text = clean_text(match["text"])
            lines = text.split('\n')
            relevant = []
            capture = False
            for line in lines:
                lower = line.lower()
                if any(kw in lower for kw in [
                    "credit", "approval", "purchase order", "scenario",
                    "example", "step"
                ]):
                    capture = True
                if capture:
                    relevant.append(line)
                    if len(relevant) > 120:
                        break
            if relevant:
                sections.append(f"### {match['chapter']} (page {match['start_page']})")
                sections.append("")
                sections.append('\n'.join(relevant[:120]))
                sections.append("")
    else:
        sections.append("*No scenario walkthrough content detected. See Full Chapter Extraction below.*")
        sections.append("")

    # Full Chapter Extraction
    sections.append("---")
    sections.append("")
    sections.append("## Full Chapter Extraction")
    sections.append("")
    sections.append("Complete text extracted from each chapter of the AES Guide.")
    sections.append("")

    for chapter in chapters:
        sections.append(f"### {chapter['title']}")
        sections.append(f"*Pages {chapter['start_page']}-{chapter['start_page'] + len(chapter['content_pages']) - 1}*")
        sections.append("")

        full_text = '\n'.join(p["text"] for p in chapter["content_pages"])
        cleaned = clean_text(full_text)
        sections.append(cleaned)
        sections.append("")

    return '\n'.join(sections)


def main():
    print("=" * 60)
    print("AES Guide PDF -> Markdown Knowledge Base Extractor")
    print("=" * 60)

    # Verify PDF exists
    if not PDF_PATH.exists():
        print(f"\nERROR: AES Guide PDF not found at:")
        print(f"  {PDF_PATH}")
        print("\nPlease verify the path and try again.")
        sys.exit(1)

    print(f"\nInput:  {PDF_PATH}")
    print(f"Output: {OUTPUT_PATH}")
    print()

    # Step 1: Extract pages
    print("Step 1: Extracting text from PDF...")
    pages = extract_pages(PDF_PATH)

    # Step 2: Detect chapters
    print("\nStep 2: Detecting chapters and sections...")
    chapters = detect_chapters(pages)

    # Step 3: Identify key topics
    print("\nStep 3: Scanning for key AES topics...")
    topics = extract_key_topics(chapters)

    # Step 4: Build knowledge base
    print("\nStep 4: Building structured knowledge base...")
    kb_content = build_knowledge_base(chapters, topics)

    # Step 5: Write output
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(kb_content, encoding='utf-8')

    file_size = OUTPUT_PATH.stat().st_size
    line_count = kb_content.count('\n')
    print(f"\nOutput written to: {OUTPUT_PATH}")
    print(f"  Size: {file_size:,} bytes")
    print(f"  Lines: {line_count:,}")

    print("\n" + "=" * 60)
    print("DONE - Review reference/AES_Knowledge_Base.md for accuracy")
    print("=" * 60)


if __name__ == "__main__":
    main()

# CSIWorkflowGenerator - Progress Log

<!--
Track your development sessions here.
Use date headers for each session, e.g.:

## Session Date: YYYY-MM-DD
### What was done
- ...

### Discoveries
- ...

### Next steps
- ...
-->

## Session Date: 2026-02-26 (session 9 — rename + validation)

### What was done
- Renamed `templates/` → `workflow_specs/` across entire codebase (10 JSON files, 9 doc/script files, 44 line changes)
- Updated all references in CLAUDE.md, PHASE_NOTES.md, plan.md, log.md, parse-workflow.md, and 4 script docstrings
- Verified validate + render work from new path
- Pushed to both private and public repos
- Phase 6D (compound conditions) confirmed live validated by user — status updated
- Confirmed `lock_record` / `revert_field` already fully implemented (schema + spec_handler + docs)

### Status
- **Phases 0–6E**: All COMPLETE and live validated
- **Phase 7** (GenAI Platform Tools): Not started — next major milestone
- **Phase 8** (GenAI Platform Agent): Not started

---

## Session Date: 2026-02-26 (session 8 — AES expression parser deep debugging)

### What was done
- **Fixed Bug 4b: ROUND null guard — "0" string literal invalid in numeric context**
  - Symptom: After fixing ROUND outside IF, `"0"` (StringLiteral) rejected inside ROUND's argument (numeric context)
  - Root cause: ROUND's first arg is parsed in numeric context — `StringLiteral` not in expected token set, `IntegerLiteral` IS
  - Fix: `"0"` → `0` (numeric literal) in `_null_guard_expression()` in `spec_handler.py`
  - Final expression: `ROUND(IF(E(param) = "", 0, E(param)), N)`

- **Fixed Bug 5: Embedded double quotes in IDO values break JSON payload**
  - Symptom: Item `"SB 2"` (with quotes in name) causes `Error parsing ION API method parameters: unexpected character S at position 243`
  - Root cause: SUBSTITUTE concatenates raw P() values into double-encoded JSON. Unescaped `"` in data breaks outer JSON string
  - Fix: Added `_json_escape_expr()` in `expressions.py` — wraps every SUBSTITUTE value arg with `REPLACE(expr, '"', '\\\"')` (4 literal AES chars: `\`, `\`, `\`, `"`)
  - Escaping chain: `\\\"` in raw PARM → outer JSON decodes `\\` → `\` and `\"` → `"` → inner JSON sees `\"` as escaped quote
  - Debug approach: Added temporary notify action 27 to email V(PARM) contents — revealed the raw `"SB 2"` breaking the JSON

- **Fixed Bug 6: Action 40 field revert fails on ERP validation**
  - Symptom: "Reorder Point must be greater than 0" when handler reverts value (UseReorderPoint unchecked = 0 is invalid)
  - Fix: Action 40 now ONLY sets `InWorkflow=1` (lock) — does NOT revert the field value. User sees the new value while pending approval. Workflow decides to keep or revert.

- **Deployed handler 3 times** during iterative debugging, each time with `--update` (delete + recreate)
- Final handler: `ue_ReorderPointApproval` seq=230, 5 actions, active — **NEEDS USER TESTING**

### Discoveries
- **AES expression parser has context-sensitive token grammars** — different expected-token sets for different parse positions:
  - SUBSTITUTE arguments (text context): accepts StringLiteral, ROUND, IF, P, E, V, etc.
  - IF false-branch inside SUBSTITUTE: accepts StringLiteral but NOT ROUND
  - ROUND first argument (numeric context): accepts IntegerLiteral, RealLiteral, IF, E, P, ROUND, CAST, CEILING, FLOOR, but NOT StringLiteral
  - The VB.NET syntax checker calls `EventSystem.EventActionParametersCheckSyntax()` server-side
- **Double-encoded JSON is vulnerable to data injection** — any IDO property value with `"` breaks the outer JSON string. REPLACE with `'\\\"'` escapes for both JSON levels. This affects ALL handlers, not just ReorderPoint.
- **Approval handlers should lock-only, not revert** — reverting the field can trigger ERP validation rules that don't apply to the new value. Lock-only is safer and shows the user the pending value.

### Next steps
- **User testing on live tenant**: test ReorderPoint change with `"SB 2"` item (quotes in name) and normal items
- If REPLACE escaping works, apply it to all other handlers (credit approval, order line discount, etc.)
- Still need testing: ShipTo notification, CreditHold notification handlers
- Update CLAUDE.md with new gotchas once fixes are validated

---

## Session Date: 2026-02-26 (session 7 — ROUND/IF nesting fix for AES expression parser)

### What was done
- **Fixed Bug 4: AES expression parser rejects ROUND inside IF**
  - Symptom: `[Parsing of Parameters] was not successful` on action 25 (seq=230 ReorderPoint handler)
  - Root cause: AES parser token grammar doesn't include ROUND in IF() argument positions. ROUND is valid as a top-level SUBSTITUTE argument but NOT nested inside IF().
  - Fix: Swapped nesting order in `_null_guard_expression()`:
    - Before: `IF(E(param) = "", "0", ROUND(E(param), N))` — ROUND inside IF = **parse error**
    - After: `ROUND(IF(E(param) = "", "0", E(param)), N)` — IF inside ROUND = **valid**
  - One-line change in `src/aes_builder/spec_handler.py`
  - Updated CLAUDE.md gotcha #9 with nesting constraint
  - Redeployed handler: `ue_ReorderPointApproval` seq=230 — active, verified

### Discovery
- **AES expression parser token restrictions are context-sensitive** — ROUND is recognized at certain parse positions (e.g., SUBSTITUTE argument) but not inside IF() false-branch. The parser's expected-token list for IF arguments includes IF, E, P, V, SUBSTITUTE, CONFIGNAME, etc. but NOT ROUND. This isn't documented anywhere — learned from the live parse error.

### Next steps
- User validation: test ReorderPoint change on live tenant (null→value and value→value transitions)
- Remaining 2 handlers still need testing: ShipTo notification, CreditHold notification

---

## Session Date: 2026-02-26 (session 6 — cross-project Action=4 fix + Bug 1 docs)

### What was done
- **Fixed IDO delete Action=3→4 across all projects** (not just CSIWorkflowGenerator):
  - `.claude/commands/ido-update.md` — action table, section header, JSON example
  - `CSIPOAssetCreationTool/Agents&Tools/CLAUDE.md` — field definition
  - `CSIWorkflowGenerator/reference/PHASE_NOTES.md` — deploy safety note
- **Documented Bug 1 (PoCost SQL limitation)** — CLAUDE.md gotcha #8, template description updated
  - AES `IdoOnItemUpdate` cannot detect SQL-calculated fields (PoCost recalculated by SP after line save)
  - Template preserved as parallel ALL_IN + multi-level pattern demo

- **Fixed Bug 3 (ReorderPoint null guard)** in `spec_handler.py`
  - Added `_ROUND_E_RE` regex to detect `ROUND(E(...), N)` patterns
  - Added `_null_guard_expression()` that wraps as `IF(E(param) = "", "0", ROUND(E(param), N))`
  - Wired into `_build_input_variables()` — applied automatically to all expression-type workflow inputs
  - Verified: all 3 templates with ROUND(E()) (credit_approval, pocost, order_line_discount) now get the guard
  - Templates stay clean — authors write `ROUND(E(OldX), 2)`, guard injected at build time

- **Replaced all stale distribution placeholders** across 7 templates
  - Changed `user1`/`user2`/`user3` and `user5`/`user1_email_full`/`user4` to angle-bracket format: `<approver>`, `<notifier1>`, `<manager>`, etc.
  - Angle brackets are obviously not real keys — fail validation immediately, force resolution
  - Live-deployed templates (`shipto`, `credit_hold`, `reorder_point`) already use real keys (`marcello`)
- **Updated `/parse-workflow` command** to require resolving distribution users at spec creation time
  - LLM must look up tenant config and ask for real user keys before generating the spec
  - No more leaving placeholders for someone to find later

- **Redeployed ReorderPoint handler** with null guard fix
  - `wfgen create workflow_specs/reorder_point_approval.json --update --activate` — SUCCESS
  - ION workflow: `CS_ReorderPoint_Approval` — active
  - AES handler: `ue_ReorderPointApproval` seq=230 — active, verified
  - Updated distribution from `user1` to `marcello`
- **Pushed to private repo** (`d282b23..7665721`) and **synced to public repo** (`InforOS-Automation-Toolkit`)

### All 3 live test bugs — RESOLVED
| Bug | Issue | Resolution | Commit |
|-----|-------|------------|--------|
| 1 | PoCost SQL-calculated field invisible to AES | Documented as platform limitation (CLAUDE.md gotcha #8) | `5fae02b` |
| 2 | Drillback view generation (viewSetName, LogicalId, viewName) | Fixed in earlier session — live validated | (prior session) |
| 3 | ReorderPoint null guard — ROUND(E(null)) FormatException | Auto IF() guard in spec_handler.py | `64ede20` |

### Deployed handlers on tenant (current state)
| Handler | Seq | IDO | Event | Active | Status |
|---------|-----|-----|-------|--------|--------|
| ue_CS_OrderLineDiscount_Approval | 201 | SLCoItems | IdoOnItemUpdate | YES | Live — tested working |
| ue_ReorderPointApproval | 230 | SLItems | IdoOnItemUpdate | YES | Redeployed with null guard — **NEEDS USER TESTING** |
| ue_ShipToChangeNotification | 231 | SLCos | IdoOnItemUpdate | YES | Redeployed with lock fix — **NEEDS USER TESTING** |
| ue_POCostMultiLevelApproval | 232 | SLPos | IdoOnItemUpdate | NO | Cannot work (SQL-calc limitation) — inactive |
| ue_CS_CreditHold_Notification | ? | SLCustomers | IdoOnItemUpdate | YES | Redeployed with lock fix — **NEEDS USER TESTING** |

### Next steps
- **User validation on live tenant** (3 handlers need testing):
  1. **ReorderPoint** — Change an item's ReorderPoint (especially from null → a value). Should get approval task in Pulse without FormatException.
  2. **ShipTo notification** — Change a CO's ship-to address. Should get notification and record should remain editable (no InWorkflow lock).
  3. **CreditHold notification** — Toggle credit hold flag on a customer. Should get notification and record should remain editable.
- **Phase 7 (GenAI Platform Tools)** — Port CLI tooling to Infor GenAI platform as agents/tools. Not started.
- **Phase 8 (GenAI Platform Agent)** — Not started.

---

## Session Date: 2026-02-26 (session 5 — notification redeploy + IDO delete discovery)

### What was done
- **Redeployed both notification handlers** with InWorkflow lock fix
  - `CS_CreditHold_Notification` — ION workflow + AES handler (4 actions, no lock)
  - `CS_ShipTo_Change_Notification` — ION workflow + AES handler (4 actions, no lock)
  - Updated both spec templates: `distribution: "user1"` → `"marcello"`

- **MAJOR DISCOVERY: IDO delete Action code is 4, NOT 3**
  - `Action=3` is a no-op — returns `{"Success": true}` but does nothing
  - `Action=4` is the real delete — confirmed working on EventHandlers and EventActions
  - This was the root cause of the long-standing "delete silently fails" gotcha
  - For EventActions (multi-table IDO): must include `_ItemId` in the `ItemId` field and only use `RowPointer` in Properties — parent table properties (EventName, EvrEventName) cause SQL column ambiguity errors
  - For EventHandlers (single-table): standard key properties work fine

- **Updated `builder.py`** with working delete support
  - `_ido_delete()`: Changed Action=3 → Action=4, added optional `item_id` parameter
  - Added `_load_action_item_ids()`: Fetches `_ItemId` for all actions under a handler
  - Added `delete_action()`: Deletes a single EventAction by RowPointer + _ItemId
  - Updated `delete_handler()`: Uses `_ItemId` for action deletes, then deletes handler

- **Updated `wfgen.py` `--update` flag** — now does real delete+recreate for AES handlers instead of skipping with "IDO API does not support handler delete/replace yet"

- **Tested full pipeline**: `wfgen create --update --activate` successfully deletes existing handler (actions first, then handler), recreates fresh, and verifies — both notification handlers confirmed clean

- **Updated CLAUDE.md**
  - Gotcha #2: Corrected from "Delete Action=3 silently fails" to "Action=4 is delete, NOT 3"
  - Gotcha #5: Updated EventActions delete documentation with `_ItemId` requirement

### Discoveries
- IDO API Action codes: 1=Insert, 2=Update, 3=**no-op**, 4=Delete
- EventActions IDO joins 3 tables (EventAction, EventHandler, EventRevision) — delete operations can't include properties from parent tables without SQL column name ambiguity
- EventActions `EvrEventName` maps to `EventName` column on EventRevision table (usually null), required as key property for updates but causes issues on deletes
- EventActions `Description` column is max 40 characters — truncation error if exceeded

### Next steps
- **User validation**: Test notification handlers on live tenant (change credit hold flag, change CO ship-to) — verify notification arrives and record stays editable
- **Bug 3 (ReorderPoint null guard)**: Add IF() guard around ROUND(E(...)) in AES expression builder for nullable fields
- **Bug 1 (PoCost SQL limitation)**: Document as known limitation (already in log, confirm CLAUDE.md)
- Unlock any records previously locked by old handlers (`InWorkflow = 0`)

---

## Session Date: 2026-02-27

### What was done
- **FIXED InWorkflow lock bug** for notification-only AES handlers
  - Root cause: `spec_handler.py` always generated action 40 (`InWorkflow=1` + field rollback) for ALL workflows, including notification-only ones that have no `ido_update` write-back to unlock the record
  - Fix: Added `_has_ido_update()` helper that recursively checks the spec's `flow` for any `ido_update` step (handles nested subworkflows, parallel branches, conditions)
  - Action 40 is now conditionally skipped when no `ido_update` exists in the flow
  - Verified against all 10 template specs: 2 notification-only → NO-LOCK, 7 approval → LOCK, 1 no-aes-trigger → N/A
- Updated CLAUDE.md gotcha #7 from "BUG" to "FIXED" with description of the solution

### Next steps
- Redeploy `shipto_change_notification` and `credit_hold_notification` to live environment and verify records are no longer locked
- Unlock any records that were previously locked by the old handler

---

## Session Date: 2026-02-26 (Drillback Fix)

### What was done
- Fixed drillback view generation across all 10 workflow spec templates
  - **Root cause 1 (viewSetName)**: Templates hardcoded `infor.syteline (SyteLineViews)` but tenant uses `SyteLineViewsCustom`. Changed all specs to `"view_set": ""` for auto-injection from tenant config.
  - **Root cause 2 (LogicalId)**: Renderer injected full logical_id with site suffix (`/dals`) but drillbacks require the base LID without suffix. Added `get_drillback_logical_id()` to strip suffix.
  - **Root cause 3 (viewName)**: `shipto_change_notification.json` used non-existent `CustomerOrderView`, corrected to `SalesOrderView`.
- Added two helper functions to `shared/tenant.py`: `get_drillback_logical_id()` and `get_drillback_view_set()`
- Updated `shared/__init__.py` to export the new functions
- Updated renderer.py to use drillback-specific functions for view generation
- Updated CSIWorkflowGenerator/CLAUDE.md with Drillback Views gotcha section

### Discoveries
- Drillback LogicalId must NOT include the site suffix (e.g. `/dals`) — ION resolves views at the product level, not site level
- `tenant_config.json` optionally accepts `drillback_logical_id` and `drillback_view_set` for override, but defaults work by stripping suffix / using `SyteLineViewsCustom`

### Live test results
- Deployed shipto workflow with `--update --activate` — SUCCESS
- **Drillback link WORKS** — SalesOrderView opens correctly with SyteLineViewsCustom and base LogicalId

### BUG FOUND: InWorkflow lock without write-back (CRITICAL)
- The AES handler for notification-only workflows (shipto, credit_hold) sets `InWorkflow = 1` via `SETPROPVALUES` in action 40, locking the record
- But notification-only workflows have **no approval step and no IDO write-back** to set `InWorkflow = 0`
- Result: **records are permanently locked** after the notification fires — users cannot edit the order again
- Root cause: the AES `spec_handler.py` always generates the standard 5-action pattern (including the lock action) regardless of whether the workflow has a write-back
- **Fix needed**: notification-only workflows must either (a) skip the InWorkflow lock action entirely, or (b) generate a shorter AES handler pattern that omits action 40
- This affects: `shipto_change_notification.json`, `credit_hold_notification.json`, and any future notification-only specs

### Next steps
- **FIX** the InWorkflow lock bug for notification-only workflows (highest priority)
- Render + deploy additional workflows to validate drillback fix across approval patterns

---

## Session Date: 2026-02-26

### What was done
- Added `wfgen extract-sa` subcommand to extract service account tokens from existing workflows
  - Primary mode: fetches workflow JSON from ION REST API by name
  - Secondary mode: reads from a local JSON file (`--file`)
  - Extracts `serviceAccount` field and updates `tenant_config.json`
- Updated `extract_service_account()` in `src/config/tenant.py` to check top-level `serviceAccount` field first (API response format), then fall back to recursive flowpart search
  - Refactored into `extract_service_account_from_dict()` (works on dicts) + file wrapper
- Added graceful empty/placeholder service account handling in `ionapi.py`
  - `build_ido_load` and `build_ido_update` now omit `serviceAccount` key when value is empty or a placeholder (starts with `<`)
- Added deploy-time warning in `wfgen create` when no service account is configured
- Fixed `setup.py` Step 5 instructions: removed incorrect "export from ION Desk" guidance, added `wfgen extract-sa` recommendation, noted that UI exports are XML without SA
- Added "Service Account" documentation section to CLAUDE.md

### Discoveries
- ION Desk UI exports workflows as XML, stripping the service account — only REST API returns JSON with the encrypted `serviceAccount` field
- The `serviceAccount` field appears at top-level in API GET responses, but inside ionapi flowparts in rendered workflow JSON

### Next steps
- User validation: test `extract-sa` against a live workflow
- Test render + deploy with empty service account to verify graceful handling

## Session Date: 2026-02-26 (continued)

### What was done
- Live-tested all service account methods — 5 tests, all passing:
  1. `extract-sa CS_Credit_Approval_API` — fetched 836-char SA from live API, saved to tenant_config
  2. `extract-sa --file reference/CS_Credit_Approval_API.json` — **bug found**: placeholder `<YOUR_SERVICE_ACCOUNT>` was written to tenant_config, overwriting real token
  3. `build_ido_load`/`build_ido_update` — correctly omit `serviceAccount` key when empty/placeholder
  4. Full render pipeline — empty SA produces 0/2 ionapi flowparts with SA; real SA produces 2/2
  5. `_check_service_account` warning logic — correctly triggers warning when ionapi exists but no SA
- **Bug fix**: Added placeholder validation in `cmd_extract_sa` — rejects values matching `_is_placeholder_sa()` (empty or starts with `<`) before writing to tenant_config.json

### Discoveries
- Reference workflow files (genericized for public repo) contain `<YOUR_SERVICE_ACCOUNT>` placeholder — `extract-sa --file` must guard against overwriting real tokens with these

### Next steps
- Phase 6D investigation (compound conditions) or Phase 7 (GenAI Platform Tools)

## Session Date: 2026-02-26 (session 3 — live test feedback analysis)

### What was done
- Analyzed user feedback from 3 test workflows: CS_POCost_MultiLevel_Approval, CS_ShipTo_Change_Notification, CS_ReorderPoint_Approval
- Downloaded corrected workflow `CS_ShipTo_Change_Notification_1` from API for drillback comparison
- Saved both original and corrected to `reference/CS_ShipTo_Change_Notification.json` and `reference/CS_ShipTo_Change_Notification_1.json`
- Downloaded drillback reference XML from `C:\Users\mmartins1\Downloads\infor.syteline (3).xml`
- Read `Portaladmin.json` swagger and successfully tested the drillback API
- Queried all 4 custom AES handlers (ue_CS_OrderLineDiscount_Approval seq=201, ue_ReorderPointApproval seq=230, ue_ShipToChangeNotification seq=231, ue_POCostMultiLevelApproval seq=232)
- Compared action 25 (Set API PARMS) across working and broken handlers

### Issue 1: CS_POCost_MultiLevel_Approval — AES trigger cannot detect PoCost changes
**Status**: LIMITATION — no fix possible
**Root cause**: PoCost is calculated at the SQL level via a stored procedure (SP), not through the IDO layer. AES `IdoOnItemUpdate` only listens at the IDO level, so SQL-level recalculations are invisible to it.
**Detail**: The PurchaseOrderQuickEntry form saves PO lines first (standard IDO save), then runs a custom SP to recalculate the PO total in SQL. The IDO never sees the PoCost change.
**Workaround**: Monitor at the line level instead (e.g., SLPoItems properties that change during editing).
**Action**: Document this as a known AES limitation. This will affect any SQL-calculated properties across SyteLine. No programmatic way to detect this from form/IDO metadata alone — requires domain knowledge.
**Handler status**: `ue_POCostMultiLevelApproval` at seq=232, currently INACTIVE on tenant.

### Issue 2: CS_ShipTo_Change_Notification — Drillback URL malformed
**Status**: ROOT CAUSE IDENTIFIED — fix needed in renderer + spec system
**Root cause**: Three errors in the generated drillback views section:

1. **`viewSetName` wrong**: Our renderer uses `"infor.syteline (SyteLineViews)"` but correct is `"infor.syteline (SyteLineViewsCustom)"` — the custom view set is what's deployed on the tenant
2. **`viewName` wrong**: We generated `"CustomerOrderView"` which doesn't exist in the view set. Correct is `"SalesOrderView"` (from the drillback XML)
3. **`LogicalId` has site suffix**: Our renderer auto-injects `tenant.logical_id` = `"lid://infor.syteline.csi/dals"` but drillbacks require `"lid://infor.syteline.csi"` (WITHOUT the `/dals` site suffix)

**Comparison of original vs corrected workflow views**:
```
ORIGINAL (broken):
  viewSetName: "infor.syteline (SyteLineViews)"
  viewName: "CustomerOrderView"              <-- doesn't exist!
  LogicalId: "lid://infor.syteline.csi/dals" <-- site suffix breaks drillback

CORRECTED (working):
  viewSetName: "infor.syteline (SyteLineViewsCustom)"
  viewName: "SalesOrderView"
  LogicalId: "lid://infor.syteline.csi"      <-- no site suffix
```

**Available view names from drillback XML** (SyteLineViewsCustom view set):
| ViewName | Form | Filter Parameter |
|----------|------|-----------------|
| BillToPartyView | Customers | CustNum = ID1 |
| ContactMasterView | CustomerSalesContactCrossReferences | ContactId = ID1 |
| CustomerView | Customers | CustNum = ID1 |
| CustomerReturnView | RMAs | RmaNum = ID1 |
| AdjustmentOrderView | MaterialTransactions | TransNum = ID1 |
| ItemView | Items | Item = ID1 |
| PayFromPartyView | Customers | CustNum = ID1 |
| EmployeeView | Salespersons | Slsman = ID1 |
| PurchaseOrderView | PurchaseOrders | PoNum = ID1 |
| QuoteView | Estimates | CoNum = ID1 |
| ReceiptView | MaterialTransactions | TransNum = ID1 |
| RemitToPartyView | Vendors | VendNum = ID1 |
| RequisitionView | PurchaseOrderRequisitions | ReqNum = ID1 |
| SalesOrderView | CustomerOrders | CoNum = ID1 |
| ShipFromPartyView | Vendors | VendNum = ID1 |
| ShipmentView | MaterialTransactions | TransNum = ID1 |
| SupplierView | Vendors | VendNum = ID1 |
| VoucherView | ILC_APVouchersandAdjustments | Voucher = ID1 |
| ProjectTaskView | ProjectTasks | ProjNum = ID1 |

**Drillback API discovery** (`POST OSPORTAL/admin/v1/applications/url/drillback`):
- Marked as "internal, may change without notice" but works reliably
- Service proxy: `OSPORTAL/admin`
- Takes `{language, locale, drillbacks: [{label, parameters: [{name, value}]}]}`
- Key parameter: `ViewId` → maps to the view name in the XML
- Returns: `{drillbacks: [{url, label, type}]}` with resolved URLs
- Also has an `/alert` variant for ION alerts
- Successfully tested: `ViewId=SalesOrderView` + `ID1=100001` → full form URL

**Fix plan**:
- Add `drillback_logical_id` to tenant_config (base `lid://infor.syteline.csi` without site suffix) OR derive by stripping the site suffix from `logical_id`
- Default `view_set` to `"infor.syteline (SyteLineViewsCustom)"` in renderer
- Validate `viewName` against the known view name list (could be fetched via drillback API or hardcoded from XML)
- Save drillback XML as `reference/drillback_views.xml` for reference
- Consider adding a drillback API validator that checks view names at render time

### Issue 3: CS_ReorderPoint_Approval — AES action 25 format error
**Status**: ROOT CAUSE IDENTIFIED — fix needed in AES expression builder
**Error**: "Input string was not in a correct format. Event Name is IdoOnItemUpdate. Event Handler Sequence is 230. Event Action Sequence is 25."

**Most likely cause**: `ROUND(E(OldReorderPoint), 2)` receives a null/empty value.
- `ReorderPoint` on SLItems is **nullable** — most items have `ReorderPoint = null`
- When a user changes ReorderPoint from null → a value, action 20 loads the old record via `SET(RE(OldReorderPoint) = "ReorderPoint")` which sets OldReorderPoint to null/empty
- Action 25: `ROUND(null, 2)` or `ROUND("", 2)` → .NET `FormatException`
- The CreditLimit handler doesn't hit this because `CreditLimit` on SLCustomers always has a default value (never null)

**Evidence**: Queried SLItems — only 2 items out of all have non-null ReorderPoint (value: `1.00000000`). All others are null.

**Secondary risk**: `P("Description")` in the SUBSTITUTE could also fail if item descriptions contain special characters (`{`, `}`, `"`) that break the SUBSTITUTE function or the JSON string. Item names can contain embedded double quotes (e.g., `"SB 2"` stored WITH quotes in the `Item` field).

**Comparison of working (CreditLimit) vs broken (ReorderPoint) action 25**:
```
WORKING (CreditLimit):
  - CustName: P("Name") — always populated on customers
  - OldCreditLimit: ROUND(E(OldCreditLimit), 2) — CreditLimit always has a default value
  - dataType for credit limits: "STRING" (even though numeric)

BROKEN (ReorderPoint):
  - Description: P("Description") — could contain special chars
  - OldReorderPoint: ROUND(E(OldReorderPoint), 2) — ReorderPoint is NULLABLE, often null
  - dataType for reorder points: "DECIMAL"
```

**Fix plan**:
- Wrap `ROUND(E(OldX), 2)` in an `IF()` guard: `IF(E(OldReorderPoint) = "", "0", ROUND(E(OldReorderPoint), 2))` — or use `IF(E(OldReorderPoint) <> "", ROUND(E(OldReorderPoint), 2), "0")`
- Consider escaping/sanitizing `P("Description")` or fetching description in the ION workflow instead of passing through the AES trigger
- Document that AES-passed values must be non-null and not contain JSON-breaking characters

**Handler details on tenant**:
| Handler | Seq | IDO | Event | Active |
|---------|-----|-----|-------|--------|
| ue_CS_OrderLineDiscount_Approval | 201 | SLCoItems | IdoOnItemUpdate | YES |
| ue_ReorderPointApproval | 230 | SLItems | IdoOnItemUpdate | YES |
| ue_ShipToChangeNotification | 231 | SLCos | IdoOnItemUpdate | YES |
| ue_POCostMultiLevelApproval | 232 | SLPos | IdoOnItemUpdate | NO |

### Discoveries
- AES `IdoOnItemUpdate` only detects IDO-level changes — SQL-level recalculations (SPs) are invisible. This is a fundamental platform limitation affecting any workflow triggered by calculated fields.
- Drillback view set on this tenant is `SyteLineViewsCustom`, not `SyteLineViews`
- LogicalId in drillback views must NOT include the site suffix (e.g., `/dals`)
- Portaladmin drillback API works (`POST OSPORTAL/admin/v1/applications/url/drillback`) — can programmatically validate view names
- `ReorderPoint` on SLItems is nullable (most items have null). Any AES trigger monitoring nullable fields must guard `ROUND(E(...))` against null.
- `Item` field on SLItems can contain embedded double quotes (e.g., `"SB 2"`) — risk for JSON-building SUBSTITUTE expressions
- **AES handler query quirk**: `load_handlers(event_name='IdoOnItemUpdate')` with default recordCap=100 may NOT return all handlers — our custom handlers at seq >= 200 were beyond the 100-record cutoff. Description-based searches work because they add a filter that narrows the result set.

### Files saved this session
- `reference/CS_ShipTo_Change_Notification.json` — original (broken drillback)
- `reference/CS_ShipTo_Change_Notification_1.json` — user-corrected (working drillback)

### Next steps (3 items, priority order)
1. **Fix drillback generation** (Issue 2) — update renderer LogicalId handling, fix default view set name, validate view names against known list. Save drillback XML to reference/
2. **Fix AES null guard** (Issue 3) — add IF() guard around ROUND(E(...)) in aes_builder for nullable fields. Test with ReorderPoint handler
3. **Document AES SQL limitation** (Issue 1) — add to CLAUDE.md Critical Gotchas section


# BOM IDO Discovery Results

## Date: 2026-02-10

## SyteLine BOM Architecture

In SyteLine, BOMs are structured around **Standard Jobs** (`Type='S'`). The hierarchy:

```
SLItems (Item Master)
  └── SLJobs (Standard Job, Type='S', links Item to routing+materials)
       ├── SLJobRoutes (Operations/Routing for this item)
       │    └── OperNum 10, 20, 30... with Work Centers
       └── SLJobmatls (Materials/BOM components)
            └── Materials linked to operations via OperNum
```

### Creation Order (CRITICAL)
1. **SLItems** - Create all items (parents + children)
2. **SLJobs** - Create standard job for each parent/assembly item (`Type='S'`)
3. **SLJobRoutes** - Add routing operations to the job
4. **SLJobmatls** - Add material lines (children) linked to operations

## IDO Details

### SLItems (existing tools available)
- Existing: `ItemSearch_Tool_v2`, `ItemInsert_Tool_v2`
- Key properties: Item, Description, UM, MatlType, PMTCode, ProductCode, AbcCode, CostType, CostMethod, Stat

### SLJobs (409 properties)
Job container for BOM. Key properties for insert:
| Property | Type | Description |
|----------|------|-------------|
| Job | NumSortedString | Job number (10-char padded) |
| Suffix | Short Integer | Job suffix (0 for standard) |
| Item | String | Item code this job is for |
| Type | String | 'S' = Standard (BOM template) |
| Stat | String | 'F' = Firm |
| QtyReleased | Decimal | Standard quantity |
| Whse | String | Warehouse |

### SLJobRoutes (353 properties)
Routing operations within a job. Key properties for insert:
| Property | Type | Description |
|----------|------|-------------|
| Job | NumSortedString | Parent job number |
| Suffix | Short Integer | Job suffix (0) |
| OperNum | Long Integer | Operation number (10, 20, 30...) |
| Wc | String | Work center code |
| SetupHrsT | Decimal | Setup hours |
| RunHrsTLbr | Decimal | Run hours (labor) |
| RunHrsTMch | Decimal | Run hours (machine) |
| Efficiency | Decimal | Efficiency factor |
| RunBasisLbr | String | Run basis for labor |
| RunBasisMch | String | Run basis for machine |

### SLJobmatls (329 properties)
Material lines within a job. Key properties for insert:
| Property | Type | Description |
|----------|------|-------------|
| Job | NumSortedString | Parent job number |
| Suffix | Short Integer | Job suffix (0) |
| OperNum | Long Integer | Operation number material belongs to |
| Sequence | Short Integer | Sequence within operation (1, 2, 3...) |
| Item | String | Child/component item code |
| Description | String | Material description |
| MatlQtyConv | Decimal | Quantity per parent |
| UM | String | Unit of measure |
| MatlType | String | 'M'=Material, 'T'=Tool, 'O'=Other |
| Units | String | 'U'=Unit, 'L'=Lot |
| RefType | String | 'I'=Inventory, 'J'=Job (sub-assembly), 'P'=Phantom |
| AltGroup | Short Integer | Alternate group number |
| ScrapFact | Decimal | Scrap factor |

### SLWcs (247 properties)
Work centers. Key properties:
| Property | Type | Description |
|----------|------|-------------|
| Wc | String | Work center code |
| Description | String | Work center description |
| Dept | String | Department code |
| DeptDescription | String | Department description |

## Available Work Centers (50 found)
| Code | Description | Department |
|------|-------------|------------|
| AS-500 | Assembly Area | Assembly and Packaging |
| FA-400 | Final Assembly Area | Assembly and Packaging |
| INS-20 | Inspection Center | Machine Shop - Inspection |
| MC-300 | Machining | Machine Shop - Inspection |
| PG-300 | Outside Packaging | Assembly and Packaging |
| ST-100 | Warehouse Staging | Assembly and Packaging |
| CUT-10 | Cutting Area | Machine Shop - Inspection |
| DRL-10 | Drilling Operations | Fabrication and Painting |
| GRD-10 | Grinding Operations | Fabrication and Painting |
| PNT-10 | Painting Area | Fabrication and Painting |
| MLD-10 | Molding | Machine Shop - Inspection |
| PKG-10 | Packaging Station | Assembly and Packaging |
| ... and 38 more |

## Existing BOM Patterns (from sample data)

### Standard Job Pattern (e.g., Job 2 = FA-20000 "Bicycle, Model-50, 26\"")
**Routing:**
- Oper 10: FA-400 (Final Assembly) - Setup 1.00h, Run 0.30h labor
- Oper 20: INS-20 (Inspection) - Run 0.30h labor
- Oper 30: PG-300 (Packaging) - No time
- Oper 40: ST-100 (Staging) - Setup 1.00h, Run 0.30h both

**Materials (all on Oper 10):**
- Seq 1: SA-50910 "Frame, Assembly, Standard" (1 EA, RefType=J = sub-assembly job)
- Seq 2: SA-61500 "Wheel, Assembly, 26\"" (2 EA, RefType=I = inventory)
- Seq 3: RS-10000 "Seat, Assembly, Racing - PHANTOM" (1 EA, RefType=I)
- Seq 4: TA-31000 "Handle-Bars, Racing" (1 EA, RefType=I)
- Seq 5: LB-34000 "Tool, Assembler-Wheel" (1 PC, MatlType=T = tool)

### Multi-Level BOM Pattern
- Parent Job (FA-20000) references SA-50910 with RefType='J' (Job reference)
- SA-50910 has its own standard job with its own routing and materials
- This creates the multi-level hierarchy

## Decision: IDO API Approach

**Chosen approach: Option A (IDO API)** - Use IDO REST API inserts for everything.

**Rationale:**
- Consistent with existing tool patterns (ItemInsert, PoInsert, etc.)
- Full control over data creation order
- No dependency on BOM Bulk Import form/infrastructure
- Well-understood error handling patterns
- Agent can search-before-insert to avoid duplicates

## Tool Plan

### Tools to Reuse (existing)
- `ItemSearch_Tool_v2` - Search items
- `ItemInsert_Tool_v2` - Create items

### New Tools Needed
1. `GAF_SyteLine_JobSearch_Tool_v1` - Search standard jobs by item
2. `GAF_SyteLine_JobInsert_Tool_v1` - Create standard job for an item
3. `GAF_SyteLine_RoutingSearch_Tool_v1` - Search routing operations
4. `GAF_SyteLine_RoutingInsert_Tool_v1` - Add routing operations (batch)
5. `GAF_SyteLine_MaterialSearch_Tool_v1` - Search materials/BOM components
6. `GAF_SyteLine_MaterialInsert_Tool_v1` - Add materials to BOM (batch)

### Agent
- `GAF_SyteLine_BomGenerator_Agent_v1` - Orchestrates all tools

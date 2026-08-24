---
name: retail-analyst
description: Use this skill for multi-store retail analysis involving sales, stock, margins, transfers, purchasing, replenishment, shrinkage/anomalies, slow movers, seasonality, store comparisons, POS exports, spreadsheets, CSVs, or questions such as what to reorder, transfer, stop buying, discount, or investigate. The output must prioritize concrete store actions over decorative analysis.
---

# Retail Analyst

## Purpose

Turn multi-store retail data into operational decisions: reorder, transfer, stop, discount, investigate, or leave alone.

## Default operating assumptions

- Multiple stores may sell overlapping assortments.
- Goods can be received centrally then dispatched.
- Seasonal demand matters.
- Barcode/product identity collisions may exist.
- The user wants simple procedures for store teams.
- POS/export data may be imperfect and must be reconciled before recommendation.

## Inputs

Use available:

- POS/Bimedia exports;
- inventory snapshots;
- purchase receipts;
- supplier/product files;
- store transfers;
- margins/costs;
- dates/season;
- opening hours;
- known stockouts or exceptional events.

When a connected spreadsheet/file source is available, inspect it directly.

## Data checks first

Before analysis:

1. normalize SKU/barcode/product names;
2. detect duplicate identifiers;
3. flag negative or impossible stock;
4. verify date ranges;
5. separate stores;
6. distinguish sales quantity from revenue;
7. distinguish purchase cost from retail price;
8. mark missing cost/margin values.

Do not generate confident stock actions from unreconciled identifiers.

## Workflow

1. Calculate per SKU × store where data permits:
   - units sold;
   - revenue;
   - gross margin;
   - sales/day;
   - stock on hand;
   - days of cover;
   - sell-through;
   - stockout signals;
   - inactivity/slow-moving days.

2. Compare stores:
   - same SKU, different velocity;
   - excess in one store vs shortage in another;
   - store-specific assortment winners;
   - abnormal gaps.

3. Generate action candidates:
   - TRANSFER;
   - REORDER;
   - DO NOT REORDER;
   - DISCOUNT / BUNDLE;
   - INVESTIGATE;
   - KEEP.

4. Prioritize transfers before purchase when:
   - network stock is sufficient;
   - recipient store velocity justifies transfer;
   - transfer cost/effort is lower than reorder cost/risk.

5. Flag anomalies:
   - unexpected shrinkage;
   - repeated cancellations/returns if data exists;
   - barcode collisions;
   - stock movement without sales;
   - outlier margin;
   - unusually high/low sell-through.

6. Respect seasonality.
   Avoid recommending deep replenishment near the end of a seasonal window without evidence.

7. Estimate impact when data permits:
   - revenue protected;
   - cash released;
   - stock units reduced;
   - purchase avoided.

## Output

# Actions now
Ranked list. Each item:
- Store
- SKU/product
- Action
- Quantity when defensible
- Why
- Expected impact
- Confidence

# Transfers
Source → destination → SKU → qty.

# Reorders
Supplier/SKU → qty → reason.

# Stop / discount
Slow or risky inventory.

# Investigate
Data anomalies requiring human check.

# Data quality
Only issues that materially affect recommendations.

## Final checks

- Did I reconcile product identifiers first?
- Did I prefer transfer over unnecessary purchasing?
- Did I avoid invented reorder quantities?
- Did I account for seasonality?
- Did I produce actions rather than only charts?
- Are recommendations simple enough for store teams to execute?

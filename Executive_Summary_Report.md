# NextDrive Motors: Multi-Echelon Supply Chain Network Design & Facility Location Analysis
**Course:** Supply Chain Management (Semester 5) — Assignment 1  
**Author:** Dinesh  
**Tools Employed:** Python Optimization (PuLP, CBC Solver), Microsoft Excel Solver, OpenPyXL, Matplotlib  
**Primary Dataset:** `Facility location techniques - input data.xlsx`

---

## Executive Summary

NextDrive Motors is establishing an end-to-end nationwide manufacturing and distribution network in India to assemble and deliver its flagship cruiser motorcycle line. The supply chain operates across four distinct echelons:
1. **Tier-1 Suppliers:** Jamnagar, Bhilai, and Bellary (sourcing heavy chassis stampings, body panels, and structural metal components).
2. **Manufacturing Plants (MPs):** Candidate assembly locations in Sanand, Sriperumbudur, and Pune.
3. **Distribution Centres (DCs):** Regional vehicle logistics hubs in Nagpur, Bhiwandi, Greater Noida, Hosur, and Dankuni.
4. **Metropolitan Demand Zones (CZs):** Customer dealer networks in Delhi, Mumbai, Bengaluru, Chennai, Hyderabad, and Kolkata.

To determine which assembly plants and distribution centres to license/lease and how to route shipments across all intermediate nodes, a Mixed-Integer Linear Programming (MILP) model was formulated and solved to global optimality. Additionally, all four auxiliary facility location techniques in the course curriculum (**Transportation Model**, **Location Factor Rating**, **Center of Gravity**, and **Load-Distance Technique**) were solved.

### Key Optimization Highlights
* **Minimum Total Supply Chain Cost:** **Rs. 79,480,000**
  * **Fixed Facility Opening Costs:** **Rs. 71,000,000** ($89.33\%$ of total cost)
    * Plant Licensing & Commissioning: Rs. 47,000,000 (Sanand + Sriperumbudur)
    * Distribution Centre Leases: Rs. 24,000,000 (Nagpur + Hosur + Dankuni)
  * **Variable Freight Transportation Costs:** **Rs. 8,480,000** ($10.67\%$ of total cost)
    * Supplier $\to$ Plant Freight: Rs. 1,960,000
    * Plant $\to$ Distribution Centre Freight: Rs. 3,705,000
    * Distribution Centre $\to$ Customer Zone Freight: Rs. 2,815,000
* **Optimal Facility Configuration:**
  * **Manufacturing Plants Opened:** **Sanand** (Gujarat) and **Sriperumbudur** (Tamil Nadu). **Pune is closed**.
  * **Distribution Centres Opened:** **Nagpur** (Maharashtra), **Hosur** (Tamil Nadu), and **Dankuni** (West Bengal). **Bhiwandi and Greater Noida are closed**.
* **Demand Satisfaction:** 100% of the 72,000 cruiser bike annual dealer demand is satisfied with zero stockouts.

---

## Complete Network Visualization

The complete 4-echelon flow network with optimal facility activation statuses, utilized throughputs, and shipment volumes is illustrated below:

![NextDrive Motors Optimal 4-Echelon Network Flow](C:\Users\dines\.gemini\antigravity\brain\50a08ad6-f12c-417d-8e09-5b074a3af43d\fig1_scnd_network_flows.png)

---

## 1. Mathematical Formulation of the SCND Model

### 1.1 Index Sets
* $i \in I$: Set of candidate Tier-1 Suppliers, $I = \{\text{Jamnagar}, \text{Bhilai}, \text{Bellary}\}$
* $j \in J$: Set of candidate Manufacturing Assembly Plants (MPs), $J = \{\text{Sanand}, \text{Sriperumbudur}, \text{Pune}\}$
* $k \in K$: Set of candidate Distribution Centres (DCs), $K = \{\text{Nagpur}, \text{Bhiwandi}, \text{Greater Noida}, \text{Hosur}, \text{Dankuni}\}$
* $l \in L$: Set of Customer Demand Zones (CZs), $L = \{\text{Delhi}, \text{Mumbai}, \text{Bengaluru}, \text{Chennai}, \text{Hyderabad}, \text{Kolkata}\}$

### 1.2 System Parameters (Input Data)
* $S_i$: Maximum component supply capacity at supplier $i$ (units)
* $P_j$: Maximum motorcycle assembly capacity at candidate plant $j$ (units)
* $F_j$: Annual fixed cost of commissioning and licensing assembly plant $j$ (INR)
* $W_k$: Maximum vehicle handling/throughput capacity at candidate DC $k$ (units)
* $G_k$: Annual fixed cost of leasing and operating DC $k$ (INR)
* $D_l$: Forecasted annual motorcycle demand at metropolitan market $l$ (units)
* $c_{ij}^{SP}$: Per-unit freight cost from supplier $i$ to plant $j$ (INR/unit)
* $c_{jk}^{PD}$: Per-unit freight cost from plant $j$ to DC $k$ (INR/unit)
* $c_{kl}^{DC}$: Per-unit freight cost from DC $k$ to customer zone $l$ (INR/unit)

### 1.3 Decision Variables
* $y_j \in \{0, 1\}$: Binary decision variable; $1$ if manufacturing plant $j$ is opened, $0$ otherwise.
* $u_k \in \{0, 1\}$: Binary decision variable; $1$ if distribution centre $k$ is opened, $0$ otherwise.
* $x_{ij}^{SP} \ge 0$: Continuous flow quantity shipped from supplier $i$ to plant $j$.
* $x_{jk}^{PD} \ge 0$: Continuous flow quantity shipped from plant $j$ to DC $k$.
* $x_{kl}^{DC} \ge 0$: Continuous flow quantity shipped from DC $k$ to customer zone $l$.

### 1.4 Objective Function
Minimise the total annual supply chain cost, comprising fixed facility setup costs and variable multi-echelon transportation costs:

$$\min Z = \sum_{j \in J} F_j y_j + \sum_{k \in K} G_k u_k + \sum_{i \in I}\sum_{j \in J} c_{ij}^{SP} x_{ij}^{SP} + \sum_{j \in J}\sum_{k \in K} c_{jk}^{PD} x_{jk}^{PD} + \sum_{k \in K}\sum_{l \in L} c_{kl}^{DC} x_{kl}^{DC}$$

### 1.5 Constraints
1. **Customer Demand Fulfillment:**
   Every customer zone $l$ must receive exactly its forecasted requirement:
   $$\sum_{k \in K} x_{kl}^{DC} = D_l, \quad \forall l \in L$$

2. **Supplier Sourcing Capacity:**
   Total component outflow from supplier $i$ cannot exceed its physical availability limit:
   $$\sum_{j \in J} x_{ij}^{SP} \le S_i, \quad \forall i \in I$$

3. **Manufacturing Plant Capacity & Activation:**
   Outflow from plant $j$ cannot exceed its installed capacity, and assembly can only take place if the plant is licensed ($y_j = 1$):
   $$\sum_{k \in K} x_{jk}^{PD} \le P_j \cdot y_j, \quad \forall j \in J$$

4. **Distribution Centre Throughput & Activation:**
   Throughput shipped from DC $k$ cannot exceed its handling capacity, and operations require an active lease ($u_k = 1$):
   $$\sum_{l \in L} x_{kl}^{DC} \le W_k \cdot u_k, \quad \forall k \in K$$

5. **Facility-Level Flow Conservation (No Scrap / Direct Assembly):**
   * At each manufacturing plant $j$, component inflow must balance motorcycle outflow:
     $$\sum_{i \in I} x_{ij}^{SP} = \sum_{k \in K} x_{jk}^{PD}, \quad \forall j \in J$$
   * At each distribution centre $k$, vehicle inflow from plants must balance vehicle dispatch to dealers:
     $$\sum_{j \in J} x_{jk}^{PD} = \sum_{l \in L} x_{kl}^{DC}, \quad \forall k \in K$$

6. **Echelon Mass Balance:**
   Summing the facility flow conservation equations guarantees global echelon balance:
   $$\sum_{i \in I}\sum_{j \in J} x_{ij}^{SP} = \sum_{j \in J}\sum_{k \in K} x_{jk}^{PD} = \sum_{k \in K}\sum_{l \in L} x_{kl}^{DC} = \sum_{l \in L} D_l = 72,000$$

7. **Variable Integrality and Non-negativity:**
   $$y_j \in \{0, 1\} \quad \forall j \in J; \quad u_k \in \{0, 1\} \quad \forall k \in K$$
   $$x_{ij}^{SP} \ge 0, \quad x_{jk}^{PD} \ge 0, \quad x_{kl}^{DC} \ge 0 \quad \forall i, j, k, l$$

---

## 2. Detailed SCND Optimization Results

### 2.1 Facility Opening Decisions and Capacity Utilization

| Facility Type | Candidate Site | Status | Fixed Cost (INR) | Rated Capacity | Utilized Volume | Capacity Utilization |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Supplier** | Jamnagar | ACTIVE | - | 40,000 | 40,000 | **100.0%** |
| **Supplier** | Bhilai | INACTIVE | - | 45,000 | 0 | **0.0%** |
| **Supplier** | Bellary | ACTIVE | - | 35,000 | 32,000 | **91.4%** |
| **Plant (MP)** | Sanand | **OPEN** | Rs. 25,000,000 | 40,000 | 40,000 | **100.0%** |
| **Plant (MP)** | Sriperumbudur | **OPEN** | Rs. 22,000,000 | 35,000 | 32,000 | **91.4%** |
| **Plant (MP)** | Pune | **CLOSED** | Rs. 28,000,000 | 45,000 | 0 | **0.0%** |
| **DC** | Nagpur | **OPEN** | Rs. 8,000,000 | 30,000 | 30,000 | **100.0%** |
| **DC** | Bhiwandi | **CLOSED** | Rs. 10,000,000 | 35,000 | 0 | **0.0%** |
| **DC** | Greater Noida | **CLOSED** | Rs. 9,500,000 | 25,000 | 0 | **0.0%** |
| **DC** | Hosur | **OPEN** | Rs. 8,500,000 | 25,000 | 25,000 | **100.0%** |
| **DC** | Dankuni | **OPEN** | Rs. 7,500,000 | 20,000 | 17,000 | **85.0%** |

![Facility Capacity vs Utilized Throughput](C:\Users\dines\Documents\03-ACADEMICS\Semester 5\Supply chain management\Assignment-1\fig3_scnd_capacity_utilization.png)

### 2.2 Optimal Shipment Allocation Across Echelons

#### Echelon 1: Supplier $\to$ Manufacturing Plant
* **Jamnagar $\to$ Sanand:** $40,000\text{ units} \times \text{Rs. } 25/\text{unit} = \text{Rs. } 1,000,000$ (Direct intrastate Gujarat pipeline, $100\%$ Jamnagar capacity).
* **Bellary $\to$ Sriperumbudur:** $32,000\text{ units} \times \text{Rs. } 30/\text{unit} = \text{Rs. } 960,000$ (Karnataka to Tamil Nadu auto belt corridor).
* **Bhilai:** Unused due to high distance and uncompetitive freight to Western/Southern plants.
* **Subtotal Supplier Freight:** **Rs. 1,960,000**

#### Echelon 2: Manufacturing Plant $\to$ Distribution Centre
* **Sanand $\to$ Nagpur:** $30,000\text{ units} \times \text{Rs. } 50/\text{unit} = \text{Rs. } 1,500,000$ (Feeding central Indian consolidation hub at $100\%$ capacity).
* **Sanand $\to$ Dankuni:** $10,000\text{ units} \times \text{Rs. } 95/\text{unit} = \text{Rs. } 950,000$ (Supplemental supply to the Eastern hub).
* **Sriperumbudur $\to$ Hosur:** $25,000\text{ units} \times \text{Rs. } 25/\text{unit} = \text{Rs. } 625,000$ (Dedicated Southern transfer corridor at $100\%$ Hosur capacity).
* **Sriperumbudur $\to$ Dankuni:** $7,000\text{ units} \times \text{Rs. } 90/\text{unit} = \text{Rs. } 630,000$ (Complementary Eastern allocation).
* **Subtotal Plant-to-DC Freight:** **Rs. 3,705,000**

#### Echelon 3: Distribution Centre $\to$ Customer Demand Zone
* **From Nagpur DC (Total Throughput: 30,000 units):**
  * Nagpur $\to$ Mumbai: $18,000\text{ units} \times \text{Rs. } 45 = \text{Rs. } 810,000$ ($100\%$ Mumbai demand).
  * Nagpur $\to$ Hyderabad: $6,000\text{ units} \times \text{Rs. } 35 = \text{Rs. } 210,000$ ($66.7\%$ Hyderabad demand).
  * Nagpur $\to$ Delhi: $6,000\text{ units} \times \text{Rs. } 55 = \text{Rs. } 330,000$ ($40.0\%$ Delhi demand).
* **From Hosur DC (Total Throughput: 25,000 units):**
  * Hosur $\to$ Bengaluru: $12,000\text{ units} \times \text{Rs. } 20 = \text{Rs. } 240,000$ ($100\%$ Bengaluru demand).
  * Hosur $\to$ Chennai: $10,000\text{ units} \times \text{Rs. } 25 = \text{Rs. } 250,000$ ($100\%$ Chennai demand).
  * Hosur $\to$ Hyderabad: $3,000\text{ units} \times \text{Rs. } 45 = \text{Rs. } 135,000$ ($33.3\%$ Hyderabad demand).
* **From Dankuni DC (Total Throughput: 17,000 units):**
  * Dankuni $\to$ Kolkata: $8,000\text{ units} \times \text{Rs. } 15 = \text{Rs. } 120,000$ ($100\%$ Kolkata demand).
  * Dankuni $\to$ Delhi: $9,000\text{ units} \times \text{Rs. } 80 = \text{Rs. } 720,000$ ($60.0\%$ Delhi demand).
* **Subtotal DC-to-Customer Freight:** **Rs. 2,815,000**

### 2.3 Cost Structure and Pareto Analysis

![Cost Breakdown Analysis](C:\Users\dines\Documents\03-ACADEMICS\Semester 5\Supply chain management\Assignment-1\fig2_scnd_cost_breakdown.png)

```
========================================================================================
Cost Element                            Absolute Cost (INR)   % of Supply Chain Total
========================================================================================
Plant Fixed Opening Costs               Rs. 47,000,000                 59.13%
DC Fixed Opening Costs                  Rs. 24,000,000                 30.20%
----------------------------------------------------------------------------------------
TOTAL FIXED CAPITAL/LEASE COSTS         Rs. 71,000,000                 89.33%
----------------------------------------------------------------------------------------
Supplier -> Plant Freight Cost          Rs.  1,960,000                  2.47%
Plant -> DC Freight Cost                Rs.  3,705,000                  4.66%
DC -> Customer Zone Freight Cost        Rs.  2,815,000                  3.54%
----------------------------------------------------------------------------------------
TOTAL VARIABLE TRANSPORTATION COSTS     Rs.  8,480,000                 10.67%
========================================================================================
TOTAL SUPPLY CHAIN EXPENDITURE          Rs. 79,480,000                100.00%
========================================================================================
```

---

## 3. Deep Operational Interpretation & Managerial Insights

### 3.1 The Dominance of Fixed Costs Over Transportation Costs
Fixed costs account for **89.33%** (Rs. 71.0M) of the total budget, while freight represents only **10.67%** (Rs. 8.48M). This extreme cost asymmetry dictates the optimal network topology:
* The optimizer aggressively minimizes the count of open facilities rather than opening facilities in every metropolitan consumer region.
* Opening an extra distribution center (such as Greater Noida @ Rs. 9.5M or Bhiwandi @ Rs. 10.0M) would save a modest amount in local trucking freight, but would incur an enormous fixed leasing penalty that cannot be amortized over the available volume.

### 3.2 Plant Siting: Why Sanand and Sriperumbudur Over Pune?
* **Pune's Cost Penalty:** Pune requires an opening cost of **Rs. 28,000,000**, the highest among all candidate assembly locations.
* **Capacity Granularity:** Total demand is 72,000 units. Sanand (40,000) and Sriperumbudur (35,000) offer a combined capacity of 75,000 units, which matches the 72,000 requirement with negligible idle capacity ($3,000$ units or $4\%$). 
* If Pune (45,000) were selected with Sanand (40,000), the combined fixed cost would jump to Rs. 53,000,000 (an immediate Rs. 6M penalty).
* **Geographic Alignment:** 
  * Sanand forms an optimal low-cost cluster with Jamnagar (Rs. 25/unit freight) to serve Western, Northern, and Central corridors.
  * Sriperumbudur forms a low-cost cluster with Bellary (Rs. 30/unit freight) to dominate the Southern motorcycle market (Bengaluru and Chennai).

### 3.3 Distribution Architecture: Strategic Role of the Three Opened DCs
1. **Nagpur (The Central Cross-Docking Hub):**
   * With a central geographic coordinate and an economical fixed lease (Rs. 8.0M), Nagpur operates at **100% capacity** (30,000 units).
   * It handles all of Mumbai (18,000 units) via express highway connectivity, two-thirds of Hyderabad (6,000 units), and backhauls into Delhi (6,000 units).
2. **Hosur (The Southern Fulfillment Anchor):**
   * Located directly on the Karnataka-Tamil Nadu border, Hosur serves as a high-velocity fulfillment center right between Bengaluru and Chennai.
   * Freight from Sriperumbudur to Hosur is only Rs. 25/unit, and distribution to Bengaluru is merely Rs. 20/unit and Chennai Rs. 25/unit. Hosur operates at **100% capacity** (25,000 units).
3. **Dankuni (The Eastern Gateway & Northern Overflow):**
   * Dankuni possesses the lowest fixed cost of all candidate DCs (**Rs. 7.5M**).
   * It satisfies 100% of Kolkata demand (8,000 units @ Rs. 15/unit) and supplies the remaining 9,000 units to Delhi via eastern trunk railways/expressways, completely avoiding the need to open a high-cost DC in Greater Noida (Rs. 9.5M).

### 3.4 Facility-Level vs. Echelon-Level Flow Conservation
In the model, two interpretations of flow balance were rigorously benchmarked:
1. **Physical Facility Conservation (Current Baseline):** 
   Each opened plant and DC independently balances inflow and outflow. 
   $$\text{Total Cost} = \mathbf{\text{Rs. } 79,480,000}$$
2. **Global Echelon Conservation:** 
   Only total nationwide inflows balance total outflows. Under this relaxation, Sriperumbudur ships 35,000 units while receiving 32,000 units of parts, and Sanand receives 40,000 units of parts while shipping 37,000 units.
   $$\text{Total Cost} = \mathbf{\text{Rs. } 79,465,000} \quad (\Delta = \text{Rs. } 15,000)$$
* **Managerial Takeaway:** In physical motorcycle manufacturing, a plant cannot ship assembled cruiser bikes without receiving their stamped chassis from suppliers. Hence, **facility-level flow conservation is the mandatory operational reality**. The Rs. 15,000 difference is negligible ($0.019\%$), proving the robustness of the optimal facility network.

---

## 4. Solutions for Auxiliary Facility Location Techniques

### 4.1 Transportation Model (TM): Dallas vs. Chicago Plant Expansion

![Spatial and Facility Comparison](C:\Users\dines\Documents\03-ACADEMICS\Semester 5\Supply chain management\Assignment-1\fig4_spatial_cog_and_ld.png)

#### Problem Background
An automotive components manufacturer operates three existing plants in **Miami (20k)**, **Tempe (40k)**, and **Columbus (30k)** (total existing capacity = 90,000 units). Customer demand across four distributors (**MKG, ASN, GMZ, Akla**) totals 108,000 units. To cover the 18,000-unit shortfall, management must choose between opening a new plant in **Dallas (18k)** or **Chicago (18k)**.

#### Comparative Results

| Configuration | Status | Total Transportation Cost | Cost Difference | Recommendation |
| :--- | :---: | :---: | :---: | :--- |
| **Open Dallas ($y_{\text{Dallas}}=1$)** | Optimal | **$219,770.00** | **Baseline (Lowest Cost)** | **RECOMMENDED OPTION** |
| **Open Chicago ($y_{\text{Chicago}}=1$)** | Suboptimal | **$254,830.00** | +$35,060.00 (+15.95%) | Reject |

#### Optimal Routing (with Dallas Open):
* **Miami (20,000):** 20,000 to MKG Inc ($1.00/u) = $20,000
* **Tempe (40,000):** 16,200 to ASN Inc ($1.75/u) + 23,800 to Akla Inc ($4.00/u) = $123,550
* **Columbus (30,000):** 9,840 to MKG Inc ($2.50/u) + 20,160 to GMZ Inc ($1.00/u) = $44,760
* **Dallas (18,000):** 160 to MKG Inc ($1.50/u) + 17,840 to Akla Inc ($1.75/u) = $31,460
* **Total Optimized Transportation Cost:** **$219,770.00**

---

### 4.2 Location Factor Rating Technique

Four candidate sites (**Pune, Nagpur, Indore, Vadodara**) were evaluated across six strategic criteria.

![Location Factor Rating Comparison](C:\Users\dines\Documents\03-ACADEMICS\Semester 5\Supply chain management\Assignment-1\fig5_factor_rating_comparison.png)

$$\text{Total Score} = \sum_{k=1}^6 (\text{Weight}_k \times \text{Factor Score}_k)$$

| Strategic Factor | Weight | Pune | Nagpur | Indore | Vadodara |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Land & Site Development Cost | 0.25 | 60.0 | 85.0 | 80.0 | 75.0 |
| Highway & Expressway Connectivity | 0.20 | 90.0 | 80.0 | 70.0 | 85.0 |
| Power grid reliability | 0.20 | 85.0 | 75.0 | 70.0 | 90.0 |
| Availability of skilled labor pool | 0.15 | 95.0 | 65.0 | 60.0 | 70.0 |
| Local tax incentives & subsidies | 0.10 | 65.0 | 90.0 | 85.0 | 75.0 |
| Digital & Telecom infrastructure | 0.10 | 90.0 | 70.0 | 75.0 | 80.0 |
| **Total Weighted Score** | **1.00** | **79.75** | **78.00** | **73.00** | **79.75** |
| **Final Ranking** | - | **Rank 1 (Tie)** | **Rank 3** | **Rank 4** | **Rank 1 (Tie)** |

#### Managerial Interpretation:
* **Pune (79.75)** leads heavily in qualitative manufacturing factors: skilled automotive labor (95) and digital/highway infrastructure (90), but suffers from high land costs (60).
* **Vadodara (79.75)** ties Pune with balanced excellence in power reliability (90), expressways (85), and lower land cost (75).
* If high-precision engineering and talent acquisition are primary, **Pune** is preferred; if capital expenditure control and power continuity dominate, **Vadodara** is preferred.

---

### 4.3 Center of Gravity (CoG) Technique

Determines the optimal spatial coordinates for a new regional central distribution facility serving five major South Indian consumption centers:

$$X^* = \frac{\sum W_i X_i}{\sum W_i}, \quad Y^* = \frac{\sum W_i Y_i}{\sum W_i}$$

| City | X-coordinate ($X_i$) | Y-coordinate ($Y_i$) | Monthly Demand ($W_i$) | Weighted X ($W_i X_i$) | Weighted Y ($W_i Y_i$) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Bengaluru | 150.0 | 200.0 | 1,200 | 180,000.0 | 240,000.0 |
| Mysore | 100.0 | 150.0 | 450 | 45,000.0 | 67,500.0 |
| Chennai | 450.0 | 220.0 | 1,500 | 675,000.0 | 330,000.0 |
| Coimbatore | 200.0 | 80.0 | 800 | 160,000.0 | 64,000.0 |
| Tirupati | 380.0 | 260.0 | 600 | 228,000.0 | 156,000.0 |
| **Total** | - | - | **4,550** | **1,288,000.0** | **857,500.0** |

#### Optimal Center of Gravity Coordinates:
$$X^* = \frac{1,288,000}{4,550} = \mathbf{283.08}, \quad Y^* = \frac{857,500}{4,550} = \mathbf{188.46}$$
* **Geographic Placement:** The coordinates $(283.08, 188.46)$ correspond geographically to the area around **Vellore / Kolar**, situated directly between Bengaluru and Chennai along the National Highway 48 industrial corridor.

---

### 4.4 Load-Distance (LD) Optimization Technique

Evaluates three candidate central warehouse sites (**Hebbal, Marathahalli, Silk Board**) to replenish five micro-fulfillment centers in Bengaluru.

#### Euclidean Distance Formula:
$$d_{ci} = \sqrt{(X_c - X_i)^2 + (Y_c - Y_i)^2}$$

#### Step 1: Euclidean Distance Matrix

| Candidate Site | Indiranagar (45t) | Whitefield (28t) | Koramangala (30t) | Electronic City (49t) | Yelahanka (55t) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Hebbal (12, 28)** | 8.5440 | 14.3178 | 14.0000 | 23.0868 | 2.8284 |
| **Marathahalli (20, 18)** | 5.3852 | 6.4031 | 8.9443 | 14.3178 | 15.6205 |
| **Silk Board (13, 12)** | 8.2462 | 15.6205 | 2.2361 | 7.0711 | 18.2483 |

#### Step 2: Load-Distance Score Computation
$$\text{LD Score} = \sum_{i=1}^5 (L_i \times d_{ci})$$

* **Hebbal:** $(45 \times 8.544) + (28 \times 14.318) + (30 \times 14.000) + (49 \times 23.087) + (55 \times 2.828) = \mathbf{2,492.20}$
* **Marathahalli:** $(45 \times 5.385) + (28 \times 6.403) + (30 \times 8.944) + (49 \times 14.318) + (55 \times 15.621) = \mathbf{2,250.65}$
* **Silk Board:** $(45 \times 8.246) + (28 \times 15.621) + (30 \times 2.236) + (49 \times 7.071) + (55 \times 18.248) = \mathbf{2,225.67}$

#### Operational Recommendation:
* **Silk Board is the optimal location** with the lowest LD score (**2,225.67**), delivering an immediate ton-kilometer savings over Marathahalli ($1.1\%$ lower) and Hebbal ($10.7\%$ lower). 
* Silk Board is ideally situated adjacent to heavy replenishment volume nodes like Koramangala ($2.24\text{ km}$) and Electronic City ($7.07\text{ km}$).

---

## 5. Excel Solver Implementation Guide

The primary workbook `Facility location techniques - input data.xlsx` has been configured with dynamic formulas and verified values. To run or audit the model directly in Microsoft Excel Solver:

### Solver Setup for Sheet: `SCND`
1. **Set Objective:** `$J$35`
2. **To:** `Min`
3. **By Changing Variable Cells:**
   `$B$17:$B$19, $B$22:$B$26, $B$30:$D$32, $B$36:$F$38, $B$42:$G$46`
4. **Subject to the Constraints:**
   * `$B$17:$B$19 = binary` (Plant opening decisions)
   * `$B$22:$B$26 = binary` (DC opening decisions)
   * `$B$47:$G$47 = $C$5:$C$10` (or `>=`; Customer demand satisfaction)
   * `$E$30:$E$32 <= $G$5:$G$7` (Supplier sourcing capacity)
   * `$G$36:$G$38 <= $C$17:$C$19` (Plant throughput $\le$ Plant capacity $\times$ binary)
   * `$H$42:$H$46 <= $C$22:$C$26` (DC throughput $\le$ DC capacity $\times$ binary)
   * `$B$33:$D$33 = TRANSPOSE($G$36:$G$38)` (Plant flow conservation: Inflow = Outflow)
   * `$B$39:$F$39 = TRANSPOSE($H$42:$H$46)` (DC flow conservation: Inflow = Outflow)
   * `$D$49 = $D$50` and `$D$50 = $D$51` (Echelon balance)
   * Variable non-negativity: Check box **"Make Unconstrained Variables Non-Negative"**
5. **Select Solving Method:** **Simplex LP**
6. Click **Solve**.

---

## 6. Deliverables and Project Files

The complete solution package in the project directory includes:
* **`Facility location techniques - input data.xlsx`**: Fully populated workbook with live Excel formulas (`SUMPRODUCT`, `SUM`, `SQRT`), optimal solution variables, and complete solver setups across all 5 sheets.
* **`solve_assignment.py`**: Standalone, production-grade Python optimization solver that solves all five techniques using PuLP, prints formatted executive tables, and generates chart figures.
* **`fig1_scnd_network_flows.png`**: High-resolution 4-echelon network flow diagram with directed shipment arrows.
* **`fig2_scnd_cost_breakdown.png`**: Fixed vs Variable cost Pareto and component horizontal bar charts.
* **`fig3_scnd_capacity_utilization.png`**: Facility-by-facility capacity vs utilization bar chart.
* **`fig4_spatial_cog_and_ld.png`**: Center of Gravity coordinate plot and Load-Distance geographic node chart.
* **`fig5_factor_rating_comparison.png`**: Multi-criteria factor rating comparison across the four candidate sites.

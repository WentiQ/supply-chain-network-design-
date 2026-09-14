"""
NextDrive Motors - Nationwide Supply Chain Network Design & Facility Location Techniques
Course: Supply Chain Management (Semester 5) - Assignment 1
Solves all 5 facility location techniques:
  1. Multi-Echelon Supply Chain Network Design (SCND) - MILP Optimization
  2. Transportation Model (TM) - Mixed-Integer Plant Expansion
  3. Location Factor Rating Method
  4. Center of Gravity (CoG) Technique
  5. Load-Distance (LD) Optimization Technique
Generates detailed solution outputs, operational metrics, and publication-grade visualizations.
"""

import math
import pulp
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Set plot style
plt.rcParams['font.sans-serif'] = 'Segoe UI', 'DejaVu Sans', 'Arial'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

# ==============================================================================
# 1. MULTI-ECHELON SUPPLY CHAIN NETWORK DESIGN (SCND)
# ==============================================================================
def solve_scnd(facility_balance=True):
    print("=" * 80)
    print(f"1. MULTI-ECHELON SCND OPTIMIZATION (facility_balance={facility_balance})")
    print("=" * 80)

    suppliers = ['Jamnagar', 'Bhilai', 'Bellary']
    plants = ['Sanand', 'Sriperumbudur', 'Pune']
    dcs = ['Nagpur', 'Bhiwandi', 'Greater Noida', 'Hosur', 'Dankuni']
    customers = ['Delhi', 'Mumbai', 'Bengaluru', 'Chennai', 'Hyderabad', 'Kolkata']

    sup_cap = {'Jamnagar': 40000, 'Bhilai': 45000, 'Bellary': 35000}
    plant_cap = {'Sanand': 40000, 'Sriperumbudur': 35000, 'Pune': 45000}
    plant_fc = {'Sanand': 25000000, 'Sriperumbudur': 22000000, 'Pune': 28000000}
    dc_cap = {'Nagpur': 30000, 'Bhiwandi': 35000, 'Greater Noida': 25000, 'Hosur': 25000, 'Dankuni': 20000}
    dc_fc = {'Nagpur': 8000000, 'Bhiwandi': 10000000, 'Greater Noida': 9500000, 'Hosur': 8500000, 'Dankuni': 7500000}
    demand = {'Delhi': 15000, 'Mumbai': 18000, 'Bengaluru': 12000, 'Chennai': 10000, 'Hyderabad': 9000, 'Kolkata': 8000}

    c_sp = {
        'Jamnagar': {'Sanand': 25, 'Sriperumbudur': 85, 'Pune': 45},
        'Bhilai': {'Sanand': 65, 'Sriperumbudur': 70, 'Pune': 55},
        'Bellary': {'Sanand': 75, 'Sriperumbudur': 30, 'Pune': 50}
    }

    c_pd = {
        'Sanand': {'Nagpur': 50, 'Bhiwandi': 35, 'Greater Noida': 55, 'Hosur': 80, 'Dankuni': 95},
        'Sriperumbudur': {'Nagpur': 60, 'Bhiwandi': 75, 'Greater Noida': 110, 'Hosur': 25, 'Dankuni': 90},
        'Pune': {'Nagpur': 40, 'Bhiwandi': 25, 'Greater Noida': 70, 'Hosur': 60, 'Dankuni': 85}
    }

    c_dc = {
        'Nagpur': {'Delhi': 55, 'Mumbai': 45, 'Bengaluru': 50, 'Chennai': 55, 'Hyderabad': 35, 'Kolkata': 60},
        'Bhiwandi': {'Delhi': 80, 'Mumbai': 15, 'Bengaluru': 65, 'Chennai': 75, 'Hyderabad': 50, 'Kolkata': 100},
        'Greater Noida': {'Delhi': 15, 'Mumbai': 85, 'Bengaluru': 110, 'Chennai': 120, 'Hyderabad': 85, 'Kolkata': 75},
        'Hosur': {'Delhi': 115, 'Mumbai': 70, 'Bengaluru': 20, 'Chennai': 25, 'Hyderabad': 45, 'Kolkata': 95},
        'Dankuni': {'Delhi': 80, 'Mumbai': 105, 'Bengaluru': 100, 'Chennai': 95, 'Hyderabad': 75, 'Kolkata': 15}
    }

    prob = pulp.LpProblem('NextDrive_SCND', pulp.LpMinimize)

    # Decision variables
    y_plant = pulp.LpVariable.dicts('y_plant', plants, cat='Binary')
    y_dc = pulp.LpVariable.dicts('y_dc', dcs, cat='Binary')
    x_sp = pulp.LpVariable.dicts('x_sp', ((i, j) for i in suppliers for j in plants), lowBound=0)
    x_pd = pulp.LpVariable.dicts('x_pd', ((j, k) for j in plants for k in dcs), lowBound=0)
    x_dc = pulp.LpVariable.dicts('x_dc', ((k, l) for k in dcs for l in customers), lowBound=0)

    # Objective Function
    cost_sp = pulp.lpSum(c_sp[i][j] * x_sp[i, j] for i in suppliers for j in plants)
    cost_pd = pulp.lpSum(c_pd[j][k] * x_pd[j, k] for j in plants for k in dcs)
    cost_dc = pulp.lpSum(c_dc[k][l] * x_dc[k, l] for k in dcs for l in customers)
    cost_plant_fixed = pulp.lpSum(plant_fc[j] * y_plant[j] for j in plants)
    cost_dc_fixed = pulp.lpSum(dc_fc[k] * y_dc[k] for k in dcs)

    prob += cost_sp + cost_pd + cost_dc + cost_plant_fixed + cost_dc_fixed

    # Constraints
    # 1. Customer Demand Satisfaction
    for l in customers:
        prob += pulp.lpSum(x_dc[k, l] for k in dcs) == demand[l], f"Demand_{l}"

    # 2. Supplier Capacity
    for i in suppliers:
        prob += pulp.lpSum(x_sp[i, j] for j in plants) <= sup_cap[i], f"SupCap_{i}"

    # 3. Plant Capacity & Activation
    for j in plants:
        prob += pulp.lpSum(x_pd[j, k] for k in dcs) <= plant_cap[j] * y_plant[j], f"PlantCap_{j}"

    # 4. DC Handling Capacity & Activation
    for k in dcs:
        prob += pulp.lpSum(x_dc[k, l] for l in customers) <= dc_cap[k] * y_dc[k], f"DCCap_{k}"

    # 5. Flow Conservation
    if facility_balance:
        # Per-facility mass conservation
        for j in plants:
            prob += pulp.lpSum(x_sp[i, j] for i in suppliers) == pulp.lpSum(x_pd[j, k] for k in dcs), f"PlantBal_{j}"
        for k in dcs:
            prob += pulp.lpSum(x_pd[j, k] for j in plants) == pulp.lpSum(x_dc[k, l] for l in customers), f"DCBal_{k}"
    else:
        # Echelon level conservation
        prob += pulp.lpSum(x_sp[i, j] for i in suppliers for j in plants) == pulp.lpSum(x_pd[j, k] for j in plants for k in dcs)
        prob += pulp.lpSum(x_pd[j, k] for j in plants for k in dcs) == pulp.lpSum(x_dc[k, l] for k in dcs for l in customers)
        for j in plants:
            prob += pulp.lpSum(x_sp[i, j] for i in suppliers) <= plant_cap[j] * y_plant[j]
        for k in dcs:
            prob += pulp.lpSum(x_pd[j, k] for j in plants) <= dc_cap[k] * y_dc[k]

    prob.solve(pulp.PULP_CBC_CMD(msg=False))

    results = {
        'status': pulp.LpStatus[prob.status],
        'total_cost': pulp.value(prob.objective),
        'trans_sp': pulp.value(cost_sp),
        'trans_pd': pulp.value(cost_pd),
        'trans_dc': pulp.value(cost_dc),
        'fixed_plant': pulp.value(cost_plant_fixed),
        'fixed_dc': pulp.value(cost_dc_fixed),
        'y_plant': {j: int(round(pulp.value(y_plant[j]))) for j in plants},
        'y_dc': {k: int(round(pulp.value(y_dc[k]))) for k in dcs},
        'flow_sp': {(i, j): pulp.value(x_sp[i, j]) for i in suppliers for j in plants},
        'flow_pd': {(j, k): pulp.value(x_pd[j, k]) for j in plants for k in dcs},
        'flow_dc': {(k, l): pulp.value(x_dc[k, l]) for k in dcs for l in customers},
        'plant_cap': plant_cap,
        'dc_cap': dc_cap,
        'sup_cap': sup_cap,
        'demand': demand
    }

    print(f"Optimal Solver Status: {results['status']}")
    print(f"Total Optimal Cost: Rs. {results['total_cost']:,.2f}")
    print(f"  Fixed Plant Costs:         Rs. {results['fixed_plant']:,.2f}")
    print(f"  Fixed DC Costs:            Rs. {results['fixed_dc']:,.2f}")
    print(f"  Supplier->Plant Freight:   Rs. {results['trans_sp']:,.2f}")
    print(f"  Plant->DC Freight:         Rs. {results['trans_pd']:,.2f}")
    print(f"  DC->Customer Freight:      Rs. {results['trans_dc']:,.2f}")
    print(f"  Total Variable Freight:    Rs. {(results['trans_sp'] + results['trans_pd'] + results['trans_dc']):,.2f}")

    print("\n--- Plant Decisions ---")
    for j in plants:
        status = "OPEN" if results['y_plant'][j] == 1 else "CLOSED"
        outflow = sum(results['flow_pd'][(j, k)] for k in dcs)
        inflow = sum(results['flow_sp'][(i, j)] for i in suppliers)
        print(f"  Plant {j:<14}: {status:<6} | Inflow={inflow:6,.0f} | Outflow={outflow:6,.0f} | Cap={plant_cap[j]:6,.0f} ({outflow/plant_cap[j]*100:5.1f}%)")

    print("\n--- DC Decisions ---")
    for k in dcs:
        status = "OPEN" if results['y_dc'][k] == 1 else "CLOSED"
        outflow = sum(results['flow_dc'][(k, l)] for l in customers)
        inflow = sum(results['flow_pd'][(j, k)] for j in plants)
        print(f"  DC {k:<14}: {status:<6} | Inflow={inflow:6,.0f} | Outflow={outflow:6,.0f} | Cap={dc_cap[k]:6,.0f} ({outflow/dc_cap[k]*100:5.1f}%)")

    print("\n--- Detailed Shipments ---")
    print("  Supplier -> Plant:")
    for (i, j), flow in results['flow_sp'].items():
        if flow > 0:
            print(f"    {i:<12} -> {j:<14}: {flow:6,.0f} units @ Rs. {c_sp[i][j]}/unit = Rs. {flow*c_sp[i][j]:,.2f}")
    print("  Plant -> DC:")
    for (j, k), flow in results['flow_pd'].items():
        if flow > 0:
            print(f"    {j:<14} -> {k:<14}: {flow:6,.0f} units @ Rs. {c_pd[j][k]}/unit = Rs. {flow*c_pd[j][k]:,.2f}")
    print("  DC -> Customer Zone:")
    for (k, l), flow in results['flow_dc'].items():
        if flow > 0:
            print(f"    {k:<14} -> {l:<12}: {flow:6,.0f} units @ Rs. {c_dc[k][l]}/unit = Rs. {flow*c_dc[k][l]:,.2f}")

    return results


# ==============================================================================
# 2. TRANSPORTATION MODEL (TM)
# ==============================================================================
def solve_tm():
    print("\n" + "=" * 80)
    print("2. TRANSPORTATION MODEL (TM) - DALLAS VS CHICAGO EXPANSION")
    print("=" * 80)

    plants = ['Miami', 'Tempe', 'Columbus', 'Dallas', 'Chicago']
    dcs = ['MKG Inc', 'ASN Inc', 'GMZ Inc', 'Akla Inc']
    cost = {
        'Miami': {'MKG Inc': 1.0, 'ASN Inc': 3.0, 'GMZ Inc': 3.5, 'Akla Inc': 1.5},
        'Tempe': {'MKG Inc': 5.0, 'ASN Inc': 1.75, 'GMZ Inc': 2.25, 'Akla Inc': 4.0},
        'Columbus': {'MKG Inc': 2.5, 'ASN Inc': 2.5, 'GMZ Inc': 1.0, 'Akla Inc': 3.0},
        'Dallas': {'MKG Inc': 1.5, 'ASN Inc': 2.5, 'GMZ Inc': 3.75, 'Akla Inc': 1.75},
        'Chicago': {'MKG Inc': 3.2, 'ASN Inc': 1.75, 'GMZ Inc': 2.0, 'Akla Inc': 4.35}
    }
    cap = {'Miami': 20000, 'Tempe': 40000, 'Columbus': 30000, 'Dallas': 18000, 'Chicago': 18000}
    dem = {'MKG Inc': 30000, 'ASN Inc': 16200, 'GMZ Inc': 20160, 'Akla Inc': 41640}

    # Solve as unified MILP
    prob = pulp.LpProblem('TM_Expansion', pulp.LpMinimize)
    x = pulp.LpVariable.dicts('flow', ((p, d) for p in plants for d in dcs), lowBound=0)
    y_dallas = pulp.LpVariable('y_Dallas', cat='Binary')
    y_chicago = pulp.LpVariable('y_Chicago', cat='Binary')

    prob += pulp.lpSum(cost[p][d] * x[p, d] for p in plants for d in dcs)

    # Demands
    for d in dcs:
        prob += pulp.lpSum(x[p, d] for p in plants) >= dem[d]

    # Existing capacities
    prob += pulp.lpSum(x['Miami', d] for d in dcs) <= cap['Miami']
    prob += pulp.lpSum(x['Tempe', d] for d in dcs) <= cap['Tempe']
    prob += pulp.lpSum(x['Columbus', d] for d in dcs) <= cap['Columbus']

    # Candidate expansion capacities linked to binary decision variables
    prob += pulp.lpSum(x['Dallas', d] for d in dcs) <= cap['Dallas'] * y_dallas
    prob += pulp.lpSum(x['Chicago', d] for d in dcs) <= cap['Chicago'] * y_chicago

    # Expansion constraint: open exactly 1 plant
    prob += y_dallas + y_chicago == 1

    prob.solve(pulp.PULP_CBC_CMD(msg=False))

    print(f"Optimal Expansion Decision: Dallas={int(round(pulp.value(y_dallas)))}, Chicago={int(round(pulp.value(y_chicago)))}")
    print(f"Optimal Transportation Cost: ${pulp.value(prob.objective):,.2f}")
    for p in plants:
        for d in dcs:
            val = pulp.value(x[p, d])
            if val > 0:
                print(f"  {p:<10} -> {d:<10}: {val:6,.0f} units @ ${cost[p][d]:.2f}/unit = ${val*cost[p][d]:,.2f}")


# ==============================================================================
# 3. LOCATION FACTOR RATING
# ==============================================================================
def solve_factor_rating():
    print("\n" + "=" * 80)
    print("3. LOCATION FACTOR RATING TECHNIQUE")
    print("=" * 80)

    factors = [
        ('Land & Site Development Cost', 0.25, [60, 85, 80, 75]),
        ('Highway & Expressway Connectivity', 0.20, [90, 80, 70, 85]),
        ('Power grid reliability', 0.20, [85, 75, 70, 90]),
        ('Availability of skilled labor pool', 0.15, [95, 65, 60, 70]),
        ('Local tax incentives & subsidies', 0.10, [65, 90, 85, 75]),
        ('Digital & Telecom infrastructure', 0.10, [90, 70, 75, 80])
    ]
    cities = ['Pune', 'Nagpur', 'Indore', 'Vadodara']

    scores = {city: 0.0 for city in cities}
    for factor, weight, vals in factors:
        for idx, city in enumerate(cities):
            scores[city] += weight * vals[idx]

    print(f"{'Factor':<36} {'Weight':<8} " + " ".join([f"{c:>10}" for c in cities]))
    print("-" * 80)
    for factor, weight, vals in factors:
        print(f"{factor:<36} {weight:<8.2f} " + " ".join([f"{v:>10.1f}" for v in vals]))
    print("-" * 80)
    print(f"{'Total Weighted Score':<36} {sum(w for _, w, _ in factors):<8.2f} " + " ".join([f"{scores[c]:>10.2f}" for c in cities]))

    ranking = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    print("\nRanking:")
    for rank, (city, score) in enumerate(ranking, 1):
        print(f"  Rank {rank}: {city:<10} with score {score:.2f}")


# ==============================================================================
# 4. CENTER OF GRAVITY (COG) TECHNIQUE
# ==============================================================================
def solve_cog():
    print("\n" + "=" * 80)
    print("4. CENTER OF GRAVITY (COG) TECHNIQUE")
    print("=" * 80)

    nodes = [
        ('Bengaluru', 150.0, 200.0, 1200.0),
        ('Mysore', 100.0, 150.0, 450.0),
        ('Chennai', 450.0, 220.0, 1500.0),
        ('Coimbatore', 200.0, 80.0, 800.0),
        ('Tirupati', 380.0, 260.0, 600.0)
    ]

    total_w = sum(w for _, _, _, w in nodes)
    total_wx = sum(w * x for _, x, _, w in nodes)
    total_wy = sum(w * y for _, _, y, w in nodes)

    cog_x = total_wx / total_w
    cog_y = total_wy / total_w

    print(f"{'Location':<14} {'X (Xi)':<10} {'Y (Yi)':<10} {'Demand (Wi)':<12} {'Weighted X':<14} {'Weighted Y':<14}")
    print("-" * 76)
    for name, x, y, w in nodes:
        print(f"{name:<14} {x:<10.1f} {y:<10.1f} {w:<12.1f} {w*x:<14.1f} {w*y:<14.1f}")
    print("-" * 76)
    print(f"{'Total':<14} {'-':<10} {'-':<10} {total_w:<12.1f} {total_wx:<14.1f} {total_wy:<14.1f}")
    print(f"\nOptimal Coordinates for New Central Facility:")
    print(f"  X* = {total_wx:.1f} / {total_w:.1f} = {cog_x:.2f}")
    print(f"  Y* = {total_wy:.1f} / {total_w:.1f} = {cog_y:.2f}")
    print(f"  Optimal Location (X*, Y*) = ({cog_x:.2f}, {cog_y:.2f})")


# ==============================================================================
# 5. LOAD-DISTANCE (LD) TECHNIQUE
# ==============================================================================
def solve_load_distance():
    print("\n" + "=" * 80)
    print("5. LOAD-DISTANCE (LD) TECHNIQUE")
    print("=" * 80)

    demand_nodes = [
        ('Indiranagar', 15.0, 20.0, 45.0),
        ('Whitefield', 25.0, 22.0, 28.0),
        ('Koramangala', 12.0, 14.0, 30.0),
        ('Electronic city', 14.0, 5.0, 49.0),
        ('Yelahanka', 10.0, 30.0, 55.0)
    ]

    candidates = [
        ('Hebbal', 12.0, 28.0),
        ('Marathahalli', 20.0, 18.0),
        ('Silk board', 13.0, 12.0)
    ]

    print("Step 1: Euclidean Distance Matrix:")
    print(f"{'Candidate Site':<16} " + " ".join([f"{name:>15}" for name, _, _, _ in demand_nodes]))
    print("-" * 95)
    ld_scores = {}
    for c_name, cx, cy in candidates:
        dists = []
        ld = 0.0
        for d_name, dx, dy, load in demand_nodes:
            dist = math.sqrt((cx - dx)**2 + (cy - dy)**2)
            dists.append(dist)
            ld += dist * load
        ld_scores[c_name] = ld
        print(f"{c_name:<16} " + " ".join([f"{d:>15.4f}" for d in dists]))

    print("\nStep 2: Load-Distance Scores:")
    for c_name, ld in ld_scores.items():
        print(f"  {c_name:<16}: LD Score = {ld:8.4f}")

    best_site = min(ld_scores.items(), key=lambda x: x[1])
    print(f"\nOptimal Candidate Site: {best_site[0]} with minimum LD score = {best_site[1]:.4f}")


# ==============================================================================
# 6. GENERATE HIGH-RESOLUTION FIGURES
# ==============================================================================
def generate_visualizations(scnd_res):
    print("\nGenerating visual diagrams and charts...")

    # --------------------------------------------------------------------------
    # Figure 1: Multi-Echelon SCND Network Flows
    # --------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(15, 9), dpi=300)
    ax.set_facecolor('#fcfdfd')

    # Column coordinates for echelons
    x_coords = {'supplier': 1.0, 'plant': 4.0, 'dc': 7.5, 'customer': 11.0}

    # Y positions
    sup_pos = {'Jamnagar': 7.5, 'Bhilai': 5.0, 'Bellary': 2.5}
    plant_pos = {'Sanand': 7.0, 'Sriperumbudur': 5.0, 'Pune': 3.0}
    dc_pos = {'Nagpur': 8.0, 'Bhiwandi': 6.25, 'Greater Noida': 4.5, 'Hosur': 2.75, 'Dankuni': 1.0}
    cust_pos = {'Delhi': 8.5, 'Mumbai': 7.0, 'Bengaluru': 5.5, 'Chennai': 4.0, 'Hyderabad': 2.5, 'Kolkata': 1.0}

    # Echelon headers
    headers = [
        ("Suppliers\n(120,000 Total Cap)", 1.0),
        ("Manufacturing Plants\n(120,000 Total Cap)", 4.0),
        ("Distribution Centres\n(135,000 Total Cap)", 7.5),
        ("Customer Demand Zones\n(72,000 Total Demand)", 11.0)
    ]
    for text, x in headers:
        ax.text(x, 9.8, text, ha='center', va='center', fontsize=12, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='#e8f0fe', edgecolor='#4285f4', lw=1.5))

    # Draw Supplier Nodes
    for s, y in sup_pos.items():
        used = sum(scnd_res['flow_sp'][(s, j)] for j in ['Sanand', 'Sriperumbudur', 'Pune'])
        cap = scnd_res['sup_cap'][s]
        color = '#1b5e20' if used > 0 else '#9e9e9e'
        ax.scatter(x_coords['supplier'], y, s=1600, color=color, zorder=4, edgecolor='black', lw=1.5)
        ax.text(x_coords['supplier'], y + 0.5, s, ha='center', va='bottom', fontsize=11, fontweight='bold', color='#1b5e20')
        ax.text(x_coords['supplier'], y, f"{used:,.0f}/\n{cap:,.0f}", ha='center', va='center', fontsize=9, color='white', fontweight='bold', zorder=5)

    # Draw Plant Nodes
    for p, y in plant_pos.items():
        is_open = scnd_res['y_plant'][p] == 1
        outflow = sum(scnd_res['flow_pd'][(p, k)] for k in scnd_res['y_dc'])
        cap = scnd_res['plant_cap'][p]
        color = '#0d47a1' if is_open else '#bdbdbd'
        ax.scatter(x_coords['plant'], y, s=2000, color=color, zorder=4, edgecolor='black', lw=1.5)
        status_txt = "OPEN" if is_open else "CLOSED"
        ax.text(x_coords['plant'], y + 0.55, f"{p} [{status_txt}]", ha='center', va='bottom', fontsize=11, fontweight='bold',
                color='#0d47a1' if is_open else '#757575')
        ax.text(x_coords['plant'], y, f"{outflow:,.0f}/\n{cap:,.0f}", ha='center', va='center', fontsize=9, color='white', fontweight='bold', zorder=5)

    # Draw DC Nodes
    for d, y in dc_pos.items():
        is_open = scnd_res['y_dc'][d] == 1
        outflow = sum(scnd_res['flow_dc'][(d, l)] for l in scnd_res['demand'])
        cap = scnd_res['dc_cap'][d]
        color = '#e65100' if is_open else '#bdbdbd'
        ax.scatter(x_coords['dc'], y, s=1800, color=color, zorder=4, edgecolor='black', lw=1.5)
        status_txt = "OPEN" if is_open else "CLOSED"
        ax.text(x_coords['dc'], y + 0.5, f"{d} [{status_txt}]", ha='center', va='bottom', fontsize=11, fontweight='bold',
                color='#e65100' if is_open else '#757575')
        ax.text(x_coords['dc'], y, f"{outflow:,.0f}/\n{cap:,.0f}", ha='center', va='center', fontsize=9, color='white', fontweight='bold', zorder=5)

    # Draw Customer Nodes
    for c, y in cust_pos.items():
        dem = scnd_res['demand'][c]
        ax.scatter(x_coords['customer'], y, s=1600, color='#4a148c', zorder=4, edgecolor='black', lw=1.5)
        ax.text(x_coords['customer'], y + 0.5, c, ha='center', va='bottom', fontsize=11, fontweight='bold', color='#4a148c')
        ax.text(x_coords['customer'], y, f"Req:\n{dem:,.0f}", ha='center', va='center', fontsize=9, color='white', fontweight='bold', zorder=5)

    # Draw Active Flows
    # S -> P
    for (s, p), flow in scnd_res['flow_sp'].items():
        if flow > 0:
            x1, y1 = x_coords['supplier'], sup_pos[s]
            x2, y2 = x_coords['plant'], plant_pos[p]
            lw = 1.5 + (flow / 40000.0) * 4.0
            ax.annotate("", xy=(x2-0.25, y2), xytext=(x1+0.25, y1),
                        arrowprops=dict(arrowstyle="->", color='#2e7d32', lw=lw, shrinkA=8, shrinkB=8, mutation_scale=18))
            ax.text((x1+x2)/2, (y1+y2)/2 + 0.15, f"{flow:,.0f}", ha='center', va='bottom', fontsize=9, fontweight='bold',
                    color='#1b5e20', bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#2e7d32', lw=0.8, alpha=0.9))

    # P -> D
    for (p, d), flow in scnd_res['flow_pd'].items():
        if flow > 0:
            x1, y1 = x_coords['plant'], plant_pos[p]
            x2, y2 = x_coords['dc'], dc_pos[d]
            lw = 1.5 + (flow / 30000.0) * 4.0
            ax.annotate("", xy=(x2-0.25, y2), xytext=(x1+0.25, y1),
                        arrowprops=dict(arrowstyle="->", color='#1565c0', lw=lw, shrinkA=8, shrinkB=8, mutation_scale=18))
            # Position labels at different fractional distances along arrow to avoid overlap
            if p == 'Sanand' and d == 'Dankuni':
                t_pos = 0.78  # Near Dankuni
            elif p == 'Sriperumbudur' and d == 'Hosur':
                t_pos = 0.32  # Near Sriperumbudur
            elif p == 'Sriperumbudur' and d == 'Dankuni':
                t_pos = 0.65
            else:
                t_pos = 0.50
            lx = x1 + t_pos * (x2 - x1)
            ly = y1 + t_pos * (y2 - y1)
            ax.text(lx, ly + 0.18, f"{flow:,.0f}", ha='center', va='bottom', fontsize=9, fontweight='bold',
                    color='#0d47a1', bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#1565c0', lw=0.8, alpha=0.95))

    # D -> C
    for (d, c), flow in scnd_res['flow_dc'].items():
        if flow > 0:
            x1, y1 = x_coords['dc'], dc_pos[d]
            x2, y2 = x_coords['customer'], cust_pos[c]
            lw = 1.5 + (flow / 18000.0) * 3.5
            ax.annotate("", xy=(x2-0.25, y2), xytext=(x1+0.25, y1),
                        arrowprops=dict(arrowstyle="->", color='#c2185b', lw=lw, shrinkA=8, shrinkB=8, mutation_scale=18))
            ax.text((x1+x2)/2, (y1+y2)/2 + 0.15, f"{flow:,.0f}", ha='center', va='bottom', fontsize=9, fontweight='bold',
                    color='#880e4f', bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#c2185b', lw=0.8, alpha=0.9))

    ax.set_xlim(0.0, 12.0)
    ax.set_ylim(0.0, 10.8)
    ax.axis('off')
    ax.set_title("NextDrive Motors - Optimal 4-Echelon Supply Chain Network Design\n(Total Cost: Rs. 79,480,000 | Total Demand Satisfied: 72,000 Units)",
                 fontsize=15, fontweight='bold', pad=20, color='#1a237e')

    plt.tight_layout()
    plt.savefig('fig1_scnd_network_flows.png', dpi=300)
    plt.close()
    print("  Saved fig1_scnd_network_flows.png")

    # --------------------------------------------------------------------------
    # Figure 2: SCND Cost Breakdown
    # --------------------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=300)

    # Left: Pie chart Fixed vs Variable
    labels_pie = [f"Fixed Facility Costs\nRs. {scnd_res['fixed_plant'] + scnd_res['fixed_dc']:,.0f}\n(89.33%)",
                  f"Transportation Costs\nRs. {scnd_res['trans_sp'] + scnd_res['trans_pd'] + scnd_res['trans_dc']:,.0f}\n(10.67%)"]
    sizes_pie = [scnd_res['fixed_plant'] + scnd_res['fixed_dc'],
                 scnd_res['trans_sp'] + scnd_res['trans_pd'] + scnd_res['trans_dc']]
    colors_pie = ['#1a73e8', '#f2994a']
    ax1.pie(sizes_pie, labels=labels_pie, colors=colors_pie, autopct='', startangle=140,
            textprops={'fontsize': 11, 'fontweight': 'bold'}, explode=(0.05, 0.05),
            wedgeprops={'edgecolor': 'white', 'linewidth': 2})
    ax1.set_title("Fixed Facility Opening vs.\nVariable Transportation Costs", fontsize=13, fontweight='bold', pad=15)

    # Right: Bar chart of cost components
    components = [
        'Plant Fixed Cost\n(Sanand + Sriperumbudur)',
        'DC Fixed Cost\n(Nagpur + Hosur + Dankuni)',
        'Plant -> DC\nFreight',
        'DC -> Customer\nFreight',
        'Supplier -> Plant\nFreight'
    ]
    values = [
        scnd_res['fixed_plant'] / 1e6,
        scnd_res['fixed_dc'] / 1e6,
        scnd_res['trans_pd'] / 1e6,
        scnd_res['trans_dc'] / 1e6,
        scnd_res['trans_sp'] / 1e6
    ]
    colors_bar = ['#1565c0', '#42a5f5', '#ff9800', '#f57c00', '#4caf50']
    bars = ax2.barh(components, values, color=colors_bar, edgecolor='black', linewidth=0.8)
    ax2.set_xlabel('Cost (in Million INR)', fontsize=11, fontweight='bold')
    ax2.set_title('Breakdown of Supply Chain Cost Elements', fontsize=13, fontweight='bold', pad=15)
    for bar in bars:
        w = bar.get_width()
        ax2.text(w + 0.8, bar.get_y() + bar.get_height()/2, f"Rs. {w:.2f} M",
                 va='center', ha='left', fontsize=10, fontweight='bold')
    ax2.set_xlim(0, 55)
    ax2.grid(axis='x', linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.savefig('fig2_scnd_cost_breakdown.png', dpi=300)
    plt.close()
    print("  Saved fig2_scnd_cost_breakdown.png")

    # --------------------------------------------------------------------------
    # Figure 3: Capacity Utilization
    # --------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(12, 6), dpi=300)
    facilities = ['Jamnagar\n(Sup)', 'Bhilai\n(Sup)', 'Bellary\n(Sup)',
                  'Sanand\n(MP)', 'Sriperumbudur\n(MP)', 'Pune\n(MP)',
                  'Nagpur\n(DC)', 'Bhiwandi\n(DC)', 'Gr. Noida\n(DC)', 'Hosur\n(DC)', 'Dankuni\n(DC)']
    capacities = [40, 45, 35, 40, 35, 45, 30, 35, 25, 25, 20]
    utilized = [40, 0, 32, 40, 32, 0, 30, 0, 0, 25, 17]

    x = np.arange(len(facilities))
    width = 0.38

    rects1 = ax.bar(x - width/2, capacities, width, label='Rated Capacity', color='#cfd8dc', edgecolor='black', lw=0.8)
    rects2 = ax.bar(x + width/2, utilized, width, label='Utilized Volume', color='#2e7d32', edgecolor='black', lw=0.8)

    ax.set_ylabel('Volume (Thousands of Units)', fontsize=11, fontweight='bold')
    ax.set_title('NextDrive Motors - Facility Capacity vs. Utilized Throughput', fontsize=14, fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(facilities, fontsize=10)
    ax.legend(frameon=True, facecolor='white', edgecolor='#cccccc', fontsize=11)
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    for i, u in enumerate(utilized):
        cap = capacities[i]
        pct = (u / cap) * 100
        if u > 0:
            ax.text(x[i] + width/2, u + 0.8, f"{pct:.0f}%", ha='center', va='bottom', fontsize=9, fontweight='bold', color='#1b5e20')
        else:
            ax.text(x[i] + width/2, 1.2, "0%", ha='center', va='bottom', fontsize=9, fontweight='bold', color='#c62828')

    plt.tight_layout()
    plt.savefig('fig3_scnd_capacity_utilization.png', dpi=300)
    plt.close()
    print("  Saved fig3_scnd_capacity_utilization.png")

    # --------------------------------------------------------------------------
    # Figure 4: Spatial CoG & Load-Distance Plots
    # --------------------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7), dpi=300)

    # Left: Center of Gravity
    nodes_cog = [
        ('Bengaluru', 150.0, 200.0, 1200.0),
        ('Mysore', 100.0, 150.0, 450.0),
        ('Chennai', 450.0, 220.0, 1500.0),
        ('Coimbatore', 200.0, 80.0, 800.0),
        ('Tirupati', 380.0, 260.0, 600.0)
    ]
    cog_x, cog_y = 283.08, 188.46

    for name, x, y, w in nodes_cog:
        ax1.scatter(x, y, s=w/2.0, color='#1565c0', alpha=0.7, edgecolors='black', lw=1.2)
        ax1.text(x, y + 10, f"{name}\n({w:.0f}u)", ha='center', va='bottom', fontsize=9, fontweight='bold', color='#0d47a1')

    ax1.scatter(cog_x, cog_y, s=350, color='#d32f2f', marker='*', edgecolors='black', lw=1.5, zorder=5, label=f'Optimal CoG\n({cog_x:.2f}, {cog_y:.2f})')
    ax1.set_title("Center of Gravity (CoG) Technique\nSouth India Demand Nodes & Optimal Facility", fontsize=12, fontweight='bold')
    ax1.set_xlabel("X Coordinate", fontsize=10, fontweight='bold')
    ax1.set_ylabel("Y Coordinate", fontsize=10, fontweight='bold')
    ax1.grid(True, linestyle='--', alpha=0.5)
    ax1.legend(loc='lower right', frameon=True)

    # Right: Load-Distance Technique
    dem_ld = [
        ('Indiranagar', 15.0, 20.0, 45.0),
        ('Whitefield', 25.0, 22.0, 28.0),
        ('Koramangala', 12.0, 14.0, 30.0),
        ('Electronic city', 14.0, 5.0, 49.0),
        ('Yelahanka', 10.0, 30.0, 55.0)
    ]
    cand_ld = [
        ('Hebbal', 12.0, 28.0, 2492.20),
        ('Marathahalli', 20.0, 18.0, 2250.65),
        ('Silk board', 13.0, 12.0, 2225.67)
    ]

    for name, x, y, load in dem_ld:
        ax2.scatter(x, y, s=load * 7, color='#7b1fa2', alpha=0.6, edgecolors='black', lw=1.2)
        ax2.text(x, y + 1.2, f"{name}\n({load:.0f}t)", ha='center', va='bottom', fontsize=8, fontweight='bold', color='#4a148c')

    for name, x, y, score in cand_ld:
        color = '#2e7d32' if name == 'Silk board' else '#ef6c00'
        marker = 'D' if name == 'Silk board' else 's'
        ax2.scatter(x, y, s=180, color=color, marker=marker, edgecolors='black', lw=1.5, zorder=5)
        ax2.text(x, y - 1.8, f"{name}\nLD={score:.1f}", ha='center', va='top', fontsize=9, fontweight='bold', color=color)

    ax2.set_title("Load-Distance Optimization Technique\nMicro-Fulfilment Nodes vs. Warehouse Candidates", fontsize=12, fontweight='bold')
    ax2.set_xlabel("X Coordinate", fontsize=10, fontweight='bold')
    ax2.set_ylabel("Y Coordinate", fontsize=10, fontweight='bold')
    ax2.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.savefig('fig4_spatial_cog_and_ld.png', dpi=300)
    plt.close()
    print("  Saved fig4_spatial_cog_and_ld.png")

    # --------------------------------------------------------------------------
    # Figure 5: Location Factor Rating Comparison
    # --------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(12, 6), dpi=300)
    criteria = [
        'Land & Site Dev.\n(25%)',
        'Highway Connect.\n(20%)',
        'Power Reliability\n(20%)',
        'Skilled Labor\n(15%)',
        'Tax Incentives\n(10%)',
        'Digital Infra.\n(10%)',
        'TOTAL WEIGHTED\nSCORE'
    ]
    pune = [60, 90, 85, 95, 65, 90, 79.75]
    nagpur = [85, 80, 75, 65, 90, 70, 78.00]
    indore = [80, 70, 70, 60, 85, 75, 73.00]
    vadodara = [75, 85, 90, 70, 75, 80, 79.75]

    x = np.arange(len(criteria))
    width = 0.2

    ax.bar(x - 1.5*width, pune, width, label='Pune (79.75)', color='#1565c0', edgecolor='black', lw=0.6)
    ax.bar(x - 0.5*width, nagpur, width, label='Nagpur (78.00)', color='#f57c00', edgecolor='black', lw=0.6)
    ax.bar(x + 0.5*width, indore, width, label='Indore (73.00)', color='#757575', edgecolor='black', lw=0.6)
    ax.bar(x + 1.5*width, vadodara, width, label='Vadodara (79.75)', color='#2e7d32', edgecolor='black', lw=0.6)

    ax.set_ylabel('Rating Score (out of 100)', fontsize=11, fontweight='bold')
    ax.set_title('Location Factor Rating Comparison Across Candidate Assembly Sites', fontsize=14, fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(criteria, fontsize=9.5)
    ax.set_ylim(40, 105)
    ax.legend(frameon=True, facecolor='white', edgecolor='#cccccc', fontsize=10)
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.savefig('fig5_factor_rating_comparison.png', dpi=300)
    plt.close()
    print("  Saved fig5_factor_rating_comparison.png")


# ==============================================================================
# MAIN RUNNER
# ==============================================================================
if __name__ == '__main__':
    scnd_res = solve_scnd(facility_balance=True)
    solve_tm()
    solve_factor_rating()
    solve_cog()
    solve_load_distance()
    generate_visualizations(scnd_res)
    print("\nAll assignment models solved successfully and figures generated!")

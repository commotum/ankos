# RoPE as Runtime Address Space — Experiment Overview

## 1. Original Experiment

**Setup**
- Controlled **next-state prediction benchmark** using small executable worlds:
  - 0D recurrences  
  - 1D cellular automata  
  - 2D grids  
  - 3D voxel systems
- Inputs are **flattened into sequences**.
- Each sequence is prefixed with a single **<Domain> token**.
- Task: predict **next state for every cell/token**.

**Goal**
- Compare positional encodings under tightly controlled conditions:
  - Scalar RoPE
  - Rank-matched Axial-RoPE
  - 4D Axial-RoPE
  - MonSTER variants

---

## 2. Key Result

**Observed pattern**
- **Scalar RoPE dominates**:
  - Best training loss
  - Best eval loss
  - Strong performance across domains (even multi-domain)

- **Until OOD-Scale**
  - When domain size changes (e.g., grid width/height):
    - RoPE performance **collapses**
    - Aggregate ranking drops sharply

- **Axial-RoPE**
  - Worse in-distribution
  - More stable under **scale shifts**
  - Overtakes RoPE in:
    - t+2D
    - t+3D
  - Still weaker in:
    - t+0D
    - t+1D

**Interpretation**
- RoPE is extremely strong **within a fixed address regime**
- EVEN WHEN THERE ARE MANY FIXED ADDRESSES ie MULTIDOMAIN
- But fails when **address arithmetic changes with scale**

---

## 3. New Hypothesis

> **RoPE behaves less like a coordinate system and more like a high-capacity address space (RAM-like).**

More specifically:

- RoPE provides a **dense 1D address space**
- The model learns **address arithmetic tied to training scale**
- The **<Domain> token already shows partial conditioning ability**

### Core Question

> Can a transformer **reinterpret the same 1D RoPE address space as multiple physical coordinate systems** using only runtime metadata?

---

## 4. New Experimental Setup (Ankos Suite)

### Key Idea

Replace:
- fixed scale + minimal domain token

With:
- **broad training distribution + explicit schema metadata**

---

### Input Format

Each sequence is prefixed with structured metadata:

```
<DOMAIN=t+2d> <X=15> <Y=15> <Z=1>
```

This defines:
- coordinate system
- scale
- evolution horizon
- boundary conditions

---

### Training Distribution

Train across **wide variation**:

- Domain types:
  - 0D / 1D / 2D / 3D / mixed

- Scale:
  - multiple grid sizes (not fixed)

- Frontier / horizon:
  - multiple prediction depths

- Boundary conditions:
  - fixed, wrap, absorbing, etc.

- Neighborhood rules:
  - varied local update rules

---

### Evaluation Regimes

- **In-distribution**
- **Interpolation (new sizes within range)**
- **OOD-Scale (larger or unseen shapes)**

---

### Critical Ablations

| Condition | Purpose |
|----------|--------|
| Domain token only | baseline |
| + scale metadata | test conditioning |
| wrong scale metadata | causal test |
| no metadata | pure address learning |
| Axial / 4D Axial | coordinate baseline |

---

## Expected Outcome

If hypothesis holds:

- RoPE + metadata:
  - retains strong ID performance
  - **recovers OOD-scale performance**

This would imply:

> A single 1D RoPE space can act as a **universal address interface**,  
> with geometry dynamically **compiled from metadata at runtime**

---

## Big Picture

This reframes positional encoding:

- Not just:
  - **coordinate priors (Axial-RoPE)**

- But also:
  - **learned address systems (RoPE)**

And asks:

> Do we actually need coordinate-specific positional encodings  
> to build multi-domain, multi-scale, spatiotemporal transformers?

---

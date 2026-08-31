# 🎨 UI/UX Design System & Style Guide (Zen Minimalist)

This document specifies the visual identity, 2-tier layout architecture, color palette, typography, and component specs for the **Japanese Foods IR** web interface.

---

## 1. Visual Identity & Zen Minimalist Philosophy

The redesigned interface adopts a **Zen Kyoto Minimalist** aesthetic that eliminates visual clutter and button collision:
- **2-Tier App Header**: Separates Brand & System Utilities (Top) from Segmented Navigation Tabs (Bottom) to guarantee **zero button overlap** across all viewport widths.
- **Harmonious Palette**: Deep obsidian lacquer (`#0a0d14`), refined slate borders (`rgba(255, 255, 255, 0.08)`), Vermilion Red (`#ff4d4f`), Cherry Blossom Pink (`#f472b6`), and Emerald Matcha (`#10b981`).
- **De-Cluttered Layouts**: Spacious cards, generous whitespace (`padding: 1.5rem+`), compact notification badges, and clean typography.

---

## 2. Color Palette & Surface Tokens

### 2.1 Core Palette Tokens
```css
--accent-red: #ff4d4f;       /* Torii Vermilion Red */
--accent-crimson: #d9363e;   /* Deep Crimson */
--accent-sakura: #f472b6;    /* Sakura Blossom Pink */
--accent-amber: #f59e0b;     /* Miso / Sesame Amber */
--accent-matcha: #10b981;    /* Matcha Emerald Green */
--accent-nori: #06b6d4;      /* Ocean Nori Cyan */
--accent-purple: #8b5cf6;    /* Japanese Eggplant */
```

### 2.2 Theme Surface Tokens

| Token | Dark Mode (`theme-dark`) | Light Mode (`theme-light`) |
|---|---|---|
| `--bg-primary` | `#0a0d14` (Midnight Lacquer) | `#f8fafc` (Washi White) |
| `--bg-secondary`| `#111624` (Deep Slate) | `#ffffff` (Pure White) |
| `--bg-card` | `rgba(18, 23, 38, 0.72)` | `rgba(255, 255, 255, 0.9)` |
| `--border-color`| `rgba(255, 255, 255, 0.08)` | `rgba(226, 232, 240, 0.9)` |
| `--text-primary`| `#f8fafc` (Crisp Light) | `#0f172a` (Ink Sumi) |
| `--text-secondary`| `#94a3b8` (Muted Slate) | `#475569` (Charcoal) |

---

## 3. 2-Tier Header Layout Architecture

```
+-------------------------------------------------------------------------+
| [🍣 JAPANESE FOODS IR · 日本料理]                  [🇹🇭 ภาษาไทย]  [🌙]   |  <- Top Bar: Branding & Utilities
+-------------------------------------------------------------------------+
|  (🔍 ค้นหา)  (🍱 วัตถุดิบ)  (📊 คลัสเตอร์)  (📖 ดัชนี)  (📈 ประเมิน) (⚙️ ข้อมูล) |  <- Bottom Bar: Segmented Tabs
+-------------------------------------------------------------------------+
```

- **Top Row (`.header-top-row`)**: Houses the Brand identity on the left, and Language Switcher Pill + Dark/Light Theme toggle button on the right.
- **Bottom Row (`.nav-tabs-wrapper`)**: Centered, horizontally scrollable segmented pill navigation bar. No buttons ever collide or wrap over tabs.

---

## 4. Component Hierarchy

### 4.1 Search Hero Card
- Prominent search input with prefix icon and quick clear button (`✕`).
- Clean category filter chips (`All`, `Ramen`, `Curry`, `Meat`, `Donburi`, `Tofu`, `Dessert`).
- Compact PRF expansion notification pill.

### 4.2 Zen Cards (`.zen-card`)
- Clean rounded corners (`18px`), backdrop filter blur (`20px`), subtle border, and soft hover elevation.

### 4.3 Interactive Tooltips (`.ir-tooltip-popup`)
- Non-intrusive floating popup triggered on `ℹ️` icon click explaining IR mathematical principles.

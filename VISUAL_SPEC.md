# Visual Spec Reference

## Background Mode Badge
```
┌────────────────────────────────────────────────┐
│                   Device Top                    │
├────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────┐ │ ← 1rem from top
│  │ 📥 Downloading Reel… processing          │ │   + safe-area-top
│  └──────────────────────────────────────────┘ │
│                                                │
│            (Background continues              │
│             normal Instagram flow)            │
│                                                │
└────────────────────────────────────────────────┘

Specs:
- Height: 48px
- Width: calc(100% - 2rem), max 520px
- Padding: 0 1rem
- Background: linear-gradient(135deg, #8A3AB9, #BC2A8D)
- Color: white
- Border-radius: 8px
- Font: 15px, weight 600
- Shadow: 0 6px 18px rgba(0,0,0,0.12)
- Animation: slide-down 200ms, fade-out 150ms
- Duration: visible for 1.4s total
```

## Normal Mode Bottom Sheet
```
┌────────────────────────────────────────────────┐
│                  Device Top                     │
│                                                 │
│              (Dimmed backdrop                   │
│               rgba(0,0,0,0.5))                  │
│                                                 │
├─────────────────────────────────────────────────┤
│  ━━━━━━━ ← Handle bar                          │
│                                                 │
│  Ready to Download                              │
│  ┌───────────────────────────────────────────┐ │
│  │ instagram.com/reel/ABC123...              │ │
│  └───────────────────────────────────────────┘ │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │          Download Now                     │ │ ← Primary CTA
│  └───────────────────────────────────────────┘ │
│  ┌───────────────────────────────────────────┐ │
│  │             Cancel                        │ │ ← Secondary
│  └───────────────────────────────────────────┘ │
│                                                 │
└─────────────────────────────────────────────────┘

Specs:
- Position: fixed, bottom 0
- Width: 100%
- Max-height: 65vh (70vh mobile)
- Padding: 1.5rem (1.25rem mobile)
- Background: var(--surface-card)
- Border-radius: 24px 24px 0 0
- Shadow: 0 -10px 40px rgba(0,0,0,0.3)
- Animation: slide-up 280ms cubic-bezier(0.32, 0.72, 0, 1)
- Handle: 40px × 4px, centered top
```

## Homepage Layout
```
┌──────────────────────────────────────────────┐
│  [IG] Reel DL               [🌙 Theme]       │ ← Nav bar
├──────────────────────────────────────────────┤
│                                              │
│   ┌────────────────────────────────────┐    │
│   │  ⚬ ⚬  (Floating shapes)           │    │
│   │                                    │    │
│   │  Save Instagram Reels              │    │ ← Hero title
│   │  Paste a public Reel link and     │    │ ← Lead
│   │  download instantly                │    │
│   │                                    │    │
│   │  ┌──────────────────┬──────────┐  │    │
│   │  │ 🔗 instagram...  │ Download │  │    │ ← Input + Button
│   │  └──────────────────┴──────────┘  │    │
│   │                                    │    │
│   │  [? Error message if any]         │    │
│   │                                    │    │
│   └────────────────────────────────────┘    │
│                                              │
│              ❤ by Hiba                       │ ← Footer
└──────────────────────────────────────────────┘

Removed:
- ❌ Badge ("Modern · Secure · Fast")
- ❌ Chips (3× feature bullets)
- ❌ Helper buttons (Paste, Demo)
- ❌ Loading state UI
- ❌ Tips/callout section
```

## Result Page Layout
```
┌──────────────────────────────────────────────┐
│  [IG] Reel DL               [🌙 Theme]       │
├──────────────────────────────────────────────┤
│                                              │
│   ┌────────────────────────────────────┐    │
│   │  ✓  Ready                          │    │ ← Status chip
│   │     Download Complete              │    │ ← Title
│   │                                    │    │
│   │  ┌──────────────────────────────┐  │    │
│   │  │     [Video Preview]          │  │    │ ← Video player
│   │  └──────────────────────────────┘  │    │
│   │                                    │    │
│   │  [A] @username                     │    │ ← Author
│   │      Title of reel                 │    │
│   │                                    │    │
│   │  ┌─────────────┐ ┌────────┐       │    │
│   │  │Download MP4 │ │Copy    │ [New] │    │ ← Action buttons
│   │  └─────────────┘ └────────┘       │    │
│   │                                    │    │
│   │  [☑ Auto-download] Starting...    │    │ ← Toggle + status
│   │                                    │    │
│   │  Duration  Size   Likes   Views    │    │ ← Metadata (conditional)
│   │  01:23     2.4MB  1.2K     15K     │    │
│   │                                    │    │
│   └────────────────────────────────────┘    │
│                                              │
└──────────────────────────────────────────────┘

Removed:
- ❌ Tips sidebar
- ❌ FAQ section
- ❌ Caption card
- ❌ Instagram/direct links
- ❌ "Powered by" links
- ❌ Extra callouts
- ❌ Published date (unless explicitly needed)
```

## Color Palette
```
Primary Gradient:   #8A3AB9 → #BC2A8D → #FCCC63
Primary Solid:      #0095F6
Success:            #00BF89
Text Primary:       #101828
Text Secondary:     #475467
Text Muted:         #667085
Border Subtle:      rgba(15, 23, 42, 0.08)
Surface Card:       rgba(255, 255, 255, 0.95)

Dark Mode:
Surface Card:       rgba(15, 15, 25, 0.85)
Text Primary:       #F3F4F6
Text Secondary:     #CBD5F5
```

## Typography Scale
```
Hero Title:    clamp(2.2rem, 4vw, 3.4rem) / 700
Section Title: clamp(1.1rem, 1.9vw, 1.45rem) / 600
Lead:          clamp(1rem, 1.8vw, 1.15rem) / 400
Body:          1rem / 400
Badge:         15px / 600
Small:         0.85–0.9rem / 500
```

## Spacing System
```
xs:  0.25rem   (4px)
sm:  0.5rem    (8px)
md:  1rem      (16px)
lg:  1.5rem    (24px)
xl:  2rem      (32px)
2xl: 3rem      (48px)

Component gaps:
- Form elements:     0.75rem
- Card sections:     1.5–2rem
- Metadata grid:     1rem
- Button groups:     0.75rem
```

## Border Radius
```
sm:  8px    (badge, small pills)
md:  12–16px (inputs, cards)
lg:  24px   (panels, sheets)
full: 999px (pills, toggles)
```

## Animation Timing
```
Fast:    150–200ms (fade, micro-interactions)
Normal:  240–280ms (slides, transitions)
Slow:    300–400ms (complex movements)

Easing:
- Slide-in:  cubic-bezier(0.32, 0.72, 0, 1)
- Fade:      ease-out
- General:   ease
```

## Breakpoints
```
Mobile:    < 640px
Tablet:    640–1024px
Desktop:   > 1024px

Key changes at mobile:
- Single-column layouts
- Full-width buttons
- Reduced padding (1rem → 0.85rem)
- Smaller font sizes (0.95rem)
- Stacked form inputs
```

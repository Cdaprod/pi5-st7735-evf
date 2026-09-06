# Approved ST7735 UI specification

The approved reference board is the current visual direction and product UI
specification for the 128×128 ST7735 prototype. It is not a disposable mockup.
All coordinates are authored at the panel's native resolution.

## Visual system

The interface uses black, clean white DejaVu Sans typography, thin gray rules,
and sparse camera-monitor telemetry. Green means active/locked/OK, yellow means
waiting or reconfiguration, red means error or focus peaking, blue means
selection, and gray means unavailable. Font roles are centralized as tiny,
small, body, header, and large, with Pillow's built-in font as a safe fallback.

Icons are drawn from Pillow lines, rectangles, polygons, ellipses, and arcs. The
set contains camera/video, connected and disconnected displays, gear,
information, warning, mode-change arrows, power, battery, and signal status. No
external icon package or web asset is required.

## Native layout

Live View reserves pixels 0–15 for status, 16–99 for the source image, and
100–127 for the HUD. The image is aspect-preserving and center-cropped into the
viewport. Four short green corner guides frame it. The HUD contains FPS, an
actual luminance histogram, and concise ISO/ZEBRA status. Focus edges are thin
red accents; zebra uses alternating diagonal marks above its threshold.

Menus use a 19-pixel icon/header area and 15-pixel rows. The active row is a
full-width blue band. Main menu order is Focus Peaking, Zebra, Crosshair,
Histogram, Brightness, Display Rotation, and System Info. Focus Peaking detail
contains Enable, Color, Threshold, and Thickness plus an analyzed live preview.

## Screen and runtime states

| Runtime condition | Approved screen |
|---|---|
| Startup | EVF / PI5 + X1301 splash |
| `DISCONNECTED` | No Signal |
| `PRESENT_NO_SIGNAL` | HDMI Detected / animated waiting dots |
| `LOCKED`, capture opening | Mode Change |
| `LOCKED`, streaming | Live View |
| Focus assist selected | Live View with red peaking |
| `MODE_CHANGE` | Mode Change with indeterminate yellow bar |
| Capture/runtime failure | Capture Error |
| Clean exit | Shutting Down |

Animations use elapsed-time phases and never sleep inside renderers. The capture
loop remains responsible for pacing, retry, and input servicing. System Info
takes resolution, rate, video node, and media node from current X1301 state.

## 128-pixel constraints

The complete diagnostic table cannot remain readable at once, so eight System
Info rows appear per scroll page. Header and HUD labels use compact typography,
and the focus preview is 120×32 pixels. These are spacing adjustments only;
hierarchy, content, semantics, and the approved visual language are preserved.

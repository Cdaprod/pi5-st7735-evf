# Contributing

Keep the hot frame path small and measurable.

For changes that affect rendering:

1. Test with `--no-display --preview-window`.
2. Test the ST7735 separately with `tools/display_test.py`.
3. Confirm the capture format with `tools/probe_capture.sh`.
4. Avoid adding blocking I/O inside the per-frame loop.
5. Preserve the `cskau/Python_ST7735` display API boundary unless a dedicated optimized backend is added.

# {{ realm("client") }} Paint
Utility wrappers around `surface`, `draw`, `render`, and `cam` APIs for common UI drawing patterns.

!!! info
	See [core/libraries/paint.lua](https://github.com/Buildstruct/bsa-platform-gmod/blob/develop/lua/bsa/core/libraries/paint.lua) for the actual design implementation.

## Functions

- `#!ts paint.color(r?: number | Color, g?: number, b?: number, a?: number)`\
	Sets active draw/text color and stores it in `paint._color`.

- `#!ts paint.rotation(w?: number, h?: number, r?: number)`\
	Pushes a rotated model matrix around `(w, h)` when `r` is provided.\
	Calling without `r` pops the matrix/filter stack.

- `#!ts paint.texture(path: string)`\
	Sets current surface texture from texture path.

- `#!ts paint.blur(x: number, y: number, w: number, h: number, passes?: number)`\
	Draws `pp/blurscreen` blur clipped to a scissor rectangle.

- `#!ts paint.blurpnl(panel: Panel, passes?: number)`\
	Draws panel-local blur by offsetting the full-screen blur texture.

## Rect

- `#!ts paint.rect.sweep(x: number, y: number, w: number, h: number, size: number, progress: number, rotation?: number)`\
	Draws a moving rotated sweep rectangle across a clipped region.

- `#!ts paint.rect.texture(x: number, y: number, w: number, h: number, rotation?: number)`\
	Draws textured rectangle, optionally rotated.

- `#!ts paint.rect.fill(x: number, y: number, w: number, h: number, rotation?: number)`\
	Draws filled rectangle, optionally rotated.

- `#!ts paint.rect.inline(x: number, y: number, w: number, h: number, thickness?: number, rotation?: number)`\
	Draws outline inside the rectangle bounds.

- `#!ts paint.rect.outline(x: number, y: number, w: number, h: number, thickness?: number, rotation?: number)`\
	Draws outline outside/around the rectangle bounds.

## Gradient
Directional helpers using VGUI gradient textures.

- `#!ts paint.gradient.single(x: number, y: number, w: number, h: number, rotation?: number)`\
	Draws default downward single gradient.

- `#!ts paint.gradient.double(x: number, y: number, w: number, h: number, colorA: Color, colorB: Color, rotation?: number)`\
	Draws base fill (`colorA`) + overlay gradient (`colorB`) downward.

- `#!ts paint.gradient.down.single(...)`
- `#!ts paint.gradient.down.double(...)`
- `#!ts paint.gradient.up.single(...)`
- `#!ts paint.gradient.up.double(...)`
- `#!ts paint.gradient.left.single(...)`
- `#!ts paint.gradient.left.double(...)`
- `#!ts paint.gradient.right.single(...)`
- `#!ts paint.gradient.right.double(...)`\
	Directional variants of `single`/`double`.

## Circ

- `#!ts paint.circ.fill(x: number, y: number, radius: number)`\
	Draws filled circle using a small 3D sphere trick.

- `#!ts paint.circ.inline(x: number, y: number, radius: number)`\
	Draws circle line at `radius - 1`.

- `#!ts paint.circ.outline(x: number, y: number, radius: number)`\
	Draws circle line at `radius`.

## Text

- `#!ts paint.text.font(name: string)`\
	Alias to `surface.SetFont`.

- `#!ts paint.text.size(...: string | Color): number, number`\
	Returns max width/height for provided text segments (supports `\n`).

- `#!ts paint.text.concat(...: any): string`\
	Concatenates string arguments only.

- `#!ts paint.text.absolute_size(...: string | Color): number[], number`\
	Returns per-line widths and total height.

- `#!ts paint.text.wrap(width: number, args: any[]): any[]`\
	Wraps string entries by width while preserving non-string entries in output.

- `#!ts paint.text.left(x: number, y: number, ...: string | Color)`\
	Draws multi-part colored text left aligned.

- `#!ts paint.text.center(x: number, y: number, ...: string | Color)`\
	Draws multi-part colored text centered per line.

- `#!ts paint.text.right(x: number, y: number, ...: string | Color)`\
	Draws multi-part colored text right aligned per line.

- `#!ts paint.text.scale(): number, number`\
	Returns text size of `"B"` for active font.

### Text.Outline

- `#!ts paint.text.outline.left(x: number, y: number, ...: string | Color)`\
	Draws black 1px four-corner outline, then foreground text.

- `#!ts paint.text.outline.center(x: number, y: number, ...: string | Color)`\
	Outlined centered variant.

- `#!ts paint.text.outline.right(x: number, y: number, ...: string | Color)`\
	Currently uses left-aligned outline behavior internally.

### Text.Format

- `#!ts paint.text.file(bytes: number): string`\
	Formats byte count to human readable unit (`B` to `EB`).

- `#!ts paint.text.duration(seconds: number): string`\
	Formats duration as `M:SS` or `H:MM:SS`.

- `#!ts paint.text.round(value: number, decimals?: number): number`\
	Rounds to decimal places.

- `#!ts paint.text.trailing(value: number, decimals?: number): string`\
	Rounded numeric string with fixed trailing decimals.

### Text.Await

- `#!ts paint.text.await.self(x: number, y: number, size: number, msg?: string, align?: "left" | "center" | "right", speed?: number)`\
	Animated ASCII loading bar based on `sin(SysTime() * speed)`.

- `#!ts paint.text.await.left(x: number, y: number, size: number, msg?: string, speed?: number)`
- `#!ts paint.text.await.center(x: number, y: number, size: number, msg?: string, speed?: number)`
- `#!ts paint.text.await.right(x: number, y: number, size: number, msg?: string, speed?: number)`\
	Alignment helpers for `await.self`.

### Text.Progress

- `#!ts paint.text.progress.self(x: number, y: number, size: number, delta: number, msg?: string, align?: "left" | "center" | "right")`\
	Draws ASCII progress bar from `delta` clamped to `0..1`.

- `#!ts paint.text.progress.left(x: number, y: number, size: number, delta: number, msg?: string)`
- `#!ts paint.text.progress.center(x: number, y: number, size: number, delta: number, msg?: string)`
- `#!ts paint.text.progress.right(x: number, y: number, size: number, delta: number, msg?: string)`\
	Alignment helpers for `progress.self`.

## Frame
Preset frame styles built from `rect` + `gradient` primitives.

- `#!ts paint.frame.inner(x: number, y: number, w: number, h: number)`\
	Dark panel with border, top gradient, and inline stroke.

- `#!ts paint.frame.button(x: number, y: number, w: number, h: number)`\
	Button style (same structure as `inner`).

- `#!ts paint.frame.button_hover(x: number, y: number, w: number, h: number)`\
	Hover variant with downward gradient.

- `#!ts paint.frame.box(x: number, y: number, w: number, h: number)`\
	Slightly brighter boxed panel style.

- `#!ts paint.frame.accent(x: number, y: number, w: number, h: number, r: number | Color, g?: number, b?: number, a?: number)`\
	Accent fill with upward gradient in provided color.

- `#!ts paint.frame.full(x: number, y: number, w: number, h: number, r: number | Color, g?: number, b?: number, a?: number)`\
	Composed style: `box` + 2px top accent strip.

# Why the recipe is what it is

Each rule came from something that went wrong while the first sets were being made.

| Tried | What happened | So now |
|---|---|---|
| Asking `image_gen` for a transparent background | It baked a heavy coloured glow around every shape, smeared into the artwork | Generate on flat white and build the transparency ourselves |
| Flat magenta background, keyed out | Works, but leaves colour fringes on edges and needs clean-up | White ground works once the art is one colour, because darkness maps directly to opacity |
| Two PNGs per scene, one per theme | Twice the files, CSS to swap them, and a recolouring step that speckled details | One mask per illustration, painted with `bg-ink` through CSS `mask-image`, so light and dark are automatic |
| A mascot character in every scene | Did not sit with the calm office-object set the docs and tutorials use | Objects only, no characters, people or faces |
| Describing the style in words only | Line weight and perspective drifted between images | Attach the app's own illustrations every time, `sheets.png` first |
| Geometric flat vector objects | Read as clip art | Slightly hand-made line art with rounded line ends |
| Hatching or textured shading | Turns to noise once masked at card size | White surfaces and one small solid shadow |

## Details worth keeping

- `make_mask.py` treats anything lighter than level 232 as fully transparent and anything darker than 45 as fully solid. White surfaces therefore become see-through and show the page colour behind them, which is what keeps the set calm in both themes.
- Illustrations are trimmed to their drawn area, then fitted with `mask-size: contain` so they stay centred at any box size.
- The masks are about 10 to 25 KB each, so there is no reason to compress further.

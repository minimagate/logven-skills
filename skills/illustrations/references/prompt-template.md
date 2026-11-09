# Prompt template

Fill in the `<...>` parts. Everything else is the wording that matches the approved set, so keep it as is. One `image_gen` call per image keeps each object distinct.

```text
Use your built-in image_gen tool to create <N> separate images, one image_gen call each. Every image is an opaque image on one perfectly flat, uniform pure white background, exactly #FFFFFF, edge to edge.

Input images: Images 1, 2 and 3 are the exact style reference, especially Image 1 (the tied stack of papers). Match their drawing style exactly: a single everyday object drawn in clean, confident, slightly hand-made black line art with one even medium line weight and rounded line ends, slight three-quarter perspective, all surfaces left white, no hatching and no texture, and one small solid black cast shadow tucked under the bottom-right edge of the object. Do not copy their objects; draw only the new object described below.

Use case: illustration-story
Asset type: <N> small minimal spot illustrations for <where they appear> on a product.
Style/medium: strictly monochrome line drawing. One single colour only, near-black ink #151619, on pure white. No colour of any kind and no grey fills, washes or gradients. Very minimal: one object (at most one small companion object), generous empty space, calm and friendly.
Composition/framing: landscape 3:2, one small self-contained object centred with a generous even margin, nothing touching the edges.

Image 1 of <N>, save as <name>.png. <Object: what it is, its angle, the one detail that carries the idea, what is deliberately not drawn.>

Image 2 of <N>, save as <name>.png. <Object.>

Colour rules, very important: only near-black ink and pure white. White areas must be exactly #FFFFFF.
Avoid: any colour, grey shading, gradients, textures, hatching, floor lines, background scenery, people, characters, faces, text, letters, numbers, logos, signatures, watermark, frames or borders.

After generating, copy the <N> final PNG files from your generated images folder into the current working directory with exactly those filenames. Do not change anything else. Finish by printing the file paths.
```

If an object carries text-like content (a newspaper, a form, a table), ask for solid bars, short lines or empty cells, and keep "text, letters, numbers" in the Avoid line.

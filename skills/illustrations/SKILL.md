---
name: illustrations
description: Generate new Logven spot illustrations with Codex in the app's fine-line office-object style and install them. Use whenever someone wants a new illustration, picture or drawing for a docs page, tutorial card, empty state, onboarding moment, progress or home page card, or wants to redo or vary the existing ones in app/assets/images/illustrations, even if they don't say "skill" or "Codex". Not for app icons (app/assets/images/icons) and not for the animated assistant blob.
---

# Illustrations

Spot drawings of single everyday objects: clean, even-weight black line art, white surfaces, one small solid shadow under the bottom-right edge. No mascot, no characters, no people. Codex draws them, a script turns each one into a single-colour mask, and the app paints that mask with the ink colour so it works in both themes.

The existing set in `app/assets/images/illustrations/` is the style reference. `sheets.png` (a tied stack of papers) is the primary one; `around.png` (desk with lamp) and `weekly-review.png` (desk calendar) are the usual companions.

Read `references/prompt-template.md` before writing a prompt. Read `references/scenes.md` when choosing an object. Read `references/lessons.md` before changing anything about the recipe.

## Workflow

1. **Agree the object.** One line per illustration: which object stands for the idea, and at most one small companion object. If the request is vague, propose objects from `references/scenes.md` rather than asking an open question.

2. **Make a working directory outside the repo** (the session scratchpad). Generated files stay there until they pass review.

3. **Write the prompt** to `prompt.txt` in that directory, from the template. Keep the style block word for word and change only the object paragraphs and filenames.

4. **Run Codex in the background**, since it takes a few minutes. The prompt must come before `-i`, because `-i` swallows every argument after it. Attach `sheets.png` first:

   ```sh
   I=<repo>/app/assets/images/illustrations
   codex exec "$(cat prompt.txt)" --skip-git-repo-check -s workspace-write -C "$PWD" \
     -i $I/sheets.png $I/around.png $I/weekly-review.png
   ```

5. **Convert each result:**

   ```sh
   mkdir -p out
   python3 -I <skill-dir>/scripts/make_mask.py <name>.png out/<name>
   ```

   This writes `out/<name>.png` (the mask) plus `-preview-light.png` and `-preview-dark.png`.

6. **Look at both previews of every image** next to `sheets.png`, and regenerate anything that fails:
   - Same line weight and hand as the reference set; no thicker or sketchier lines.
   - Surfaces white, no hatching, texture, grey or colour.
   - One small solid shadow at the bottom right, nothing else filled except deliberate solid details.
   - No people, faces, characters, text, letters or numbers.
   - Thin lines survive at small size. Mentally shrink it to about 128 by 80 pixels (the `h-20 w-32` box).

7. **Install:** copy `out/<name>.png` to `app/assets/images/illustrations/<name>.png` and render it with:

   ```erb
   <%= render "shared/illustration", name: "<name>" %>
   ```

   Size is set by `h-20 w-32` in `app/views/shared/_illustration.html.erb`; callers wrap it in a sized flex box when they need more room.

8. **Show the result:** say which files changed and open the previews with `open -a Preview`. If you cannot see the page in a browser, say so.

## When the style has to change

The files in `app/assets/images/illustrations/` define the style. If the team deliberately redraws the set, update the style block in the template to match and keep attaching the new primary reference first.

Attach only the app's own illustrations to the Codex call. Everything attached leaves the machine.

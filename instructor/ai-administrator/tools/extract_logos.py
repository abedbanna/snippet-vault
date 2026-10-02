#!/usr/bin/env python3
"""Pull the header logos out of page 1 of the curriculum PDF into brand/."""
import fitz, pathlib, sys
PDF = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path.home() / "Downloads" / "Course Curriculum_ AI Administrator.pdf"
OUT = pathlib.Path(__file__).resolve().parent.parent / "brand"; OUT.mkdir(exist_ok=True)
doc = fitz.open(PDF); page = doc[0]
infos = page.get_images(full=True)
for i, info in enumerate(infos):
    xref = info[0]; pix = fitz.Pixmap(doc, xref)
    if pix.n - pix.alpha >= 4: pix = fitz.Pixmap(fitz.csRGB, pix)
    rects = page.get_image_rects(xref)
    r = rects[0] if rects else None
    name = OUT / f"logo_{i}_x{int(r.x0) if r else 0}.png"
    pix.save(name)
    print(name.name, pix.width, pix.height, "at", r)
# also render the header strip as one image
clip = fitz.Rect(0, 0, page.rect.width, 95)
page.get_pixmap(matrix=fitz.Matrix(4, 4), clip=clip, alpha=False).save(OUT / "header_strip.png")
print("header_strip.png written")

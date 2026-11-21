from __future__ import annotations

from pathlib import Path

from PIL import Image


def apply_alpha(image_path: Path, mask_path: Path, output_path: Path) -> None:
    with Image.open(image_path) as source_image, Image.open(mask_path) as source_mask:
        if source_image.mode not in {"RGB", "RGBA"}:
            raise ValueError(
                f"Alpha application requires RGB or RGBA input, got {source_image.mode}. "
                "Convert color spaces explicitly before this command."
            )
        rgb = source_image if source_image.mode == "RGB" else source_image.convert("RGB")
        alpha = source_mask.convert("L")
        if alpha.size != rgb.size:
            alpha = alpha.resize(rgb.size, Image.Resampling.LANCZOS)
        red, green, blue = rgb.split()
        rgba = Image.merge("RGBA", (red, green, blue, alpha))
        output_path.parent.mkdir(parents=True, exist_ok=True)
        rgba.save(output_path, optimize=True)

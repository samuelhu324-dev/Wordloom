import argparse
import json
from pathlib import Path


def load_meta(meta_path: Path) -> dict:
    with meta_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_page(root: Path, filename: str) -> str:
    path = root / filename
    with path.open("r", encoding="utf-8") as f:
        return f.read().rstrip() + "\n"


def apply_template(template_path: Path, pages: list[str]) -> str:
    text = template_path.read_text(encoding="utf-8")
    # Very small placeholder engine: {{page_1}}, {{page_2}}, ...
    for idx, content in enumerate(pages, start=1):
        placeholder = f"{{{{page_{idx}}}}}"
        text = text.replace(placeholder, content)
    return text


def generate_cv(demo_id: str, variant_id: str) -> None:
    repo_root = Path(__file__).resolve().parents[2]
    cv_root = repo_root / "docs" / "demo" / demo_id / "_cv"
    meta_path = cv_root / f"{variant_id}-meta.json"

    if not meta_path.exists():
        raise SystemExit(f"Metadata file not found: {meta_path}")

    meta = load_meta(meta_path)

    # Resolve template
    templates_root = repo_root / "docs" / "demo" / "templates"
    template_path = templates_root / meta["template"]
    if not template_path.exists():
        raise SystemExit(f"Template file not found: {template_path}")

    # Load pages in configured order
    pages_content: list[str] = []
    for page_name in meta.get("pages", []):
        pages_content.append(load_page(cv_root, page_name))

    rendered = apply_template(template_path, pages_content)

    # Ensure output directory exists
    out_dir = cv_root / "out"
    out_dir.mkdir(parents=True, exist_ok=True)
    output_basename = meta.get("output_basename", variant_id)
    out_path = out_dir / f"{output_basename}.md"

    out_path.write_text(rendered, encoding="utf-8")

    # Evidence-style summary line
    rel_out = out_path.relative_to(repo_root)
    rel_src = cv_root.relative_to(repo_root)
    print(f"[OK] Generated CV variant {variant_id} from {rel_src} to {rel_out}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate structured CV from markdown + metadata")
    parser.add_argument("demo_id", help="Demo identifier, e.g. demo-001")
    parser.add_argument("variant_id", help="CV variant id, e.g. cv-001-backend-en")

    args = parser.parse_args()
    generate_cv(args.demo_id, args.variant_id)


if __name__ == "__main__":
    main()

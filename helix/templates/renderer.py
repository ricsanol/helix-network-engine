from pathlib import Path
from jinja2 import Environment, FileSystemLoader, StrictUndefined


class TemplateRenderer:
    def __init__(self, templates_root: str = "templates"):
        self.env = Environment(
            loader=FileSystemLoader(templates_root),
            undefined=StrictUndefined,
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def render(self, template_path: str, context: dict) -> str:
        template = self.env.get_template(template_path)
        return template.render(**context)

    def render_to_file(self, template_path: str, context: dict, output_file: str):
        rendered = self.render(template_path, context)

        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered, encoding="utf-8")

        return rendered
import subprocess
from pathlib import Path
from typing import Any
import os
from hatchling.builders.hooks.plugin.interface import BuildHookInterface

class GettextCompileHook(BuildHookInterface):
    def initialize(self, version: str, build_data: dict[str, Any]) -> None:
        if self.target_name != "wheel":
            return

        project_name = self.metadata.core.name
        locale_dir = Path(self.root) / "locales"

        if not locale_dir.exists():
            self.app.abort(f"Folder {locale_dir} with translations not found.\n")

        # Try reading the list of languages for which there are translations
        langs = []
        linguas = locale_dir / "LINGUAS"
        try:
            with open(linguas, encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        langs.extend(line.split())
        except OSError:
            self.app.display_info(f"Could not find file LINGUAS in {locale_dir}")

        build_config = self.build_config.build_config
        for lang in langs:
            po_file = locale_dir / f"{lang}.po"
            mo_file = locale_dir / lang / "LC_MESSAGES" / f"{project_name}.mo"

            if os.path.exists(mo_file):
                os.remove(mo_file)

            os.makedirs(os.path.dirname(mo_file), exist_ok=True)

            try:
                subprocess.run(
                    ["msgfmt", "-o", str(mo_file), str(po_file)],
                    check=True,
                    capture_output=True,
                    text=True
                )
            except subprocess.CalledProcessError as e:
                self.app.display_error(f"Failed to compile {po_file}: {e.stderr}")
                raise
            except FileNotFoundError:
                self.app.abort("msgfmt not found. Please install gettext-tools.\n")

            build_config["targets"]["wheel"]["shared-data"][mo_file] = f"share/locale/{lang}/LC_MESSAGES/{project_name}.mo"

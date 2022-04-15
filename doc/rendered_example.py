import os
import subprocess
import tempfile
from pathlib import Path
from typing import List

from docutils import nodes
from sphinx.directives.code import CodeBlock

DOC_ROOT_DIR = Path(__file__).parent
# Note that these dirs don't respond automatically to config changes
STATIC_RENDER_DIR = DOC_ROOT_DIR / "_build" / "html" / "_static" / "rendered_examples"


class RenderedExample(CodeBlock):
    """Directive for auto-rendering doc examples

    Code examples in ``rendered-example`` RST blocks will automatically be rendered in
    images, identified by their code hashes, and included in the generated HTML below
    the code.

    Neoscore import, setup, and render code is automatically added to examples. Examples
    which need to include these setup bits (useful early in docs for full "hello
    world"-type programs) can disable this behavior by including a ``neoscore.show()``
    call anywhere in the example. When that snippet is detected, this directive only
    replaces that line with an appropriate image export call and leaves the rest of the
    code unchanged.
    """

    def run(self) -> List[nodes.Node]:
        # Run superclass first
        result = super().run()
        # Now render the code block to an image
        script_file = tempfile.NamedTemporaryFile("w", suffix=".py")
        # Script ID should be stable across builds for unchanged scripts
        # use the hex of the script's hash (stripping leading '0x')
        script_id = hex(hash(tuple(self.content)))[2:]
        STATIC_RENDER_DIR.mkdir(parents=True, exist_ok=True)
        export_path = STATIC_RENDER_DIR / (script_id + ".png")
        # Add setup and render code to script
        script_lines = list(self.content)
        RenderedExample.post_process_script(script_lines, export_path)
        script_text = "\n".join(script_lines)
        script_file.write(script_text)
        script_file.flush()
        os.fsync(script_file.fileno())
        subprocess.check_call(["python", script_file.name])

        # This hackily assumes exported images live 2 dirs down from root
        image_uri = "/".join(export_path.parts[-3:])
        image_node = nodes.image(uri=image_uri, classes=["rendered-example"])
        result.append(image_node)
        return result

    @staticmethod
    def post_process_script(script: list[str], export_path: Path):
        """Modify `script` in-place preparing it for render"""
        render_line = (
            f"neoscore.render_image("
            + "neoscore.document.pages[0].document_space_bounding_rect,"
            + f"'{export_path}', 130, autocrop=True)"
        )

        if any(("neoscore.show()" in line for line in script)):
            # Assume script includes setup code too
            # Just overwrite the `show` line with image export
            for i in range(len(script)):
                script[i] = script[i].replace("neoscore.show()", render_line)
        else:
            script.insert(0, "from neoscore.common import *")
            script.insert(1, "neoscore.setup()")
            script.append(render_line)

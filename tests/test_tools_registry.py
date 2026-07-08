import sys
import types
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

js_module = types.ModuleType("js")
js_module.Headers = object()
js_module.fetch = None
js_module.Object = types.SimpleNamespace(fromEntries=None)
sys.modules.setdefault("js", js_module)

pyodide_module = types.ModuleType("pyodide")
ffi_module = types.ModuleType("pyodide.ffi")
ffi_module.to_js = lambda value, dict_converter=None: value
pyodide_module.ffi = ffi_module
sys.modules.setdefault("pyodide", pyodide_module)
sys.modules.setdefault("pyodide.ffi", ffi_module)

from topyappers_mcp.tools import TOOL_HANDLERS, TOOLS  # noqa: E402


class ToolsRegistryTests(unittest.TestCase):
    def test_registry_imports_all_tool_modules(self):
        names = [tool["name"] for tool in TOOLS]
        self.assertEqual(len(names), 14)
        self.assertEqual(set(names), set(TOOL_HANDLERS))
        self.assertIn("search_creators", names)
        self.assertIn("get_song_weeks", names)


if __name__ == "__main__":
    unittest.main()


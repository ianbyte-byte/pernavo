import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "understanding-system" / "scripts" / "excalidraw_scene.py"


def load_builder():
    spec = importlib.util.spec_from_file_location("excalidraw_scene", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ExcalidrawSceneTests(unittest.TestCase):
    def test_entity_relationship_uses_rectangles_diamonds_and_limits(self):
        module = load_builder()
        document = module.build(
            {
                "title": "客户与订单",
                "nodes": [
                    {"id": "customer", "text": "客户", "shape": "rectangle"},
                    {"id": "places", "text": "下单", "shape": "diamond"},
                    {"id": "order", "text": "订单", "shape": "rectangle"},
                ],
                "edges": [
                    {"from": "customer", "to": "places", "text": "1"},
                    {"from": "places", "to": "order", "text": "N"},
                ],
            }
        )
        self.assertEqual(document["type"], "excalidraw")
        self.assertEqual(document["version"], 2)
        kinds = [element["type"] for element in document["elements"]]
        self.assertIn("diamond", kinds)
        self.assertEqual(kinds.count("rectangle"), 2)
        texts = [element["text"] for element in document["elements"] if element["type"] == "text"]
        self.assertEqual(texts, ["客户与订单", "客户", "下单", "订单", "1", "N"])
        ids = {element["id"] for element in document["elements"]}
        for element in document["elements"]:
            if element["type"] == "arrow":
                self.assertIn(element["startBinding"]["elementId"], ids)
                self.assertIn(element["endBinding"]["elementId"], ids)
                self.assertIsNone(element["endArrowhead"])

    def test_flow_keeps_the_data_name_and_an_arrowhead(self):
        module = load_builder()
        document = module.build(
            {
                "nodes": [
                    {"id": "order", "text": "订单服务"},
                    {"id": "queue", "text": "消息队列"},
                ],
                "edges": [{"from": "order", "to": "queue", "text": "订单已创建"}],
            }
        )
        arrow = next(element for element in document["elements"] if element["type"] == "arrow")
        self.assertEqual(arrow["endArrowhead"], "arrow")
        texts = [element.get("text") for element in document["elements"]]
        self.assertIn("订单已创建", texts)

    def test_cli_writes_utf8_and_rejects_a_bad_edge(self):
        scene = {
            "nodes": [
                {"id": "created", "text": "已创建"},
                {"id": "deducted", "text": "已扣减"},
            ],
            "edges": [{"from": "created", "to": "deducted", "text": "完成扣减"}],
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "scene.json"
            target = root / "state.excalidraw"
            source.write_text(json.dumps(scene, ensure_ascii=False), encoding="utf-8")
            completed = subprocess.run(
                ["python3", str(SCRIPT), str(source), "-o", str(target)],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            document = json.loads(target.read_text(encoding="utf-8"))
            self.assertEqual(document["source"], "https://excalidraw.com")
            bad = root / "bad.json"
            bad.write_text('{"nodes":[{"id":"a","text":"甲"}],"edges":[{"from":"a","to":"missing"}]}', encoding="utf-8")
            failed = subprocess.run(
                ["python3", str(SCRIPT), str(bad), "-o", str(root / "no.excalidraw")],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(failed.returncode, 2)
            self.assertFalse((root / "no.excalidraw").exists())


if __name__ == "__main__":
    unittest.main()

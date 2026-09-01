import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "test-engineering" / "scripts" / "grade_api_jsonl.py"
EXAMPLES = ROOT / "skills" / "test-engineering" / "examples" / "api-test-gate"
SPEC = importlib.util.spec_from_file_location("grade_api_jsonl", SCRIPT)
grade_api_jsonl = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(grade_api_jsonl)


class GradeApiJsonlTests(unittest.TestCase):
    def test_czlhc_negative_only_is_incomplete(self):
        example = EXAMPLES / "czlhc-negative"
        report = grade_api_jsonl.run(example / "api-test-matrix.json", None, example)
        self.assertFalse(report["pass"])
        self.assertEqual("incomplete", report["status"])
        self.assertIn("create-valid", report["missing"])
        self.assertIn("no_passed_business_success", report["reasons"])

    def test_setposition_with_reconciliation_passes(self):
        example = EXAMPLES / "setposition-pass"
        report = grade_api_jsonl.run(example / "api-test-matrix.json", None, example)
        self.assertTrue(report["pass"])
        self.assertEqual("passed", report["status"])

    def test_http_200_result_minus_one_is_not_business_success(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "matrix.json").write_text(
                json.dumps(
                    {
                        "schema_version": "pernavo.api_test_matrix.v1",
                        "jsonl": "evidence.jsonl",
                        "required_cases": [{"id": "create-valid", "kind": "business-success"}],
                    }
                ),
                encoding="utf-8",
            )
            (root / "evidence.jsonl").write_text(
                json.dumps(
                    {
                        "case_id": "create-valid",
                        "http_status": 200,
                        "result": -1,
                        "verdict": "passed",
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            report = grade_api_jsonl.run(root / "matrix.json", None, root)
            self.assertFalse(report["pass"])
            self.assertTrue(any("result=-1" in item or "result=1" in item for item in report["reasons"]))


if __name__ == "__main__":
    unittest.main()

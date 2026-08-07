import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "report-writer" / "SKILL.md"
ENGINEERING = ROOT / "skills" / "report-writer" / "references" / "engineering-review.md"
LOG_EVIDENCE = ROOT / "skills" / "report-writer" / "references" / "log-evidence.md"
HTTP_API = ROOT / "skills" / "report-writer" / "references" / "http-api-test.md"


class ReportWriterContractTests(unittest.TestCase):
    def test_general_report_requests_trigger_the_skill(self):
        contract = SKILL.read_text(encoding="utf-8")

        self.assertIn("Use whenever the user asks to write, create, generate, format, or persist a report", contract)
        self.assertIn("写报告, 生成报告, 输出报告", contract)

    def test_format_is_selected_from_report_use(self):
        contract = SKILL.read_text(encoding="utf-8")

        self.assertIn("## Choose the file format from the report's use", contract)
        self.assertIn("Spreadsheet (`.xlsx`)", contract)
        self.assertIn("PDF (`.pdf`)", contract)
        self.assertIn("Self-contained HTML (`.html`)", contract)
        self.assertIn("Word (`.docx`)", contract)
        self.assertIn("Slides (`.pptx`)", contract)
        self.assertIn("Use Markdown as the fallback", contract)

    def test_html_has_deterministic_complexity_thresholds(self):
        contract = SKILL.read_text(encoding="utf-8")

        self.assertIn("more than twenty primary rows", contract)
        self.assertIn("more than eight columns", contract)
        self.assertIn("four or more evidence channels", contract)
        self.assertIn("Do not choose a format merely for decoration", contract)

    def test_engineering_review_is_a_submodule(self):
        contract = SKILL.read_text(encoding="utf-8")
        engineering = ENGINEERING.read_text(encoding="utf-8")

        self.assertIn("[engineering review](references/engineering-review.md)", contract)
        self.assertIn("# Engineering Review Report Module", engineering)
        self.assertIn("P1, P2, and P3 findings", engineering)
        self.assertIn("SonarQube", engineering)

    def test_html_is_portable_accessible_and_escapes_untrusted_content(self):
        contract = SKILL.read_text(encoding="utf-8")

        self.assertIn("no network dependency", contract)
        self.assertIn("Escape untrusted text", contract)
        self.assertIn("readable when JavaScript is disabled", contract)

    def test_logs_use_jsonl_or_raw_log_and_reports_only_embed_bounded_evidence(self):
        contract = SKILL.read_text(encoding="utf-8")
        logs = LOG_EVIDENCE.read_text(encoding="utf-8")

        self.assertIn("[log evidence](references/log-evidence.md)", contract)
        self.assertIn("UTF-8 JSONL / NDJSON", logs)
        self.assertIn("Raw stdout or stderr", logs)
        self.assertIn("correlation_id", logs)
        self.assertIn("SHA-256", logs)
        self.assertIn("bounded excerpt", logs)

    def test_http_api_module_requires_complete_cases_and_interaction_logs(self):
        contract = SKILL.read_text(encoding="utf-8")
        http_api = HTTP_API.read_text(encoding="utf-8")

        self.assertIn("[HTTP API test](references/http-api-test.md)", contract)
        self.assertIn("all cases required by the endpoint contract and risk model", http_api)
        self.assertIn("Authentication", http_api)
        self.assertIn("Authorization", http_api)
        self.assertIn("Idempotency", http_api)
        self.assertIn("http.request", http_api)
        self.assertIn("http.response", http_api)
        self.assertIn("sanitized HAR 1.2", http_api)
        self.assertIn("Never log reusable credentials", http_api)

        examples = [
            json.loads(line)
            for line in http_api.splitlines()
            if line.startswith('{"ts"')
        ]
        self.assertEqual(2, len(examples))
        for event in examples:
            for field in ("ts", "level", "source", "event", "target", "correlation_id"):
                self.assertIn(field, event)

        request, response = examples
        self.assertEqual("http.request", request["event"])
        self.assertIn("authorization", request["redactions"])
        self.assertEqual("[REDACTED]", request["headers"]["authorization"])
        self.assertEqual("http.response", response["event"])
        self.assertEqual(201, response["http_status"])
        self.assertEqual("passed", response["status"])


if __name__ == "__main__":
    unittest.main()

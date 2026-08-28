import io
import json
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import Mock, patch


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import pagespeed_check


class PagespeedCheckCliTest(unittest.TestCase):
    @patch.object(pagespeed_check.requests, "get")
    def test_psi_json_includes_detailed_audit_rows(self, mock_get):
        response = Mock(status_code=200)
        response.json.return_value = {
            "analysisUTCTimestamp": "2026-08-28T00:00:00Z",
            "lighthouseResult": {
                "categories": {"performance": {"score": 0.9}},
                "audits": {
                    "unused-javascript": {
                        "title": "Reduce unused JavaScript",
                        "score": 0.5,
                        "details": {
                            "type": "table",
                            "headings": [{"key": "url", "label": "URL"}],
                            "items": [{"url": "https://example.com/app.js"}],
                        },
                    }
                },
            },
        }
        mock_get.return_value = response

        stdout = io.StringIO()
        argv = [
            "pagespeed_check.py",
            "https://example.com",
            "--strategy",
            "mobile",
            "--psi-only",
            "--api-key",
            "test-key",
            "--json",
        ]
        with patch.object(sys, "argv", argv), redirect_stdout(stdout):
            pagespeed_check.main()

        result = json.loads(stdout.getvalue())
        audit = result["psi"]["mobile"]["audit_details"]["unused-javascript"]
        self.assertEqual(audit["items"], [{"url": "https://example.com/app.js"}])


if __name__ == "__main__":
    unittest.main()

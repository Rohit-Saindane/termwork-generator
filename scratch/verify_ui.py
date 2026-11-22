import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
from app import app

class TestTermWorkForge(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_homepage(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        html = res.data.decode('utf-8')
        
        # Check no hardcoded Operating Systems
        self.assertNotIn("Operating Systems (1CS)", html)
        
        # Check red dot writing tag removed
        self.assertNotIn('<span class="rec">', html)
        self.assertNotIn('>writing<', html)
        
        # Check tabs 2, 3, 4 are locked
        self.assertIn('id="tab-step-2" role="tab" tabindex="0" title="Upload Practical Index PDF to unlock"', html)
        self.assertIn('id="tab-step-3" role="tab" tabindex="0" title="Upload Practical Index PDF to unlock"', html)
        self.assertIn('id="tab-step-4" role="tab" tabindex="0" title="Upload Practical Index PDF to unlock"', html)
        
        # Check Full Screen buttons exist
        self.assertIn('id="btn-step3-fs-preview"', html)
        self.assertIn('id="btn-trigger-fullscreen-preview"', html)
        self.assertIn('id="fullscreen-modal"', html)
        
        # Check asset versioning v=3.4
        self.assertIn('notebook.css?v=3.4', html)
        self.assertIn('app.js?v=3.4', html)
        print("✓ Homepage HTML checks passed!")

    def test_static_files(self):
        res_css = self.client.get('/static/css/notebook.css')
        self.assertEqual(res_css.status_code, 200)
        css = res_css.data.decode('utf-8')
        self.assertIn('.fs-modal-wrap', css)
        self.assertIn('.fs-dim', css)
        self.assertIn('.tab.locked', css)
        
        res_js = self.client.get('/static/js/app.js')
        self.assertEqual(res_js.status_code, 200)
        js = res_js.data.decode('utf-8')
        self.assertIn('openFullscreenPreview', js)
        self.assertIn('renderFullscreenSheet', js)
        self.assertNotIn('DEFAULT_PRACTICALS', js)
        print("✓ Static CSS & JS checks passed!")

if __name__ == '__main__':
    unittest.main()

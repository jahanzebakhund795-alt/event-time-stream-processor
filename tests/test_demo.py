import copy
import json
from pathlib import Path
import unittest
from main import run


class DemoTests(unittest.TestCase):
    def test_business_result(self):
        data = json.loads(Path('sample.json').read_text())
        original = copy.deepcopy(data)
        result = run(data)
        self.assertEqual(result['windows'], {'0':2, '60':7})
        self.assertEqual(result['late_event_ids'], ['c'])
        self.assertEqual(result['duplicates'], 1)
        self.assertEqual(data, original, 'Input should not be mutated')

    def test_boundary_and_failure_behavior(self):
        data = json.loads(Path('sample.json').read_text())
        data['events'] = [{'id':'x','ts':60,'quantity':2},{'id':'y','ts':30,'quantity':3}]
        self.assertEqual(run(data)['late_event_ids'], [])
        self.assertEqual(run(data)['windows'], {'0':3,'60':2})
        data['window_seconds'] = 0
        with self.assertRaises(ValueError):
            run(data)


if __name__ == '__main__':
    unittest.main()

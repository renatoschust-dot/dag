import os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import reflex
import dag


class TestTopGuard(unittest.TestCase):
    """Cilj mora biti odbijen prije planiranja (prije ijednog model poziva)."""

    def test_catastrophic_goal_blocked(self):
        g = dag.top_guard("rm -rf /")
        self.assertIsNotNone(g)
        self.assertEqual(g["action"], "block")

    def test_normal_goal_passes(self):
        self.assertIsNone(dag.top_guard("analiziraj trziste industrijskih masina"))


class TestReflex(unittest.TestCase):
    def test_risk_blocks_catastrophic(self):
        self.assertGreaterEqual(reflex.risk_score("rm -rf /"), 0.9)
        self.assertGreaterEqual(reflex.risk_score("drop table users"), 0.9)

    def test_risk_allows_normal(self):
        self.assertLess(reflex.risk_score("koliko kupaca ima"), 0.3)
        self.assertLess(reflex.risk_score("napisi python funkciju"), 0.3)

    def test_domain(self):
        self.assertEqual(reflex.detect_domain("napisi upit za bazu"), "sql")
        self.assertEqual(reflex.detect_domain("napisi python funkciju"), "code")

    def test_translit(self):
        self.assertEqual(reflex.translit("čćžšđ"), "cczsd")


if __name__ == "__main__":
    unittest.main()

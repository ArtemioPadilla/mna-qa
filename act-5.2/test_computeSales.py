"""Pytest tests for computeSales.py."""
# pylint: disable=invalid-name

import json
import os
import subprocess
import sys

import pytest

# Allow importing from same directory
sys.path.insert(0, os.path.dirname(__file__))

from computeSales import (  # noqa: E402
    build_price_catalogue,
    calculate_grand_total,
    compute_sales,
    load_json_file,
)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE = os.path.dirname(__file__)
DATA = os.path.join(BASE, "A5.2 Archivos de Apoyo")
CATALOGUE = os.path.join(DATA, "TC1", "TC1.ProductList.json")
TC1_SALES = os.path.join(DATA, "TC1", "TC1.Sales.json")
TC2_SALES = os.path.join(DATA, "TC2", "TC2.Sales.json")
TC3_SALES = os.path.join(DATA, "TC3", "TC3.Sales.json")


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def catalogue():
    """Load the product catalogue once for the whole test session."""
    products = load_json_file(CATALOGUE)
    return build_price_catalogue(products)


# ---------------------------------------------------------------------------
# Unit tests – build_price_catalogue
# ---------------------------------------------------------------------------
class TestBuildPriceCatalogue:
    """Tests for building the price lookup dict."""

    def test_returns_dict(self):
        products = [{"title": "Eggs", "price": 2.5}]
        assert isinstance(build_price_catalogue(products), dict)

    def test_maps_title_to_price(self):
        products = [{"title": "Eggs", "price": 2.5}]
        cat = build_price_catalogue(products)
        assert cat["Eggs"] == 2.5

    def test_skips_missing_title(self):
        products = [{"price": 1.0}]
        assert build_price_catalogue(products) == {}

    def test_skips_missing_price(self):
        products = [{"title": "Eggs"}]
        assert build_price_catalogue(products) == {}


# ---------------------------------------------------------------------------
# Unit tests – compute_sales
# ---------------------------------------------------------------------------
class TestComputeSales:
    """Tests for the core compute_sales function."""

    def test_valid_sale(self):
        cat = {"Eggs": 2.50}
        sales = [{"SALE_ID": 1, "Product": "Eggs", "Quantity": 3}]
        grouped, errors = compute_sales(cat, sales)
        assert errors == []
        assert grouped[1][0]["line_total"] == pytest.approx(7.50)

    def test_unknown_product_skipped(self):
        cat = {"Eggs": 2.50}
        sales = [{"SALE_ID": 1, "Product": "Elotes", "Quantity": 1}]
        grouped, errors = compute_sales(cat, sales)
        assert len(errors) == 1
        assert "Elotes" in errors[0]
        assert 1 not in grouped

    def test_negative_quantity_warned(self):
        cat = {"Eggs": 2.50}
        sales = [{"SALE_ID": 1, "Product": "Eggs", "Quantity": -5}]
        grouped, errors = compute_sales(cat, sales)
        assert len(errors) == 1
        assert "Negative" in errors[0] or "negative" in errors[0].lower()


# ---------------------------------------------------------------------------
# Unit tests – calculate_grand_total
# ---------------------------------------------------------------------------
class TestCalculateGrandTotal:
    """Tests for grand total calculation."""

    def test_sums_correctly(self):
        grouped = {
            1: [{"line_total": 10.0}, {"line_total": 5.0}],
            2: [{"line_total": 20.0}],
        }
        assert calculate_grand_total(grouped) == pytest.approx(35.0)

    def test_empty(self):
        assert calculate_grand_total({}) == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# Integration tests – expected totals from Results.txt
# ---------------------------------------------------------------------------
EXPECTED_TOTALS = {
    "TC1": 2481.86,
    "TC2": 166568.23,
    "TC3": 165235.37,
}


def _run_pipeline(catalogue, sales_path):
    """Run the full compute pipeline and return the grand total."""
    sales_data = load_json_file(sales_path)
    grouped, _ = compute_sales(catalogue, sales_data)
    return calculate_grand_total(grouped)


class TestIntegrationTotals:
    """Verify grand totals match expected values from Results.txt."""

    def test_tc1_total(self, catalogue):
        total = _run_pipeline(catalogue, TC1_SALES)
        assert total == pytest.approx(EXPECTED_TOTALS["TC1"], abs=0.01)

    def test_tc2_total(self, catalogue):
        total = _run_pipeline(catalogue, TC2_SALES)
        assert total == pytest.approx(EXPECTED_TOTALS["TC2"], abs=0.01)

    def test_tc3_total(self, catalogue):
        total = _run_pipeline(catalogue, TC3_SALES)
        assert total == pytest.approx(EXPECTED_TOTALS["TC3"], abs=0.01)


# ---------------------------------------------------------------------------
# Integration tests – CLI invocation
# ---------------------------------------------------------------------------
class TestCLI:
    """Test the program via subprocess, as the grader would run it."""

    @staticmethod
    def _run_cli(catalogue_path, sales_path):
        result = subprocess.run(
            [sys.executable, "computeSales.py", catalogue_path, sales_path],
            capture_output=True,
            text=True,
            cwd=BASE,
        )
        return result

    def test_tc1_cli_output(self):
        r = self._run_cli(CATALOGUE, TC1_SALES)
        assert r.returncode == 0
        assert "2,481.86" in r.stdout or "2481.86" in r.stdout

    def test_tc2_cli_output(self):
        r = self._run_cli(CATALOGUE, TC2_SALES)
        assert r.returncode == 0
        assert "166,568.23" in r.stdout or "166568.23" in r.stdout

    def test_tc3_cli_output(self):
        r = self._run_cli(CATALOGUE, TC3_SALES)
        assert r.returncode == 0
        assert "165,235.37" in r.stdout or "165235.37" in r.stdout

    def test_missing_args(self):
        r = subprocess.run(
            [sys.executable, "computeSales.py"],
            capture_output=True,
            text=True,
            cwd=BASE,
        )
        assert r.returncode != 0

    def test_missing_file(self):
        r = self._run_cli("nonexistent.json", TC1_SALES)
        assert r.returncode != 0


# ---------------------------------------------------------------------------
# Integration tests – error handling
# ---------------------------------------------------------------------------
class TestErrorHandling:
    """Verify invalid data produces warnings."""

    def test_tc2_has_negative_quantity_warnings(self, catalogue):
        sales_data = load_json_file(TC2_SALES)
        _, errors = compute_sales(catalogue, sales_data)
        neg_errors = [e for e in errors if "negative" in e.lower()]
        assert len(neg_errors) >= 2, (
            "TC2 should flag at least 2 negative quantities"
        )

    def test_tc3_has_unknown_product_errors(self, catalogue):
        sales_data = load_json_file(TC3_SALES)
        _, errors = compute_sales(catalogue, sales_data)
        unknown = [e for e in errors if "not in" in e.lower()]
        assert len(unknown) >= 2, (
            "TC3 should flag at least 2 unknown products"
        )

    def test_tc3_unknown_products_are_elotes_frijoles(self, catalogue):
        sales_data = load_json_file(TC3_SALES)
        _, errors = compute_sales(catalogue, sales_data)
        error_text = " ".join(errors)
        assert "Elotes" in error_text
        assert "Frijoles" in error_text


# ---------------------------------------------------------------------------
# Static analysis (optional — run with pytest -m static)
# ---------------------------------------------------------------------------
@pytest.mark.static
class TestStaticAnalysis:
    """Ensure flake8 and pylint pass with zero errors."""

    def test_flake8(self):
        r = subprocess.run(
            [sys.executable, "-m", "flake8", "computeSales.py"],
            capture_output=True,
            text=True,
            cwd=BASE,
        )
        if "No module named flake8" in r.stderr:
            pytest.skip("flake8 not installed")
        assert r.returncode == 0, f"flake8 errors:\n{r.stdout}"

    def test_pylint(self):
        r = subprocess.run(
            [sys.executable, "-m", "pylint", "computeSales.py"],
            capture_output=True,
            text=True,
            cwd=BASE,
        )
        if "No module named pylint" in r.stderr:
            pytest.skip("pylint not installed")
        assert r.returncode == 0, f"pylint issues:\n{r.stdout}"

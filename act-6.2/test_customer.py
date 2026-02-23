"""Unit tests for Customer class."""
# pylint: disable=invalid-name

import json
import os
import tempfile
import unittest

from customer import Customer


class TestCustomerCreate(unittest.TestCase):
    """Tests for Customer.create_customer."""

    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(
            suffix=".json", delete=False
        )
        self.tmp.close()
        self.path = self.tmp.name

    def tearDown(self):
        if os.path.exists(self.path):
            os.unlink(self.path)

    def test_create_valid(self):
        """Create a valid customer."""
        customer = Customer.create_customer(
            "C1", "Ana Lopez", "ana@mail.com",
            file_path=self.path
        )
        self.assertIsNotNone(customer)
        self.assertEqual(customer.customer_id, "C1")
        self.assertEqual(customer.name, "Ana Lopez")

    def test_create_persists(self):
        """Created customer is saved to JSON file."""
        Customer.create_customer(
            "C1", "Ana Lopez", "ana@mail.com",
            file_path=self.path
        )
        with open(self.path, "r", encoding="utf-8") as fhandle:
            data = json.load(fhandle)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["customer_id"], "C1")

    def test_create_multiple(self):
        """Create two customers sequentially."""
        Customer.create_customer(
            "C1", "Ana", "ana@mail.com", file_path=self.path
        )
        Customer.create_customer(
            "C2", "Bob", "bob@mail.com", file_path=self.path
        )
        records = Customer.load_all(self.path)
        self.assertEqual(len(records), 2)

    def test_create_duplicate_id(self):
        """Negative: duplicate customer_id returns None."""
        Customer.create_customer(
            "C1", "Ana", "ana@mail.com", file_path=self.path
        )
        result = Customer.create_customer(
            "C1", "Bob", "bob@mail.com", file_path=self.path
        )
        self.assertIsNone(result)

    def test_create_empty_id(self):
        """Negative: empty customer_id returns None."""
        result = Customer.create_customer(
            "", "Ana", "ana@mail.com", file_path=self.path
        )
        self.assertIsNone(result)

    def test_create_empty_name(self):
        """Negative: empty name returns None."""
        result = Customer.create_customer(
            "C1", "", "ana@mail.com", file_path=self.path
        )
        self.assertIsNone(result)

    def test_create_invalid_email(self):
        """Negative: email without @ returns None."""
        result = Customer.create_customer(
            "C1", "Ana", "invalid-email", file_path=self.path
        )
        self.assertIsNone(result)

    def test_create_empty_email(self):
        """Negative: empty email returns None."""
        result = Customer.create_customer(
            "C1", "Ana", "", file_path=self.path
        )
        self.assertIsNone(result)


class TestCustomerDelete(unittest.TestCase):
    """Tests for Customer.delete_customer."""

    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(
            suffix=".json", delete=False
        )
        self.tmp.close()
        self.path = self.tmp.name
        Customer.create_customer(
            "C1", "Ana", "ana@mail.com", file_path=self.path
        )

    def tearDown(self):
        if os.path.exists(self.path):
            os.unlink(self.path)

    def test_delete_existing(self):
        """Delete an existing customer."""
        result = Customer.delete_customer(
            "C1", file_path=self.path
        )
        self.assertTrue(result)
        records = Customer.load_all(self.path)
        self.assertEqual(len(records), 0)

    def test_delete_nonexistent(self):
        """Negative: delete non-existent customer."""
        result = Customer.delete_customer(
            "C999", file_path=self.path
        )
        self.assertFalse(result)


class TestCustomerDisplay(unittest.TestCase):
    """Tests for Customer.display_customer."""

    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(
            suffix=".json", delete=False
        )
        self.tmp.close()
        self.path = self.tmp.name
        Customer.create_customer(
            "C1", "Ana", "ana@mail.com", file_path=self.path
        )

    def tearDown(self):
        if os.path.exists(self.path):
            os.unlink(self.path)

    def test_display_existing(self):
        """Display an existing customer returns dict."""
        result = Customer.display_customer(
            "C1", file_path=self.path
        )
        self.assertIsNotNone(result)
        self.assertEqual(result["name"], "Ana")

    def test_display_nonexistent(self):
        """Negative: display non-existent customer."""
        result = Customer.display_customer(
            "C999", file_path=self.path
        )
        self.assertIsNone(result)


class TestCustomerModify(unittest.TestCase):
    """Tests for Customer.modify_customer."""

    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(
            suffix=".json", delete=False
        )
        self.tmp.close()
        self.path = self.tmp.name
        Customer.create_customer(
            "C1", "Ana", "ana@mail.com", file_path=self.path
        )

    def tearDown(self):
        if os.path.exists(self.path):
            os.unlink(self.path)

    def test_modify_name(self):
        """Modify customer name."""
        result = Customer.modify_customer(
            "C1", file_path=self.path, name="Ana Maria"
        )
        self.assertTrue(result)
        record = Customer.display_customer(
            "C1", file_path=self.path
        )
        self.assertEqual(record["name"], "Ana Maria")

    def test_modify_email(self):
        """Modify customer email."""
        result = Customer.modify_customer(
            "C1", file_path=self.path, email="new@mail.com"
        )
        self.assertTrue(result)
        record = Customer.display_customer(
            "C1", file_path=self.path
        )
        self.assertEqual(record["email"], "new@mail.com")

    def test_modify_nonexistent(self):
        """Negative: modify non-existent customer."""
        result = Customer.modify_customer(
            "C999", file_path=self.path, name="X"
        )
        self.assertFalse(result)

    def test_modify_invalid_email(self):
        """Negative: modify with invalid email returns False."""
        result = Customer.modify_customer(
            "C1", file_path=self.path, email="bad-email"
        )
        self.assertFalse(result)

    def test_modify_empty_email(self):
        """Negative: modify with empty email returns False."""
        result = Customer.modify_customer(
            "C1", file_path=self.path, email=""
        )
        self.assertFalse(result)


class TestCustomerPersistence(unittest.TestCase):
    """Tests for Customer persistence edge cases."""

    def test_load_nonexistent_file(self):
        """Loading from non-existent file returns []."""
        result = Customer.load_all("/tmp/nonexistent_cust.json")
        self.assertEqual(result, [])

    def test_load_corrupted_json(self):
        """Negative: corrupted JSON returns []."""
        tmp = tempfile.NamedTemporaryFile(
            suffix=".json", delete=False, mode="w"
        )
        tmp.write("not json at all")
        tmp.close()
        result = Customer.load_all(tmp.name)
        self.assertEqual(result, [])
        os.unlink(tmp.name)

    def test_to_dict_from_dict_roundtrip(self):
        """Serialize and deserialize a Customer."""
        customer = Customer("C1", "Ana", "ana@mail.com")
        data = customer.to_dict()
        restored = Customer.from_dict(data)
        self.assertEqual(restored.customer_id, "C1")
        self.assertEqual(restored.email, "ana@mail.com")


if __name__ == "__main__":
    unittest.main()

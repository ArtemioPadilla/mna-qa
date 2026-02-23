"""Unit tests for Reservation class."""
# pylint: disable=invalid-name

import json
import os
import tempfile
import unittest

from hotel import Hotel
from customer import Customer
from reservation import Reservation


class TestReservationCreate(unittest.TestCase):
    """Tests for Reservation.create_reservation."""

    def setUp(self):
        self.hotel_file = tempfile.NamedTemporaryFile(
            suffix=".json", delete=False
        )
        self.hotel_file.close()
        self.customer_file = tempfile.NamedTemporaryFile(
            suffix=".json", delete=False
        )
        self.customer_file.close()
        self.res_file = tempfile.NamedTemporaryFile(
            suffix=".json", delete=False
        )
        self.res_file.close()

        Hotel.create_hotel(
            "H1", "Grand", "CDMX", 2,
            file_path=self.hotel_file.name
        )
        Customer.create_customer(
            "C1", "Ana", "ana@mail.com",
            file_path=self.customer_file.name
        )

    def tearDown(self):
        for path in (self.hotel_file.name,
                     self.customer_file.name,
                     self.res_file.name):
            if os.path.exists(path):
                os.unlink(path)

    def test_create_valid(self):
        """Create a valid reservation."""
        res = Reservation.create_reservation(
            "R1", "C1", "H1",
            file_path=self.res_file.name,
            hotel_file=self.hotel_file.name,
            customer_file=self.customer_file.name
        )
        self.assertIsNotNone(res)
        self.assertEqual(res.reservation_id, "R1")
        self.assertEqual(res.customer_id, "C1")
        self.assertEqual(res.hotel_id, "H1")

    def test_create_persists(self):
        """Created reservation is saved to JSON file."""
        Reservation.create_reservation(
            "R1", "C1", "H1",
            file_path=self.res_file.name,
            hotel_file=self.hotel_file.name,
            customer_file=self.customer_file.name
        )
        with open(self.res_file.name, "r",
                  encoding="utf-8") as fhandle:
            data = json.load(fhandle)
        self.assertEqual(len(data), 1)

    def test_create_decrements_rooms(self):
        """Creating reservation decrements available rooms."""
        Reservation.create_reservation(
            "R1", "C1", "H1",
            file_path=self.res_file.name,
            hotel_file=self.hotel_file.name,
            customer_file=self.customer_file.name
        )
        record = Hotel.display_hotel(
            "H1", file_path=self.hotel_file.name
        )
        self.assertEqual(record["rooms_available"], 1)

    def test_create_duplicate_id(self):
        """Negative: duplicate reservation_id returns None."""
        Reservation.create_reservation(
            "R1", "C1", "H1",
            file_path=self.res_file.name,
            hotel_file=self.hotel_file.name,
            customer_file=self.customer_file.name
        )
        result = Reservation.create_reservation(
            "R1", "C1", "H1",
            file_path=self.res_file.name,
            hotel_file=self.hotel_file.name,
            customer_file=self.customer_file.name
        )
        self.assertIsNone(result)

    def test_create_empty_id(self):
        """Negative: empty reservation_id returns None."""
        result = Reservation.create_reservation(
            "", "C1", "H1",
            file_path=self.res_file.name,
            hotel_file=self.hotel_file.name,
            customer_file=self.customer_file.name
        )
        self.assertIsNone(result)

    def test_create_nonexistent_customer(self):
        """Negative: non-existent customer returns None."""
        result = Reservation.create_reservation(
            "R1", "C999", "H1",
            file_path=self.res_file.name,
            hotel_file=self.hotel_file.name,
            customer_file=self.customer_file.name
        )
        self.assertIsNone(result)

    def test_create_nonexistent_hotel(self):
        """Negative: non-existent hotel returns None."""
        result = Reservation.create_reservation(
            "R1", "C1", "H999",
            file_path=self.res_file.name,
            hotel_file=self.hotel_file.name,
            customer_file=self.customer_file.name
        )
        self.assertIsNone(result)

    def test_create_no_rooms_available(self):
        """Negative: no rooms available returns None."""
        Reservation.create_reservation(
            "R1", "C1", "H1",
            file_path=self.res_file.name,
            hotel_file=self.hotel_file.name,
            customer_file=self.customer_file.name
        )
        Reservation.create_reservation(
            "R2", "C1", "H1",
            file_path=self.res_file.name,
            hotel_file=self.hotel_file.name,
            customer_file=self.customer_file.name
        )
        result = Reservation.create_reservation(
            "R3", "C1", "H1",
            file_path=self.res_file.name,
            hotel_file=self.hotel_file.name,
            customer_file=self.customer_file.name
        )
        self.assertIsNone(result)


class TestReservationCancel(unittest.TestCase):
    """Tests for Reservation.cancel_reservation."""

    def setUp(self):
        self.hotel_file = tempfile.NamedTemporaryFile(
            suffix=".json", delete=False
        )
        self.hotel_file.close()
        self.customer_file = tempfile.NamedTemporaryFile(
            suffix=".json", delete=False
        )
        self.customer_file.close()
        self.res_file = tempfile.NamedTemporaryFile(
            suffix=".json", delete=False
        )
        self.res_file.close()

        Hotel.create_hotel(
            "H1", "Grand", "CDMX", 5,
            file_path=self.hotel_file.name
        )
        Customer.create_customer(
            "C1", "Ana", "ana@mail.com",
            file_path=self.customer_file.name
        )
        Reservation.create_reservation(
            "R1", "C1", "H1",
            file_path=self.res_file.name,
            hotel_file=self.hotel_file.name,
            customer_file=self.customer_file.name
        )

    def tearDown(self):
        for path in (self.hotel_file.name,
                     self.customer_file.name,
                     self.res_file.name):
            if os.path.exists(path):
                os.unlink(path)

    def test_cancel_valid(self):
        """Cancel an existing reservation."""
        result = Reservation.cancel_reservation(
            "R1",
            file_path=self.res_file.name,
            hotel_file=self.hotel_file.name
        )
        self.assertTrue(result)
        records = Reservation.load_all(self.res_file.name)
        self.assertEqual(len(records), 0)

    def test_cancel_restores_room(self):
        """Cancelling reservation increments available rooms."""
        Reservation.cancel_reservation(
            "R1",
            file_path=self.res_file.name,
            hotel_file=self.hotel_file.name
        )
        record = Hotel.display_hotel(
            "H1", file_path=self.hotel_file.name
        )
        self.assertEqual(record["rooms_available"], 5)

    def test_cancel_nonexistent(self):
        """Negative: cancel non-existent reservation."""
        result = Reservation.cancel_reservation(
            "R999",
            file_path=self.res_file.name,
            hotel_file=self.hotel_file.name
        )
        self.assertFalse(result)


class TestReservationPersistence(unittest.TestCase):
    """Tests for Reservation persistence edge cases."""

    def test_load_nonexistent_file(self):
        """Loading from non-existent file returns []."""
        result = Reservation.load_all("/tmp/nonexistent_res.json")
        self.assertEqual(result, [])

    def test_load_corrupted_json(self):
        """Negative: corrupted JSON returns []."""
        tmp = tempfile.NamedTemporaryFile(
            suffix=".json", delete=False, mode="w"
        )
        tmp.write("<<<corrupted>>>")
        tmp.close()
        result = Reservation.load_all(tmp.name)
        self.assertEqual(result, [])
        os.unlink(tmp.name)

    def test_to_dict_from_dict_roundtrip(self):
        """Serialize and deserialize a Reservation."""
        res = Reservation("R1", "C1", "H1")
        data = res.to_dict()
        restored = Reservation.from_dict(data)
        self.assertEqual(restored.reservation_id, "R1")
        self.assertEqual(restored.customer_id, "C1")


if __name__ == "__main__":
    unittest.main()

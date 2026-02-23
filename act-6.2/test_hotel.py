"""Unit tests for Hotel class."""
# pylint: disable=invalid-name

import json
import os
import tempfile
import unittest

from hotel import Hotel


class TestHotelCreate(unittest.TestCase):
    """Tests for Hotel.create_hotel."""

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
        """Create a valid hotel."""
        hotel = Hotel.create_hotel(
            "H1", "Grand", "CDMX", 10, file_path=self.path
        )
        self.assertIsNotNone(hotel)
        self.assertEqual(hotel.hotel_id, "H1")
        self.assertEqual(hotel.name, "Grand")
        self.assertEqual(hotel.rooms, 10)
        self.assertEqual(hotel.rooms_available, 10)

    def test_create_persists(self):
        """Created hotel is saved to JSON file."""
        Hotel.create_hotel(
            "H1", "Grand", "CDMX", 10, file_path=self.path
        )
        with open(self.path, "r", encoding="utf-8") as fhandle:
            data = json.load(fhandle)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["hotel_id"], "H1")

    def test_create_multiple(self):
        """Create two hotels sequentially."""
        Hotel.create_hotel(
            "H1", "Grand", "CDMX", 10, file_path=self.path
        )
        Hotel.create_hotel(
            "H2", "Plaza", "GDL", 5, file_path=self.path
        )
        records = Hotel.load_all(self.path)
        self.assertEqual(len(records), 2)

    def test_create_duplicate_id(self):
        """Negative: duplicate hotel_id returns None."""
        Hotel.create_hotel(
            "H1", "Grand", "CDMX", 10, file_path=self.path
        )
        result = Hotel.create_hotel(
            "H1", "Other", "GDL", 5, file_path=self.path
        )
        self.assertIsNone(result)

    def test_create_empty_id(self):
        """Negative: empty hotel_id returns None."""
        result = Hotel.create_hotel(
            "", "Grand", "CDMX", 10, file_path=self.path
        )
        self.assertIsNone(result)

    def test_create_empty_name(self):
        """Negative: empty name returns None."""
        result = Hotel.create_hotel(
            "H1", "", "CDMX", 10, file_path=self.path
        )
        self.assertIsNone(result)

    def test_create_zero_rooms(self):
        """Negative: zero rooms returns None."""
        result = Hotel.create_hotel(
            "H1", "Grand", "CDMX", 0, file_path=self.path
        )
        self.assertIsNone(result)

    def test_create_negative_rooms(self):
        """Negative: negative rooms returns None."""
        result = Hotel.create_hotel(
            "H1", "Grand", "CDMX", -5, file_path=self.path
        )
        self.assertIsNone(result)

    def test_create_string_rooms(self):
        """Negative: string rooms returns None."""
        result = Hotel.create_hotel(
            "H1", "Grand", "CDMX", "ten", file_path=self.path
        )
        self.assertIsNone(result)


class TestHotelDelete(unittest.TestCase):
    """Tests for Hotel.delete_hotel."""

    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(
            suffix=".json", delete=False
        )
        self.tmp.close()
        self.path = self.tmp.name
        Hotel.create_hotel(
            "H1", "Grand", "CDMX", 10, file_path=self.path
        )

    def tearDown(self):
        if os.path.exists(self.path):
            os.unlink(self.path)

    def test_delete_existing(self):
        """Delete an existing hotel."""
        result = Hotel.delete_hotel("H1", file_path=self.path)
        self.assertTrue(result)
        records = Hotel.load_all(self.path)
        self.assertEqual(len(records), 0)

    def test_delete_nonexistent(self):
        """Negative: delete non-existent hotel returns False."""
        result = Hotel.delete_hotel("H999", file_path=self.path)
        self.assertFalse(result)


class TestHotelDisplay(unittest.TestCase):
    """Tests for Hotel.display_hotel."""

    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(
            suffix=".json", delete=False
        )
        self.tmp.close()
        self.path = self.tmp.name
        Hotel.create_hotel(
            "H1", "Grand", "CDMX", 10, file_path=self.path
        )

    def tearDown(self):
        if os.path.exists(self.path):
            os.unlink(self.path)

    def test_display_existing(self):
        """Display an existing hotel returns its dict."""
        result = Hotel.display_hotel("H1", file_path=self.path)
        self.assertIsNotNone(result)
        self.assertEqual(result["name"], "Grand")

    def test_display_nonexistent(self):
        """Negative: display non-existent hotel returns None."""
        result = Hotel.display_hotel("H999", file_path=self.path)
        self.assertIsNone(result)


class TestHotelModify(unittest.TestCase):
    """Tests for Hotel.modify_hotel."""

    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(
            suffix=".json", delete=False
        )
        self.tmp.close()
        self.path = self.tmp.name
        Hotel.create_hotel(
            "H1", "Grand", "CDMX", 10, file_path=self.path
        )

    def tearDown(self):
        if os.path.exists(self.path):
            os.unlink(self.path)

    def test_modify_name(self):
        """Modify hotel name."""
        result = Hotel.modify_hotel(
            "H1", file_path=self.path, name="Grand Deluxe"
        )
        self.assertTrue(result)
        record = Hotel.display_hotel("H1", file_path=self.path)
        self.assertEqual(record["name"], "Grand Deluxe")

    def test_modify_location(self):
        """Modify hotel location."""
        result = Hotel.modify_hotel(
            "H1", file_path=self.path, location="Cancun"
        )
        self.assertTrue(result)
        record = Hotel.display_hotel("H1", file_path=self.path)
        self.assertEqual(record["location"], "Cancun")

    def test_modify_rooms(self):
        """Modify hotel room count adjusts availability."""
        Hotel.reserve_room("H1", file_path=self.path)
        result = Hotel.modify_hotel(
            "H1", file_path=self.path, rooms=20
        )
        self.assertTrue(result)
        record = Hotel.display_hotel("H1", file_path=self.path)
        self.assertEqual(record["rooms"], 20)
        self.assertEqual(record["rooms_available"], 19)

    def test_modify_nonexistent(self):
        """Negative: modify non-existent hotel returns False."""
        result = Hotel.modify_hotel(
            "H999", file_path=self.path, name="X"
        )
        self.assertFalse(result)

    def test_modify_invalid_rooms(self):
        """Negative: modify rooms with string returns False."""
        result = Hotel.modify_hotel(
            "H1", file_path=self.path, rooms="ten"
        )
        self.assertFalse(result)

    def test_modify_negative_rooms(self):
        """Negative: modify rooms with negative returns False."""
        result = Hotel.modify_hotel(
            "H1", file_path=self.path, rooms=-1
        )
        self.assertFalse(result)


class TestHotelReserveRoom(unittest.TestCase):
    """Tests for Hotel.reserve_room."""

    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(
            suffix=".json", delete=False
        )
        self.tmp.close()
        self.path = self.tmp.name
        Hotel.create_hotel(
            "H1", "Grand", "CDMX", 2, file_path=self.path
        )

    def tearDown(self):
        if os.path.exists(self.path):
            os.unlink(self.path)

    def test_reserve_success(self):
        """Reserve a room decrements availability."""
        result = Hotel.reserve_room("H1", file_path=self.path)
        self.assertTrue(result)
        record = Hotel.display_hotel("H1", file_path=self.path)
        self.assertEqual(record["rooms_available"], 1)

    def test_reserve_no_rooms(self):
        """Negative: no rooms available returns False."""
        Hotel.reserve_room("H1", file_path=self.path)
        Hotel.reserve_room("H1", file_path=self.path)
        result = Hotel.reserve_room("H1", file_path=self.path)
        self.assertFalse(result)

    def test_reserve_nonexistent(self):
        """Negative: reserve at non-existent hotel."""
        result = Hotel.reserve_room("H999", file_path=self.path)
        self.assertFalse(result)


class TestHotelCancelReservation(unittest.TestCase):
    """Tests for Hotel.cancel_reservation."""

    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(
            suffix=".json", delete=False
        )
        self.tmp.close()
        self.path = self.tmp.name
        Hotel.create_hotel(
            "H1", "Grand", "CDMX", 2, file_path=self.path
        )
        Hotel.reserve_room("H1", file_path=self.path)

    def tearDown(self):
        if os.path.exists(self.path):
            os.unlink(self.path)

    def test_cancel_success(self):
        """Cancel reservation increments availability."""
        result = Hotel.cancel_reservation(
            "H1", file_path=self.path
        )
        self.assertTrue(result)
        record = Hotel.display_hotel("H1", file_path=self.path)
        self.assertEqual(record["rooms_available"], 2)

    def test_cancel_all_rooms_free(self):
        """Negative: all rooms already free returns False."""
        Hotel.cancel_reservation("H1", file_path=self.path)
        result = Hotel.cancel_reservation(
            "H1", file_path=self.path
        )
        self.assertFalse(result)

    def test_cancel_nonexistent(self):
        """Negative: cancel at non-existent hotel."""
        result = Hotel.cancel_reservation(
            "H999", file_path=self.path
        )
        self.assertFalse(result)


class TestHotelPersistence(unittest.TestCase):
    """Tests for Hotel persistence edge cases."""

    def test_load_nonexistent_file(self):
        """Loading from a non-existent file returns []."""
        result = Hotel.load_all("/tmp/nonexistent_hotel.json")
        self.assertEqual(result, [])

    def test_load_corrupted_json(self):
        """Negative: corrupted JSON returns []."""
        tmp = tempfile.NamedTemporaryFile(
            suffix=".json", delete=False, mode="w"
        )
        tmp.write("{invalid json")
        tmp.close()
        result = Hotel.load_all(tmp.name)
        self.assertEqual(result, [])
        os.unlink(tmp.name)

    def test_to_dict_from_dict_roundtrip(self):
        """Serialize and deserialize a Hotel."""
        hotel = Hotel("H1", "Grand", "CDMX", 10)
        hotel.rooms_available = 7
        data = hotel.to_dict()
        restored = Hotel.from_dict(data)
        self.assertEqual(restored.hotel_id, "H1")
        self.assertEqual(restored.rooms_available, 7)


if __name__ == "__main__":
    unittest.main()

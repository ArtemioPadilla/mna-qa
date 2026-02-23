"""Hotel management with JSON file persistence."""

import json
import os


class Hotel:
    """Represents a hotel with rooms that can be reserved."""

    DATA_FILE = "hotels.json"

    def __init__(self, hotel_id, name, location, rooms):
        """Initialize a Hotel instance.

        Args:
            hotel_id: Unique string identifier.
            name: Hotel display name.
            location: City or address string.
            rooms: Total number of rooms (positive int).
        """
        self.hotel_id = hotel_id
        self.name = name
        self.location = location
        self.rooms = rooms
        self.rooms_available = rooms

    def to_dict(self):
        """Serialize hotel to a dictionary."""
        return {
            "hotel_id": self.hotel_id,
            "name": self.name,
            "location": self.location,
            "rooms": self.rooms,
            "rooms_available": self.rooms_available,
        }

    @classmethod
    def from_dict(cls, data):
        """Deserialize a hotel from a dictionary."""
        hotel = cls(
            data["hotel_id"],
            data["name"],
            data["location"],
            data["rooms"],
        )
        hotel.rooms_available = data.get(
            "rooms_available", data["rooms"]
        )
        return hotel

    @staticmethod
    def load_all(file_path=None):
        """Load all hotel records from JSON file.

        Returns a list of dicts. Returns [] on error.
        """
        path = file_path or Hotel.DATA_FILE
        if not os.path.exists(path):
            return []
        try:
            with open(path, "r", encoding="utf-8") as fhandle:
                return json.load(fhandle)
        except (json.JSONDecodeError, IOError) as exc:
            print(f"Error loading {path}: {exc}")
            return []

    @staticmethod
    def save_all(records, file_path=None):
        """Save all hotel records to JSON file."""
        path = file_path or Hotel.DATA_FILE
        with open(path, "w", encoding="utf-8") as fhandle:
            json.dump(
                records, fhandle, indent=2, ensure_ascii=False
            )

    @classmethod
    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def create_hotel(cls, hotel_id, name, location, rooms,
                     file_path=None):
        """Create a new hotel and persist it.

        Returns the Hotel instance or None on failure.
        """
        if not hotel_id or not name:
            print("Error: hotel_id and name are required.")
            return None
        if not isinstance(rooms, int) or rooms <= 0:
            print("Error: rooms must be a positive integer.")
            return None

        records = cls.load_all(file_path)
        if any(r["hotel_id"] == hotel_id for r in records):
            print(f"Error: Hotel '{hotel_id}' already exists.")
            return None

        hotel = cls(hotel_id, name, location, rooms)
        records.append(hotel.to_dict())
        cls.save_all(records, file_path)
        return hotel

    @classmethod
    def delete_hotel(cls, hotel_id, file_path=None):
        """Delete a hotel by ID.

        Returns True if deleted, False if not found.
        """
        records = cls.load_all(file_path)
        original_len = len(records)
        records = [
            r for r in records if r["hotel_id"] != hotel_id
        ]
        if len(records) == original_len:
            print(f"Error: Hotel '{hotel_id}' not found.")
            return False
        cls.save_all(records, file_path)
        return True

    @classmethod
    def display_hotel(cls, hotel_id, file_path=None):
        """Display hotel information.

        Returns the hotel dict or None if not found.
        """
        records = cls.load_all(file_path)
        for record in records:
            if record["hotel_id"] == hotel_id:
                print(
                    f"Hotel: {record['name']} | "
                    f"Location: {record['location']} | "
                    f"Rooms: {record['rooms_available']}"
                    f"/{record['rooms']}"
                )
                return record
        print(f"Error: Hotel '{hotel_id}' not found.")
        return None

    @staticmethod
    def _validate_rooms(value):
        """Validate that rooms is a positive integer."""
        if not isinstance(value, int) or value <= 0:
            print("Error: rooms must be a positive integer.")
            return False
        return True

    @classmethod
    def modify_hotel(cls, hotel_id, file_path=None, **kwargs):
        """Modify hotel attributes (name, location, rooms).

        Returns True if modified, False otherwise.
        """
        records = cls.load_all(file_path)
        for record in records:
            if record["hotel_id"] == hotel_id:
                if "rooms" in kwargs:
                    if not cls._validate_rooms(kwargs["rooms"]):
                        return False
                    diff = kwargs["rooms"] - record["rooms"]
                    record["rooms_available"] = max(
                        0, record["rooms_available"] + diff
                    )
                for key in ("name", "location", "rooms"):
                    if key in kwargs:
                        record[key] = kwargs[key]
                cls.save_all(records, file_path)
                return True
        print(f"Error: Hotel '{hotel_id}' not found.")
        return False

    @classmethod
    def reserve_room(cls, hotel_id, file_path=None):
        """Reserve one room (decrement rooms_available).

        Returns True on success, False on failure.
        """
        records = cls.load_all(file_path)
        for record in records:
            if record["hotel_id"] == hotel_id:
                if record["rooms_available"] <= 0:
                    print(
                        f"Error: No rooms available at "
                        f"'{record['name']}'."
                    )
                    return False
                record["rooms_available"] -= 1
                cls.save_all(records, file_path)
                return True
        print(f"Error: Hotel '{hotel_id}' not found.")
        return False

    @classmethod
    def cancel_reservation(cls, hotel_id, file_path=None):
        """Cancel a reservation (increment rooms_available).

        Returns True on success, False on failure.
        """
        records = cls.load_all(file_path)
        for record in records:
            if record["hotel_id"] == hotel_id:
                if record["rooms_available"] >= record["rooms"]:
                    print("Error: All rooms already available.")
                    return False
                record["rooms_available"] += 1
                cls.save_all(records, file_path)
                return True
        print(f"Error: Hotel '{hotel_id}' not found.")
        return False

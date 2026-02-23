"""Reservation management with JSON file persistence."""

import json
import os

from hotel import Hotel
from customer import Customer


class Reservation:
    """Links a customer to a hotel room reservation."""

    DATA_FILE = "reservations.json"

    def __init__(self, reservation_id, customer_id, hotel_id):
        """Initialize a Reservation instance.

        Args:
            reservation_id: Unique string identifier.
            customer_id: ID of the customer making the reservation.
            hotel_id: ID of the hotel being reserved.
        """
        self.reservation_id = reservation_id
        self.customer_id = customer_id
        self.hotel_id = hotel_id

    def to_dict(self):
        """Serialize reservation to a dictionary."""
        return {
            "reservation_id": self.reservation_id,
            "customer_id": self.customer_id,
            "hotel_id": self.hotel_id,
        }

    @classmethod
    def from_dict(cls, data):
        """Deserialize a reservation from a dictionary."""
        return cls(
            data["reservation_id"],
            data["customer_id"],
            data["hotel_id"],
        )

    @staticmethod
    def load_all(file_path=None):
        """Load all reservation records from JSON file.

        Returns a list of dicts. Returns [] on error.
        """
        path = file_path or Reservation.DATA_FILE
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
        """Save all reservation records to JSON file."""
        path = file_path or Reservation.DATA_FILE
        with open(path, "w", encoding="utf-8") as fhandle:
            json.dump(
                records, fhandle, indent=2, ensure_ascii=False
            )

    @classmethod
    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def create_reservation(cls, reservation_id, customer_id,
                           hotel_id, file_path=None,
                           hotel_file=None, customer_file=None):
        """Create a reservation linking a customer to a hotel.

        Verifies that both the customer and hotel exist, and
        that the hotel has available rooms.

        Returns the Reservation instance or None on failure.
        """
        if not reservation_id:
            print("Error: reservation_id is required.")
            return None

        records = cls.load_all(file_path)
        if any(r["reservation_id"] == reservation_id
               for r in records):
            print(
                f"Error: Reservation '{reservation_id}' "
                f"already exists."
            )
            return None

        customers = Customer.load_all(customer_file)
        if not any(c["customer_id"] == customer_id
                   for c in customers):
            print(f"Error: Customer '{customer_id}' not found.")
            return None

        hotels = Hotel.load_all(hotel_file)
        if not any(h["hotel_id"] == hotel_id for h in hotels):
            print(f"Error: Hotel '{hotel_id}' not found.")
            return None

        if not Hotel.reserve_room(hotel_id, hotel_file):
            return None

        reservation = cls(reservation_id, customer_id, hotel_id)
        records.append(reservation.to_dict())
        cls.save_all(records, file_path)
        return reservation

    @classmethod
    def cancel_reservation(cls, reservation_id, file_path=None,
                           hotel_file=None):
        """Cancel a reservation and release the hotel room.

        Returns True if cancelled, False if not found.
        """
        records = cls.load_all(file_path)
        target = None
        for record in records:
            if record["reservation_id"] == reservation_id:
                target = record
                break

        if target is None:
            print(
                f"Error: Reservation '{reservation_id}' "
                f"not found."
            )
            return False

        Hotel.cancel_reservation(target["hotel_id"], hotel_file)
        records = [
            r for r in records
            if r["reservation_id"] != reservation_id
        ]
        cls.save_all(records, file_path)
        return True

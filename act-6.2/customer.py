"""Customer management with JSON file persistence."""

import json
import os


class Customer:
    """Represents a customer who can make hotel reservations."""

    DATA_FILE = "customers.json"

    def __init__(self, customer_id, name, email):
        """Initialize a Customer instance.

        Args:
            customer_id: Unique string identifier.
            name: Customer full name.
            email: Customer email address.
        """
        self.customer_id = customer_id
        self.name = name
        self.email = email

    def to_dict(self):
        """Serialize customer to a dictionary."""
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "email": self.email,
        }

    @classmethod
    def from_dict(cls, data):
        """Deserialize a customer from a dictionary."""
        return cls(
            data["customer_id"],
            data["name"],
            data["email"],
        )

    @staticmethod
    def load_all(file_path=None):
        """Load all customer records from JSON file.

        Returns a list of dicts. Returns [] on error.
        """
        path = file_path or Customer.DATA_FILE
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
        """Save all customer records to JSON file."""
        path = file_path or Customer.DATA_FILE
        with open(path, "w", encoding="utf-8") as fhandle:
            json.dump(
                records, fhandle, indent=2, ensure_ascii=False
            )

    @staticmethod
    def _validate_email(email):
        """Validate that email contains @."""
        if not email or "@" not in email:
            print("Error: a valid email is required.")
            return False
        return True

    @classmethod
    def create_customer(cls, customer_id, name, email,
                        file_path=None):
        """Create a new customer and persist it.

        Returns the Customer instance or None on failure.
        """
        if not customer_id or not name:
            print("Error: customer_id and name are required.")
            return None
        if not cls._validate_email(email):
            return None

        records = cls.load_all(file_path)
        if any(r["customer_id"] == customer_id for r in records):
            print(
                f"Error: Customer '{customer_id}' already exists."
            )
            return None

        customer = cls(customer_id, name, email)
        records.append(customer.to_dict())
        cls.save_all(records, file_path)
        return customer

    @classmethod
    def delete_customer(cls, customer_id, file_path=None):
        """Delete a customer by ID.

        Returns True if deleted, False if not found.
        """
        records = cls.load_all(file_path)
        original_len = len(records)
        records = [
            r for r in records
            if r["customer_id"] != customer_id
        ]
        if len(records) == original_len:
            print(f"Error: Customer '{customer_id}' not found.")
            return False
        cls.save_all(records, file_path)
        return True

    @classmethod
    def display_customer(cls, customer_id, file_path=None):
        """Display customer information.

        Returns the customer dict or None if not found.
        """
        records = cls.load_all(file_path)
        for record in records:
            if record["customer_id"] == customer_id:
                print(
                    f"Customer: {record['name']} | "
                    f"Email: {record['email']}"
                )
                return record
        print(f"Error: Customer '{customer_id}' not found.")
        return None

    @classmethod
    def modify_customer(cls, customer_id, file_path=None,
                        **kwargs):
        """Modify customer attributes (name, email).

        Returns True if modified, False otherwise.
        """
        records = cls.load_all(file_path)
        for record in records:
            if record["customer_id"] == customer_id:
                if "email" in kwargs:
                    if not cls._validate_email(kwargs["email"]):
                        return False
                for key in ("name", "email"):
                    if key in kwargs:
                        record[key] = kwargs[key]
                cls.save_all(records, file_path)
                return True
        print(f"Error: Customer '{customer_id}' not found.")
        return False

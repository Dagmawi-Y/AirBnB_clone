#!/usr/bin/python3
"""
Module for the BaseModel class.
"""
import uuid
from datetime import datetime
import models


class BaseModel:
    """
    Represents the base model for all other models.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes a new BaseModel instance.

        Args:
            *args: Not used.
            **kwargs: Key-value pairs of attributes.
        """
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if "created_at" in kwargs:
                self.created_at = datetime.strptime(
                    kwargs["created_at"], "%Y-%m-%dT%H:%M:%S.%f"
                )
            if "updated_at" in kwargs:
                self.updated_at = datetime.strptime(
                    kwargs["updated_at"], "%Y-%m-%dT%H:%M:%S.%f"
                )
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        """
        Returns a string representation of the BaseModel instance.
        """
        return "[{}] ({}) {}".format(
            self.__class__.__name__, self.id, self.__dict__
        )

    def __repr__(self):
        """
        Returns a string representation of the BaseModel instance.
        """
        return self.__str__()

    def save(self):
        """
        Updates the updated_at attribute and saves the instance to storage.
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """
        Returns a dictionary representation of the BaseModel instance.
        """
        new_dict = self.__dict__.copy()
        new_dict["__class__"] = self.__class__.__name__
        new_dict["created_at"] = self.created_at.isoformat()
        new_dict["updated_at"] = self.updated_at.isoformat()
        return new_dict
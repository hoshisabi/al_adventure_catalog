# adventure_model.py
from dataclasses import dataclass, field
import datetime
from decimal import Decimal
from typing import List, Optional, Any, Dict

@dataclass
class Adventure:
    product_id: str
    title: Optional[str] = None
    full_title: Optional[str] = None
    authors: List[str] = field(default_factory=list)
    code: Optional[str] = None
    date_created: Optional[datetime.date] = None
    # hours: Now expects ["X-Y"] for ranges or ["X"] for single values
    hours: List[str] = field(default_factory=list)
    tiers: List[str] = field(default_factory=list) # e.g., ["1", "2", "3", "4"]
    apl_values: List[str] = field(default_factory=list) # e.g., ["1", "2", "3", "4"] for APLs covered
    level_ranges: List[str] = field(default_factory=list) # e.g., ["1-4", "5-10"] for levels
    url: Optional[str] = None
    campaigns: List[str] = field(default_factory=list)
    season: Optional[str] = None
    is_adventure: Optional[bool] = None
    price: Optional[Decimal] = None
    needs_review: bool = False # Flag for human intervention

    def to_json(self) -> Dict[str, Any]:
        """Converts the Adventure object to a JSON-serializable dictionary."""
        data = self.__dict__.copy()
        # Convert datetime.date to string
        if isinstance(data.get("date_created"), datetime.date):
            data["date_created"] = data["date_created"].isoformat()
        # Convert Decimal to string
        if isinstance(data.get("price"), Decimal):
            data["price"] = str(data["price"])

        # Ensure lists are not None, but empty lists instead, and other None handling
        for k in ['authors', 'hours', 'tiers', 'apl_values', 'level_ranges', 'campaigns']:
            if data.get(k) is None:
                data[k] = []
        
        # Remove fields that should not be in the final JSON if they are None or empty lists
        # (This is more for cleaner output, not strict schema enforcement)
        keys_to_remove = []
        for k, v in data.items():
            if v is None or (isinstance(v, list) and not v):
                # We want to keep False for needs_review, so exclude it
                if k != 'needs_review':
                    keys_to_remove.append(k)
        
        for k in keys_to_remove:
            del data[k]

        return data

    @classmethod
    def from_json(cls, json_data: Dict[str, Any]) -> 'Adventure':
        """Creates an Adventure object from a JSON dictionary."""
        # Convert string back to Decimal
        if 'price' in json_data and json_data['price'] is not None:
            json_data['price'] = Decimal(str(json_data['price'])) # Ensure it's string for Decimal conversion
        # Convert string back to datetime.date
        if 'date_created' in json_data and json_data['date_created'] is not None:
            # Handle potential different date formats if they exist, or ISO format
            if isinstance(json_data['date_created'], str):
                try:
                    json_data['date_created'] = datetime.date.fromisoformat(json_data['date_created'])
                except ValueError:
                    # Fallback for old format if necessary, though new system should write ISO
                    try:
                        json_data['date_created'] = datetime.datetime.strptime(json_data['date_created'], '%Y%m%d').date()
                    except ValueError:
                        json_data['date_created'] = None # If still fails, set to None
            else: # If it's already a date object (e.g., from existing in-memory object)
                pass


        # Ensure 'needs_review' is correctly handled if it was not in old JSONs
        if 'needs_review' not in json_data:
            json_data['needs_review'] = False # Default for old files

        # Filter out keys not in the dataclass constructor to prevent errors
        valid_keys = {f.name for f in dataclass.__init__.__wrapped__.__annotations__.values() if hasattr(f, 'name')}
        filtered_json_data = {k: v for k, v in json_data.items() if k in cls.__dataclass_fields__}
        
        return cls(**filtered_json_data)
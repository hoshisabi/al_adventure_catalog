# Refactoring Plan

## Local Storage Migration
- **Goal**: Move from external JSON/cookie-based inventory to browser Local Storage.
- **Benefits**: Better persistence, no size limits like cookies, easier offline access.
- **Tasks**:
    - Update `filter.js` to load from/save to `localStorage`.
    - Provide import/export functionality for the `product_id -> URL` mapping.
    - Deprecate cookie-based `inventory_url` in favor of local management.

## Local Storage for Private Inventory (Added 2026-02-09)
- Maintain the list of product ID -> drive link in local storage as an alternative plan.

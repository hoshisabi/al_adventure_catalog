# Adventure Code Recognition Rules

This document explains how the adventure catalog tooling recognizes and parses various adventure codes from product titles on DMsGuild.

## Overview

The system uses a series of regular expressions and prefix-based matching to identify adventure codes. This process happens in two main places:
1. `adventure_utils.py`: Contains the primary regex-based extraction logic (`get_adventure_code_and_campaigns`).
2. `adventure.py`: Contains legacy and fallback logic for code recognition (`get_dc_code_and_campaign`).

## Supported Code Formats

### 1. Adventurers League (DDAL/DDEX)
Standard Adventurers League modules follow the `DDALSS-EE` or `DDEXSS-EE` format, where `SS` is the season and `EE` is the episode number.

*   **Normalization**: Single-digit seasons are automatically zero-padded for consistency.
*   **Examples**:
    *   `DDEX3-01` → `DDEX03-01`
    *   `DDAL5-01` → `DDAL05-01`
    *   `DDAL10-01` → `DDAL10-01` (No padding for 10+)

### 2. DungeonCraft (DC)
DungeonCraft adventures use a variety of prefixes followed by `-DC-` and a series identifier.

*   **Format**: `{Campaign}-DC-{Identifier}-{Number}`
*   **Campaign Prefixes**: `FR` (Forgotten Realms), `EB` (Eberron), `RV` (Ravenloft), `DL` (Dragonlance), `SJ` (Spelljammer), `PS` (Planescape), `WBW` (Wild Beyond the Witchlight).
*   **Examples**:
    *   `FR-DC-STRAT-TALES-02`
    *   `PS-DC-NBDD-01`
    *   `RV-DC-DBH-01`
    *   `DC-POA-ICE01-01` (Normalized to `DC-POA` for Season 10)

### 3. Community Content (CCC)
Convention-Created Content modules.

*   **Normalization**: The system ensures a dash follows the `CCC` prefix if it's missing.
*   **Examples**:
    *   `CCC-BMG-01`
    *   `CCCTHENT01-03` → `CCC-THENT01-03`
    *   `CCC-GSP-01-01`

### 4. Hardcover Tie-ins (DDHC/DDIA)
Adventures that tie into official hardcover releases.

*   **DDHC Examples**: `DDHC-TOA-10`, `DDHC-MORD-03`
*   **DDIA Examples**: `DDIA-MORD`, `DDIA-VOLO`, `DDIA05`

### 5. Eberron Salvage Missions (EB-SM)
Special missions for the Oracle of War campaign.

*   **Examples**: `EB-SM-01`, `EB-SM-METALLUS`, `EB-SM-GHOST`

### 6. Dreams of the Red Wizards (DRW)
Modern AL campaign content.

*   **Examples**: `DDAL-DRW-01`, `BMG-DRW-01`

## Special Cases

### BK to PO-BK Mapping
Some adventures from the "Border Kingdoms" series use a `BK-` prefix in their titles without the standard `PO-` prefix. The system recognizes these as part of the `PO-BK` (Forgotten Realms) campaign.

*   **Rule**: If a code starts with `BK-` followed by numbers, it is mapped to the `Forgotten Realms` campaign.
*   **Example**: `BK-05-02` is recognized as part of the `PO-BK` series.

### Dash Normalization
The system automatically normalizes various Unicode dash variants (like en-dash `–` or em-dash `—`) to standard hyphens `-` before processing, ensuring consistent matching.

### Campaign Mapping
If a code is successfully extracted, the system uses a mapping table to assign the correct campaign:
*   `DDAL04` → `Forgotten Realms`, `Ravenloft`
*   `EB-DC` → `Eberron`
*   `DL-DC` → `Dragonlance`
*   `RV-DC` → `Ravenloft`
*   Most others default to `Forgotten Realms` based on prefix or AL season rules.

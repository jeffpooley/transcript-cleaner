#!/usr/bin/env python3

import json
import re
from pathlib import Path

print("=== CLEANING AND FINALIZING V2 EXTRACTION ===\n")

# Load extracted files
with open('extracted_dictionary_v2.json', 'r', encoding='utf-8') as f:
    extracted_dict = json.load(f)

with open('extracted_acronyms_v2.json', 'r', encoding='utf-8') as f:
    extracted_acronyms = json.load(f)

# Load existing dictionaries
with open('dictionary.json', 'r', encoding='utf-8') as f:
    existing_dict = json.load(f)

with open('acronyms.json', 'r', encoding='utf-8') as f:
    existing_acronyms = json.load(f)

# Clean extracted dictionary
polished_dict = {}

# Words that shouldn't start a proper name
bad_starts = {
    'and', 'but', 'or', 'so', 'because', 'since', 'when', 'where',
    'what', 'which', 'this', 'that', 'there', 'then', 'they',
    'he', 'she', 'it', 'we', 'you', 'i', 'if', 'for', 'with',
    'from', 'about', 'after', 'before', 'during', 'while',
    'did', 'was', 'were', 'had', 'has', 'have', 'is', 'are',
    'do', 'does', 'will', 'would', 'could', 'should', 'can',
    'may', 'might', 'must', 'shall', 'got', 'get', 'like',
    'also', 'although', 'an', 'as', 'at'
}

# Common non-name phrases to exclude
exclude_phrases = {
    'african american', 'american states', 'american embassy',
    'bar association', 'brown sugar', 'cable awards',
    'the world', 'the united', 'the state', 'the national',
    'the american', 'the international', 'the federal',
    'boxing specials', 'special programming', 'entertainment network',
    'los angeles california', 'california hollywood los',
    'boulevard east', 'movie channel', 'television network',
    'american medical association', 'american scholar'
}

for key, value in extracted_dict.items():
    # Remove line breaks and normalize whitespace
    value = re.sub(r'\s+', ' ', value).strip()
    key = re.sub(r'\s+', ' ', key).strip()

    # Skip if empty after cleaning
    if not key or not value:
        continue

    # Skip if starts with a bad word
    first_word = key.split()[0].lower()
    if first_word in bad_starts:
        continue

    # Skip if in exclude list
    if key in exclude_phrases:
        continue

    # Skip if it's a generic phrase (contains articles, prepositions)
    if any(word in key.split() for word in ['the', 'of', 'in', 'on', 'at', 'to', 'a', 'an']):
        continue

    # Skip possessives (names ending with 's)
    if value.endswith("'s"):
        continue

    # Skip if value is too short or too long
    if len(value) < 4 or len(value) > 50:
        continue

    # Keep names that look like person names (2-3 words, each capitalized)
    # or proper nouns like "Annenberg School"
    words = value.split()
    if 2 <= len(words) <= 3:
        # All words should be capitalized properly
        if all(w[0].isupper() or w in ["'s", "'", "-"] for w in words if w):
            polished_dict[key] = value

# Clean extracted acronyms
polished_acronyms = {}
exclude_acronyms = {'TV', 'PR', 'OK'}  # Too common/short or errors
fix_acronyms = {
    'USA': 'United States of America'
}

for acronym, expansion in extracted_acronyms.items():
    if acronym in exclude_acronyms:
        continue

    # Normalize whitespace
    expansion = re.sub(r'\s+', ' ', expansion).strip()

    if acronym in fix_acronyms:
        expansion = fix_acronyms[acronym]

    polished_acronyms[acronym] = expansion

# Merge with existing (existing takes precedence for conflicts)
merged_dict = {**polished_dict, **existing_dict}
merged_acronyms = {**polished_acronyms, **existing_acronyms}

# Sort
merged_dict = dict(sorted(merged_dict.items()))
merged_acronyms = dict(sorted(merged_acronyms.items()))

# Calculate statistics
new_dict_entries = set(polished_dict.keys()) - set(existing_dict.keys())
new_acronym_entries = set(polished_acronyms.keys()) - set(existing_acronyms.keys())

print(f"Dictionary:")
print(f"  Raw extracted: {len(extracted_dict)}")
print(f"  After cleaning: {len(polished_dict)}")
print(f"  Existing entries: {len(existing_dict)}")
print(f"  New entries from extraction: {len(new_dict_entries)}")
print(f"  Total after merge: {len(merged_dict)}\n")

print(f"Acronyms:")
print(f"  Raw extracted: {len(extracted_acronyms)}")
print(f"  After cleaning: {len(polished_acronyms)}")
print(f"  Existing entries: {len(existing_acronyms)}")
print(f"  New entries from extraction: {len(new_acronym_entries)}")
print(f"  Total after merge: {len(merged_acronyms)}\n")

# Save merged files
with open('merged_dictionary.json', 'w', encoding='utf-8') as f:
    json.dump(merged_dict, f, indent=2, ensure_ascii=False)

with open('merged_acronyms.json', 'w', encoding='utf-8') as f:
    json.dump(merged_acronyms, f, indent=2, ensure_ascii=False)

print("✓ Saved merged_dictionary.json")
print("✓ Saved merged_acronyms.json\n")

# Show new additions
if new_dict_entries:
    print(f"New dictionary entries ({len(new_dict_entries)}):")
    for i, key in enumerate(sorted(new_dict_entries)):
        if i >= 40:  # Show first 40
            print(f"  ... and {len(new_dict_entries) - 40} more")
            break
        print(f'  "{key}" → "{merged_dict[key]}"')
    print()

if new_acronym_entries:
    print(f"New acronym entries ({len(new_acronym_entries)}):")
    for acronym in sorted(new_acronym_entries):
        print(f'  "{acronym}" → "{merged_acronyms[acronym]}"')
    print()

print("=== NEXT STEPS ===")
print("1. Review merged_dictionary.json and merged_acronyms.json")
print("2. Remove any unwanted entries")
print("3. When satisfied, replace dictionary.json and acronyms.json:")
print("   mv merged_dictionary.json dictionary.json")
print("   mv merged_acronyms.json acronyms.json")
print("4. Commit and push to GitHub\n")

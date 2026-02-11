#!/usr/bin/env python3

import json

print("=== FINAL CLEANUP - Removing only obvious errors ===\n")

# Load merged files
with open('merged_dictionary.json', 'r', encoding='utf-8') as f:
    merged_dict = json.load(f)

with open('merged_acronyms.json', 'r', encoding='utf-8') as f:
    merged_acronyms = json.load(f)

# Remove only obvious non-names (keep institutions and places)
remove_dict = {
    'black community',
    'black perspective',
    'business ethics',
    'circuit court',
    'communication associations',
    'communication alumni oral',
    'chicken noodle network'  # Nickname for CNN, not needed
}

# Remove obvious acronym errors
remove_acronyms = {
    'SAGE',  # Wrong: "Publications"
    'THREE'  # Wrong: "[footnotes"
}

# Clean dictionary
cleaned_dict = {k: v for k, v in merged_dict.items() if k not in remove_dict}

# Clean acronyms
cleaned_acronyms = {k: v for k, v in merged_acronyms.items() if k not in remove_acronyms}

# Save cleaned versions
with open('merged_dictionary.json', 'w', encoding='utf-8') as f:
    json.dump(cleaned_dict, f, indent=2, ensure_ascii=False)

with open('merged_acronyms.json', 'w', encoding='utf-8') as f:
    json.dump(cleaned_acronyms, f, indent=2, ensure_ascii=False)

print(f"Dictionary: Removed {len(remove_dict)} generic concepts")
for item in sorted(remove_dict):
    print(f'  - "{item}"')

print(f"\nAcronyms: Removed {len(remove_acronyms)} errors")
for item in sorted(remove_acronyms):
    print(f'  - "{item}"')

print(f"\nFinal counts:")
print(f"  Dictionary: {len(cleaned_dict)} entries")
print(f"  Acronyms: {len(cleaned_acronyms)} entries")

print("\n✓ Cleaned merged_dictionary.json")
print("✓ Cleaned merged_acronyms.json")

print("\nKept institutions and places like:")
print("  - Boston University, Columbia University")
print("  - Beverly Hills")
print("  - Comedy Central")
print("  - American Cancer Society")
print("\nReady to replace your dictionary.json and acronyms.json files!")

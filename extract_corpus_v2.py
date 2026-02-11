#!/usr/bin/env python3

import os
import re
import json
from pathlib import Path

# Read all XML files from the example directory
xml_dir = Path(__file__).parent / 'example xml transcripts'
files = list(xml_dir.glob('*.xml'))

print(f"Found {len(files)} XML files to process...\n")

all_proper_names = set()
all_acronyms = {}

# Process each XML file
for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"Processing: {file_path.name}")

    # Try to extract VTT transcript first
    vtt_match = re.search(r'<vtt_transcript><!\[CDATA\[(.*?)\]\]></vtt_transcript>', content, re.DOTALL)

    # If no VTT, try plain text transcript
    if not vtt_match:
        plain_match = re.search(r'<transcript>(.*?)</transcript>', content, re.DOTALL)
        if plain_match:
            transcript = plain_match.group(1)
            print(f"  Found plain text transcript")
        else:
            print(f"  ⚠️  No transcript found")
            continue
    else:
        transcript = vtt_match.group(1)
        print(f"  Found VTT transcript")

    # Extract acronym expansions: ACRONYM [Full Name]
    # Pattern: all-caps word (2+ letters) followed by [expansion]
    acronym_pattern = r'\b([A-Z]{2,})\s+\[([^\]]+)\]'
    acronym_matches = re.finditer(acronym_pattern, transcript)
    acronym_count = 0

    for match in acronym_matches:
        acronym = match.group(1)
        full_name = match.group(2)

        # Skip if it's a speaker label (followed by colon)
        speaker_pattern = rf'\b{re.escape(acronym)}:\s'
        if re.search(speaker_pattern, transcript):
            continue

        # Add to acronyms (prefer first occurrence if duplicates)
        if acronym not in all_acronyms:
            all_acronyms[acronym] = full_name
            acronym_count += 1

    # Extract proper names: 2-3 consecutive capitalized words
    # Remove timestamp lines, speaker labels, footnote markers, and expansion brackets first
    cleaned_transcript = transcript
    cleaned_transcript = re.sub(r'^\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}$', '', cleaned_transcript, flags=re.MULTILINE)
    cleaned_transcript = re.sub(r'^(Q\d*|[A-Z]+):\s', '', cleaned_transcript, flags=re.MULTILINE)
    cleaned_transcript = re.sub(r'\[\[footnote\]\].*?\[\[/footnote\]\]', '', cleaned_transcript)
    cleaned_transcript = re.sub(r'\[([^\]]+)\]', '', cleaned_transcript)

    # Pattern: 2-3 consecutive capitalized words
    name_pattern = r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z']+){1,2})\b"
    name_matches = re.finditer(name_pattern, cleaned_transcript)
    name_count = 0

    skip_words = {
        'The', 'And', 'But', 'For', 'With', 'From', 'When', 'Where',
        'What', 'Which', 'This', 'That', 'There', 'Then', 'They',
        'He Said', 'She Said', 'I Said', 'You Know', 'I Think',
        'New York', 'Los Angeles', 'United States', 'Time Warner',
        'Every Time', 'First Time', 'Long Time', 'Good Time',
        'One Time', 'Same Time', 'Next Time', 'Last Time',
        'All The', 'In The', 'On The', 'At The', 'To The',
        'Of The', 'For The', 'With The', 'By The', 'From The',
        'Freedom Forum', 'University Of', 'Columbia University'
    }

    for match in name_matches:
        name = match.group(1)

        # Skip common non-names
        if name in skip_words:
            continue

        # Only include if it looks like a person name (not all caps, not single letter words)
        if not re.match(r'^[A-Z\s\']+$', name) and not re.search(r'\b[A-Z]\b', name):
            all_proper_names.add(name)
            name_count += 1

    print(f"  ✓ Found {acronym_count} new acronyms, {name_count} proper name instances\n")

# Convert sets to sorted lists/dicts
proper_names_list = sorted(list(all_proper_names))

# Create dictionary entries (correct -> correct for whitelisting)
dictionary = {}
for name in proper_names_list:
    key = name.lower()
    dictionary[key] = name

# Sort acronyms alphabetically
sorted_acronyms = dict(sorted(all_acronyms.items()))

# Output results
print('\n=== EXTRACTION COMPLETE ===\n')
print(f"Total unique proper names: {len(proper_names_list)}")
print(f"Total unique acronyms: {len(sorted_acronyms)}\n")

# Save to files
script_dir = Path(__file__).parent
extracted_dict_path = script_dir / 'extracted_dictionary_v2.json'
extracted_acronyms_path = script_dir / 'extracted_acronyms_v2.json'

with open(extracted_dict_path, 'w', encoding='utf-8') as f:
    json.dump(dictionary, f, indent=2, ensure_ascii=False)

with open(extracted_acronyms_path, 'w', encoding='utf-8') as f:
    json.dump(sorted_acronyms, f, indent=2, ensure_ascii=False)

print(f"✓ Saved extracted dictionary to: extracted_dictionary_v2.json")
print(f"✓ Saved extracted acronyms to: extracted_acronyms_v2.json\n")

# Show samples
print('Sample proper names (first 15):')
for name in proper_names_list[:15]:
    print(f'  "{name.lower()}" → "{name}"')

print(f'\n... and {len(proper_names_list) - 15} more' if len(proper_names_list) > 15 else '')

print('\nSample acronyms (first 15):')
for i, (acronym, full) in enumerate(sorted_acronyms.items()):
    if i >= 15:
        break
    print(f'  "{acronym}" → "{full}"')

print('\n=== NEXT STEPS ===')
print('Run clean_extracted.py and finalize_corpus.py again with the new v2 files\n')

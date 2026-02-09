# VTT Transcript Cleaner

A web-based tool for cleaning and restructuring VTT transcripts from oral history interviews. Designed to work with MacWhisper transcripts.

## Features

- **Text Corrections**
  - Dictionary-based substitutions for proper names and terms
  - Automatic removal of filler words (uh, um)
  - Case-insensitive matching for phonetic variations

- **Timestamp Restructuring**
  - Consolidates timestamps around speaker turns (marked by `NAME:`)
  - Splits segments longer than 2 minutes at sentence boundaries
  - Maintains proper VTT format

- **Safety & Transparency**
  - Never overwrites original files
  - Generates detailed change report
  - Side-by-side diff view of original vs corrected
  - Downloads as `_corrected.vtt`

## Usage

### Local Mac Usage

1. Open `index.html` in your web browser (Chrome, Safari, Firefox, etc.)
2. Select your VTT transcript file
3. Click "Process Transcript" (dictionary is already built-in!)
4. Review the changes in the side-by-side view
5. Download the corrected VTT and report

### Built-in Dictionary

The app includes a built-in dictionary for communication research oral histories. To edit the dictionary:
1. Open `index.html` in a text editor
2. Find the `dictionary` object near the top of the `<script>` section
3. Add/remove/modify entries as needed
4. Save the file

**Optional:** You can still upload a custom dictionary JSON file to override the built-in one for specific projects.

### Dictionary Format

The dictionary uses this format (whether built-in or uploaded):

```json
{
  "gobner": "Gerbner",
  "gerbner": "Gerbner",
  "terry gross": "Terry Gross",
  "teri gross": "Terry Gross",
  "npr": "NPR"
}
```

**Tips:**
- All matching is case-insensitive
- Whole word matching only (won't replace partial matches)
- Add multiple entries for common phonetic variations
- The built-in dictionary is perfect for recurring names across multiple interviews

## Requirements

- Speaker turns must be marked with `NAME:` at the start of paragraphs (e.g., `GROSS:`)
- VTT file from MacWhisper or similar transcription tool

## Acronym Expansion

The app automatically expands acronyms on first mention by adding the full name in square brackets:
- Example: `HBO` → `HBO [Home Box Office]` (first mention only)
- Subsequent mentions remain as just `HBO`
- Excludes common words: TV, US, OK, AM, PM, single letters

**Built-in acronyms include:** HBO, NPR, PBS, FCC, CBS, NBC, ABC, BBC, CNN, ESPN, MTV, MLB, NFL, NBA, NHL, NCAA

### Acronym Manager (NEW!)

Add new acronyms via the UI - no file editing needed!

**Workflow:**
1. In the "Acronym Manager" section, enter:
   - Acronym (e.g., "FTC")
   - Full name (e.g., "Federal Trade Commission")
2. Click "Add to Acronyms" (or press Enter)
3. Custom additions are saved to browser localStorage
4. When done, click "Download Updated Acronyms"
5. Save as `acronyms.json` in the app folder
6. Replace the old `acronyms.json` file
7. Refresh browser to load updated acronyms

**Features:**
- View all custom additions
- Delete unwanted entries
- Works immediately (no refresh needed)
- Download merged acronyms (built-in + custom)

## Proper Name Marking (NEW!)

First mentions of full human names (2-3 word names) are automatically marked with double curly brackets for easy identification and verification:
- Detects multi-word names: `{{Terry Gross}}`, `{{George Gerbner}}`, `{{Marty Glickman}}`
- Only marks names with 2-3 consecutive capitalized words (typical for full human names)
- Skips single-word names, place names, and organizations
- Subsequent mentions are not marked (only first reference)
- After processing, search for `{{` in the editable transcript to find all flagged names
- Verify spellings and remove brackets once confirmed

## Hard-Coded Rules

The following corrections are applied automatically:
- Remove "uh" and "um" (with or without trailing commas)
- Replace colloquialisms:
  - "gonna" → "going to"
  - "gotta" → "got to"
  - "'em" → "them"
  - "yeah" → "yes" (preserves capitalization)
- Remove quotation marks and handle formatting:
  - `He said "this is a quote"` → `He said, This is a quote` (adds comma, capitalizes)
  - `He said, "this is a quote"` → `He said, This is a quote` (keeps comma, capitalizes)
  - `"The whole sentence"` → `The whole sentence` (capitalizes)
  - Handles both straight (`"`) and curly (`""`) quotes
- Capitalize first word after speaker labels:
  - `GROSS: hello there` → `GROSS: Hello there`
  - `Q1: the answer` → `Q1: The answer`
  - Exception: `GROSS: —and that` stays lowercase (after em-dash)
- Replace double hyphens (--) with em-dashes (—), removing spaces on either side
- Clean up extra whitespace

## Future Enhancements

- Deploy to GitHub Pages for iPad access
- Additional customizable rules
- Batch processing multiple files
- Import proper names dictionary from existing corrected transcripts

## Technical Details

- Pure HTML/CSS/JavaScript - no build process required
- Works entirely in the browser - no server needed
- Compatible with all modern browsers

## License

Private project for oral history transcript processing.

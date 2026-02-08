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
3. Optionally select a dictionary JSON file (see format below)
4. Click "Process Transcript"
5. Review the changes in the side-by-side view
6. Download the corrected VTT and report

### Dictionary Format

Create a JSON file with phonetic variations mapped to correct spellings:

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
- Build your dictionary incrementally as you process files

## Requirements

- Speaker turns must be marked with `NAME:` at the start of paragraphs (e.g., `GROSS:`)
- VTT file from MacWhisper or similar transcription tool

## Hard-Coded Rules

The following corrections are applied automatically:
- Remove "uh" and "um" (with or without trailing commas)
- Replace colloquialisms:
  - "gonna" → "going to"
  - "gotta" → "got to"
  - "'em" → "them"
- Replace double hyphens (--) with em-dashes (—), removing spaces on either side
- Clean up extra whitespace

## Future Enhancements

- Deploy to GitHub Pages for iPad access
- Extract proper names from existing corrected PDF transcripts
- Additional customizable rules
- Batch processing multiple files

## Technical Details

- Pure HTML/CSS/JavaScript - no build process required
- Works entirely in the browser - no server needed
- Compatible with all modern browsers

## License

Private project for oral history transcript processing.

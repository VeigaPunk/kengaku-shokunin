# Fetch receipt — Zenodo record 22769923

- URL (landing): https://zenodo.org/records/22769923
- URL (bytes fetched): https://zenodo.org/records/22769923/files/184_phase22E_prereg_v1.md (record's markdown alternate; served as text/markdown)
- Access date: 2026-10-30 (UTC)
- Fetch method: read tool, alternate-markdown (HTTP success)
- Title: "184 · ΦΑΣΗ 22.Ε — ΠΡΟ-ΔΗΛΩΣΗ v1" (Phase 22.E pre-declaration v1, Linear A / Knossos scope criterion)
- Document date: 15 September 2026; status line says "ΜΗ ΚΛΕΙΔΩΜΕΝΟ — εκκρεμεί κλείδωμα κατωφλίων" (NOT LOCKED — threshold locking pending) as of the document text itself

## Located quotes (verbatim)

§9 "Χρονοσφράγιση — δίδαγμα #19" (Timestamping — lesson #19), the ordered protocol:

> 1. Κατάθεση της προ-δήλωσης στο Zenodo · `ots stamp`
> 2. Αναμονή αγκύρωσης σε block του Bitcoin · καταγραφή ύψους block
> 3. **Μετά**: εκτέλεση του harvester · `ots stamp` στο παραγόμενο CSV
> 4. Καταγραφή του ύψους block των δεδομένων και του **διαστήματος** μεταξύ των δύο

(translation: 1. Deposit the pre-declaration at Zenodo · `ots stamp`. 2. Wait for anchoring in a Bitcoin block · record block height. 3. **After that**: run the harvester · `ots stamp` the produced CSV. 4. Record the data's block height and the **interval** between the two.)

Same section, closing lines:

> Το διάστημα αναφέρεται ως μέγεθος της μελέτης. Είναι το τεκμήριο τυφλότητας.

(translation: The interval is reported as a measure of the study. It is the evidence of blinding.)

§2, acquisition commitment:

> Η συγκομιδή γίνεται με το `185_damos_kn_full_harvester.py`, με το φίλτρο token αντιγραμμένο αυτολεξεί από το `054_wingspread_parser.py`, **μετά** την κατάθεση της παρούσας προ-δήλωσης.

(translation: The harvest is done with `185_damos_kn_full_harvester.py`, ..., **after** the deposition of this pre-declaration.)

§8, deposit gate (§ "Πύλη κατάθεσης — δίδαγμα #17"):

> Ο harvester **και** ο runner αρνούνται να τρέξουν αν δεν υπάρχει `184.PROOF.txt` που περιέχει:
> 1. το Zenodo DOI της κατάθεσης αυτού του αρχείου, και
> 2. το SHA-256 του `184_phase22E_prereg_v1.md` όπως κατατέθηκε,
> και το SHA-256 του αρχείου στον δίσκο να ταιριάζει.

(translation: The harvester **and** the runner refuse to run unless a `184.PROOF.txt` exists containing: 1. the Zenodo DOI of the deposition of this file, and 2. the SHA-256 of `184_phase22E_prereg_v1.md` as deposited, and the on-disk file's SHA-256 matching.)

## Note

This is the strongest hit of the sweep: a publicly deposited, dated preregistration that hard-codes an OpenTimestamps→Bitcoin-block anchoring of the prereg before any data acquisition, uses block-height ordering (prereg anchor precedes data anchor) as the published blinding evidence, and gates tool execution on a deposited SHA-256. Verdict treatment in prior-art.md: known for leg (a).

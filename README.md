# Add Ranges and page numbers to IIIF Manifest from a CSV.

Specific to a workflow of the Bibliotheca Hertziana.

## Usage

```sh
python3 addmeta.py [-h] -u URI -i INPUTFILE -c CSVFILE [-o OUTPUTFILE]
```

## CSV structure:

Use level to nest TOC entries.

```csv
filename,canvas label,structure,level
p0001,59r,Philosophia magnetica per principia propria proposita et ad prima in suo genere promota,0
p0002,59v,[blank],1
p0003,60r,Lectori,1
```

Headers _may_ be changed.

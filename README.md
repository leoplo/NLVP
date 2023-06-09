# NLVP

Tool to find keywords in scanned PDFs initially created to go through french
"actes administratifs".


## collaborative maps

[https://sunders.uber.space/](https://sunders.uber.space/) and
[https://www.sous-surveillance.net/-la-carte-.html](https://www.sous-surveillance.net/-la-carte-.html)
are 2 collaborative maps to which anyone can contribute.
To locate surveillance devices in France one should go through
"actes administratifs" as indicated in the
"[guide vidéosurveillance de Technopolice](https://technopolice.fr/guide-videosurveillance.pdf)".


## dependencies

Optical Character Recognition is done by
[tesseract-ocr](https://tesseract-ocr.github.io/).


## installation


### Debian

```bash
# apt install python3-pip tesseract-ocr
$ pip3 install pytesseract pdf2image
```


## usage


### GUI

```bash
$ ./nlvp
```


### CLI

Search for keyword `vidéoprotection` (default keyword)
```bash
$ ./nlvp --cli -f path_to_pdf_file
```

Search for keywords `autorisation` and `vidéosurveillance`
```bash
$ ./nlvp --cli -f path_to_pdf_file -k autorisation vidéosurveillance
```

## test cases

Until now the script has been used on
[https://www.nord.gouv.fr/contenu/telechargement/78311/479701/file/Recueil+N%C2%B0254+sp+du+03+Novembre+2021.pdf](https://www.nord.gouv.fr/contenu/telechargement/78311/479701/file/Recueil+N%C2%B0254+sp+du+03+Novembre+2021.pdf)
and [https://www.ville-gravelines.fr/sites/default/files/autorisation_prefectoral_videoprotection_intermarche.pdf](https://www.ville-gravelines.fr/sites/default/files/autorisation_prefectoral_videoprotection_intermarche.pdf)
and seems to do fine.

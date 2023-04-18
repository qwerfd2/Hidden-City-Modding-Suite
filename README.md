Hidden-City-Modding-Suite

Two scripts that can extract the content of ```.v_sf``` files for The Hidden City - Hidden Mystery, and another script that can decrypt the ```save_data.xml``` save file.

---

**extract.py**: Extract ```.v_sf``` file(s).

 - Extract every ```.v_sf``` file under the same directory: ```python extract.py all output_dir```

 - Extract a single ```.v_sf``` file under the same directory: ```python extract.py pack.v_sf output_dir```

Files will be extracted to ```output_dir``` folder.

---


**save.py**: Decrypt save file ```save_data.xml``` or encrypt ```plaintext.xml``` under the same directory.

Decrypt ```save_data.xml```: ```python save.py d```, plaintext save will be saved to ```plaintext.xml```.

Encrypt ```plaintext.xml```: ```python save.py e```, encrypted save will be saved to ```save_data.xml```.

Encrypt is currently unnecessary as the game accepts plaintext.

---
 
Dependencies:

 - script.py: ```python 3```
 
 - decrypt.py: ```python 3```

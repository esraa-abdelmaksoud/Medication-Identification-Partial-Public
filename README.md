# **Drug Detection**
Adding drug details to a system without typing can be challenging if there is no code on its pack. Though there should be at least one type of code printed on the pack such as a barcode, some manufacturers still don't print any codes on their products. This leads to a tough workload for pharmacy technicians because they have to create new barcodes for such products. This repository includes a solution to detect drug details from the packagings, but some parts are removed until publishing a detailed article of this solution.

The solution includes use of:
1) OCR
2) Image pre-processing
3) Fuzzy matching
4) Spelling correction

The following is an example for the solution:

**Input**

![20210831_144347](https://user-images.githubusercontent.com/73304837/151094845-92c150bf-7b8e-4700-96f9-694c90395736.jpg)

**Output**
```
- Name: Flumox
- Dose: 1000
- Size: 15
- Type: tablets
```

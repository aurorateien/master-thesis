# master-thesis
Necessary scripts for my master thesis: 3D electron diffraction for structure determination

1. _AuCalibration.ipynb_: Used for determining ellipticity distortion in test sample (Au). Adapted script from Tina Bergh.
2. _applyMatrixToData.ipynb_: Apply distortion correction to data. 
3. _removeRectangle.ipynb_: Removes untrusted rectangle for all .tiff files in folder. 
4. _Manual datasets_: Necessary datasets used in the manual. Includes an Excel file with an overview of all datasets with corresponding data collection parameters.
5. _ContRotDataConverter_: Script adapted from Stockholm (PhD-student Evgeniia Ikonnikova) for conversion of fileformats and removal of untrusted rectangle. Features for correcting distortion is also included. Note that these features are not optimized for the NTNU detector, except the cameralength and scale are adapted to NTNU setup. Follow the Word-manual in the folder for usage. Simple GUI is available by running dataConverterGUI.py. 

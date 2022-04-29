# Using Keystroke Dynamics to Authenticate a User Based on their Typing

This is the repository for the above project. It involves recording a users keystrokes and being able to ensure that they are who they say they are.


## Requirements and running the program

The project only runs on Windows 10. It has been tested and created on python 3.9 and as such has only been guarenteed to work on this version. The program requires the user to have admin priviliges and as such will not work on university computers.
Inside [Code/Application/dist](Code/Application/dist) is an executable called main.exe which will work without python and is the executable for the project. [Code/Application](Code/Application) contains the source code for the project. In order to run it from the source code simply run the [main.py](Code/Application/main.py) file. In order to do this, the following packages are required.

| Package      | Version |
| ----------- | ----------- |
| fastdtw    | 0.3.4 |
| keyboard   | 0.13.5 |
| numpy      | 1.22.3 |
| pip        | 20.2.3 |
| scipy      | 1.8.0 |
| setuptools | 9.2.1 |
| json | any |

Files under [Code/Test code](Code/Test code) may require further packages and are deprecated.

Inside [Code/Application](Code/Application) there is a make.bat file which can be used to create your own executable. The first step is to delete the build and dist folders along with their contents. This is in order to allow the directory to refresh. In order to do this, install the packages above along with pyinstaller and then run the file. This will output the produced executable inside the dist folder.

When running the program, it will create a folder called Data in which the created word and profile files will be stored in whatever the working directory is.

## Repository map
<pre>
📦FinalYearProject
 ┣ 📂Code
 ┃ ┣ 📂Application
 ┃ ┃ ┣ 📂build
 ┃ ┃ ┃ ┗ 📂main
 ┃ ┃ ┃ ┃ ┣ 📜Analysis-00.toc
 ┃ ┃ ┃ ┃ ┣ 📜base_library.zip
 ┃ ┃ ┃ ┃ ┣ 📜EXE-00.toc
 ┃ ┃ ┃ ┃ ┣ 📜main.exe.manifest
 ┃ ┃ ┃ ┃ ┣ 📜main.pkg
 ┃ ┃ ┃ ┃ ┣ 📜PKG-00.toc
 ┃ ┃ ┃ ┃ ┣ 📜PYZ-00.pyz
 ┃ ┃ ┃ ┃ ┣ 📜PYZ-00.toc
 ┃ ┃ ┃ ┃ ┣ 📜Tree-00.toc
 ┃ ┃ ┃ ┃ ┣ 📜Tree-01.toc
 ┃ ┃ ┃ ┃ ┣ 📜Tree-02.toc
 ┃ ┃ ┃ ┃ ┣ 📜warn-main.txt
 ┃ ┃ ┃ ┃ ┗ 📜xref-main.html
 ┃ ┃ ┣ 📂dist
 ┃ ┃ ┃ ┗ 📜main.exe
 ┃ ┃ ┣ 📂__pycache__
 ┃ ┃ ┃ ┣ 📜DBConnection.cpython-38.pyc
 ┃ ┃ ┃ ┣ 📜DBConnection.cpython-39.pyc
 ┃ ┃ ┃ ┣ 📜Interval.cpython-38.pyc
 ┃ ┃ ┃ ┣ 📜Interval.cpython-39.pyc
 ┃ ┃ ┃ ┣ 📜KeyboardClass.cpython-39.pyc
 ┃ ┃ ┃ ┣ 📜keyboardTest.cpython-39.pyc
 ┃ ┃ ┃ ┣ 📜main.cpython-39.pyc
 ┃ ┃ ┃ ┣ 📜main2.cpython-39.pyc
 ┃ ┃ ┃ ┣ 📜profile.cpython-38.pyc
 ┃ ┃ ┃ ┣ 📜profile.cpython-39.pyc
 ┃ ┃ ┃ ┣ 📜ProfileError.cpython-39.pyc
 ┃ ┃ ┃ ┣ 📜sec.cpython-39.pyc
 ┃ ┃ ┃ ┣ 📜stopThread.cpython-39.pyc
 ┃ ┃ ┃ ┣ 📜Training.cpython-39.pyc
 ┃ ┃ ┃ ┣ 📜user_profile.cpython-39.pyc
 ┃ ┃ ┃ ┣ 📜Utilities.cpython-38.pyc
 ┃ ┃ ┃ ┣ 📜Utilities.cpython-39.pyc
 ┃ ┃ ┃ ┣ 📜Word.cpython-38.pyc
 ┃ ┃ ┃ ┣ 📜Word.cpython-39.pyc
 ┃ ┃ ┃ ┣ 📜WordProcessing.cpython-38.pyc
 ┃ ┃ ┃ ┗ 📜WordProcessing.cpython-39.pyc
 ┃ ┃ ┣ 📜Interval.py
 ┃ ┃ ┣ 📜KeyboardClass.py
 ┃ ┃ ┣ 📜keyboardEvent.py
 ┃ ┃ ┣ 📜main.py
 ┃ ┃ ┣ 📜main.spec
 ┃ ┃ ┣ 📜make.bat
 ┃ ┃ ┣ 📜packagesRequired.txt
 ┃ ┃ ┣ 📜Pause.png
 ┃ ┃ ┣ 📜Play.png
 ┃ ┃ ┣ 📜ProfileError.py
 ┃ ┃ ┣ 📜tester.py
 ┃ ┃ ┣ 📜Training.py
 ┃ ┃ ┣ 📜TrainingText.csv
 ┃ ┃ ┣ 📜user_profile.py
 ┃ ┃ ┣ 📜Word.py
 ┃ ┃ ┣ 📜Words0.json
 ┃ ┃ ┣ 📜Words1.json
 ┃ ┃ ┣ 📜Words2.json
 ┃ ┃ ┗ 📜Words3.json
 ┃ ┣ 📂Demo System
 ┃ ┃ ┣ 📂build
 ┃ ┃ ┃ ┗ 📂main
 ┃ ┃ ┃ ┃ ┣ 📜Analysis-00.toc
 ┃ ┃ ┃ ┃ ┣ 📜base_library.zip
 ┃ ┃ ┃ ┃ ┣ 📜EXE-00.toc
 ┃ ┃ ┃ ┃ ┣ 📜main.exe.manifest
 ┃ ┃ ┃ ┃ ┣ 📜main.pkg
 ┃ ┃ ┃ ┃ ┣ 📜PKG-00.toc
 ┃ ┃ ┃ ┃ ┣ 📜PYZ-00.pyz
 ┃ ┃ ┃ ┃ ┣ 📜PYZ-00.toc
 ┃ ┃ ┃ ┃ ┣ 📜Tree-00.toc
 ┃ ┃ ┃ ┃ ┣ 📜Tree-01.toc
 ┃ ┃ ┃ ┃ ┣ 📜Tree-02.toc
 ┃ ┃ ┃ ┃ ┣ 📜warn-main.txt
 ┃ ┃ ┃ ┃ ┗ 📜xref-main.html
 ┃ ┃ ┣ 📂dist
 ┃ ┃ ┃ ┗ 📜main.exe
 ┃ ┃ ┣ 📂__pycache__
 ┃ ┃ ┃ ┣ 📜Interval.cpython-39.pyc
 ┃ ┃ ┃ ┣ 📜KeyboardClass.cpython-39.pyc
 ┃ ┃ ┃ ┣ 📜main.cpython-39.pyc
 ┃ ┃ ┃ ┣ 📜Training.cpython-39.pyc
 ┃ ┃ ┃ ┣ 📜user_profile.cpython-39.pyc
 ┃ ┃ ┃ ┗ 📜Word.cpython-39.pyc
 ┃ ┃ ┣ 📜Interval.py
 ┃ ┃ ┣ 📜KeyboardClass.py
 ┃ ┃ ┣ 📜keyboardEvent.py
 ┃ ┃ ┣ 📜main.py
 ┃ ┃ ┣ 📜main.spec
 ┃ ┃ ┣ 📜make.bat
 ┃ ┃ ┣ 📜packagesRequired.txt
 ┃ ┃ ┣ 📜Pause.png
 ┃ ┃ ┣ 📜Play.png
 ┃ ┃ ┣ 📜ProfileError.py
 ┃ ┃ ┣ 📜tester.py
 ┃ ┃ ┣ 📜Training.py
 ┃ ┃ ┣ 📜TrainingText.csv
 ┃ ┃ ┣ 📜user_profile.py
 ┃ ┃ ┣ 📜Word.py
 ┃ ┃ ┣ 📜Words0.json
 ┃ ┃ ┣ 📜Words1.json
 ┃ ┃ ┣ 📜Words2.json
 ┃ ┃ ┗ 📜Words3.json
 ┃ ┣ 📂Test code
 ┃ ┃ ┣ 📂Data
 ┃ ┃ ┃ ┗ 📂Pickles
 ┃ ┃ ┃ ┃ ┣ 📜1
 ┃ ┃ ┃ ┃ ┣ 📜60SecondTestData
 ┃ ┃ ┃ ┃ ┣ 📜60SecondTestDataToBeChecked.p
 ┃ ┃ ┃ ┃ ┣ 📜Hello1
 ┃ ┃ ┃ ┃ ┣ 📜Hello2
 ┃ ┃ ┃ ┃ ┣ 📜HoeyTestData
 ┃ ┃ ┃ ┃ ┗ 📜Imposter
 ┃ ┃ ┣ 📂Graphs
 ┃ ┃ ┃ ┣ 📜60SecondTestDataKDS.png
 ┃ ┃ ┃ ┣ 📜60SecondTestDataKDS10Seconds.png
 ┃ ┃ ┃ ┣ 📜60SecondTestDataKDS1Word.png
 ┃ ┃ ┃ ┣ 📜Figure_1.png
 ┃ ┃ ┃ ┣ 📜Genuine vs Imposter.png
 ┃ ┃ ┃ ┗ 📜NormalVsDTW.png
 ┃ ┃ ┣ 📂__pycache__
 ┃ ┃ ┃ ┣ 📜DBConnection.cpython-39.pyc
 ┃ ┃ ┃ ┣ 📜keyboardTest.cpython-39.pyc
 ┃ ┃ ┃ ┣ 📜keyboardTestMac.cpython-39.pyc
 ┃ ┃ ┃ ┗ 📜setup.cpython-39.pyc
 ┃ ┃ ┣ 📜DBConnection.py
 ┃ ┃ ┣ 📜DynamicTImeWarping.py
 ┃ ┃ ┣ 📜JSONTest.py
 ┃ ┃ ┣ 📜keyboardTest.py
 ┃ ┃ ┣ 📜keyboardTestMac.py
 ┃ ┃ ┣ 📜keyStorage.db
 ┃ ┃ ┣ 📜loginTest.py
 ┃ ┃ ┣ 📜Plan.md
 ┃ ┃ ┣ 📜Prototype.py
 ┃ ┃ ┣ 📜setup.py
 ┃ ┃ ┣ 📜temp.py
 ┃ ┃ ┗ 📜temp2.py
 ┃ ┗ 📜ProjectWorkSpace.code-workspace
 ┣ 📂Notes
 ┃ ┣ 📂Images
 ┃ ┃ ┣ 📜ConfMatrixTest2.png
 ┃ ┃ ┣ 📜CorrGraph.png
 ┃ ┃ ┣ 📜CorrGraph2.png
 ┃ ┃ ┣ 📜DecisionsGraph.png
 ┃ ┃ ┣ 📜DistancesDict.png
 ┃ ┃ ┣ 📜EUCGraph.png
 ┃ ┃ ┣ 📜EUCGraph2.png
 ┃ ┃ ┣ 📜EucVs2D.png
 ┃ ┃ ┣ 📜FolderStruct.png
 ┃ ┃ ┣ 📜GantChartAll.png
 ┃ ┃ ┣ 📜HELLO KDS.png
 ┃ ┃ ┣ 📜IfLen1.png
 ┃ ┃ ┣ 📜KDS1.png
 ┃ ┃ ┣ 📜KDS1DTW.png
 ┃ ┃ ┣ 📜KDS2.png
 ┃ ┃ ┣ 📜KDS2DTW.png
 ┃ ┃ ┣ 📜KDSboth.png
 ┃ ┃ ┣ 📜KDSbothDTW.png
 ┃ ┃ ┣ 📜KeyboardEvent.png
 ┃ ┃ ┣ 📜KeyboardEventPreProc.png
 ┃ ┃ ┣ 📜MathsBackend.png
 ┃ ┃ ┣ 📜NewMaths.png
 ┃ ┃ ┣ 📜OldPlan.png
 ┃ ┃ ┣ 📜OOP.png
 ┃ ┃ ┣ 📜PairingWrong.png
 ┃ ┃ ┣ 📜PauseEx.png
 ┃ ┃ ┣ 📜Play.png
 ┃ ┃ ┣ 📜PlayEx.png
 ┃ ┃ ┣ 📜SemanticsEx.png
 ┃ ┃ ┣ 📜SimplePairing.png
 ┃ ┃ ┣ 📜SystemPlan.png
 ┃ ┃ ┣ 📜UncompressedData.png
 ┃ ┃ ┣ 📜ValidationProc.png
 ┃ ┃ ┣ 📜WordCheck.png
 ┃ ┃ ┗ 📜WordsChosenVsTime.png
 ┃ ┣ 📜Dissertation Sauce2.aux
 ┃ ┣ 📜Dissertation Sauce2.bbl
 ┃ ┣ 📜Dissertation Sauce2.bcf
 ┃ ┣ 📜Dissertation Sauce2.blg
 ┃ ┣ 📜Dissertation Sauce2.log
 ┃ ┣ 📜Dissertation Sauce2.pdf
 ┃ ┣ 📜Dissertation Sauce2.run.xml
 ┃ ┣ 📜Dissertation Sauce2.synctex.gz
 ┃ ┣ 📜Dissertation Sauce2.tex
 ┃ ┣ 📜Dissertation Sauce2.toc
 ┃ ┣ 📜GantChartAll.gan
 ┃ ┣ 📜GantChartSem1.gan
 ┃ ┣ 📜GantChartSem1.png
 ┃ ┣ 📜GantChartSem2.gan
 ┃ ┣ 📜GantChartSem2.png
 ┃ ┣ 📜Interim Report.docx
 ┃ ┣ 📜Paper and demo notes.pdf
 ┃ ┗ 📜reference.bib
 ┣ 📜.gitignore
 ┗ 📜README.md
 </pre>

 ## Folder explanation
This section contains a description of the main folders inside the repository.

### Code
Contains all of the code for the project including test code and actual code.

### Application
As explained above, this contains the source code along with the executable inside the dist folder. Included in this directory is a tester file which comprises of some tests that can be run.

### Demo System

Contained inside here is the source code for the demo system along with an executable. The modules needed are the same as above. The only difference between the two systems is that the demo contains print statements throughout which explain what is going on.

### Test Code 
Contains test code that was used when starting the project. Has not been updated in quite some time and is a little bit of a mess. Inside this folder, is stored some example data stored inside pickles.

### Notes
This contains all things dissertation and notes along with it. The dissertation in pdf form, the interim report and all dissertation related files are stored here. As well as these important documents is a number of note files which I created along the way. The source of the dissertation is also here as I wrote it in LaTeX.

### tester.py
[Code/Application/tester.py](Code/Application/tester.py)
Contains all the code necessary to run the tests in the dissertation. Further packages are required for this. These are listed below:

| Package      | Version |
| ----------- | ----------- |
| fastdtw    | 0.3.4 |
| keyboard   | 0.13.5 |
| numpy      | 1.22.3 |
| pip        | 20.2.3 |
| scipy      | 1.8.0 |
| setuptools | 9.2.1 |
| matplotlib | any |
| sklearn | any |




# Using Keystroke Dynamics to Authenticate a User Based on their Typing

This is the repository for the above project. It involves recording a users keystrokes and being able to ensure that they are who they say they are.


## Requirements and running the program

The project only runs on Windows 10. It has been tested and created on python 3.9 and as such has only been guarenteed to work on this version. Inside Code/Application/dist is an executable called main.exe which will work without python and is the executable for the project. Code/Application contains the source code for the project. In order to run it from the source code simply run the main.py file. In order to do this, the following packages are required.

| Package      | Version |
| ----------- | ----------- |
| fastdtw    | 0.3.4 |
| keyboard   | 0.13.5 |
| numpy      | 1.22.3 |
| pip        | 20.2.3 |
| scipy      | 1.8.0 |
| setuptools | 9.2.1 |

Files under Code/Test Code may require further packages. 

Inside Code/Application there is a make.bat file which can be used to create your own executable. In order to do this, install the packages above along with pyinstaller and then run the file. This will output the produeced executable inside the dist folder.

When running the program, it will create a folder called Data in which the created word and profile files will be stored in whatever the working directory is.

## Repository map
<pre>
📦jtf10
 ┣ 📂Code
 ┃ ┣ 📂Application
 ┃ ┃ ┣ 📂build
 ┃ ┃ ┃ ┗ 📂main
 ┃ ┃ ┃ ┃ ┣ 📜Analysis-00.toc
 ┃ ┃ ┃ ┃ ┣ 📜EXE-00.toc
 ┃ ┃ ┃ ┃ ┣ 📜PKG-00.toc
 ┃ ┃ ┃ ┃ ┣ 📜PYZ-00.pyz
 ┃ ┃ ┃ ┃ ┣ 📜PYZ-00.toc
 ┃ ┃ ┃ ┃ ┣ 📜Tree-00.toc
 ┃ ┃ ┃ ┃ ┣ 📜Tree-01.toc
 ┃ ┃ ┃ ┃ ┣ 📜Tree-02.toc
 ┃ ┃ ┃ ┃ ┣ 📜base_library.zip
 ┃ ┃ ┃ ┃ ┣ 📜main.exe.manifest
 ┃ ┃ ┃ ┃ ┣ 📜main.pkg
 ┃ ┃ ┃ ┃ ┣ 📜warn-main.txt
 ┃ ┃ ┃ ┃ ┗ 📜xref-main.html
 ┃ ┃ ┣ 📂dist
 ┃ ┃ ┃ ┗ 📜main.exe
 ┃ ┃ ┣ 📜Interval.py
 ┃ ┃ ┣ 📜KeyboardClass.py
 ┃ ┃ ┣ 📜Pause.png
 ┃ ┃ ┣ 📜Play.png
 ┃ ┃ ┣ 📜ProfileError.py
 ┃ ┃ ┣ 📜Training.py
 ┃ ┃ ┣ 📜TrainingText.csv
 ┃ ┃ ┣ 📜Word.py
 ┃ ┃ ┣ 📜data.pickle
 ┃ ┃ ┣ 📜keyboardEvent.py
 ┃ ┃ ┣ 📜main.py
 ┃ ┃ ┣ 📜main.spec
 ┃ ┃ ┣ 📜make.bat
 ┃ ┃ ┣ 📜packagesRequired.txt
 ┃ ┃ ┣ 📜sec.py
 ┃ ┃ ┣ 📜sec.spec
 ┃ ┃ ┣ 📜tester.py
 ┃ ┃ ┗ 📜user_profile.py
 ┃ ┣ 📂Test code
 ┃ ┃ ┣ 📂Data
 ┃ ┃ ┃ ┣ 📂Pickles
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
 ┃ ┃ ┣ 📜DBConnection.py
 ┃ ┃ ┣ 📜DynamicTImeWarping.py
 ┃ ┃ ┣ 📜JSONTest.py
 ┃ ┃ ┣ 📜Plan.md
 ┃ ┃ ┣ 📜Prototype.py
 ┃ ┃ ┣ 📜keyStorage.db
 ┃ ┃ ┣ 📜keyboardTest.py
 ┃ ┃ ┣ 📜keyboardTestMac.py
 ┃ ┃ ┣ 📜loginTest.py
 ┃ ┃ ┣ 📜setup.py
 ┃ ┃ ┣ 📜temp.py
 ┃ ┃ ┗ 📜temp2.py
 ┃ ┗ 📜ProjectWorkSpace.code-workspace
 ┣ 📂Notes
 ┃ ┣ 📂Images
 ┃ ┃ ┣ 📜CorrGraph.png
 ┃ ┃ ┣ 📜CorrGraph2.png
 ┃ ┃ ┣ 📜DecisionsGraph.png
 ┃ ┃ ┣ 📜DistancesDict.png
 ┃ ┃ ┣ 📜EUCGraph.png
 ┃ ┃ ┣ 📜EUCGraph2.png
 ┃ ┃ ┣ 📜EucVs2D.png
 ┃ ┃ ┣ 📜FolderStruct.png
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
 ┃ ┃ ┣ 📜OOP.png
 ┃ ┃ ┣ 📜OldPlan.png
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
 ┃ ┣ 📜GantChartAll.png
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

### Test Code 
Contains test code that was used when starting the project. Has not been updated in quite some time and is a little bit of a mess. Inside this folder, is stored some example data stored inside pickles.

### Notes
This contains all things dissertation and notes along with it. The dissertation in pdf form, the interim report and all dissertation related files are stored here. As well as these important documents is a number of note files which I created along the way. The source of the dissertation is also here as I wrote it in LaTeX.


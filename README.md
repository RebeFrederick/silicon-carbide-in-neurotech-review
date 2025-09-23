# Silicon-Carbide-in-Neurotech-Review
Data analysis and visualization as part of publication: "State-of-the-Art Review of the Use of Silicon Carbide in Implanted Neural Interfaces" <br/>
(doi: TBD) <br/>
Deku Lab 2025 - Rebecca A. Frederick, Ph.D. <br/>
READ ME for Data Analysis and Data Visualization Files <br/>
Updated: 2025-SEP-30 by Rebecca A. Frederick


# Code Build
Python data analysis code created using Spyder IDE (v6.0.1) <br/>
Spyder installed via Anaconda Navigator (v2.6.4) <br/>
Code developed using Python (v3.12.7) <br/>
Python Packages:
- kaleido (v1.0.0)
- matplotlib (v3.10.0)
- os (from Python v3.12.7)
- pandas (v2.2.3)
- plotly (v6.1.2)
- statsmodels (v0.14.5)


# File: "SiC_analysis_main.py"
1. Installs and Initializes Python Packages
2. Loads Raw Data Files <br/>
   - "0_SiC-Review_Included-Articles-Master-List.csv"
   - "0_SiC-Review_Included-Articles-Reviews-List.csv"
3. Creates Variables and Data Frames
4. Creates Interactive and Static Plots


## Data File: "0_SiC-Review_Included-Articles-List.csv"
Contains raw data list of all articles included in the review.
- Includes metadata for each article:
    - Reference ID (First Author & Year)
    - Publication Date (Year + Month and Day when available)
    - Title
    - Authors (full list, each author separated by "and")
    - DOI
    - PubMed ID
- Includes labels assigned by review authors:
    - Type of Silicon Carbide Reported/Discussed
        - Amorphous (a-SiC)
        - Crystalline (3C-SiC)
        - Crystalline (4H-SiC)
        - Crystalline (6H-SiC)
        - Crystalline (Unspecified)
        - Other
    - Application/Use Category
        - Neural Interface
        - Biosensor
        - Cadiovascular
        - Orthopedic or Dental
        - Drug Delivery
        - Other Technologies
    - Type of Experiments and Data Reported
        - Fabrication Methods
        - Material Properties
        - Benchtop Studies
        - Cell Culture (In Vitro) Studies
        - Ex Vivo Studies
        - In Vivo Studies - Animal Data
        - In Vivo Studies - Human Data


<br/>

***END OF READ ME FILE***

## Amazon Reviews 2023 Data Analysis Project

This project focuses on processing, analyzing, and modeling data from the [Amazon Reviews 2023 dataset](https://amazon-reviews-2023.github.io), which is approximately **200GB** in size.

**System Specifications**
- **CPU:** Intel Xeon E5-2690  
- **Memory:** 64GB 2400MHz ECC RAM  
- **Swap Space:** Additional 100GB dedicated  
- **Storage:** 300GB 3D NAND SATA SSD  
 
Explore the data through interactive visualizations [here](https://carrot2803.github.io/comp3610A3/).

View the processed data visualizations and PDF reports [here](https://github.com/carrot2803/comp3610A3/tree/master/data/processed).

Browse additional relevant images on [Imgur](https://imgur.com/a/comp-3610-assignment-3-2iUDUBa).


The relevant notebooks for your use is in the root directory.

## Installation Guide
<details>
<summary><code>There are several ways you can install the application</code></summary>

1. **Clone the repository**:
    ```sh
    git clone https://github.com/carrot2803/comp3610A3.git
    cd comp3610A3
    ```

2. **(Optional) Create a virtual environment**:

    - Using `venv`:
        ```sh
        python -m venv venv
        source venv/bin/activate    # On Windows use `venv\Scripts\activate`
        ```
    - Using `conda`:
        ```sh
        conda create --name your-env-name python=3.x
        conda activate your-env-name
        ```

3. **Install the required packages**:
    ```sh
    pip install -r requirements.txt
    ```

#### **Alernative**
- [Downloading repository as ZIP](https://github.com/carrot2803/comp3610A3/archive/refs/heads/master.zip)
- Running the following command in a terminal, assuming you have [GitHub CLI](https://cli.github.com/) installed:
    ```sh
        gh repo clone carrot2803/comp3610A3
        cd comp3610A3
    ```
After obtaining the code using one of the above methods, follow steps 2 and 3 from the main installation guide to set up a virtual environment and install the required packages.

</details>

## Package Structure
    root/ 
    ├── amazon/
    │   ├── constants.py
    │   ├── utils.py
    │   ├── models/
    │   │   ├── metrics.py
    │   │   └── normalize.py
    │   └── visuals/
    │       ├── plots.py
    │       └── line.py                         
    ├── data/
    │   ├── raw/
    │   ├── intermediate/
    │   └── processed/
    ├── 1-data-acquisition.ipynb
    ├── 2-data-cleaning.ipynb
    ├── 3-data-analysis.ipynb
    ├── 4-logistic-regression.ipynb
    ├── 5-als-system.ipynb
    ├── 6-kmeans.ipynb
    └── requirements.txt

Only relevant file details mentioned.

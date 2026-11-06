**College Major and Graduate Earnings: A College Scorecard Data Acquisition Project**



**Project Overview**



This project investigates how earnings four years after college completion differ across academic majors and between public and private nonprofit universities in the United States.



The project uses the U.S. Department of Education's College Scorecard API to acquire program-level earnings data and creates a cleaned dataset for exploratory data analysis.



**Research Questions**



1. Which college major categories have the highest median earnings?



2\. How do program earnings differ between public and private nonprofit universities?



3\. Do public-private earnings differences vary across major categories?



**Data Source**



* Source: U.S. Department of Education, College Scorecard



* API: https://collegescorecard.ed.gov/data/api/



* Unit of observation: University-major bachelor's degree program



* Outcome: Median earnings four years after completion



**Data Acquisition and Cleaning**



The data pipeline includes:



1. Retrieving institution and program records from the College Scorecard API using pagination.

2. Extracting bachelor's degree programs from nested JSON responses.

3. Converting the records into a structured pandas DataFrame.

4. Retaining public and private nonprofit universities.

5. Excluding programs without reported institution-specific four-year median earnings.

6. Grouping majors using two-digit CIP codes.

7. Creating earnings differences and ratios relative to national program benchmarks.



The initial acquisition produced 5,507 program observations across 175 institutions. The cleaned dataset contains 2,369 observations across 122 institutions, with 13 variables.



**Preliminary Findings**



* Engineering had the highest median program earnings ($97,656), followed by Computer Science ($92,014).



* Visual and Performing Arts had the lowest median among the reported broad categories ($43,758).



* Private nonprofit programs had a median of $62,886, compared with $59,041.50 for public programs.



* Engineering was an exception to the overall public-private pattern, with a slightly higher median among public programs.



These results are descriptive associations, not causal estimates.



**Repository Structure**



data/

&#x20;   college\_earnings\_raw.csv

&#x20;   college\_earnings\_clean.csv



scripts/

&#x20;   test\_api.py

&#x20;   test\_programs.py

&#x20;   acquire\_data.py

&#x20;   clean\_data.py

&#x20;   eda.py



figures/

&#x20;   earnings\_by\_major.png

&#x20;   public\_vs\_private.png

&#x20;   earnings\_distribution.png

&#x20;   earnings\_by\_major\_and\_type.png



pyproject.toml

uv.lock

README.md



**Reproducing the Analysis**



**1. Install Dependencies**



uv sync



**2. Configure the API Key**



Obtain a College Scorecard API key and set the COLLEGE\_SCORECARD\_API\_KEY environment variable.



For example, in PowerShell:



$env:COLLEGE\_SCORECARD\_API\_KEY = "YOUR\_API\_KEY"



Never commit your actual API key to GitHub.



**3. Run the Data Pipeline**



Run the following commands from the repository root:



uv run python scripts/acquire\_data.py

uv run python scripts/clean\_data.py

uv run python scripts/eda.py



These scripts generate the CSV datasets and exploratory figures.



**Limitations and Ethics**



* The sample was collected from the first 20 pages of institution results and is not a nationally representative random sample.



* Many programs lack institution-specific earnings estimates. Excluding these programs may introduce selection bias.



* Each program receives equal weight in the summaries, regardless of the number of graduates.



* Earnings comparisons do not control for student characteristics, institutional selectivity, geography, or other confounders.



* Broad CIP categories contain multiple related disciplines.



* Publicly released aggregate earnings data are used rather than individual student records.



**Tools**



* Python



* pandas



* requests



* matplotlib



* seaborn



* uv



**Author**



Takato Migita



STAT 386 — Data Science Process

Brigham Young University


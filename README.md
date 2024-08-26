# An Empirical Study of Refactorings Related to Performance Issues - Replication Package

## Requirements

### For RefactoringMiner:

- Java >= 8
  Check the project's repository for a detailed instructions: [Link To Repo:](https://github.com/tsantalis/RefactoringMiner#how-to-build-refactoringminer)

### For Python script:

- Python >= 3.6

Use the following command to install dependencies

```
pip install
```

### For R script:

Follow the link to install R which is compatible to your device: [Website:](https://cran.r-project.org/)

### For Data Storage:

We use MongoDB to store our data. This is the link to download MongoDB: [URL](https://www.mongodb.com/try/download/community-kubernetes-operator)

## Datasets

Our datasets collected during our data collection and processing stages can be found [here](https://drive.google.com/drive/folders/1ZK9a9_kf-NpaIkN-QApH8kp2aH9ymppg?usp=sharing)

## GitHub API

An ACCESS TOKEN is required to extract data from GitHub API. Learn more from [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)

## Package Structure

The package structure is in 3 parts:

- Data Collection
- Data Processing
- Data Analysis

#### Data Collection

This part contains all scripts used to collect data from GitHub API and RefactoringMiner. Data includes:

- Java projects
- Performance issues, pull requests and commits
- Performance refactorings
- Project refactorings

Scripts can be found in `1_data_collection` directory.

#### Data Processing

This part contains all scripts used to process our collected data into refined datasets. This process includes:

- Categorization of refactorings
- Filtering refactorings and performance issues
- Verifying refactorings and performance issues

Scripts can be found in `2_data_processing` directory.

#### Data Analysis

This part contains several directories used for our analysis. These directories are:

- `data` directory: used to store the results of the analysis for each RQ.
- `figures` directory: contains all the figures derived from our analysis and being used in the paper.
- `scripts` directory: contains all the scripts used for our analysis for each RQ.

Directories can be found in `3_data_analysis` directory.

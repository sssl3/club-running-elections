# club-running-elections

[Club Running](https://virginia.clubrunning.org) is an athletic CIO at the University of Virginia. This repository contains the source code for the ranked-choice voting application the club uses to conduct its elections process. This application was developed in Fall 2024 and is a more user-friendly version of the application used in previous years. 

This application uses the [single-transferable vote](https://en.wikipedia.org/wiki/Single_transferable_vote) implementation from the [pyrankvote](https://github.com/jontingvold/pyrankvote) module to count/report election results. 

## Requirements
Create a conda environment in Python 3.9.20 and install required packages

```bash
conda create -n <env_name>
conda activate <env_name>
pip install -r requirements.txt
```
## Dependencies

Tool supports Google Sheets input.

Packages used: pyrankvote, gspread, oauth2client.service_account, pandas, numpy

To use the `"private_sheet"` option to read in a Google Sheet that is not publicly accessible, you must generate a service account with a private key and associated email address to make API calls to the private sheet. Instructions on how to do this can be found on the Google Developers [page](https://developers.google.com/sheets/api/guides/concepts) or in the readme of [this](https://github.com/juampynr/google-spreadsheet-reader) repository.

## Configuration File (`config.json`)
The configuration file should contain the following parameters:

* `"url"`: The URL of the spreadsheet containing the ballots. (Required)
* `"candidates_to_drop"`: The list of candidates to be excluded during the tallying process. (Optional)
* `"position"`: The position for which the votes are being counted for. (Required)
* `"sheet_setting"`: Selection for whether spreadsheet containing ballots is publicly or privately accessible. (Required)
     - `"private"`, `"public"`
     - Selection of `"private"` option requires setup of Google Sheets API/service account.
* `"keyfile"`: The file path to the private key file associated with the service account. (Required if `"private"` option is selected for `"sheet_setting"` parameter)

## Usage
To tabulate, use the following command:

```bash
python main.py -c config.json
```

The application expects to ingest a spreadsheet that is in the output form of (timestamp, candidate A, candidate B,..., candidate X) that a Google Form multiple choice grid question generates when linked to a spreadsheet. The columns of the question should contain all of the candidates, while the rows should indicate "first choice," "second choice," etc.

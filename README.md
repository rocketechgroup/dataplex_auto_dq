# Dataplex Auto DQ

## Extract YAML from Dataplex Data Quality Scan

This script will extract the YAML from a Dataplex Data Quality Scan and print it to STDOUT.

```
pip install -r requirements.txt

export PROJECT=<your gcp project>
export LOCATION=<your gcp location where the table is located>
export DATA_SCAN=<your id of the data quality scan>
python main.py
```

The output will look like [data_quality_check.yaml](examples/data_quality_check.yaml)

For instructions to use the GCLOUD CLI to import the YAML and create the data quality scan, see [data quality scan](https://cloud.google.com/dataplex/docs/use-auto-data-quality#create-scan)
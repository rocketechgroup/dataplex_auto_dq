# Dataplex Auto DQ

## Extract YAML from Dataplex Data Quality Scan

This script will extract the YAML from a Dataplex Data Quality Scan and print it to STDOUT.

```
export PROJECT=<your gcp project>
export LOCATION=<your gcp location where the table is located>
export DATA_SCAN=<your id of the data quality scan>
python main.py
```

The output will look like [data_quality_check.yaml](examples/data_quality_check.yaml)
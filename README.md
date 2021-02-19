[![Brighter AI logo](brighter.png)](https://brighter.ai/)

# Redact Python Client

This project provides convenient access to [brighter AI's](https://brighter.ai/) [Redact API](https://docs.identity.ps/) 
for the anonymization of faces and license plates.

Lear more:
- About us: [Brighter AI](https://brighter.ai/)
- Try [Redact](https://product.brighter.ai/) online
- [API Documentation](https://docs.identity.ps/)

## Installation

Directly install the latest version from GitHub: 

```shell
pip install git+https://github.com/brighter-ai/redact-client.git
```

For a specific version, append `@[version]`. 


## Quickstart

The pip package automatically installs two command-line shortcuts (`redact_file` and `redact_folder`) that let you 
anonymize individual files or whole folders, respectively.

```shell
Usage: redact_file [OPTIONS] FILE_PATH
                   OUT_TYPE:[images|videos|archives|overlays]
                   SERVICE:[blur|dnat|extract]
```

```shell
Usage: redact_folder [OPTIONS] IN_DIR OUT_DIR
                     INPUT_TYPE:[images|videos|archives]
                     OUT_TYPE:[images|videos|archives|overlays]
                     SERVICE:[blur|dnat|extract]
```

Add `--help` to see additional options. 


### Examples

Anonymize an individual image from the command line:

```shell
redact_file image.jpg images blur --redact-url=http://127.0.0.1:8787
```

Per default, the result will be stored in `image_redacted.jpg`.

Larger amounts of data (images in this case) can be 
anonymized in batches:

```shell
redact_folder ./in_dir ./out_dir images images blur --redact-url=127.0.0.1:8787
```


## Library Usage

The `redact` package itself provides different ways to use the Redact API from Python.

### (Batch) File Processing

The command-line shortcuts described above can be called programmatically through modules 
`redact.tools.redact_file` and `redact.tools.redact_folder`. The latter allows for anonymizing
several objects in parallel which usually results in a significant speed-up.

### API Requests

The class `redact.redact_requests.RedactRequests` maps the [API endpoints](https://docs.identity.ps/) to Python methods.  
It is intended to reduce boiler-plate code around the API calls.

### Redact Jobs

In addition, the classes `RedactInstance` and `RedactJob` provide convenient high-level access to the API:

```python
from redact.redact_instance import RedactInstance

redact = RedactInstance.create(service='blur', out_type='images', redact_url='http://127.0.0.1:8787')
with open('image.jpg', 'rb') as f:
    result = redact.start_job(file=f).wait_until_finished().download_result()
```

The anonymization can be further configured by adding additional `JobArguments` to `start_job()`. See `example.py`.

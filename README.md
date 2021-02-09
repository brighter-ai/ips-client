# IPS Python Client

This project provides convenient access to the [Identity Protection Suite (IPS) API](https://docs.identity.ps/). 

## Installation

Directly install the latest version from GitHub: 

```shell
pip install git+ssh://git@github.com/brighter-ai/ips-client.git
```

For a specific version, append `@[version]`. 


## Quickstart

The pip package automatically installs two command-line shortcuts (`ips_anon_file` and `ips_anon_folder`) that let you anonymize 
individual files or whole folders, respectively.

```shell
Usage: ips_anon_file [OPTIONS] FILE_PATH
                     OUT_TYPE:[images|videos|archives|overlays]
                     SERVICE:[blur|dnat|extract]
```

```shell
Usage: ips_anon_folder [OPTIONS] IN_DIR OUT_DIR
                       INPUT_TYPE:[images|videos|archives]
                       OUT_TYPE:[images|videos|archives|overlays]
                       SERVICE:[blur|dnat|extract]
```

Add `--help` to see additional options. 


### Example (image)

Anonymize an individual image:

```shell
ips_anon_file image.jpg images blur --ips-url=http://127.0.0.1:8787
```

Per default, the result will be stored in `image_anonymized.jpg`.

### Example (folder)

Larger amounts of data (images in this case) can be anonymized in batches:

```shell
ips_anon_folder ./in_dir ./out_dir images images blur --ips-url=127.0.0.1:8787
```


## Library Usage

The described command-line operations can also be performed programmatically through the 
Python modules `ips_client.tools.anonymize_file` and `ips_client.tools.anonymize_folder`.

If you want to have more fine-grained access to the API, you may want to use `IPSInstance` and `IPSJob`:

```python
from ips_client.ips_instance import IPSInstance

ips = IPSInstance.create(service='blur', out_type='images', ips_url='http://127.0.0.1:8787')
with open('image.jpg', 'rb') as f:
    result = ips.start_job(file=f).wait_until_finished().download_result()
```

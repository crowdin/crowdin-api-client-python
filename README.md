[<p align='center'><img src='https://support.crowdin.com/assets/logos/crowdin-dark-symbol.png' data-canonical-src='https://support.crowdin.com/assets/logos/crowdin-dark-symbol.png' width='150' height='150' align='center'/></p>](https://crowdin.com)

# Crowdin Python client [![Tweet](https://img.shields.io/twitter/url/http/shields.io.svg?style=social)](https://twitter.com/intent/tweet?url=https%3A%2F%2Fgithub.com%2Fcrowdin%2Fcrowdin-api-client-python&text=The%20Crowdin%20Python%20client%20is%20a%20lightweight%20interface%20to%20the%20Crowdin%20API)&nbsp;[![GitHub Repo stars](https://img.shields.io/github/stars/crowdin/crowdin-api-client-python?style=social&cacheSeconds=1800)](https://github.com/crowdin/crowdin-api-client-python/stargazers)

The Crowdin Python client is a lightweight interface to the Crowdin API. It provides common services for making API requests.

Crowdin API is a full-featured RESTful API that helps you to integrate localization into your development process. The endpoints that we use allow you to easily make calls to retrieve information and to execute actions needed.

<div align="center">

[**`API Client Docs`**](https://crowdin.github.io/crowdin-api-client-python/) &nbsp;|&nbsp;
[**`Crowdin API`**](https://developer.crowdin.com/api/v2/) &nbsp;|&nbsp;
[**`Crowdin Enterprise API`**](https://developer.crowdin.com/enterprise/api/v2/)

[![PyPI](https://img.shields.io/pypi/v/crowdin-api-client?cacheSeconds=3600)](https://pypi.org/project/crowdin-api-client/)
[![Downloads](https://pepy.tech/badge/crowdin-api-client)](https://pepy.tech/project/crowdin-api-client)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/crowdin-api-client?cacheSeconds=3600)](https://pypi.org/project/crowdin-api-client/)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/crowdin/crowdin-api-client-python/Python%20package)
[![codecov](https://codecov.io/gh/crowdin/crowdin-api-client-python/branch/main/graph/badge.svg?token=sOUWIcNjWO)](https://codecov.io/gh/crowdin/crowdin-api-client-python)
[![GitHub issues](https://img.shields.io/github/issues/crowdin/crowdin-api-client-python?cacheSeconds=3600)](https://github.com/crowdin/crowdin-api-client-python/issues)
[![License](https://img.shields.io/github/license/crowdin/crowdin-api-client-python?cacheSeconds=3600)](https://github.com/crowdin/crowdin-api-client-python/blob/master/LICENSE)

</div>

## Table of Contents
* [Installation](#installation)
* [Quick Start](#quick-start)
* [Seeking Assistance](#seeking-assistance)
* [Contributing](#contributing)
* [License](#license)

## Installation

```console
pip install crowdin-api-client
```

## Quick Start

### Create and list projects

```python
from crowdin_api import CrowdinClient

class FirstCrowdinClient(CrowdinClient):
    TOKEN = "__token__"
    ORGANIZATION = "organizationName" # Optional, for Crowdin Enterprise only
    TIMEOUT = 60  # Optional, sets http request timeout.
    RETRY_DELAY = 0.1  # Optional, sets the delay between failed requests 
    MAX_RETRIES = 5  # Optional, sets the number of retries
    HEADERS = {"Some-Header": ""}  # Optional, sets additional http request headers
    PAGE_SIZE = 25  # Optional, sets default page size 

client = FirstCrowdinClient()

# Create Project
project_response = client.projects.add_project(name="New project", sourceLanguageId="en")

# Get list of Projects
projects = client.projects.list_projects()

# Get list of Projects with offset and limit
projects = client.projects.list_projects(offset=10, limit=20)

# Get list of Projects by page
projects = client.projects.list_projects(page=2) # offset=25, limit=25
```

### Add a file

```python
from crowdin_api import CrowdinClient

class FirstCrowdinClient(CrowdinClient):
    TOKEN = "__token__"

client = FirstCrowdinClient()

file_name = '__path_to_the_file__'

storage = client.storages.add_storage(open(file_name, 'rb'))

my_file = client.source_files.add_file(__project_id__, storage['data']['id'], file_name)

print(my_file)
```

## Seeking Assistance

If you find any problems or would like to suggest a feature, please read the [How can I contribute](https://github.com/crowdin/crowdin-api-client-python/blob/main/CONTRIBUTING.md#how-can-i-contribute) section in our contributing guidelines.

Need help working with Crowdin Python client or have any questions? [Contact](https://crowdin.com/contacts) Customer Success Service.

## Contributing

If you want to contribute please read the [Contributing](https://github.com/crowdin/crowdin-api-client-python/blob/main/CONTRIBUTING.md) guidelines.

## License
<pre>
The Crowdin Python client is licensed under the MIT License.
See the LICENSE file distributed with this work for additional
information regarding copyright ownership.

Except as contained in the LICENSE file, the name(s) of the above copyright
holders shall not be used in advertising or otherwise to promote the sale,
use or other dealings in this Software without prior written authorization.
</pre>

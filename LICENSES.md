# Third-Party Licenses

This project uses open-source third-party Python packages. The following notices summarize the relevant licenses for the directly used dependencies.

This file is provided for documentation purposes and does not replace the original license texts of the respective projects.

## Direct dependencies

| Package | Purpose in this project | License | Copyright / Notice |
|---|---|---|---|
| Streamlit | Web app / GUI framework | Apache License 2.0 | Streamlit Inc.; Snowflake Inc. and contributors |
| Plotly.py | Interactive plotting and visualization | MIT License | Plotly Technologies Inc. and contributors |

## Streamlit

Streamlit is used to build the interactive web-based user interface of this project.

- Project: Streamlit
- License: Apache License 2.0
- SPDX identifier: Apache-2.0
- Source: https://github.com/streamlit/streamlit
- License text: https://github.com/streamlit/streamlit/blob/develop/LICENSE

The Apache License 2.0 permits use, modification, distribution, and sublicensing, provided that the license terms, copyright notices, and required notices are preserved.

## Plotly.py

Plotly.py is used to create interactive charts and visualizations in this project.

- Project: Plotly.py
- License: MIT License
- SPDX identifier: MIT
- Source: https://github.com/plotly/plotly.py
- License text: https://github.com/plotly/plotly.py/blob/main/LICENSE.txt

The MIT License permits use, copying, modification, merging, publishing, distribution, sublicensing, and selling copies of the software, provided that the copyright notice and permission notice are included.

## Important note about transitive dependencies

Streamlit and Plotly.py depend on additional third-party packages, for example packages from the Python data and web ecosystem. If this project is distributed publicly or commercially, the licenses of all installed dependencies should also be reviewed.

A common way to generate a more complete dependency license overview is:

```bash
pip install pip-licenses
pip-licenses --format=markdown --with-license-file --output-file THIRD_PARTY_LICENSES_FULL.md
```

Alternatively, for a shorter overview:

```bash
pip-licenses --format=markdown --output-file THIRD_PARTY_LICENSES_OVERVIEW.md
```

## Project license

This file only documents third-party licenses. It does not define the license of this project itself.

If this project should be open-sourced, add a separate `LICENSE` file at the project root, for example with one of the following licenses:

- MIT License
- Apache License 2.0
- BSD 3-Clause License

## Disclaimer

This file is not legal advice. For commercial distribution or institutional publication, verify all direct and transitive dependencies and their license obligations.

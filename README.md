# td_exam_booker
Bot to automate the application of exam re-scheduling at td.gov.hk

## Installation

1. set up `vitualenv`
under the project directory
```
virtualenv venv --python=python3
```

2. activate vitualenv
under the project directory
```
source ./venv/bin/activate
```

3. working in Dev mode
```
pip install -e .
```

## Usage
modify `./client.json`
```json
//structure
{
    "clients": [{
            "code": "<exam code>",
            "b-year": "1990",
            "b-month": "8",
            "b-date": "14",
            "mobile": "<mobile>",
            "lens": "n",
            "district": "kowloon/hk"
        },
        ...]
}

```
under the project directory
```
. ./run_script.sh
```

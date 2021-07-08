
# Incov-19 API

Is an API built-in using [fastApi](https://github.com/tiangolo/fastapi) for my website [incov-19](https://incov-19.netlify.app/).

## Installation

Clone this repository
```
https://github.com/jirenmaa/incov-19-api.git
```

Navigate to project folder
```bash
cd incov-19-api
```


Install requirements using python [pip](https://pypi.org/project/pip/)

```bash
pip install -r requirements.txt
```

## Local Usage

```python
uvicorn main:app --reload
```

Navigate to [http://localhost:8000](http://localhost:8000) to use the API.

Endpoint Name | url |
--- | --- |
medicalnewstoday | /medicalnewstoday |
msn | /msn |
9news | /9news |

It will take some time to scrape the site, so take it easy.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to test your changes before making a pull request.

## License
[MIT](https://choosealicense.com/licenses/mit/)
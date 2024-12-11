# 👨🏽‍💻 user_management_api

## 📜 Project Description

- ### Is a project under development, created with the aim of offering a robust and scalable solution for user management and system authentication. Developed using FastAPI as its main framework, this API adopts Clean Architecture principles to ensure modularity, simplified maintenance and easy expansion.

## 📂 Project Structure

```plaintext
    user_management_api/                  #
    │
    ├── src/                             #
    │   │
    │   ├── adapters/                    #
    │   │
    │   ├── api/                         #
    │   │
    │   ├── core/                        #
    │   │
    │   ├── dtos/                        #
    │   │
    │   ├── infrastructure/              #
    │   │
    │   ├── usecases/                    #
    │   │
    │   ├── utils/                       #
    │   │
    ├── tests/                           #
    │   │
    ├── .flake8                          #
    ├── .gitattributes                   #
    ├── .gitignore                       #
    ├── .isort.cfg                       #
    ├── pyproject.toml                   #
    ├── README.md                        #
    └── requirements.txt                 #
```

## 🎛️ Features

## 🛠️ Technologies Used

## 🤹🏽‍♂️ Dependencies

```bash
py -m pip freeze > requirements.txt
```

```bash
py -m pip install -r requirements.txt
```

## 🛣️ API Routes

## ▶️ Environment

## 👨🏽‍⚖️ Formatting
```bash
black app && isort app && flake8 app
```

## ✅ Running

```bash
uvicorn src.api.main:app
```

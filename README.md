# JarviX

Code for **JarviX: A LLM No Code Platform for Tabular Data Analysis and Optimization**, EMNLP 2023 Industry Track.

- Paper: [ACL Anthology](https://aclanthology.org/2023.emnlp-industry.59) · [DOI](https://doi.org/10.18653/v1/2023.emnlp-industry.59)

```
Shang-Ching Liu, ShengKun Wang, Wenqi Lin, Chung-Wei Hsiung, Yi-Chen Hsieh, Yu-Ping Cheng, Sian-Hong Luo, Tsungyao Chang, and Jianwei Zhang.
JarviX: A LLM No Code Platform for Tabular Data Analysis and Optimization.
In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing: Industry Track, pages 622–630, Singapore. Association for Computational Linguistics.
```

This repository has a Vue frontend (`frontend-q`) and a Flask backend (`backend`).

## Frontend

```bash
cd frontend-q
npm install
npm run serve
```

(A Vue CLI-compatible toolchain is required.)

## Backend

```bash
cd backend
pip install -r requirement.txt
export OPENAI_API_KEY=YOUR_KEY
flask run
```

The dependency file in this repo is `backend/requirement.txt`.

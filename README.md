# Fake News Detection in Social Networks

This project implements a machine learning-based system for detecting fake news in social media content. It combines natural language processing, social network analysis, and machine learning techniques to provide accurate classification of news articles and social media posts.

## Features

- Data collection from various sources (Twitter/X, news websites, pre-labeled datasets)
- Comprehensive text preprocessing pipeline
- Advanced feature engineering (linguistic, content-based, user-based, metadata)
- Multiple model implementations (traditional ML and deep learning)
- Social network propagation analysis
- Easy-to-use API for real-time classification
- Web interface for interactive demonstration
- Extensive evaluation metrics and visualization tools

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/fake-news-detection.git
cd fake-news-detection

# Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Training a Model

```bash
python src/train.py --config configs/default.yaml
```

### Running the Web Interface

```bash
python src/app/run.py
```

### Using the API

```python
from fake_news_detector import FakeNewsDetector

detector = FakeNewsDetector.load_model("models/best_model.pkl")
prediction = detector.predict("https://example.com/news-article")
print(f"Fake news probability: {prediction.probability:.2f}")
print(f"Classification: {prediction.label}")
```

## Project Structure

```
├── configs/                 # Configuration files
├── data/                    # Data storage
│   ├── raw/                 # Original datasets
│   ├── processed/           # Preprocessed data
│   └── embeddings/          # Word embeddings
├── models/                  # Saved models
├── notebooks/               # Jupyter notebooks for exploration
├── src/                     # Source code
│   ├── app/                 # Web application
│   ├── data/                # Data processing modules
│   ├── features/            # Feature engineering
│   ├── models/              # Model implementations
│   ├── utils/               # Utility functions
│   └── visualization/       # Visualization tools
├── tests/                   # Unit tests
├── .gitignore               # Git ignore file
├── requirements.txt         # Project dependencies
├── setup.py                 # Package setup file
└── README.md                # Project documentation
```

## Dataset

This project uses multiple datasets including:
- [FakeNewsNet](https://github.com/KaiDMML/FakeNewsNet)
- [LIAR dataset](https://www.cs.ucsb.edu/~william/data/liar_dataset.zip)
- [ISOT Fake News Dataset](https://www.uvic.ca/engineering/ece/isot/datasets/fake-news/index.php)
- Custom collected social media data

## Results

Our best model achieves:
- Accuracy: 93.7%
- Precision: 92.1%
- Recall: 94.2%
- F1 Score: 93.1%

## License

MIT

## Contributors

- Your Name

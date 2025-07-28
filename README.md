# Toxicytube

**Toxicytube** is an integrated approach for YouTube comment analysis, focusing on sentiment classification and toxic speech detection in Portuguese.

## 📁 Project Structure

```
Toxicytube/
│
├── 1_data_gathering/                  # Comment collection using YouTube Data API
│
├── 2_data_processing/
│   ├── toxic_speech_detection/       # Toxic speech classification
│   ├── sentiment_analysis_xlm/       # Sentiment analysis using XLM-R model
│   ├── sentiment_analysis_gpt/       # Sentiment analysis using GPT
│   └── comparison/                   # Model comparison (e.g., RoBERTa vs GPT)
│
├── 3_visualization/                  # Visualizations and figure generation
│   └── figures/                      # Output figures (charts, plots)
│
├── README.md                         # Project overview and instructions
├── requirements.txt                  # Python dependencies
└── .gitignore                        # Files and folders ignored by Git
```

## 🚀 Getting Started

1. Clone this repository:
```bash
git clone https://github.com/your-username/Toxicytube.git
cd Toxicytube
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the scripts step by step from `1_data_gathering` to `3_visualization`.

## 📜 License

This project is licensed under the MIT License.

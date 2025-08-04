import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import json
import os
import argparse
import re
import nltk
from nltk.corpus import stopwords

# Baixar stopwords caso ainda não estejam disponíveis
nltk.download('stopwords')


def load_json_data(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)


def generate_pie_chart(df):
    sentiment_counts = df['sentimento'].value_counts().reset_index()
    sentiment_counts.columns = ['sentimento', 'count']

    colors = {'positive': 'green', 'neutral': 'blue', 'negative': 'red'}
    labels = sentiment_counts['sentimento']
    values = sentiment_counts['count']
    color_values = [colors[label] for label in labels]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        textinfo='label+percent',
        marker=dict(colors=color_values),
        showlegend=False
    )])

    fig.update_layout(title_text='Distribuição de Sentimentos')
    return fig


def generate_timeseries_chart(df):
    df['publishedAt'] = pd.to_datetime(df['publishedAt'])
    df['date'] = df['publishedAt'].dt.date
    time_series = df.groupby(['date', 'sentimento']).size().reset_index(name='count')

    fig = px.line(
        time_series,
        x='date',
        y='count',
        color='sentimento',
        color_discrete_map={"positive": "green", "neutral": "blue", "negative": "red"},
        title='Evolução Temporal dos Sentimentos'
    )
    return fig


def generate_wordcloud(df, output_image):
    stop_words = set(stopwords.words('portuguese'))
    palavras = []

    for msg in df['message'].dropna().tolist():
        msg = msg.lower()
        msg = re.sub(r':[a-zA-Z0-9_]+:', '', msg)
        msg = re.sub(r'[^\w\s]', '', msg)
        for palavra in msg.split():
            if palavra not in stop_words and len(palavra) > 2:
                palavras.append(palavra)

    texto_final = ' '.join(palavras)

    wordcloud = WordCloud(
        width=1200,
        height=800,
        background_color='white',
        stopwords=stop_words,
        collocations=False
    ).generate(texto_final)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(output_image)
    plt.close()
    print(f"[INFO] Wordcloud salva em: {output_image}")


def main(json_file):
    if not os.path.exists(json_file):
        print(f"[ERRO] Arquivo não encontrado: {json_file}")
        return

    data = load_json_data(json_file)
    df = pd.DataFrame(data)

    video_id = os.path.splitext(os.path.basename(json_file))[0].replace("sentiments_comparision_", "")
    output_html = f"{video_id}.html"
    output_wordcloud = f"{video_id}.png"

    pie_fig = generate_pie_chart(df)
    time_fig = generate_timeseries_chart(df)
    generate_wordcloud(df, output_wordcloud)

    # Exporta os gráficos em um único arquivo HTML
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(pie_fig.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(time_fig.to_html(full_html=False, include_plotlyjs=False))

    print(f"[INFO] Dashboard interativo salvo em: {output_html}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualização de sentimentos: gráfico de pizza, séries temporais e wordcloud")
    parser.add_argument("--json", required=True, help="Caminho para o arquivo sentiments_comparision_VIDEO_ID.json")
    args = parser.parse_args()
    main(args.json)

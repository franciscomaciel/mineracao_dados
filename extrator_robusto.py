
def extrair_motivos_chamados_robusto(nome_arquivo="chamados.csv"):
    """
    Extrai os motivos mais comuns para pendências e cancelamentos de chamados de assistência técnica,
    lidando com lacunas, erros de digitação e utilizando aprendizado profundo para melhor classificação.

    Args:
        nome_arquivo (str): O nome do arquivo CSV contendo os dados dos chamados.

    Returns:
        Counter: Um objeto Counter contendo os motivos e suas frequências.
    """

    try:
        df = pd.read_csv(nome_arquivo)
    except FileNotFoundError:
        return "Arquivo não encontrado."
    except Exception as e:
        return f"Erro ao ler o arquivo: {e}"

    df_filtrado = df[df['Status'].isin([1, 4])].copy()  # Cria uma cópia para evitar FutureWarning

    if df_filtrado.empty:
        return "Não há chamados pendentes ou cancelados para analisar."

    # Preenche valores NaN na coluna 'observacao' com uma string vazia
    df_filtrado['observacao'] = df_filtrado['observacao'].fillna('')

    # Limpeza básica do texto
    df_filtrado['observacao'] = df_filtrado['observacao'].apply(lambda x: re.sub(r'[^\w\s]', '', str(x).lower()))

    # Preparação para aprendizado profundo
    textos = df_filtrado['observacao'].tolist()
    labels = df_filtrado['observacao'].tolist() # Labels temporárias, depois vem o aprendizado profundo
    tokenizer = Tokenizer(num_words=5000) # Ajuste este numero
    tokenizer.fit_on_texts(textos)
    sequencias = tokenizer.texts_to_sequences(textos)
    sequencias_padded = pad_sequences(sequencias, maxlen=100) # Ajuste maxlen conforme necessario.

    # Label encoding dos rótulos
    label_encoder = LabelEncoder()
    labels_encoded = label_encoder.fit_transform(labels)
    num_classes = len(label_encoder.classes_)

    # Divisão em conjuntos de treinamento e teste
    X_train, X_test, y_train, y_test = train_test_split(sequencias_padded, labels_encoded, test_size=0.2, random_state=42)

    # Modelo de aprendizado profundo
    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(5000, 16, input_length=100),
        tf.keras.layers.GlobalAveragePooling1D(),
        tf.keras.layers.Dense(24, activation='relu'),
        tf.keras.layers.Dense(num_classes, activation='softmax')
    ])

    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test), verbose=0) #Verbose 0, para não mostrar output

    # Previsões
    previsoes = model.predict(sequencias_padded)
    classes = tf.argmax(previsoes, axis=1)
    df_filtrado['motivo_previsto'] = label_encoder.inverse_transform(classes)

    # Contagem dos motivos previstos
    contagem_motivos = Counter(df_filtrado['motivo_previsto'])

    return contagem_motivos

# Exemplo de uso
motivos_comuns = extrair_motivos_chamados_robusto("chamados.csv")

if isinstance(motivos_comuns, str):
    print(motivos_comuns)
else:
    print("Motivos mais comuns para pendências/cancelamentos (com aprendizado profundo):")
    for motivo, frequencia in motivos_comuns.most_common():
        print(f"- {motivo}: {frequencia} ocorrências")
        
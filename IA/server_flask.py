from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Carrega o modelo salvo
loaded_model = joblib.load("./model/model.pickle")

# Carrega o encoder salvo
loaded_encoder = joblib.load("./model/encoder.pickle")


@app.route("/prever", methods=["POST"])
def prever_post():
    # Verifica se a solicitação contém dados JSON
    if not request.is_json:
        return "A solicitação deve conter dados JSON", 400

    # Obtém os dados do corpo da solicitação
    data = request.json

    if data is None:
        return "Dados não informados", 400

    # Verifica se os campos necessários estão presentes nos dados
    required_fields = [
        "Age",
        "Sex",
        "ChestPainType",
        "RestingBP",
        "Cholesterol",
        "FastingBS",
        "RestingECG",
        "MaxHR",
        "ExerciseAngina",
        "Oldpeak",
        "ST_Slope",
    ]
    for field in required_fields:
        if field not in data:
            return f"Parâmetro {field.upper()} não informado", 400

    # Obtém os valores dos campos
    age = data["Age"]
    sex = data["Sex"]
    chest_pain = data["ChestPainType"]
    resting_bp = data["RestingBP"]
    cholesterol = data["Cholesterol"]
    fasting_bs = data["FastingBS"]
    resting_ecg = data["RestingECG"]
    max_hr = data["MaxHR"]
    exercise = data["ExerciseAngina"]
    oldpeak = data["Oldpeak"]
    st_slope = data["ST_Slope"]

    # Create a new DataFrame
    new_data = pd.DataFrame(
        {
            "Age": [age],
            "Sex": [sex],
            "ChestPainType": [chest_pain],
            "RestingBP": [resting_bp],
            "Cholesterol": [cholesterol],
            "FastingBS": [fasting_bs],
            "RestingECG": [resting_ecg],
            "MaxHR": [max_hr],
            "ExerciseAngina": [exercise],
            "Oldpeak": [oldpeak],
            "ST_Slope": [st_slope],
        }
    )

    try:
        # Codifica os dados com o encoder carregado
        data_encoded = loaded_encoder.transform(
            new_data[
                ["Sex", "ChestPainType", "RestingECG", "ExerciseAngina", "ST_Slope"]
            ]
        ).toarray()

        encoded_column_names = loaded_encoder.get_feature_names_out(
            ["Sex", "ChestPainType", "RestingECG", "ExerciseAngina", "ST_Slope"]
        )

        data_encoded_df = pd.DataFrame(data_encoded, columns=encoded_column_names)

        data_final = pd.concat([new_data, data_encoded_df], axis=1)

        new_data_encoded = data_final.drop(
            ["Sex", "ChestPainType", "RestingECG", "ExerciseAngina", "ST_Slope"], axis=1
        )
    except Exception as e:
        return f"Erro ao codificar os dados: {str(e)}", 400

    # Faz a previsão com o modelo carregado
    predicted_type = loaded_model.predict(new_data_encoded)

    # Retornar o resultado como JSON
    return jsonify({"previsao": "Saudável" if predicted_type[0] == 0 else "Doente"})


if __name__ == "__main__":
    print("Servidor Flask em execução")
    # Executar o aplicativo Flask
    app.run(debug=True)

# ENDPOINTS:
# POST /prever - retorna a previsão com base nos parâmetros informados

""" 
Exemplo de chamada POST:
http://localhost:5000/prever 

JSON de entrada:
Examplo Saudável:
{
    "Age": 40,
    "Sex": "M",
    "ChestPainType": "ATA",
    "RestingBP": 140,
    "Cholesterol": 289,
    "FastingBS": 0,
    "RestingECG": "Normal",
    "MaxHR": 172,
    "ExerciseAngina": "N",
    "Oldpeak": 0,
    "ST_Slope": "Up"
}

Exemplo Doente:
# 58,M,ATA,136,164,0,ST,99,Y,2,Flat
{
    "Age": 58,
    "Sex": "M",
    "ChestPainType": "ATA",
    "RestingBP": 136,
    "Cholesterol": 164,
    "FastingBS": 0,
    "RestingECG": "ST",
    "MaxHR": 99,
    "ExerciseAngina": "Y",
    "Oldpeak": 2,
    "ST_Slope": "Flat"
}
"""

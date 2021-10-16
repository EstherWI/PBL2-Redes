
from flask import Flask, request,  jsonify
import os

app = Flask(__name__)

'''
Json de dados do paciente
'''
tabelaDados = {
    'pacientes': [
        
    ]
}

class CrudPaciente():

    def getTodosPacientes(self)->dict:
        return tabelaDados['pacientes']
        
    def getPacienteByCPF(self, cpf: int)->dict:
        tabela= tabelaDados['pacientes']
        for x in tabela:
            if(x['cpf']==cpf):
                return x
        return None

    def add(self, paciente: dict):
        tabelaDados['pacientes'].append(paciente)

    def updatePaciente(self, cpf: int, dados: dict) -> bool:
        i= None
        aux = 0
        tabela = tabelaDados['pacientes']
        for p in tabela:
            if(p['cpf']==cpf):
                i = aux #aqui pegar o index do paciente em questão
            aux = aux+1
        if i!=None:
            tabela[i]['temp'] = dados['temp']
            tabela[i]['freq'] = dados['freq']
            tabela[i]['pressao'] = dados['pressao']
            tabela[i]['saturacao'] = dados['saturacao']
            return True
        else:
            return False
    def reportPaciente(self, cpf: int, dados: dict) -> bool:
            i= None
            aux = 0
            tabela = tabelaDados['pacientes']
            for p in tabela:
                if(p['cpf']==cpf):
                    i = aux #aqui pegar o index do paciente em questão
                aux = aux+1
            if i!=None:
                tabela[i]['statusSaude'] = dados['statusSaude']
                return True
            else:
                return False

dados = CrudPaciente()



@app.route('/paciente', methods=['GET'])
def listaTodos():
  
    return jsonify(dados.getTodosPacientes()), 200


@app.route('/paciente/status/<int:cpf>', methods=['PUT'])
def reportStatus(cpf: int):
    dataUpdate = request.json
    if dados.reportPaciente(cpf, dataUpdate):
        return jsonify({'status': 'Sucess'}), 200
    else:
        return jsonify({'status': 'Paciente não encontrado'}), 404

@app.route('/paciente/<int:cpf>', methods=['PUT'])
def update(cpf: int):
    dataUpdate = request.json
    if dados.updatePaciente(cpf, dataUpdate):
        return jsonify({'status': 'Sucess'}), 200
    else:
        return jsonify({'status': 'Paciente não encontrado'}), 404

@app.route('/paciente/<int:cpf>', methods=['GET'])
def get(cpf: int):
    if dados.getPacienteByCPF(cpf):
        return jsonify(dados.getPacienteByCPF(cpf)), 200
    else:
        return jsonify({'status': 'Paciente não encontrado'}), 404

@app.route('/paciente/criar', methods=['POST'])
def criar():
    paciente = request.json
    dados.add(paciente)
 
    return jsonify({'status': 'Sucess'}), 200
   
port = int(os.environ.get("PORT", 5000))
app.run(debug=True ,host='0.0.0.0', port=port)



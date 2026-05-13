# 🛰️ WEATHPATH | Deep Route Analytics
> **The Next-Gen Logistics & Weather Intelligence Engine**

![Python](https://img.shields.io/badge/python-3.9+-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg?style=for-the-badge)
![Interface](https://img.shields.io/badge/UI-Streamlit_WebApp-blueviolet.svg?style=for-the-badge&logo=streamlit&logoColor=white)

---

## ⚡ O que é o WEATHPATH?
O **WEATHPATH** não é apenas um script de clima. É um motor de **Deep Analytics** desenvolvido para transformar dados brutos de satélite em decisões logísticas estratégicas. Ele funde variáveis meteorológicas críticas com lógica de transporte rodoviário para garantir que a carga chegue ao destino com o menor risco e a maior eficiência possível.

---

## 🛠️ Deep Analytics & Features "Hardcore"

### 🛡️ Módulo de Segurança (Safety First)
* **Detecção de Aquaplanagem:** Algoritmo que cruza milímetros de chuva com probabilidade de perda de tração.
* **Alerta de Visibilidade Crítica:** Monitoramento de névoa e tempestades via sensores de pressão e umidade com análise visual de pista.
* **Modo Atenção Dinâmico:** Interface web com painéis técnicos coloridos que alertam visualmente quando os parâmetros saem da zona verde.

### 📦 Inteligência Logística
* **Cálculo de ETA Adaptativo:** Estimativa real de chegada baseada em distância e carga horária, integrando hora e data exata da chegada.
* **Módulos Inteligentes:** Roteirização customizada adaptada para perfis de **Frota Comercial** ou **Viagem Pessoal**.
* **Geocodificação Dinâmica:** Integração direta com links de rotas externas para o Google Maps em tempo real.

### ☁️ Monitoramento Atmosférico
* **Vetor de Ventos:** Velocidade e dinâmica de ventos e umidade essencial para cargas de alto volume.
* **Ciclo Solar:** Horários precisos de *Sunrise* e *Sunset* para gestão de fadiga noturna e planejamento de paradas.
* **Probabilidade de Precipitação (PoP):** Dados granulares sobre chance de chuva por região coletados via satélite.

---

## 🖥️ Visual Stack (Cyberpunk Industrial UI)
Esqueça telas brancas convencionais. O **WEATHPATH** entrega uma experiência web operacional de alta densidade inspirada em terminais de comando Linux:
* **Rich Terminal Clone:** Injeção de CSS customizado com paleta de cores escura operacional e fontes mono de alta legibilidade.
* **Tabelas de Alta Densidade:** Matriz meteorológica e parâmetros técnicos organizados para leitura rápida.
* **Feedback Assíncrono:** Spinners nativos e barras de carregamento durante a sintonização com os satélites de clima.

---

## 🚀 Como Rodar o Motor

1. **Clone o repositório:**
   ```
   git clone [https://github.com/NathnF0/WEATHPATH.git](https://github.com/NathnF0/WEATHPATH.git)
   cd WEATHPATH
   
2. **Instale as dependências de elite:**
```
pip install -r requirements.txt
```

3. **Configuração da Chave de Satélite (API Key)**
Para que o WEATHPATH acesse os dados em tempo real, você precisa de uma credencial oficial.

Obtenha sua Chave: Acesse o portal OpenWeatherMap, crie uma conta gratuita e gere sua API Key na seção "My API Keys".

Injete a Credencial: Na raiz do projeto, crie ou altere o arquivo .env e adicione a sua chave da seguinte forma:

```
API_KEY=sua_chave_aqui_sem_aspas
```
**[!IMPORTANT]**
SEGURANÇA EM PRIMEIRO LUGAR: O arquivo .env está configurado no .gitignore para nunca ser enviado publicamente ao GitHub. Mantenha suas credenciais sempre em sigilo.

4. **Inicie o Sistema Web:**
```
streamlit run main.py
```

## **👤 Architect & Lead Developer**
"No código, como na estrada, a clareza é a única forma de evitar o desastre. O WEATHPATH é a minha resposta para o caos climático." — NathnF

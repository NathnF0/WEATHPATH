import os
import requests
import math
import urllib.parse
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

# Configuração de ambiente
caminho_env = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=caminho_env)

# Configuração da Página Web (Streamlit)
st.set_page_config(
    page_title="WEATHPATH - Inteligência Logística",
    page_icon="🛰️",
    layout="wide"
)

# --- INJEÇÃO DE CSS INDUSTRIAL (CLONE ESTÉTICO DO RICH TERMINAL) ---
st.markdown("""
    <style>
        /* Define o fundo escuro operacional e fontes mono */
        .stApp {
            background-color: #0b0f19;
            color: #e2e8f0;
            font-family: 'Courier New', Courier, monospace;
        }
        
        /* Customização de Prompts de Input */
        input {
            background-color: #111827 !important;
            color: #38bdf8 !important;
            border: 1px solid #1e3a8a !important;
            font-family: 'Courier New', Courier, monospace !important;
        }
        
        /* Banner Centralizado Estilo Rich Panel */
        .rich-banner {
            background-color: #111827;
            border: 2px solid #2563eb;
            border-radius: 4px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.7);
            margin-bottom: 25px;
        }
        
        /* Tabelas de Alta Densidade Estilo Rich Table */
        .rich-table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            background-color: #0f172a;
            border: 1px solid #334155;
        }
        .rich-table th {
            background-color: #1e293b;
            color: #38bdf8;
            padding: 12px;
            text-align: left;
            border-bottom: 2px solid #2563eb;
            font-size: 14px;
            font-weight: bold;
        }
        .rich-table td {
            padding: 12px;
            border-bottom: 1px solid #334155;
            font-size: 14px;
        }
        
        /* Blocos de Métricas Customizados */
        .metric-card {
            background-color: #1e293b;
            border: 1px solid #475569;
            padding: 15px;
            border-radius: 4px;
            text-align: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.3);
        }
        .metric-card-label { color: #94a3b8; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; }
        .metric-card-value { color: #ffffff; font-size: 18px; font-weight: bold; margin-top: 5px; }

        /* Painéis de Recomendação Técnica com Cores Fortes */
        .rich-panel {
            padding: 18px;
            border-radius: 4px;
            font-weight: bold;
            margin-top: 20px;
            border-left: 6px solid;
            box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        }
        .panel-green { background-color: #064e3b; border-color: #10b981; color: #a7f3d0; }
        .panel-orange { background-color: #78350f; border-color: #f59e0b; color: #fde68a; }
        .panel-red { background-color: #7f1d1d; border-color: #ef4444; color: #fca5a5; }
        .panel-blue { background-color: #1e3a8a; border-color: #3b82f6; color: #bfdbfe; }
    </style>
""", unsafe_allow_html=True)


class GestorLogisticaWeb:
    def __init__(self):
        self.chave_api = os.getenv("API_KEY") or st.secrets.get("API_KEY", "")
        self.url_base = "http://api.openweathermap.org/data/2.5/weather"
        self.url_forecast = "http://api.openweathermap.org/data/2.5/forecast"
        
    def calcular_distancia_haversine(self, lat1, lon1, lat2, lon2):
        R = 6371 
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return round((R * c) * 1.30, 2)

    def buscar_dados(self, cidade):
        if not self.chave_api:
            st.error("🔑 API_KEY não configurada. Verifique seu arquivo .env.")
            return None
            
        params = {"q": cidade, "appid": self.chave_api, "units": "metric", "lang": "pt_br"}
        
        try:
            res_atual = requests.get(self.url_base, params=params, timeout=10)
            res_atual.raise_for_status()
            
            res_prev = requests.get(self.url_forecast, params=params, timeout=10)
            res_prev.raise_for_status()

            return {
                "atual": res_atual.json(), 
                "previsao": res_prev.json()
            }
        except requests.exceptions.RequestException:
            st.error(f"❌ **Erro de Conexão:** Não foi possível localizar '{cidade}'. Verifique o nome ou a chave de API.")
            return None
        except Exception as e:
            st.error(f"❌ **Erro Inesperado:** {e}")
            return None

    def processar_viagem_completa(self, origem_nome, destino_nome, tipo_usuario):
        dados_origem = self.buscar_dados(origem_nome)
        dados_destino = self.buscar_dados(destino_nome)

        if not dados_origem or not dados_destino:
            return {"erro": "Uma das cidades não foi localizada no radar geográfico."}

        lat1, lon1 = dados_origem['atual']['coord']['lat'], dados_origem['atual']['coord']['lon']
        lat2, lon2 = dados_destino['atual']['coord']['lat'], dados_destino['atual']['coord']['lon']
        
        km_final = self.calcular_distancia_haversine(lat1, lon1, lat2, lon2)
        
        vel_media = 95 if tipo_usuario == "PESSOAL" else 75
        tempo_total = km_final / vel_media
        chegada_dt = datetime.now() + timedelta(hours=tempo_total)

        previsoes = dados_destino['previsao']['list']
        clima_futuro = previsoes[0]
        for p in previsoes:
            dt_p = datetime.strptime(p['dt_txt'], '%Y-%m-%d %H:%M:%S')
            if dt_p >= chegada_dt:
                clima_futuro = p
                break
        
        origem_encoded = urllib.parse.quote(dados_origem['atual']['name'])
        destino_encoded = urllib.parse.quote(dados_destino['atual']['name'])
        link_maps = f"https://www.google.com/maps/dir/{origem_encoded}/{destino_encoded}"

        return {
            "origem": dados_origem['atual']['name'],
            "destino": dados_destino['atual']['name'],
            "distancia": f"{km_final} KM",
            "tempo": f"{tempo_total:.1f}h",
            "chegada": chegada_dt.strftime("%d/%m às %H:%M"),  # <- Modificado aqui para incluir o dia/mês
            "clima_full": {
                "temp": f"{clima_futuro['main']['temp']}°C",
                "sensacao": f"{clima_futuro['main']['feels_like']}°C",
                "desc": clima_futuro['weather'][0]['description'].capitalize(),
                "umidade": f"{clima_futuro['main']['humidity']}%",
                "vento": f"{clima_futuro['wind']['speed']} m/s",
                "pop": f"{int(clima_futuro.get('pop', 0) * 100)}%",
                "visibilidade": f"{clima_futuro.get('visibility', 10000) / 1000} KM"
            },
            "maps": link_maps 
        }

# ----------------- INTERFACE INTERATIVA (STREAMLIT) -----------------

app = GestorLogisticaWeb()

# Cabeçalho da Aplicação Estilizado
st.markdown(f"""
    <div class="rich-banner">
        <h2 style="color: #ffffff; margin: 0; font-weight: bold; letter-spacing: 2px;">🛰️ SISTEMA DE INTELIGÊNCIA LOGÍSTICA</h2>
        <div style="color: #38bdf8; font-weight: bold; margin-top: 5px; font-size: 14px;">ESTRADA SEGURA v6.0 - DEEP ANALYTICS WEB</div>
        <div style="color: #10b981; font-size: 11px; margin-top: 10px; font-family: monospace; opacity: 0.8;">
            [STATUS: OPERACIONAL ATIVO] | Monitoramento em tempo real via satélite
        </div>
    </div>
""", unsafe_allow_html=True)

# Menu Lateral de Navegação
modo = st.sidebar.selectbox(
    "Selecione o Módulo de Controle",
    ["Inteligência de Rota (Frota)", "Planejador Pessoal (Viagem)", "Consulta Rápida Meteorológica"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ Status do Sistema")
st.sidebar.success("● Núcleo de Roteirização Ativo")
st.sidebar.info(f"📅 {datetime.now().strftime('%d/%m/%Y | %H:%M')}")

# Lógica dos Módulos de Rota (Frota e Pessoal)
if modo in ["Inteligência de Rota (Frota)", "Planejador Pessoal (Viagem)"]:
    tipo = "FROTA" if "Frota" in modo else "PESSOAL"
    
    st.markdown(f"### 🚛 Painel de Operação — <span style='color:#38bdf8;'>Modo {tipo}</span>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        origem = st.text_input("Cidade de Origem", placeholder="Ex: São Paulo").strip()
    with col2:
        destino = st.text_input("Cidade de Destino", placeholder="Ex: Rio de Janeiro").strip()
        
    if st.button("🚀 Iniciar Deep Analytics de Rota"):
        if origem and destino:
            with st.spinner("Acessando satélites e processando malha rodoviária..."):
                res = app.processar_viagem_completa(origem, destino, tipo)
                
            if "erro" in res:
                st.error(res['erro'])
            else:
                # Exibição dos Parâmetros de Deslocamento
                st.markdown("<br><h4 style='color: #e2e8f0; border-bottom: 1px solid #2563eb; padding-bottom: 5px;'>📊 PARÂMETROS DE DESLOCAMENTO</h4>", unsafe_allow_html=True)
                m1, m2, m3, m4 = st.columns(4)
                with m1: st.markdown(f'<div class="metric-card"><div class="metric-card-label">Origem</div><div class="metric-card-value">{res["origem"]}</div></div>', unsafe_allow_html=True)
                with m2: st.markdown(f'<div class="metric-card"><div class="metric-card-label">Destino</div><div class="metric-card-value">{res["destino"]}</div></div>', unsafe_allow_html=True)
                with m3: st.markdown(f'<div class="metric-card"><div class="metric-card-label">Distância Estimada</div><div class="metric-card-value" style="color:#f59e0b;">{res["distancia"]}</div></div>', unsafe_allow_html=True)
                with m4: st.markdown(f'<div class="metric-card"><div class="metric-card-label">Previsão ETA</div><div class="metric-card-value" style="color:#10b981;">{res["chegada"]}</div></div>', unsafe_allow_html=True)
                
                # Análise Meteorológica no Destino (Tabela Rich Customizada)
                st.markdown(f"<br><h4 style='color: #e2e8f0; border-bottom: 1px solid #2563eb; padding-bottom: 5px;'>🌦️ MATRIZ METEOROLÓGICA EM {res['destino'].upper()}</h4>", unsafe_allow_html=True)
                c = res['clima_full']
                
                # Tratamento visual da Visibilidade
                vis_valor = float(c['visibilidade'].replace(' KM', ''))
                if vis_valor >= 10: vis_status = "<span style='color:#10b981; font-weight:bold;'>MÁXIMA (10km+)</span>"
                elif vis_valor > 5: vis_status = "<span style='color:#f59e0b; font-weight:bold;'>MODERADA</span>"
                else: vis_status = "<span style='color:#ef4444; font-weight:bold;'>REDUZIDA / PERIGO</span>"
                
                st.markdown(f"""
                    <table class="rich-table">
                        <thead>
                            <tr>
                                <th>INDICADOR TÉCNICO</th>
                                <th>DADO COLETADO VIA SATÉLITE</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr><td>🪐 Condição Estimada</td><td><b>{c['desc']}</b></td></tr>
                            <tr><td>🌡️ Temperatura / Sensação</td><td>{c['temp']} (Sente como {c['sensacao']})</td></tr>
                            <tr><td>☔ Chance de Chuva (PoP)</td><td style="color:#f59e0b; font-weight:bold;">{c['pop']}</td></tr>
                            <tr><td>👁️ Visibilidade da Pista</td><td>{vis_status}</td></tr>
                            <tr><td>💨 Dinâmica de Ventos e Umidade</td><td>{c['vento']} | {c['umidade']}</td></tr>
                        </tbody>
                    </table>
                """, unsafe_allow_html=True)
                
                # Módulo de Recomendação Técnica (Painel Colorido)
                pop_valor = int(c['pop'].replace('%', ''))
                
                if pop_valor > 70:
                    panel_style = "panel-red"
                    recomendacao = f"⚠ ALERTA DE RISCO: Alta probabilidade de chuva forte ({c['pop']}). Risco severo de aquaplanagem!"
                elif vis_valor < 5:
                    panel_style = "panel-orange"
                    recomendacao = f"⚠ ATENÇÃO CRÍTICA: Visibilidade reduzida ({vis_valor} KM). Reduza a velocidade de rodagem."
                elif "Chuva" in c['desc']:
                    panel_style = "panel-blue"
                    recomendacao = "⚠ ADVERTÊNCIA: Pista molhada confirmada no destino. Redobrar o cuidado em curvas."
                else:
                    panel_style = "panel-green"
                    recomendacao = "✓ PARÂMETROS SEGUROS: Condições ideais detectadas na pista. Boa viagem!"
                    
                st.markdown(f"""
                    <div class="rich-panel {panel_style}">
                        <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 1px; opacity: 0.8;">💡 RECOMENDAÇÃO TÉCNICA OPERACIONAL</div>
                        <div style="font-size: 15px; margin-top: 5px;">{recomendacao}</div>
                    </div>
                """, unsafe_allow_html=True)
                    
                # Link do Google Maps Estilo Shell Command
                st.markdown(f"<br><div style='font-size:13px;'>[LINK] Conexão Externa: <a href='{res['maps']}' target='_blank' style='color:#38bdf8; text-decoration:underline;'>Google Maps Connection Link</a></div>", unsafe_allow_html=True)
        else:
            st.warning("⚠️ Por favor, preencha os campos de Origem e Destino.")

# Lógica do Módulo de Consulta Rápida
elif modo == "Consulta Rápida Meteorológica":
    st.markdown("### 📡 Estação Meteorológica Dinâmica", unsafe_allow_html=True)
    cidade_busca = st.text_input("Digite o nome da cidade para consulta instantânea")
    
    if st.button("📡 Sintonizar Estação"):
        if cidade_busca:
            with st.spinner("Coletando dados ativos de satélite..."):
                dados = app.buscar_dados(cidade_busca)
                
            if dados:
                atual = dados['atual']
                previsao = dados['previsao']
                pop = previsao.get('list', [{}])[0].get('pop', 0)
                
                st.markdown(f"<br><h4 style='color: #10b981; border-bottom: 1px solid #10b981; padding-bottom: 5px;'>📡 RELATÓRIO METEOROLÓGICO: {atual['name'].upper()}</h4>", unsafe_allow_html=True)
                
                nascer = datetime.fromtimestamp(atual['sys']['sunrise']).strftime('%H:%M')
                por_sol = datetime.fromtimestamp(atual['sys']['sunset']).strftime('%H:%M')
                
                st.markdown(f"""
                    <table class="rich-table">
                        <thead>
                            <tr>
                                <th>INDICADOR TÉCNICO</th>
                                <th>DADO ATUAL EM TEMPO REAL</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr><td>🌡️ Temperatura Atual</td><td style="color:#ffffff; font-weight:bold;">{atual['main']['temp']}°C</td></tr>
                            <tr><td>🔥 Sensação Térmica</td><td>{atual['main']['feels_like']}°C</td></tr>
                            <tr><td>☁️ Condição do Céu</td><td>{atual['weather'][0]['description'].capitalize()}</td></tr>
                            <tr><td>☔ Chance de Chuva</td><td>{int(pop * 100)}%</td></tr>
                            <tr><td>💧 Umidade Relativa</td><td>{atual['main']['humidity']}%</td></tr>
                            <tr><td>⏲️ Pressão Atmosférica</td><td>{atual['main']['pressure']} hPa</td></tr>
                            <tr><td>🌅 Ciclo Solar (Nascer / Pôr)</td><td>☀️ {nascer} / 🌙 {por_sol}</td></tr>
                        </tbody>
                    </table>
                """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Digite o nome de uma cidade.")
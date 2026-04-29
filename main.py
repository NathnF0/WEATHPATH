import os
import requests
import csv
import urllib.parse
import random
import math
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv

# Bibliotecas Masterclass de Personalização
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt
from rich.align import Align

# Configuração de ambiente
caminho_env = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=caminho_env)

console = Console()

class GestorLogisticaMaster:
    def __init__(self):
        self.chave_api = os.getenv("API_KEY")
        self.url_base = "http://api.openweathermap.org/data/2.5/weather"
        self.url_forecast = "http://api.openweathermap.org/data/2.5/forecast"
        self.arquivo_historico = Path(__file__).parent / "historico_logistica.csv"
        
        self.frases_tecnicas = [
            "Monitoramento em tempo real via satélite OpenWeather.",
            "Otimizando rotas, garantindo segurança e precisão.",
            "Inteligência de dados aplicada à malha rodoviária.",
            "Sincronização global de dados meteorológicos ativos."
        ]

    def exibir_banner(self, modo="PRINCIPAL"):
        os.system('cls' if os.name == 'nt' else 'clear')
        titulo = Text("SISTEMA DE INTELIGÊNCIA LOGÍSTICA", style="bold white")
        subtitulo = Text("ESTRADA SEGURA v6.0 - DEEP ANALYTICS", style="cyan")
        
        banner_conteudo = Text()
        banner_conteudo.append("\n 🛰️  ", style="bold cyan")
        banner_conteudo.append("NÚCLEO DE ROTEIRIZAÇÃO E CLIMA CRÍTICO\n", style="bold white")
        banner_conteudo.append(f" Status: [Ativo] | Modo: {modo}\n", style="dim green")
        banner_conteudo.append(f" {datetime.now().strftime('%d/%m/%Y | %H:%M:%S')}\n", style="dim white")

        console.print(Panel(Align.center(banner_conteudo), title=titulo, subtitle=subtitulo, border_style="blue", padding=(1, 2)))
        console.print(f"[dim italic white]ℹ️ {random.choice(self.frases_tecnicas)}[/]\n", justify="center")

    def calcular_distancia_haversine(self, lat1, lon1, lat2, lon2):
        R = 6371 
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        # Aumentei o fator de correção para 1.3 (30%) para melhorar a precisão
        return round((R * c) * 1.30, 2)

    def buscar_dados(self, cidade):
        params = {"q": cidade, "appid": self.chave_api, "units": "metric", "lang": "pt_br"}
        
        try:
            # Tenta buscar os dados atuais
            res_atual = requests.get(self.url_base, params=params, timeout=10)
            res_atual.raise_for_status() # Dispara erro se a API falhar (ex: cidade errada)
            
            # Tenta buscar a previsão
            res_prev = requests.get(self.url_forecast, params=params, timeout=10)
            res_prev.raise_for_status()

            return {
                "atual": res_atual.json(), 
                "previsao": res_prev.json()
            }

        except requests.exceptions.RequestException as e:
            console.print(f"[bold red]❌ ERRO DE CONEXÃO:[/] Verifique sua internet ou a cidade digitada.")
            return None
        except Exception as e:
            console.print(f"[bold red]❌ ERRO INESPERADO:[/] {e}")
            return None
    
    def consultar_clima_cidade(self, cidade_nome):
        with console.status("[bold yellow]Acessando satélites...", spinner="point"):
            dados = self.buscar_dados(cidade_nome)
            
        if not dados:
            console.print(Panel(f"[bold red]ERRO:[/] Cidade '{cidade_nome}' fora de alcance.", border_style="red"))
            return

        atual = dados['atual']
        
        # Tabela Master de Clima
        t_simples = Table(title=f"📡 RELATÓRIO METEOROLÓGICO: {atual['name'].upper()}", expand=True, border_style="yellow")
        t_simples.add_column("INDICADOR TÉCNICO", style="cyan")
        t_simples.add_column("DADO COLETADO", style="bold white")
        pop = dados.get('previsao', {}).get('list', [{}])[0].get('pop', 0)
        pop_formatado = f"{int(pop * 100)}%"
        
        # Dados de Temperatura
        t_simples.add_row("🌡️ Temperatura Atual", f"{atual['main']['temp']}°C")
        t_simples.add_row("🔥 Sensação Térmica", f"{atual['main']['feels_like']}°C")
        t_simples.add_row("☁️ Condição do Céu", atual['weather'][0]['description'].capitalize())
        
        # Dados de Atmosfera
        t_simples.add_row("☔ Chance de Chuva", pop_formatado)
        t_simples.add_row("💧 Umidade Relativa", f"{atual['main']['humidity']}%")
        t_simples.add_row("⏲️ Pressão Atmosférica", f"{atual['main']['pressure']} hPa")
        t_simples.add_row("🌫️ Cobertura de Nuvens", f"{atual['clouds']['all']}%")

        # Dados de Dinâmica
        t_simples.add_row("💨 Velocidade do Vento", f"{atual['wind']['speed']} m/s")
        t_simples.add_row("🧭 Direção do Vento", f"{atual['wind'].get('deg', 0)}°")
        
        # Dados de Astronomia (Conversão de Timestamp para Horário)
        nascer = datetime.fromtimestamp(atual['sys']['sunrise']).strftime('%H:%M')
        por_sol = datetime.fromtimestamp(atual['sys']['sunset']).strftime('%H:%M')
        t_simples.add_row("🌅 Nascer do Sol", nascer)
        t_simples.add_row("🌇 Pôr do Sol", por_sol)
        
        console.print(Panel(t_simples, border_style="yellow", subtitle="Dados em tempo real via OpenWeather API"))

    def processar_viagem_completa(self, origem_nome, destino_nome, tipo_usuario):
        with console.status("[bold blue]Iniciando Deep Analytics de Rota...", spinner="earth"):
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
            
            # CORREÇÃO DO LINK DO MAPS AQUI:
            origem_encoded = urllib.parse.quote(dados_origem['atual']['name'])
            destino_encoded = urllib.parse.quote(dados_destino['atual']['name'])
            link_maps = f"https://www.google.com/maps/dir/{origem_encoded}/{destino_encoded}"

            # ... código anterior onde você definiu link_maps ...

            return {
                "origem": dados_origem['atual']['name'],
                "destino": dados_destino['atual']['name'],
                "distancia": f"{km_final} KM",
                "tempo": f"{tempo_total:.1f}h",
                "chegada": chegada_dt.strftime("%H:%M"),
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

    def exibir_analise_detalhada(self, res, tipo):
        if "erro" in res:
            console.print(Panel(f"[bold red]ALERTA:[/] {res['erro']}", border_style="red"))
            return

        t_rota = Table(title="🚛 PARÂMETROS DE DESLOCAMENTO", expand=True, border_style="blue")
        t_rota.add_column("Origem", justify="center")
        t_rota.add_column("Destino", justify="center")
        t_rota.add_column("Distância Real Est.", justify="center")
        t_rota.add_column("Previsão de Chegada (ETA)", justify="center", style="bold yellow")
        t_rota.add_row(res['origem'], res['destino'], res['distancia'], res['chegada'])
        console.print(t_rota)

        t_clima = Table(title=f"🌦️ ANÁLISE METEOROLÓGICA EM {res['destino'].upper()}", expand=True, border_style="cyan")
        t_clima.add_column("Métrica", style="dim")
        t_clima.add_column("Valor Analítico", style="bold white")
        
        c = res['clima_full']
        
        # Lógica para traduzir os "10km" em algo visual
        vis_valor = float(c['visibilidade'].replace(' KM', ''))
        if vis_valor >= 10:
            vis_status = "[bold green]MÁXIMA (10km+)[/]"
        elif vis_valor > 5:
            vis_status = "[bold yellow]MODERADA[/]"
        else:
            vis_status = "[bold red]REDUZIDA / PERIGO[/]"

        t_clima.add_row("Condição Estimada", c['desc'])
        t_clima.add_row("Temperatura / Sensação", f"{c['temp']} (Sente como {c['sensacao']})")
        t_clima.add_row("Probabilidade de Chuva", f"[bold yellow]{c['pop']}[/]")
        t_clima.add_row("Visibilidade da Pista", vis_status)
        t_clima.add_row("Vento / Umidade", f"{c['vento']} | {c['umidade']}")
        
        console.print(Panel(t_clima, border_style="cyan"))

        cor = "green" if tipo == "PESSOAL" else "blue"
        msg = "✓ Boa viagem! Mantenha a atenção na sinalização." if tipo == "PESSOAL" else "✓ Logística validada. Dados de frota sincronizados."
        console.print(f"[bold {cor}]{msg}[/]")
        console.print(f"[dim]Link da Rota: [link={res['maps']}][u]Google Maps Connection[/u][/link][/]\n")

        c = res['clima_full']
        
        # Garantindo que os valores sejam números para a comparação
        pop_valor = int(c['pop'].replace('%', ''))
        
        # Extrai apenas o número da visibilidade (remove o " KM" se existir)
        try:
            vis_valor = float(str(c['visibilidade']).replace(' KM', ''))
        except:
            vis_valor = 10.0 # Valor padrão caso falhe

        recomendacao = "[bold green]√ Condições ideais para rodagem. Boa viagem![/]"
        
        if pop_valor > 70:
            recomendacao = f"[bold red]⚠ ALERTA: Alta probabilidade de chuva forte ({c['pop']}). Risco de aquaplanagem![/]"
        elif vis_valor < 5:
            recomendacao = f"[bold yellow]⚠ ATENÇÃO: Visibilidade reduzida ({vis_valor}km). Reduza a velocidade![/]"
        elif "Chuva" in c['desc']:
            recomendacao = "[bold blue]⚠ Pista molhada confirmada no destino. Redobre o cuidado nas curvas.[/]"

        console.print(Panel(recomendacao, title="💡 RECOMENDAÇÃO TÉCNICA", border_style="white"))

def iniciar():
    app = GestorLogisticaMaster()
    while True:
        app.exibir_banner("MENU DE CONTROLE")
        console.print("[bold yellow][1][/] Inteligência de Rota (Empresa/Frota)")
        console.print("[bold yellow][2][/] Planejador Pessoal (Viagem)")
        console.print("[bold yellow][3][/] Consulta Rápida (Estação Metereológica)") # <--- NOVA OPÇÃO
        console.print("[bold red][4][/] Desligar Sistema")
        
        op = Prompt.ask("\nComando", choices=["1", "2", "3", "4"])
        if op in ["1", "2"]:
            tipo = "FROTA" if op == "1" else "PESSOAL"
            app.exibir_banner(tipo)
            ori = Prompt.ask("Cidade de Origem")
            des = Prompt.ask("Cidade de Destino")
            
            analise = app.processar_viagem_completa(ori, des, tipo)
            app.exibir_analise_detalhada(analise, tipo)
            Prompt.ask("\n[dim]Pressione ENTER para retornar[/]")

        elif op == "3":
            app.exibir_banner("CONSULTA RÁPIDA")
            cidade = Prompt.ask("Digite o nome da cidade")
            app.consultar_clima_cidade(cidade)
            Prompt.ask("\n[dim]Pressione ENTER para retornar[/]")

        elif op == "4":
            console.print("\n[bold blue]Finalizando processos... Sistema offline.[/]")
            break

if __name__ == "__main__":
    iniciar()
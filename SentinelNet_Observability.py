# -*- coding: utf-8 -*-
import subprocess
import sys

# --- AUTO-INSTALAÇÃO ---
def install_dependencies():
    try:
        import telebot
    except ImportError:
        print("Instalando pyTelegramBotAPI...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyTelegramBotAPI"])

install_dependencies()

import customtkinter as ctk
from tkinter import ttk, messagebox
import json, os, threading, requests, time, random
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

class SentinelFullPower(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- DADOS DO BOT ---
        self.bot_token = "8542730672:AAG7_-5ipKrI-floIz7gTN5linpo-Rz-0gY"
        self.chat_id = "7694564020"
        self.bot = telebot.TeleBot(self.bot_token)

        self.title("SENTINEL OMNI | INFRAESTRUTURA COMPLETA BRASIL")
        self.geometry("1600x950")
        self.configure(fg_color="#000000")

        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.config_file = os.path.join(self.base_path, "DATABASE_BRASIL_TOTAL.json")
        
        self.status_cache = {}
        self.lock_status = set() # SISTEMA DE TRAVA TOTAL
        self.cidade_atual = None
        self.running = True
        
        self.setup_layout()
        
        # Protocolo de segurança para fechamento de janela
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Threads de Operação
        threading.Thread(target=self.inicializar_sistema, daemon=True).start()
        threading.Thread(target=self.safe_bot_polling, daemon=True).start()

    def on_closing(self):
        """Garante que o sistema feche todas as threads antes de encerrar"""
        self.running = False
        self.destroy()

    def safe_bot_polling(self):
        """Watchdog do Bot: Se a conexão cair, ele tenta reconectar sem derrubar o programa"""
        while self.running:
            try:
                self.ouvir_bot()
            except Exception as e:
                print(f"Erro na conexão do Bot: {e}. Reiniciando conexão em 5s...")
                time.sleep(5)

    def inicializar_sistema(self):
        if os.path.exists(self.config_file):
            self.atualizar_status_loading("CARREGANDO BANCO DE DADOS LOCAL...")
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.infra = json.load(f)
            except:
                self.infra = self.get_ibge_data_total()
        else:
            self.infra = self.get_ibge_data_total()

        self.after(0, self.popular_tree)
        threading.Thread(target=self.engine_status, daemon=True).start()

    def get_ibge_data_total(self):
        base_final = {"BRASIL": {}}
        try:
            self.atualizar_status_loading("CONECTANDO AO SERVIDOR...")
            r = requests.get("https://servicodados.ibge.gov.br/api/v1/localidades/estados", timeout=15)
            estados = sorted(r.json(), key=lambda x: x['nome'])
            
            for i, est in enumerate(estados, 1):
                nome_uf = est['nome'].upper()
                sigla = est['sigla']
                self.atualizar_status_loading(f"SINCRONIZANDO {nome_uf}...")
                base_final["BRASIL"][nome_uf] = {}
                c_req = requests.get(f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{sigla}/municipios", timeout=15)
                cidades = sorted(c_req.json(), key=lambda x: x['nome'])
                
                nomes_lojas = ["FERREIRA", "FARMÁCIA", "SUPERMERCADO", "POSTO CENTRAL", "LOGÍSTICA", 
                               "CENTRO TECH", "BASE ALPHA", "ALMOXARIFADO", "NAVEGAÇÃO", "TERMINAL 10"]
                
                for c in cidades:
                    nome_cid = c['nome'].upper()
                    base_final["BRASIL"][nome_uf][nome_cid] = []
                    for j in range(10):
                        base_final["BRASIL"][nome_uf][nome_cid].append({
                            "unidade": nomes_lojas[j],
                            "endereco": f"AV. PRINCIPAL, {random.randint(100, 999)}",
                            "cidade": nome_cid
                        })
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(base_final, f, indent=2, ensure_ascii=False)
            return base_final
        except Exception as e:
            self.atualizar_status_loading(f"ERRO CRÍTICO: MODO DE CONTINGÊNCIA ATIVO")
            return {"BRASIL": {"ERRO": {"CONEXÃO": []}}}

    def send_telegram_alert(self, loja_nome, cidade):
        key = f"{cidade}_{loja_nome}"
        self.status_cache[key] = {
            "status": "🚨 QUEDA TOTAL: AGUARDANDO TI LOCAL",
            "cor": "#FF0000"
        }
        self.after(0, self.renderizar_lista_lojas)

        try:
            markup = InlineKeyboardMarkup()
            btn_fix = InlineKeyboardButton("✅ REATIVAR UNIDADE", callback_data=f"fix|{cidade}|{loja_nome}")
            markup.add(btn_fix)

            msg = (f"🚨 *ALERTA DE INSTABILIDADE CRÍTICA*\n\n"
                   f"📍 *UNIDADE:* {loja_nome}\n"
                   f"🏙️ *CIDADE:* {cidade}\n"
                   f"❌ *STATUS:* QUEDA TOTAL DE HARDWARE\n"
                   f"🛠️ *AÇÃO:* INTERVENÇÃO FÍSICA NECESSÁRIA.")
            
            self.bot.send_message(self.chat_id, msg, parse_mode="Markdown", reply_markup=markup)
        except: pass

    def ouvir_bot(self):
        @self.bot.callback_query_handler(func=lambda call: call.data.startswith('fix|'))
        def callback_reativar(call):
            try:
                _, cidade, loja_nome = call.data.split('|')
                key = f"{cidade}_{loja_nome}"
                
                if key in self.lock_status:
                    self.lock_status.remove(key)
                    self.status_cache[key] = {"status": "Sistema Estável", "cor": "#00FF00"}
                    self.bot.answer_callback_query(call.id, "Reativando...")
                    self.bot.edit_message_text(f"✅ *UNIDADE REATIVADA:* {loja_nome}", 
                                              chat_id=call.message.chat.id, 
                                              message_id=call.message.message_id, 
                                              parse_mode="Markdown")
                    self.after(0, self.renderizar_lista_lojas)
            except: pass

        self.bot.polling(none_stop=True, timeout=60)

    def engine_status(self):
        while self.running:
            try:
                if self.cidade_atual:
                    uf, cidade = self.cidade_atual
                    for loja in self.infra["BRASIL"][uf][cidade]:
                        key = f"{cidade}_{loja['unidade']}"
                        
                        if key in self.lock_status:
                            self.status_cache[key] = {
                                "status": "🚨 QUEDA TOTAL: REPARO SOFTWARE IMPOSSÍVEL",
                                "cor": "#FF0000"
                            }
                        else:
                            if random.random() < 0.03:
                                self.lock_status.add(key)
                                self.send_telegram_alert(loja['unidade'], cidade)
                            else:
                                is_ok = random.random() > 0.10
                                self.status_cache[key] = {
                                    "status": "Sistema Estável" if is_ok else "EM MANUTENÇÃO AUTOMÁTICA",
                                    "cor": "#00FF00" if is_ok else "#FFFF00"
                                }
                    self.after(0, self.renderizar_lista_lojas)
            except: pass
            time.sleep(5)

    def setup_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=350, corner_radius=0, fg_color="#050505", border_width=1, border_color="#00FF00")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.sidebar, text="SENTINEL", font=("Courier New", 40, "bold"), text_color="#00FF00").pack(pady=(20, 0))
        self.lbl_loading = ctk.CTkLabel(self.sidebar, text="INICIALIZANDO...", font=("Consolas", 11), text_color="#008000")
        self.lbl_loading.pack(pady=5)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#050505", foreground="#00FF00", fieldbackground="#050505", borderwidth=0, font=("Consolas", 10))
        style.map("Treeview", background=[('selected', '#003300')], foreground=[('selected', '#00FF00')])

        self.tree = ttk.Treeview(self.sidebar, show="tree")
        self.tree.pack(fill="both", expand=True, padx=5, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.ao_selecionar_cidade)

        self.main_view = ctk.CTkScrollableFrame(self, fg_color="#000000", corner_radius=0)
        self.main_view.grid(row=0, column=1, sticky="nsew")
        
        self.msg_welcome = ctk.CTkLabel(self.main_view, text="> SELECIONE UF E CIDADE NO MENU", 
                                        font=("Consolas", 16), text_color="#003300")
        self.msg_welcome.pack(pady=400)

    def popular_tree(self):
        self.atualizar_status_loading("MONITORAMENTO ONLINE")
        root = self.tree.insert("", "end", text="BRASIL")
        for uf in sorted(self.infra["BRASIL"].keys()):
            id_uf = self.tree.insert(root, "end", text=uf)
            for cid in sorted(self.infra["BRASIL"][uf].keys()):
                self.tree.insert(id_uf, "end", text=cid)

    def atualizar_status_loading(self, texto):
        self.after(0, lambda: self.lbl_loading.configure(text=texto))

    def ao_selecionar_cidade(self, event):
        try:
            item = self.tree.selection()[0]
            texto = self.tree.item(item, "text")
            pai = self.tree.parent(item)
            if pai and self.tree.item(pai, "text") != "":
                self.cidade_atual = (self.tree.item(pai, "text"), texto)
                self.msg_welcome.pack_forget()
                self.renderizar_lista_lojas()
        except: pass

    def gerar_relatorio_queda(self):
        if not self.cidade_atual: return
        uf, cidade = self.cidade_atual
        nome_arquivo = f"RELATORIO_{cidade.replace(' ', '_')}.txt"
        try:
            with open(nome_arquivo, "w", encoding="utf-8") as f:
                f.write(f"SISTEMA SENTINEL - RELATÓRIO CRÍTICO\nCIDADE: {cidade}\n")
                for k, v in self.status_cache.items():
                    if cidade in k and v['cor'] == "#FF0000":
                        f.write(f"[FALHA] {k}\n")
            messagebox.showinfo("SENTINEL", f"Relatório Salvo: {nome_arquivo}")
        except: pass

    def renderizar_lista_lojas(self):
        if not self.cidade_atual: return
        uf, cidade = self.cidade_atual
        for child in self.main_view.winfo_children(): child.destroy()

        header = ctk.CTkFrame(self.main_view, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(20, 30))
        ctk.CTkLabel(header, text=f"// TERMINAL: {cidade}", font=("Consolas", 22, "bold"), text_color="#00FF00").pack(side="left")
        
        ctk.CTkButton(header, text="GERAR LOG DE ERROS", fg_color="#330000", text_color="#FF0000", 
                      command=self.gerar_relatorio_queda).pack(side="right")

        for loja in self.infra["BRASIL"][uf][cidade]:
            st = self.status_cache.get(f"{cidade}_{loja['unidade']}", {"status": "OPERACIONAL", "cor": "#00FF00"})
            
            bloco = (f"UNIDADE: {loja['unidade']}\n"
                     f"> ENDEREÇO: {loja['endereco']}\n"
                     f"> STATUS ATUAL: {st['status']}\n"
                     f"{'-'*100}")
            
            ctk.CTkLabel(self.main_view, text=bloco, font=("Consolas", 15), justify="left", text_color=st['cor']).pack(padx=30, anchor="w")

if __name__ == "__main__":
    app = SentinelFullPower()
    app.mainloop()
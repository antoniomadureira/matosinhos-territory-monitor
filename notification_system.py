"""
Sistema de Notificações e Relatórios Automáticos
Gera alertas e relatórios quando há atualizações nos dados
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

class NotificationSystem:
    """Sistema de notificações para o Matosinhos Monitor."""
    
    def __init__(self, config_file="config_notifications.json"):
        self.config_file = config_file
        self.config = self.load_config()
        self.alerts = []
    
    def load_config(self):
        """Carrega configuração de notificações."""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Configuração padrão
            default_config = {
                "enabled": True,
                "email": {
                    "enabled": False,
                    "smtp_server": "smtp.gmail.com",
                    "smtp_port": 587,
                    "sender": "noreply@cm-matosinhos.pt",
                    "recipients": ["admin@cm-matosinhos.pt"],
                    "username": "",
                    "password": ""
                },
                "slack": {
                    "enabled": False,
                    "webhook_url": ""
                },
                "thresholds": {
                    "critical": 20,  # % de desvio crítico
                    "warning": 10,   # % de desvio para aviso
                    "info": 5        # % de desvio informativo
                }
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2)
            
            return default_config
    
    def check_data_updates(self, old_data_file, new_data_file):
        """Verifica se houve atualizações nos dados."""
        if not os.path.exists(old_data_file):
            return None, None
        
        with open(old_data_file, 'r', encoding='utf-8') as f:
            old_data = json.load(f)
        
        with open(new_data_file, 'r', encoding='utf-8') as f:
            new_data = json.load(f)
        
        changes = self.detect_changes(old_data, new_data)
        
        return old_data, changes
    
    def detect_changes(self, old_data, new_data):
        """Detecta mudanças entre dois datasets."""
        changes = {
            "added": [],
            "removed": [],
            "modified": [],
            "significant": []
        }
        
        old_indicators = old_data.get('indicadores', {})
        new_indicators = new_data.get('indicadores', {})
        
        # Indicadores adicionados
        for key in new_indicators:
            if key not in old_indicators:
                changes["added"].append({
                    "indicator": key,
                    "value": new_indicators[key]['valor'],
                    "year": new_indicators[key]['ano']
                })
        
        # Indicadores removidos
        for key in old_indicators:
            if key not in new_indicators:
                changes["removed"].append({
                    "indicator": key,
                    "value": old_indicators[key]['valor'],
                    "year": old_indicators[key]['ano']
                })
        
        # Indicadores modificados
        for key in old_indicators:
            if key in new_indicators:
                old_val = old_indicators[key]['valor']
                new_val = new_indicators[key]['valor']
                
                if old_val != new_val:
                    # Tentar converter para numérico
                    try:
                        old_num = float(str(old_val).replace(' ', '').replace(',', '.'))
                        new_num = float(str(new_val).replace(' ', '').replace(',', '.'))
                        
                        change_pct = ((new_num - old_num) / old_num) * 100 if old_num != 0 else 0
                        
                        change_info = {
                            "indicator": key,
                            "old_value": old_val,
                            "new_value": new_val,
                            "change_pct": change_pct,
                            "year": new_indicators[key]['ano']
                        }
                        
                        changes["modified"].append(change_info)
                        
                        # Verificar se é mudança significativa
                        if abs(change_pct) >= self.config['thresholds']['warning']:
                            changes["significant"].append(change_info)
                    
                    except ValueError:
                        # Valores não numéricos
                        changes["modified"].append({
                            "indicator": key,
                            "old_value": old_val,
                            "new_value": new_val,
                            "change_pct": None,
                            "year": new_indicators[key]['ano']
                        })
        
        return changes
    
    def create_alert(self, level, message, details=None):
        """Cria um alerta."""
        alert = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message,
            "details": details
        }
        
        self.alerts.append(alert)
        
        return alert
    
    def generate_report(self, data_file="dados_ods.json", output_file="relatorio_ods.md"):
        """Gera relatório markdown dos dados ODS."""
        
        if not os.path.exists(data_file):
            return None
        
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        report = []
        report.append("# 📊 Relatório ODS - Matosinhos\n")
        report.append(f"**Data de Geração:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
        report.append(f"**Concelho:** {data['metadata']['concelho']}\n")
        report.append(f"**Fonte:** {data['metadata']['fonte']}\n\n")
        
        report.append("---\n\n")
        
        # Resumo Executivo
        report.append("## 📈 Resumo Executivo\n\n")
        
        total_ind = len(data['indicadores'])
        ods_com_dados = len([v for v in data['ods'].values() if v['indicadores']])
        
        report.append(f"- **Total de Indicadores:** {total_ind}\n")
        report.append(f"- **ODS com Dados:** {ods_com_dados} de 17\n")
        report.append(f"- **Cobertura:** {(ods_com_dados/17)*100:.1f}%\n\n")
        
        # Indicadores por ODS
        report.append("## 🎯 Indicadores por ODS\n\n")
        
        for ods_code, ods_info in data['ods'].items():
            if ods_info['indicadores']:
                report.append(f"### {ods_code} - {ods_info['nome']}\n\n")
                
                for ind in ods_info['indicadores']:
                    report.append(f"- **{ind['chave']}:** {ind['valor']} {ind['unidade']} ({ind['ano']})\n")
                
                report.append("\n")
        
        # Alertas
        if self.alerts:
            report.append("## 🚨 Alertas e Notificações\n\n")
            
            for alert in self.alerts:
                icon = {
                    "critical": "🔴",
                    "warning": "🟡",
                    "info": "🔵"
                }.get(alert['level'], "ℹ️")
                
                report.append(f"{icon} **{alert['level'].upper()}** - {alert['message']}\n")
                report.append(f"   *{alert['timestamp']}*\n\n")
        
        # Guardar relatório
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(''.join(report))
        
        print(f"✅ Relatório gerado: {output_file}")
        
        return output_file
    
    def send_email_notification(self, subject, body, attachments=None):
        """Envia notificação por email."""
        
        if not self.config['email']['enabled']:
            print("⚠️ Notificações por email desativadas")
            return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.config['email']['sender']
            msg['To'] = ', '.join(self.config['email']['recipients'])
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'html'))
            
            # Anexar ficheiros
            if attachments:
                for file_path in attachments:
                    if os.path.exists(file_path):
                        with open(file_path, 'rb') as f:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(f.read())
                            encoders.encode_base64(part)
                            part.add_header(
                                'Content-Disposition',
                                f'attachment; filename= {os.path.basename(file_path)}'
                            )
                            msg.attach(part)
            
            # Enviar
            server = smtplib.SMTP(
                self.config['email']['smtp_server'],
                self.config['email']['smtp_port']
            )
            server.starttls()
            server.login(
                self.config['email']['username'],
                self.config['email']['password']
            )
            
            server.send_message(msg)
            server.quit()
            
            print("✅ Email enviado com sucesso")
            return True
        
        except Exception as e:
            print(f"❌ Erro ao enviar email: {e}")
            return False
    
    def create_html_email(self, changes):
        """Cria email HTML formatado com as mudanças."""
        
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                          color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .alert-success {{ background: #d1fae5; border-left: 4px solid #10b981; 
                                 padding: 15px; margin: 10px 0; }}
                .alert-warning {{ background: #fef3c7; border-left: 4px solid #f59e0b; 
                                 padding: 15px; margin: 10px 0; }}
                .alert-danger {{ background: #fee2e2; border-left: 4px solid #ef4444; 
                                padding: 15px; margin: 10px 0; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
                th {{ background-color: #667eea; color: white; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📊 Matosinhos Territory Monitor</h1>
                <p>Atualização de Dados ODS</p>
            </div>
            
            <div class="content">
                <h2>Resumo das Alterações</h2>
                
                <p><strong>Data:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
        """
        
        if changes['added']:
            html += f"""
                <div class="alert-success">
                    <strong>✅ Novos Indicadores ({len(changes['added'])})</strong>
                    <ul>
            """
            for item in changes['added']:
                html += f"<li>{item['indicator']}: {item['value']} ({item['year']})</li>"
            html += "</ul></div>"
        
        if changes['significant']:
            html += f"""
                <div class="alert-warning">
                    <strong>⚠️ Mudanças Significativas ({len(changes['significant'])})</strong>
                    <table>
                        <tr>
                            <th>Indicador</th>
                            <th>Valor Anterior</th>
                            <th>Novo Valor</th>
                            <th>Variação</th>
                        </tr>
            """
            for item in changes['significant']:
                html += f"""
                    <tr>
                        <td>{item['indicator']}</td>
                        <td>{item['old_value']}</td>
                        <td>{item['new_value']}</td>
                        <td>{item['change_pct']:+.1f}%</td>
                    </tr>
                """
            html += "</table></div>"
        
        if changes['removed']:
            html += f"""
                <div class="alert-danger">
                    <strong>🗑️ Indicadores Removidos ({len(changes['removed'])})</strong>
                    <ul>
            """
            for item in changes['removed']:
                html += f"<li>{item['indicator']}</li>"
            html += "</ul></div>"
        
        html += """
                <p style="margin-top: 30px; color: #64748b; font-size: 0.9rem;">
                    Este é um email automático do Matosinhos Territory Monitor.<br>
                    Câmara Municipal de Matosinhos
                </p>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def run_daily_check(self):
        """Executa verificação diária e envia notificações se necessário."""
        
        print("🔄 Executando verificação diária...")
        
        # Verificar se há novos dados
        current_data = "dados_ods.json"
        backup_data = "dados_ods_backup.json"
        
        if not os.path.exists(current_data):
            print("⚠️ Ficheiro de dados não encontrado")
            return
        
        old_data, changes = self.check_data_updates(backup_data, current_data)
        
        if changes and any([changes['added'], changes['modified'], changes['removed']]):
            print("✅ Mudanças detectadas!")
            
            # Criar alertas
            if changes['significant']:
                for item in changes['significant']:
                    self.create_alert(
                        "warning" if abs(item['change_pct']) < 20 else "critical",
                        f"Mudança significativa em {item['indicator']}: {item['change_pct']:+.1f}%",
                        item
                    )
            
            # Gerar relatório
            report_file = self.generate_report()
            
            # Enviar notificação
            if self.config['email']['enabled']:
                html_body = self.create_html_email(changes)
                self.send_email_notification(
                    "📊 Atualização de Dados ODS - Matosinhos",
                    html_body,
                    attachments=[report_file] if report_file else None
                )
            
            # Fazer backup dos dados atuais
            import shutil
            shutil.copy(current_data, backup_data)
            print("✅ Backup atualizado")
        
        else:
            print("ℹ️ Sem mudanças detectadas")
    
    def export_alerts_log(self, output_file="alerts_log.json"):
        """Exporta log de alertas."""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.alerts, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Log de alertas exportado: {output_file}")


def main():
    """Função principal - executar verificação."""
    
    print("=" * 70)
    print("SISTEMA DE NOTIFICAÇÕES - MATOSINHOS MONITOR")
    print("=" * 70)
    
    notif_system = NotificationSystem()
    
    # Menu interativo
    print("\nEscolha uma opção:")
    print("1. Executar verificação diária")
    print("2. Gerar relatório manual")
    print("3. Testar notificação por email")
    print("4. Configurar sistema")
    
    choice = input("\nOpção (1-4): ").strip()
    
    if choice == "1":
        notif_system.run_daily_check()
    
    elif choice == "2":
        report_file = notif_system.generate_report()
        print(f"\n✅ Relatório gerado: {report_file}")
    
    elif choice == "3":
        print("\n⚠️ Para testar email, configure primeiro as credenciais em config_notifications.json")
        print("Depois ative email.enabled = true")
        
        if notif_system.config['email']['enabled']:
            test_html = """
            <html>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
                <h2 style="color: #667eea;">🧪 Email de Teste</h2>
                <p>Este é um email de teste do sistema de notificações.</p>
                <p>Se recebeu este email, o sistema está configurado corretamente!</p>
                <p style="color: #64748b; font-size: 0.9rem; margin-top: 30px;">
                    Matosinhos Territory Monitor<br>
                    Câmara Municipal de Matosinhos
                </p>
            </body>
            </html>
            """
            
            notif_system.send_email_notification(
                "🧪 Teste - Sistema de Notificações",
                test_html
            )
    
    elif choice == "4":
        print(f"\n📝 Edite o ficheiro: {notif_system.config_file}")
        print("Configure:")
        print("  - Email SMTP")
        print("  - Destinatários")
        print("  - Thresholds de alertas")
    
    print("\n" + "=" * 70)
    print("✅ CONCLUÍDO")
    print("=" * 70)


if __name__ == "__main__":
    main()

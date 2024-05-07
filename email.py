import tkinter as tk
import tkinter.messagebox as messagebox
import yfinance as yf
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def fetch_data(symbol):
    today = datetime.today()
    start_of_year = datetime(today.year, 1, 1)
    start_of_month = today - timedelta(days=30)
    data_ytd = yf.download(symbol, start=start_of_year, end=today)
    data_month = yf.download(symbol, start=start_of_month, end=today)
    latest = data_ytd.iloc[-1]
    first_ytd = data_ytd.iloc[0]
    first_month = data_month.iloc[0]
    previous = data_ytd.iloc[-2]
    close_price = latest['Close']
    daily_change = (latest['Close'] - previous['Close']) / previous['Close'] * 100
    monthly_change = (latest['Close'] - first_month['Close']) / first_month['Close'] * 100
    ytd_change = (latest['Close'] - first_ytd['Close']) / first_ytd['Close'] * 100
    return close_price, daily_change, monthly_change, ytd_change

def generate_chart(symbol, period, title, filename):
    data = yf.download(symbol, period=period)
    data['Close'].plot()
    plt.title(title)
    plt.savefig(filename)
    plt.close()

def get_news():
    with open('C:/Users/João Victor/Desktop/Email/noticias.txt', 'r', encoding='utf-8') as f:
        news = f.readlines()
    return news

def send_email(client_email, ibov_values, small_values, dolar_values, sp500_values):
    smtp_server = 'smtp.gmail.com'
    port = 587
    sender_email = ''
    password = ''
    with open('C:/Users/João Victor/Desktop/Email/config.txt', 'r') as f:
        sender_email = f.readline().strip()
        password = f.readline().strip()

    msg = MIMEMultipart()
    msg['From'] = 'João Victor - Assessor Exclusivo <' '>'
    msg['To'] = client_email
    msg['Subject'] = 'Fechamento de mercado e notícias - Assessoria Exclusiva l Toro Santander'

    ibov_close, ibov_daily, ibov_monthly, ibov_ytd = ibov_values
    small_close, small_daily, small_monthly, small_ytd = small_values
    dolar_close, dolar_daily, dolar_monthly, dolar_ytd = dolar_values
    sp500_close, sp500_daily, sp500_monthly, sp500_ytd = sp500_values

    ibov_close_formatted = "{:,.3f}".format(ibov_close).replace(',', '.').replace('.000', '')
    sp500_close_formatted = "{:,.0f}".format(sp500_close).replace(',', '.')

    body = f"""
    <p>Prezado(a) cliente,</p>
    <p><br></p>
    <p>Seguem os dados de fechamento do Ibovespa, Small Caps, Dólar e S&amp;P 500 de hoje e as notícias do dia:</p>
    <p><strong><br></strong><strong>IBOVESPA:</strong></p>
    <p>Fechamento do dia: {ibov_close_formatted}</p>
    <p>Variação diária: {ibov_daily:.2f}%</p>
    <p>Variação mensal: {ibov_monthly:.2f}%</p>
    <p>Variação no ano: {ibov_ytd:.2f}%</p>
    <p><strong><br></strong><strong>SMALL CAPS:</strong></p>
    <p>Fechamento do dia: {small_close:.2f}</p>
    <p>Variação diária: {small_daily:.2f}%</p>
    <p>Variação mensal: {small_monthly:.2f}%</p>
    <p>Variação no ano: {small_ytd:.2f}%</p>
    <p><strong><br></strong><strong>DÓLAR:</strong></p>
    <p>Cotação do dia: R${dolar_close:.2f}</p>
    <p>Variação diária: {dolar_daily:.2f}%</p>
    <p>Variação mensal: {dolar_monthly:.2f}%</p>
    <p>Variação no ano: {dolar_ytd:.2f}%</p>
    <p><strong><br></strong><strong>S&amp;P 500:</strong></p>
    <p>Fechamento do dia: {sp500_close_formatted}</p>
    <p>Variação diária: {sp500_daily:.2f}%</p>
    <p>Variação mensal: {sp500_monthly:.2f}%</p>
    <p>Variação no ano: {sp500_ytd:.2f}%</p>
    <p><br></p>
    <div style="text-align: center;"><span style="font-size: 28px;">&nbsp;</span><strong><span style="font-size: 28px;">Notícias do dia:</span></strong></div>
    """

    for line in get_news():
        line = line.strip()
        if line:
            link, headline = line.split(',', 1)
            body += f"<p><strong><br></strong><a href='{link}'><strong>{headline.strip()}</strong></a></p>\n"

    body += """
    <p><br><br><strong>Observa&ccedil;&atilde;o: Se n&atilde;o desejar mais receber estes e-mails, basta responder a esta mensagem solicitando a interrup&ccedil;&atilde;o do envio deste tipo de conte&uacute;do.</strong></p>
<p><br></p>
<p>Estou &agrave; disposi&ccedil;&atilde;o para quaisquer d&uacute;vidas!</p>
<p>--</p>
<p>Atenciosamente,&nbsp;</p>
<div><br>
    <table border="0" cellpadding="0" cellspacing="0" width="100%">
        <tbody>
            <tr>
                <td valign="middle" style="width: 24.0457%;"><a href="http://www.toroinvestimentos.com.br/" target="_blank"><img src="https://ci6.googleusercontent.com/proxy/32IaoPP9UI3u9pQUn-nBoSWqDawc5BwnFM92U4V3bu4xzkcNh71SdFD08cnSpF6fnvt5KH7FtUNBJTwCc3Wf_1cpx55CWzBE4gFMqecZKx6vEMimAxgZRRt8JvTQ8-FCvw=s0-d-e1-ft#https://cdn.toroinvestimentos.com.br/corretora/images/email/logo-principal.png" border="0" alt="Toro Investimentos"></a></td>
                <td width="auto" valign="middle" style="width: 75.8377%;">
                    <div>
                        <p><strong><span style="font-size: 26px; color: rgb(75, 0, 130);">Jo&atilde;o Victor</span></strong></p>
                        <p>Assessoria Exclusiva</p>
                        <p><br></p>
                        <p><u><a href="http://www.toroinvestimentos.com.br/" target="_blank"><span style="color: rgb(147, 101, 184);">toroinvestimentos.com.br</span></a></u></p>
                    </div>
                </td>
            </tr>
        </tbody>
    </table>
</div>
<table border="0" cellpadding="0" cellspacing="0">
    <tbody>
        <tr>
            <td><br></td>
            <td>
                <p><br></p>
            </td>
        </tr>
    </tbody>
</table>
<table border="0" cellpadding="0" cellspacing="0">
    <tbody>
        <tr>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
        </tr>
    </tbody>
</table>
    """

    msg.attach(MIMEText(body, 'html', 'utf-8'))

    generate_chart('^BVSP', '1y', 'Variação do Ibovespa nos últimos 12 meses', 'ibovespa.png')
    with open('ibovespa.png', 'rb') as f:
        img = MIMEImage(f.read())
    img.add_header('Content-Disposition', 'attachment', filename='ibovespa.png')
    msg.attach(img)

    generate_chart('SMAL11.SA', '1y', 'Variação do Small Caps nos últimos 12 meses', 'small.png')
    with open('small.png', 'rb') as f:
        img = MIMEImage(f.read())
    img.add_header('Content-Disposition', 'attachment', filename='small.png')
    msg.attach(img)

    generate_chart('USDBRL=X', '1y', 'Variação do Dólar nos últimos 12 meses', 'dolar.png')
    with open('dolar.png', 'rb') as f:
        img = MIMEImage(f.read())
    img.add_header('Content-Disposition', 'attachment', filename='dolar.png')
    msg.attach(img)

    generate_chart('^GSPC', '1y', 'Variação do S&P 500 nos últimos 12 meses', 'sp500.png')
    with open('sp500.png', 'rb') as f:
        img = MIMEImage(f.read())
    img.add_header('Content-Disposition', 'attachment', filename='sp500.png')
    msg.attach(img)

    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(sender_email, password)
        server.send_message(msg)

def execute_code():
    try:
        with open('C:/Users/João Victor/Desktop/Email/destinatarios.txt', 'r') as f:
            client_emails = [email.strip() for email in f.readlines()]
        ibov_values = fetch_data('^BVSP')
        small_values = fetch_data('SMAL11.SA')
        dolar_values = fetch_data('USDBRL=X')
        sp500_values = fetch_data('^GSPC')
        for client_email in client_emails:
            send_email(client_email, ibov_values, small_values, dolar_values, sp500_values)
        messagebox.showinfo('Sucesso', 'O código foi executado com sucesso.')
    except Exception as e:
        messagebox.showerror('Erro', f'Ocorreu um erro ao executar o código:\n\n{str(e)}')

#CRIAR A JANELA PRINCIPAL (INTERFACE)
window = tk.Tk()
window.title('Executar Código')
window.geometry('300x100')

# BOTAO PARA EXECUTAR O CÓDIGO
button = tk.Button(window, text='Executar', command=execute_code)
button.pack(pady=20)

# LOOP DA INTERFACE GRÁFICA
window.mainloop()

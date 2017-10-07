################################################
##### PROGRAMADO POR: LEANDRO L. MONTANARI #####
################################################

# Importações
from urllib.error import HTTPError
from webbrowser import open as abrirurl
import urllib.request
import json
import isodate
import time
import os
import sys

instrucoes_iniciais1 = 'Insira a sua YouTube Data API v3 (se não souber como conseguir uma, digite "ajuda" sem as aspas e pressione Enter): '
instrucoes_iniciais2 = 'Insira a sua YouTube Data API v3: '
inst_help = 'Para conseguir a sua YouTube Data API v3, acesse: https://developers.google.com/youtube/registering_an_application?hl=pt-br\n'
inp_api = str(input(instrucoes_iniciais1)).strip()
print('')
fmt_ia = inp_api.strip().lower().replace('"', '')

if fmt_ia == 'ajuda':
    print(inst_help)
    abrirurl('https://developers.google.com/youtube/registering_an_application?hl=pt-br')
    inp_api = str(input(instrucoes_iniciais2)).strip()
    print('')
    
while True:

    # Listas que serão utilizada para armazenar os dados dos vídeos obtidos
    lista_de_videos = []
    duracao_dos_videos = []
    titulo_dos_videos = []

    # Variáveis de contagem e de controle posterior
    repeticoes = 0
    contagem = 0
    seguir_adiante = "n"
    salvar_log = "n"
    continuar_log = "n"

    # Instruções e variáveis necessárias para obter os resultados na API do YouTube
    instrucoes_do_input = 'Digite o usuário ou ID do canal que deseja somar. Por exemplo, "portadosfundos" ou "UCEWHPFNilsT0IfQfutVzsag" para o canal do Porta dos Fundos: '
    instrucoes_do_log = 'Deseja salvar um log dos resultados em texto? Digite "S" para sim ou "N" para não: '
    ytb = "https://www.youtube.com/watch?v="
    api_key = inp_api
    res = 50

    # Função de remover caracteres inválidos em caso de entrada errada do usuário
    def RemYT(yt_url):
        removererro1 = yt_url.replace('http://','')
        removererro2 = removererro1.replace('https://','')
        removererro3 = removererro2.replace('www.youtube.com/','')
        removererro4 = removererro3.replace('youtube.com/','')
        removererro5 = removererro4.replace('user/','')
        removererro6 = removererro5.replace('channel/','')
        removererro7 = removererro6.replace('/videos','')
        removererro8 = removererro7.replace('"','')
        yt_url = removererro8
        return yt_url

    while seguir_adiante == "n":

        # Solicitação de entrada do usuário
        usuario = input('%s' % (instrucoes_do_input))

        # Usuário já sem os caracteres inválidos
        usuario = RemYT(usuario)

        # Verifica se o usuário inseriu o "User ID" ou o "Channel ID" direto
        if usuario[0] == "U" and usuario[1] == "C" and len(usuario) == 24:
            
            # O usuário inseriu um "Channel ID"

            id_canal = usuario
            lista_id = []

            for cada_caractere in id_canal:
                lista_id.append(cada_caractere)

            lista_id[1] = "U"
            pl_up_can = "".join(lista_id)
            segunda_url = ("https://www.googleapis.com/youtube/v3/playlistItems?part=snippet,contentDetails&key=%s&maxResults=%s&playlistId=%s" % (api_key,res,pl_up_can))

            try:
                with urllib.request.urlopen(segunda_url, timeout=60) as url:
                    resultado = json.loads(url.read().decode())

                    seguir_adiante = "s"

            except HTTPError as e1:
                if e1.code == 400:
                    print("")
                    print("Sua YouTube Data API v3 é inválida!\n")
                    print(inst_help)
                    api_key = str(input('Digite uma YouTube Data API v3 válida: '))
                    print("")
                else:
                    print("")
                    print("ID de canal inexistente!")
                    print("")
            
            
        else:
            
            # O usuário inseriu um "User ID"

            url_base = ("https://www.googleapis.com/youtube/v3/channels?part=contentDetails&key=%s&maxResults=%s&forUsername=%s" % (api_key,res,usuario))

            try:
                with urllib.request.urlopen(url_base, timeout=60) as url:
                    data = json.loads(url.read().decode())
                    controle_item = len(data["items"])

                    if controle_item == 0:
                        print("")
                        print("Usuário inexistente!")
                        print("")
                        
                    else:
                        id_canal = data["items"][0]["id"]
                        pl_up_can = data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

                        seguir_adiante = "s"
            except HTTPError as e2:
                if e2.code == 400:
                    print("")
                    print("Sua YouTube Data API v3 é inválida!\n")
                    print(inst_help)
                    api_key = str(input('Digite uma YouTube Data API v3 válida: '))
                    print("")
                else:
                    print("")
                    print("Erro HTTP {}!".format(e2.code))
                    print("")

    while True:
        print('')
        salvar_log = input('%s' % (instrucoes_do_log)).lower()

        if salvar_log in ('s', 'n', '"s"', '"n"'):
            break
        print('')
        print('Resposta inválida!')

    # Começa a rotina
    segunda_url = ("https://www.googleapis.com/youtube/v3/playlistItems?part=snippet,contentDetails&key=%s&maxResults=%s&playlistId=%s" % (api_key,res,pl_up_can))

    with urllib.request.urlopen(segunda_url, timeout=60) as url:
        resultado = json.loads(url.read().decode())

        nome_do_canal = resultado["items"][0]["snippet"]["channelTitle"]

        if usuario[0] == "U" and usuario[1] == "C" and len(usuario) == 24:
            print('')
            print('Carregando vídeos do canal "%s" (ID: %s)...' % (nome_do_canal,usuario))
            print('')

            if salvar_log == 's' or salvar_log == '"s"':
                nome_do_log = "Log de "+nome_do_canal+" (ID = "+usuario+").txt"
                texto = open(nome_do_log, "w", encoding="utf-8")

                texto.write(nome_do_canal)
                texto.write("\n\n")
                
                continuar_log = "s"
            
        else:
            print('')
            print('Carregando vídeos do canal "%s" (%s)...' % (nome_do_canal,usuario))
            print('')

            if salvar_log == 's' or salvar_log == '"s"':
                nome_do_log = "Log de "+nome_do_canal+" ("+usuario+").txt"
                texto = open(nome_do_log, "w", encoding="utf-8")

                texto.write(nome_do_canal)
                texto.write("\n\n")
                
                continuar_log = "s"

        total_de_videos = resultado["pageInfo"]["totalResults"]
        paginas_necessarias = int(total_de_videos/res)
        
        qts_videos = len(resultado["items"])

        for i in range(0,qts_videos):
            if resultado["items"][i]["kind"] == "youtube#playlistItem":
                id_video = resultado["items"][i]["contentDetails"]["videoId"]
                lista_de_videos.append(id_video)

    if total_de_videos > 50:
        token = resultado["nextPageToken"]
        while repeticoes < paginas_necessarias:
            
            repeticoes += 1
            proxima_url = ("https://www.googleapis.com/youtube/v3/playlistItems?part=snippet,contentDetails&key=%s&maxResults=%s&playlistId=%s&pageToken=%s" % (api_key,res,pl_up_can,token))


            with urllib.request.urlopen(proxima_url, timeout=60) as url:
                novo_resultado = json.loads(url.read().decode())
                
                qts_videos = len(novo_resultado["items"])

                for n in range(0,qts_videos):
                    if novo_resultado["items"][n]["kind"] == "youtube#playlistItem":
                        id_video = novo_resultado["items"][n]["contentDetails"]["videoId"]
                        lista_de_videos.append(id_video)

                if qts_videos >= 50:
                    token = novo_resultado["nextPageToken"]


    # Obtenção dos dados dos vídeos

    videos_encontrados = len(lista_de_videos)
    soma_parcial = 0
    soma_total = 0

    if videos_encontrados != 1:
        
        log_videos = ("%s Vídeos Encontrados" % (videos_encontrados))
        print(log_videos)
        
        if continuar_log == "s":
            texto.write(log_videos)
            texto.write("\n\n")
            
    else:
        log_videos = ("%s Vídeo Encontrado" % (videos_encontrados))
        print(log_videos)

        if continuar_log == "s":
            texto.write(log_videos)
            texto.write("\n\n")

    print("")
    print("Listando...")
    print("")
    print("----------")

    if continuar_log == "s":
        texto.write("----------")

    def tempo(t_secs):
        try:
            val = int(t_secs)
        except ValueError:
            return "Erro! O valor inserido não é um número inteiro."
        pos = abs( int(t_secs) )
        day = pos / (3600*24)
        rem = pos % (3600*24)
        hour = rem / 3600
        rem = rem % 3600
        mins = rem / 60
        secs = rem % 60

        if int(day) != 1:
            txt_dia = "Dias"
        else:
            txt_dia = "Dia"

        if int(hour) != 1:
            txt_hora = "Horas"
        else:
            txt_hora = "Hora"

        if int(mins) != 1:
            txt_minuto = "Minutos"
        else:
            txt_minuto = "Minuto"

        if int(secs) != 1:
            txt_segundo = "Segundos"
        else:
            txt_segundo = "Segundo"
        
        res = '%03d %s, %02d %s, %02d %s e %02d %s' % (day, txt_dia, hour, txt_hora, mins, txt_minuto, secs, txt_segundo)
        if int(t_secs) < 0:
            res = "-%s" % res
        return res

    def conv_dur(d_secs):
        try:
            d_val = int(d_secs)
        except ValueError:
            return "Erro! O valor inserido não é um número inteiro."
        d_pos = abs( int(d_secs) )
        d_day = d_pos / (3600*24)
        d_rem = d_pos % (3600*24)
        d_hour = d_rem / 3600
        d_rem = d_rem % 3600
        d_mins = d_rem / 60
        d_secs = d_rem % 60
        
        d_res = '%03d:%02d:%02d:%02d' % (d_day, d_hour, d_mins, d_secs)
        if int(d_secs) < 0:
            d_res = "-%s" % d_res
        return d_res

    for t in lista_de_videos:

        try:
            
            url_ytb = ("https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails&key=%s&id=%s" % (api_key,t))

            ytb_completo = ytb+t

            with urllib.request.urlopen(url_ytb, timeout=60) as url:
                parametros = json.loads(url.read().decode())

            ytb_duracao = parametros["items"][0]["contentDetails"]["duration"]
            ytb_titulo = parametros["items" ][0]["snippet"]["title"]
            
            duracao_dos_videos.append(ytb_duracao)
            titulo_dos_videos.append(ytb_titulo)
            
            contagem += 1

            duracao_em_segundos = isodate.parse_duration(duracao_dos_videos[contagem-1]).seconds
            duracao_formatada = conv_dur(duracao_em_segundos)

            print("")

            if continuar_log == "s":
                texto.write("\n\n")
            
            if contagem < 10:
                linha1 = ("#00%s - %s - %s" % (contagem,titulo_dos_videos[contagem-1],ytb_completo))
                print(linha1)
                
                if continuar_log == "s":
                    texto.write(linha1)
                    texto.write("\n")
            elif contagem < 100:
                linha1 = ("#0%s - %s - %s" % (contagem,titulo_dos_videos[contagem-1],ytb_completo))
                print(linha1)
                
                if continuar_log == "s":
                    texto.write(linha1)
                    texto.write("\n")
            else:
                linha1 = ("#%s - %s - %s" % (contagem,titulo_dos_videos[contagem-1],ytb_completo))
                print(linha1)
                
                if continuar_log == "s":
                    texto.write(linha1)
                    texto.write("\n")

            linha2 = ("DURAÇÃO (DDD:HH:MM:SS): %s" % (duracao_formatada))
            print(linha2)
            soma_parcial += duracao_em_segundos
            sp_formatada = tempo(soma_parcial)
            linha3 = ("SOMA PARCIAL: %s" % (sp_formatada))
            print(linha3)

            print("")
            print("----------")

            if continuar_log == "s":
                texto.write(linha2)
                texto.write("\n")
                texto.write(linha3)
                texto.write("\n\n")
                texto.write("----------")

        except (KeyboardInterrupt, SystemExit):
            print("")
            print("Operação cancelada!")
            print("")
            print("----------")
            raise SystemExit

    soma_total = soma_parcial
    st_formatada = tempo(soma_total)
    
    media_por_video = soma_total / videos_encontrados
    med_formatada = tempo(media_por_video)

    print("")
    linha4 = ("MÉDIA POR VIDEO: %s" % (med_formatada))
    print(linha4)
    print("")
    linhafinal = ("SOMA TOTAL: %s" % (st_formatada))
    print(linhafinal)
    print("")
    print("----------")

    if continuar_log == "s":
        texto.write("\n\n")
        texto.write(linha4)
        texto.write("\n\n")
        texto.write(linhafinal)
        texto.write("\n\n")
        texto.write("----------")
        texto.close()

    while True:
        print("")
        reiniciar = input('Deseja inserir outro canal? Digite "S" para sim ou "N" para não: ').lower()
        print("")

        if reiniciar in ('s', 'n', '"s"', '"n"'):
            break
        print('Resposta inválida!')
        
    if reiniciar == 's' or reiniciar == '"s"':
        continue
    else:
        sys.exit(0)
        break

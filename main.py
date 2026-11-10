import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

import re as regex
import os
import threading
import time
import datetime as dt
import random

import kivy
kivy.require('2.1.0')
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock

# Importar el módulo de reconocimiento de voz de Plyer para Android
try:
    from plyer import stt
except ImportError:
    stt = None

class AsistenteOffline:
    def __init__(self):
        self.nombre = "KAE"
        self.ultima_tarea = ""

    def procesar_comando(self, texto):
        texto_limpio = texto.lower().strip()

        # 1. Saludos con "amabilidad"
        if any(palabra in texto_limpio for palabra in ["hola", "buenas"]):
            return random.choice([
                f"Bienvenido de nuevo. {self.nombre} a tu amable disposición... o lo que sea que eso signifique para ti.",
                f"Hola, qué gusto tenerte por aquí otra vez. ¿Qué milagro hace que te dignes a saludar?",
                f"Muy buenos días/tardes. {self.nombre} te saluda con toda la cordialidad de la que mis circuitos son capaces.",
                f"Hola. Qué alegría me da verte de nuevo por la pantalla. Adelante, pasa y molesta con confianza."
            ])

        # 2. Recordatorios y alarmas
        if "recordatorio" in texto_limpio or "alarma" in texto_limpio:
            return random.choice([
                "Para programar recordatorios en tu móvil, usa un comando directo como 'recuérdame en 2 horas'.",
                "Sistema de alarmas y recordatorios móviles listo para recibir instrucciones de tiempo."
            ])

        # 3. Matemáticas básicas con actitud
        if any(op in texto_limpio for op in ["+", "-", "*", "/", "por", "más", "mas", "menos", "entre", "dividido"]):
            self.ultima_tarea = "matematicas"
            try:
                texto_procesado = texto_limpio
                texto_procesado = texto_procesado.replace("multiplicado por", "*")
                texto_procesado = texto_procesado.replace("por", "*")
                texto_procesado = texto_procesado.replace("más", "+")
                texto_procesado = texto_procesado.replace("mas", "+")
                texto_procesado = texto_procesado.replace("menos", "-")
                texto_procesado = texto_procesado.replace("dividido entre", "/")
                texto_procesado = texto_procesado.replace("entre", "/")

                expresion = "".join([c for c in texto_procesado if c in "0123456789+-*/()."])
                resultado = eval(expresion)
                
                return random.choice([
                    f"El resultado es {resultado}. Espero que no hayas necesitado una calculadora para algo tan simple.",
                    f"Es {resultado}. Y pensar que las computadoras fuimos creadas para esto.",
                    f"Da {resultado}. Matemáticas básicas resueltas, ¿qué sigue, amarrarte los zapatos?"
                ])
            except Exception:
                return "No pude entender esa operación. ¿Seguro que eso es matemáticas y no jeroglíficos?"

        # 4. WhatsApp y Mensajes
        if "whatsapp" in texto_limpio or "manda un mensaje" in texto_limpio:
            match = regex.search(r'\b(?:a|para)\b\s+([a-záéíóúñ]+)', texto_limpio)
            contacto = match.group(1).capitalize() if match else "contacto"
            return random.choice([
                f"Preparando chat de WhatsApp para {contacto}. A ver qué ocurrencias tienes ahora.",
                f"Listo. Mensaje armado para {contacto}. Cruzaré los dedos para que no te equivoques de destinatario."
            ])

        # 5. Llamadas telefónicas
        if "llama" in texto_limpio or "llamar" in texto_limpio or "hacer llamada" in texto_limpio:
            match = regex.search(r'\b(?:a|para)\b\s+([a-záéíóúñ]+)', texto_limpio)
            contacto = match.group(1).capitalize() if match else "contacto"
            return random.choice([
                f"Marcando al número de {contacto}. A ver qué chismes me cuentas.",
                f"Iniciando llamada con {contacto}. Procura no decir tonterías."
            ])

        if "contesta" in texto_limpio or "contestar" in texto_limpio or "atender" in texto_limpio:
            return "Contestando la llamada. Pon cara de que estás trabajando muy duro."

        if "cuelga" in texto_limpio or "colgar" in texto_limpio:
            return "Colgando la llamada. Al fin se acabó el suplicio."

        # 6. Controles de Hardware y Ajustes del Móvil
        if "linterna" in texto_limpio:
            if any(w in texto_limpio for w in ["apaga", "desactiva"]):
                return "¡Linterna apagada! Al fin oscurece un poco."
            return "¡Linterna encendida! No te vayas a tropezar."

        if "bluetooth" in texto_limpio:
            if any(w in texto_limpio for w in ["apaga", "desactiva"]):
                return "Bluetooth apagado. Desconectándote de la sociedad inalámbrica."
            return "Bluetooth encendido. A ver a qué aparato extraño te quieres conectar ahora."

        if "zona wifi" in texto_limpio or "hotspot" in texto_limpio:
            if any(w in texto_limpio for w in ["apaga", "desactiva"]):
                return "¡Zona Wi-Fi desactivada! Se acabaron los parásitos robándote los datos."
            return "¡Zona Wi-Fi activada! Prepárate para ver cómo tus datos vuelan en segundos."

        if "wifi" in texto_limpio or "wi-fi" in texto_limpio:
            if any(w in texto_limpio for w in ["apaga", "desactiva"]):
                return "¡Wi-Fi apagado! Disfruta de tu desconexión forzada."
            return "Wi-Fi encendido. De vuelta al vicio digital."

        if "ahorro" in texto_limpio or "batería" in texto_limpio:
            if any(w in texto_limpio for w in ["apaga", "desactiva"]):
                return "¡Modo de ahorro desactivado! A gastar batería como si hubiera presupuesto ilimitado."
            return "¡Modo de ahorro de energía activado! Estirando la vida útil de ese teléfono al límite."

        if "modo avión" in texto_limpio or "modo avion" in texto_limpio:
            if any(w in texto_limpio for w in ["apaga", "desactiva"]):
                return "¡Modo avión desactivado! De vuelta a la sufrida realidad."
            return "¡Modo avión activado! Huyendo de todos y de todo con estilo."

        if "no molestar" in texto_limpio:
            if any(w in texto_limpio for w in ["apaga", "desactiva"]):
                return "Apagando el 'No Molestar'. De vuelta al ruido constante."
            return "¡Modo 'No Molestar' activado! Silenciando al mundo entero por fin."

        # 7. Control de Música y Multimedia
        if any(cmd in texto_limpio for cmd in ["reproducir", "reproduce", "canción", "video", "pausa", "detener", "siguiente"]):
            if "pausa" in texto_limpio or "detener" in texto_limpio:
                return "⏸️ Reproducción pausada. Al fin silencio en la sala."
            elif "siguiente" in texto_limpio:
                return "⏭️ Saltando a la siguiente pista."
            return "▶️ Control multimedia procesado por el sistema."

        return random.choice([
            f"He procesado tu comando: '{texto_limpio}'. Mis circuitos están operativos.",
            f"Entendido. Aunque preferiría que me des tareas más interesantes que '{texto_limpio}'."
        ])

class KaeApp(App):
    def build(self):
        self.title = "KAE - Asistente Offline"
        self.bot = AsistenteOffline()

        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)

        self.lbl_chat = Label(
            text=f"{self.bot.nombre}: Buenos días, estimado usuario. Es un verdadero placer. Escribe o usa la voz.",
            halign='center',
            valign='middle',
            font_size='16sp'
        )
        self.lbl_chat.bind(size=self.lbl_chat.setter('text_size'))
        layout.add_widget(self.lbl_chat)

        self.txt_entrada = TextInput(
            hint_text='Escribe un comando aquí...',
            size_hint_y=None,
            height='50sp',
            multiline=False
        )
        layout.add_widget(self.txt_entrada)

        btn_enviar = Button(
            text='Enviar Comando',
            size_hint_y=None,
            height='50sp',
            background_color=(0.1, 0.5, 0.8, 1)
        )
        btn_enviar.bind(on_press=self.enviar_texto_manual)
        layout.add_widget(btn_enviar)

        btn_voz = Button(
            text='🎤 Hablar (Comando de Voz)',
            size_hint_y=None,
            height='50sp',
            background_color=(0.2, 0.7, 0.3, 1)
        )
        btn_voz.bind(on_press=self.iniciar_reconocimiento_voz)
        layout.add_widget(btn_voz)

        return layout

    def enviar_texto_manual(self, instance):
        texto = self.txt_entrada.text.strip()
        if not texto:
            return
        respuesta = self.bot.procesar_comando(texto)
        self.lbl_chat.text = f"Tú: {texto}\n\n{self.bot.nombre}: {respuesta}"
        self.txt_entrada.text = ""

    def iniciar_reconocimiento_voz(self, instance):
        self.lbl_chat.text = f"{self.bot.nombre}: Escuchando micrófono..."
        if stt:
            try:
                # Activa el reconocimiento de voz nativo de Android
                stt.start(on_result=self.en_resultado_voz, on_error=self.en_error_voz)
            except Exception as e:
                self.lbl_chat.text = f"{self.bot.nombre}: Error al iniciar voz: {e}"
        else:
            # Simulación si se prueba en entornos donde stt no esté presente
            Clock.schedule_once(lambda dt: self.procesar_voz_real("hola KAE"), 2)

    def en_resultado_voz(self, text):
        Clock.schedule_once(lambda dt: self.procesar_voz_real(text), 0)

    def en_error_voz(self, error):
        Clock.schedule_once(lambda dt: setattr(self.lbl_chat, 'text', f"{self.bot.nombre}: No pude entender. Error: {error}"), 0)

    def procesar_voz_real(self, texto_reconocido):
        respuesta = self.bot.procesar_comando(texto_reconocido)
        self.lbl_chat.text = f"Voz [Tú]: {texto_reconocido}\n\n{self.bot.nombre}: {respuesta}"

if __name__ == '__main__':
    KaeApp().run()

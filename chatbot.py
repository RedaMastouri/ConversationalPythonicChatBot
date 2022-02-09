from flask import Flask, request
import requests
from waitress import serve
from twilio.twiml.messaging_response import MessagingResponse
from pyngrok import ngrok

#Gunicorn
#from gunicorn.app.wsgiapp import run

#Flask app
app = Flask(__name__)

#Ngrok tunneling
#http_tunnel = ngrok.connect()
#ssh_tunnel = ngrok.connect(22, "tcp")


#Webservices
@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    if 'quote' in incoming_msg:
        # return a quote
        r = requests.get('https://api.quotable.io/random')
        if r.status_code == 200:
            data = r.json()
            quote = f'{data["content"]} ({data["author"]})'
        else:
            quote = 'I could not retrieve a quote at this time, sorry.'
        msg.body(quote)
        responded = True
    if 'cat' in incoming_msg:
        # return a cat pic
        msg.media('https://cataas.com/cat')
        responded = True
    if not responded:
        msg.body('I only know about famous quotes and cats, sorry!')
    return str(resp)



# This is the main function
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug = True)
    
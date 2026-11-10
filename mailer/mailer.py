import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'notification-mailer'}), 200

@app.route('/send-ticket', methods=['POST'])
def send_ticket():
    data = request.get_json(silent=True) or {}
    recipient = data.get('recipient_email', 'unknown')
    name = data.get('recipient_name', 'Visitor')
    event = data.get('event_title', 'Event')
    
    print(f"[NOTIFICATION SERVICE] Сгенерирован и отправлен билет участнику {name} ({recipient}) на событие '{event}'", flush=True)
    return jsonify({
        'status': 'sent',
        'recipient': recipient,
        'event': event
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

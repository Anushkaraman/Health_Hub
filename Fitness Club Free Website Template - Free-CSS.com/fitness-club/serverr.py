from flask import Flask, jsonify, request, send_file
import matplotlib.pyplot as plt
import io

app = Flask(__name__)

# In-memory data store for simplicity (replace with database in production)
data = {
    "progress": [0] * 20
}

@app.route('/progress', methods=['GET'])
def get_progress():
    return jsonify(data['progress'])

@app.route('/progress', methods=['POST'])
def update_progress():
    day = request.json.get('day')
    index = request.json.get('index')
    data['progress'][day] |= (1 << index)
    return jsonify(data['progress'])

def generate_chart(total_progress, daily_progress):
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))

    # Total Progress Chart
    total_completed = sum(1 for x in total_progress if x == 15)
    total_remaining = len(total_progress) - total_completed
    axs[0].pie([total_completed, total_remaining], labels=['Completed', 'Remaining'], autopct='%1.1f%%', colors=['#4caf50', '#f44336'])
    axs[0].set_title('Total Progress')

    # Daily Progress Chart
    daily_watched = bin(daily_progress).count('1')
    daily_remaining = 4 - daily_watched
    axs[1].pie([daily_watched, daily_remaining], labels=['Watched', 'Remaining'], autopct='%1.1f%%', colors=['#4caf50', '#f44336'])
    axs[1].set_title('Daily Progress')

    # Save it to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    return buf

@app.route('/chart/total', methods=['GET'])
def get_total_chart():
    buf = generate_chart(data['progress'], sum(data['progress']))
    return send_file(buf, mimetype='image/png')

@app.route('/chart/daily', methods=['GET'])
def get_daily_chart():
    today = int(request.args.get('day', 0))
    buf = generate_chart(data['progress'], data['progress'][today])
    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)

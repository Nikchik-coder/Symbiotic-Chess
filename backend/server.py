from flask import Flask, jsonify, request
from flask_cors import CORS
from game import SymbioticChessGame

app = Flask(__name__)
CORS(app)  # This will allow the frontend to make requests to this server

game = SymbioticChessGame()

def piece_to_dict(piece):
    if piece is None:
        return None
    return {
        'piece_type': piece.piece_type,
        'color': piece.color,
        'combined_pieces': piece.combined_pieces,
        'display_info': piece.get_display_info()
    }

def board_to_json(board):
    json_board = []
    for row in board:
        json_row = [piece_to_dict(p) for p in row]
        json_board.append(json_row)
    return json_board

@app.route('/state', methods=['GET'])
def get_state():
    return jsonify({
        'board': board_to_json(game.board),
        'current_turn': game.current_turn,
        'merge_count': game.merge_count,
        'last_move': game.last_move,
        'captured_pieces': {
            'white': [piece_to_dict(p) for p in game.captured_pieces['white']],
            'black': [piece_to_dict(p) for p in game.captured_pieces['black']]
        },
        'status_message': game.status_message
    })

@app.route('/move', methods=['POST'])
def move():
    data = request.json
    start_pos, end_pos = game.parse_move(data['move'])
    
    if start_pos is None:
        game.status_message = "Invalid move format."
    elif game.is_valid_move(start_pos, end_pos):
        game.move_piece(start_pos, end_pos)
        game.switch_turn()
    else:
        game.status_message = "Invalid move."
        
    return jsonify({'status': 'ok'})


@app.route('/merge', methods=['POST'])
def merge():
    data = request.json
    pos1, _ = game.parse_move(f"{data['pos1']}a1")
    pos2, _ = game.parse_move(f"{data['pos2']}a1")
    game.attempt_merge(pos1, pos2)
    return jsonify({'status': 'ok'})

@app.route('/disintegrate', methods=['POST'])
def disintegrate():
    data = request.json
    pos, _ = game.parse_move(f"{data['pos']}a1")
    target_pos, _ = game.parse_move(f"{data['target_pos']}a1")
    game.attempt_disintegrate(pos, target_pos)
    return jsonify({'status': 'ok'})

@app.route('/reset', methods=['POST'])
def reset():
    global game
    game = SymbioticChessGame()
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True)

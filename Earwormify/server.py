from flask import Flask, render_template, request, redirect, url_for
from waitress import serve
import spotipy_call

app = Flask(__name__)
app.config['SECRET_KEY'] = 'baosejralsdordpamz'

sp_auth = spotipy_call.sp_auth
client = spotipy_call.client

@app.route('/')
@app.route('/index')
def index():
    if not sp_auth.validate_token(spotipy_call.cache_handler.get_cached_token()):
        
        return redirect(sp_auth.get_authorize_url())
    return redirect(url_for('home_page'))


@app.route('/')
@app.route('/home_page')
def home_page():
    return render_template("playlist2.html", 
                    title=client.current_user()['display_name'],
                    )

@app.route('/get_playlist', methods = ['POST'])
def get_playlist():
    #artist_list = spotipy_call.get_top_artists()
    #new_playlist = spotipy_call.create_playlist()
    #sort_method = request.form['sort_method']
    if request.method == 'POST':
        sort_method = request.form.get('sort_method')
    else:
        sort_method = 'popularity'
    song_list = spotipy_call.sort_songs("genre")
     
    return render_template("playlist2.html", 
                    title=client.current_user()['display_name'], 
                    sorted_songs=song_list
                    )



@app.route('/callback')
def callback():
    sp_auth.get_access_token(request.args['code'])
    return redirect(url_for('home_page')) 



if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8080)

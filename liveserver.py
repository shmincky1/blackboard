import flask
import multiprocessing
import blackboard
import shutil

def run_liveserver(args, dispatcher):
	app = flask.Flask(__name__)
	app.register_blueprint(flask.Blueprint('server_viz', __name__, static_url_path='/sv', static_folder='server_viz'))
	app.register_blueprint(flask.Blueprint('out', __name__, static_url_path='/out', static_folder='out'))
	app.register_blueprint(flask.Blueprint('statecache', __name__, static_url_path='/sc', static_folder='statecache'))
	addr=args.address
	if ":" not in addr:
		addr+=":5000"
	addr=addr.split(":")
	multiprocessing.Process(target=app.run, args=(addr[0], int(addr[1]))).start()
	statebuffer=[]
	statebuffer.extend(blackboard.STATES)
	stopwords=blackboard.process_stopwords(args.stopwords)
	while 1:
		i=0
		iterstates=[]
		while i<int(args.states_per_cycle):
			iterstates.append(statebuffer.pop())
			if len(statebuffer)==0:
				statebuffer.extend(blackboard.STATES)
			i+=1
		blackboard.CacheBuilder(iterstates, dispatcher, args.simple_monitor, args.datasource, True, True, args.no_state_name, stopwords, args.q).run()
		blackboard.MapBuilder(iterstates, 'dummy', False, "integrated.png", args.simple_monitor, args.q).run()
		shutil.copy("integrated.png", "server_viz/integrated.png")
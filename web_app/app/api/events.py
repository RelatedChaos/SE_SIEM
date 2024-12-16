from app.api import bp

@bp.rooute('/events', methods = ['GET'])
def get_events(q):
    pass

@bp.rooute('/events', methods = ['POST'])
def post_events(event):
    pass


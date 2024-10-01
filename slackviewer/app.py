import os

import flask


app = flask.Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

app.data = app.app_ctx_globals_class()

@app.route("/channel/<name>/")
def channel_name(name):
    messages = app.data.channels[name]
    channels = list(app.data.channels.keys())
    groups = list(app.data.groups.keys()) if app.data.groups else {}
    dm_users = list(app.data.dm_users)
    mpim_users = list(app.data.mpim_users)

    return flask.render_template("viewer.html", messages=messages,
                                 name=name.format(name=name),
                                 channels=sorted(channels),
                                 groups=sorted(groups) if groups else {},
                                 dm_users=dm_users,
                                 mpim_users=mpim_users,
                                 no_sidebar=app.no_sidebar,
                                 no_external_references=app.no_external_references)

def send_file(name, attachment):
    try_path = os.path.join(app.data.path, name, "attachments", attachment)
    if os.path.exists(try_path):
        return flask.send_file(try_path)
    return flask.send_file(os.path.join(app.data.path, "attachments", attachment))

@app.route("/channel/<name>/attachments/<attachment>")
def channel_name_attachment(name, attachment):
    return send_file(name, attachment)


@app.route("/group/<name>/")
def group_name(name):
    messages = app.data.groups[name]
    channels = list(app.data.channels.keys())
    groups = list(app.data.groups.keys())
    dm_users = list(app.data.dm_users)
    mpim_users = list(app.data.mpim_users)

    return flask.render_template("viewer.html", messages=messages,
                                 name=name.format(name=name),
                                 channels=sorted(channels),
                                 groups=sorted(groups),
                                 dm_users=dm_users,
                                 mpim_users=mpim_users,
                                 no_sidebar=app.no_sidebar,
                                 no_external_references=app.no_external_references)


@app.route("/group/<name>/attachments/<attachment>")
def group_name_attachment(name, attachment):
    return send_file(name, attachment)


@app.route("/dm/<id>/")
def dm_id(id):
    messages = app.data.dms[id]
    channels = list(app.data.channels.keys())
    groups = list(app.data.groups.keys())
    dm_users = list(app.data.dm_users)
    mpim_users = list(app.data.mpim_users)

    return flask.render_template("viewer.html", messages=messages,
                                 id=id.format(id=id),
                                 channels=sorted(channels),
                                 groups=sorted(groups),
                                 dm_users=dm_users,
                                 mpim_users=mpim_users,
                                 no_sidebar=app.no_sidebar,
                                 no_external_references=app.no_external_references)


@app.route("/dm/<name>/attachments/<attachment>")
def dm_name_attachment(name, attachment):
    return send_file(name, attachment)


@app.route("/mpim/<name>/")
def mpim_name(name):
    messages = app.data.mpims.get(name, list())
    channels = list(app.data.channels.keys())
    groups = list(app.data.groups.keys())
    dm_users = list(app.data.dm_users)
    mpim_users = list(app.data.mpim_users)

    return flask.render_template("viewer.html", messages=messages,
                                 name=name.format(name=name),
                                 channels=sorted(channels),
                                 groups=sorted(groups),
                                 dm_users=dm_users,
                                 mpim_users=mpim_users,
                                 no_sidebar=app.no_sidebar,
                                 no_external_references=app.no_external_references)


@app.route("/mpim/<name>/attachments/<attachment>")
def mpim_name_attachment(name, attachment):
    return send_file(name, attachment)


@app.route("/")
def index():
    channels = list(app.data.channels.keys())
    groups = list(app.data.groups.keys())
    dms = list(app.data.dms.keys())
    mpims = list(app.data.mpims.keys())
    if channels:
        if "general" in channels:
            return channel_name("general")
        else:
            return channel_name(channels[0])
    elif groups:
        return group_name(groups[0])
    elif dms:
        return dm_id(dms[0])
    elif mpims:
        return mpim_name(mpims[0])
    else:
        return "No content was found in your export that we could render."

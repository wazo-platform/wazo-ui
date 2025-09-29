var socket = null;
var started = false;
var btn_loading = null;

$(document).ready(function() {
    btn_loading = Ladda.create(document.querySelector('.ladda-button'));
    search_plugins();
});

function connect(host, port, prefix, token) {
    if (socket != null) {
        console.log("socket already connected");
        return;
    }

    if (!host) {
        host = window.location.host;
    }

    var ws_url = "wss://" + host + ":" + port + prefix + "/?token=" + token;
    socket = new WebSocket(ws_url);
    socket.onclose = function(event) {
        socket = null;
        console.log("websocketd closed with code " + event.code + " and reason '" + event.reason + "'");
    };
    socket.onmessage = function(event) {
        if (started) {
            var payload = JSON.parse(event.data);
            if (payload.data.status == 'completed') {
                console.log('Time to reload webi');
                location.reload();
            }
            return;
        }

        var msg = JSON.parse(event.data);
        switch (msg.op) {
            case "init":
                subscribe("plugin_install_progress");
                subscribe("plugin_uninstall_progress");
                start();
                break;
            case "start":
                started = true;
                console.log("waiting for messages");
                break;
        }
    };
    started = false;
}

function subscribe(event_name) {
    var msg = {
        op: "subscribe",
        data: {
          event_name: event_name
        }
    };
    socket.send(JSON.stringify(msg));
};

function start() {
    var msg = {
        op: "start"
    };
    socket.send(JSON.stringify(msg));
}

$(document).on('click', ".btn-remove-plugin", function() {
  let namespace = $(this).attr("data-namespace");
  let name = $(this).attr("data-name");

  let body = {
    namespace: namespace,
    name: name,
  }

  let remove_url = $(this).attr("data-remove-url");
  remove_plugin.call(this, remove_url, body);
});

$(document).on('click', ".btn-install-plugin", function() {
  let namespace = $(this).attr("data-namespace");
  let name = $(this).attr("data-name");

  let body = {
    method: 'market',
    options: {
      namespace: namespace,
      name: name,
    },
  }

  let install_url = $(this).attr("data-install-url");
  install_plugin.call(this, install_url, body);
});

$(document).on('click', ".btn-upgrade-plugin", function() {
  let namespace = $(this).attr("data-namespace");
  let name = $(this).attr("data-name");
  let version = $(this).attr("data-version");

  let body = {
    method: 'market',
    options: {
      namespace: namespace,
      name: name,
      version: version,
    },
  }

  let upgrade_url = $(this).attr("data-upgrade-url");
  install_plugin.call(this, upgrade_url, body);
});

$(document).on('click', ".btn-git-install-plugin", function() {
  let url = $('#git-url-to-install').val();
  let branch = $('#git-branch-tag').val();
  let options = ((branch) ? {ref: branch} : {});

  if (url) {
    let body = {
      url: url,
      method: 'git',
      options: options
    }

    install_url = $(this).attr("data-install-url");
    install_plugin(install_url, body, from_git=true);
  }
});

$('#search_plugin').on('change', function() {
  search_plugins();
});

$('#installed_plugin').on('change', function() {
  search_plugins();
});

$('#show_only_official').on('change', function() {
  search_plugins();
});

function search_plugins() {
  let term = $('#search_plugin').val();
  let official = $('#show_only_official').is(':checked');
  let installed = $('#installed_plugin').val();
  let search_url = $('#search_plugin').attr("data-search-url");

  let body = {}
  if (term) {
    body.search = term;
  }
  if (official) {
    body.namespace = 'official';
  }
  if (installed) {
    if (installed === 'installed') {
      body.installed = true;
    } else if (installed === 'not_installed') {
      body.installed = false;
    }
  }

  call_ajax_plugin(search_url, callback_search, body);
}

function remove_plugin(remove_url, body) {
  res = confirm('Are you sure you want to remove this plugin?');
  if (res == true) {
    launch_remove_plugin.call(this, remove_url, body);
  }
}

function install_plugin(install_url, body, from_git=false) {
  res = confirm('Are you sure you want to install this plugin?');
  if (res == true) {
    if (from_git) {
      btn_loading.start();
    }
    launch_install_plugin.call(this, install_url, body);
  }
}

function launch_install_plugin(install_url, body) {
  $(this).closest('.plugin-container').find('.overlay').removeClass('hidden');
  call_ajax_plugin(install_url, callback_install, body);
}

function launch_remove_plugin(remove_url, body) {
  $(this).closest('.plugin-container').find('.overlay').removeClass('hidden');
  call_ajax_plugin(remove_url, callback_remove, body);
}

function callback_install(data) {
}

function callback_remove(data) {
}

function callback_search(data) {
  $('#plugins').html(data);
}

function callback_filter(data) {
  $('#plugins').html(data);
}

function call_ajax_plugin(url, callback, body) {
  $.ajax({
    url: url,
    type: 'POST',
    contentType: 'application/json',
    data: JSON.stringify(body),
    success: function(data) {
      callback(data);
    },
    error: function(data) {
      setTimeout(function() {
        console.log('There is some error, please reload');
        location.reload();
      }, 4000);
    }
  });
}

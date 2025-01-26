// NOTE: you may have to run this after onload
(async () => {
  let Dispatcher, lookupAsset, lookupApp, apps = {};
  let token = "TOKENHERE"
  if (!token) {
    console.error('Failed to retrieve token');
    return;
  }

  const ws = new WebSocket('ws://127.0.0.1:1997'); // connect to arRPC bridge websocket

  ws.onmessage = async (event) => {
    let msg;
    try {
      msg = JSON.parse(event.data);
    } catch (error) {
      console.error('Failed to parse WebSocket message:', error);
      return;
    }

    if (!Dispatcher) {
      let wpRequire;
      window.webpackChunkdiscord_app.push([[Symbol()], {}, (x) => (wpRequire = x)]);
      window.webpackChunkdiscord_app.pop();

      const modules = wpRequire.c;

      for (const id in modules) {
        const mod = modules[id]?.exports;

        for (const prop in mod) {
          const candidate = mod[prop];
          try {
            if (candidate && candidate.register && candidate.wait) {
              Dispatcher = candidate;
              break;
            }
          } catch {
            continue;
          }
        }

        if (Dispatcher) break;
      }
    }

    if (!Dispatcher) {
      console.error('Failed to find Dispatcher');
      return;
    }

    async function lookupApp(id) {
      try {
        const authHeaders = new Headers({ Authorization: token });
        const response = await fetch(`https://discord.com/api/v9/applications/${id}`, { headers: authHeaders });
        return await response.json();
      } catch (error) {
        console.error('Failed to fetch app data:', error);
        return null;
      }
    }

    async function lookupAsset(id, descriptor) {
      try {
        const authHeaders = new Headers({ Authorization: token });
        const uploadHeaders = new Headers({
          Authorization: token,
          'Content-Type': 'application/json',
        });

        const isUrl = (string) => {
          try {
            new URL(string);
            return true;
          } catch {
            return false;
          }
        };

        if (isUrl(descriptor)) {
          const response = await fetch(`https://discord.com/api/v9/applications/${id}/external-assets`, {
            method: 'POST',
            headers: uploadHeaders,
            body: JSON.stringify({ urls: [descriptor] }),
          });

          const data = await response.json();
          return `mp:${data[0]?.external_asset_path}`;
        }

        const response = await fetch(`https://discord.com/api/v9/oauth2/applications/${id}/assets?nocache=true`, {
          headers: authHeaders,
        });

        const data = await response.json();
        const asset = data.find((item) => item.name === descriptor);
        return asset?.id || null;
      } catch (error) {
        console.error('Failed to fetch asset data:', error);
        return null;
      }
    }

    if (msg.activity) {
      const { application_id: appId, assets } = msg.activity;

      if (assets?.large_image) {
        msg.activity.assets.large_image = await lookupAsset(appId, assets.large_image);
      }

      if (assets?.small_image) {
        msg.activity.assets.small_image = await lookupAsset(appId, assets.small_image);
      }

      if (!apps[appId]) {
        apps[appId] = await lookupApp(appId);
      }

      const app = apps[appId];
      if (app && !msg.activity.name) {
        msg.activity.name = app.name;
      }

      Dispatcher.dispatch({ type: 'LOCAL_ACTIVITY_UPDATE', ...msg }); // set RPC status
      console.log("RPC Dispatched")
    }
  };
})();

<template>
    <BContainer fluid class="bv-example-row">
        <BRow>
            <BCol>
<div style="display: flex;"> 
    <img :src="PresenceStore.songimg" :alt="PresenceStore.songalt" style="border-radius: 0.5%;" height=430px width=430px>    
    &nbsp;
    &nbsp;
    &nbsp;
    &nbsp;
    &nbsp;
    <div>
    <h2 style="color: white;">{{ PresenceStore.devicename }}</h2>
    <h4 style="color: white;">{{ PresenceStore.songname }}</h4>
    <BTable show-empty :items="PresenceStore.play_history" style="" :fields="songs_field" :table-class="'table-dark .th-lg'" responsive>
        <template #cell(songimg)="row">
            <img :alt="row.item.songname" :src="row.value" style="width: 70px; height: 70px;">
        </template>
        <template #cell(songname)="row">
            {{row.value}} 
        </template>
        <template #cell(artistname)="row">
            {{row.value}}
        </template>
       
        <template v-slot:empty>
            <h1 style="font-style: bold; color: white;">No songs played yet!</h1>
        </template>
        
    </BTable>
    </div>
</div>
</BCol>
</BRow>
</BContainer>
</template>

<script setup>
import "../assets/main.css"

import { usePresenceStore } from '/src/stores/PresenceStore.ts';
const PresenceStore = usePresenceStore();

const songs_field = [
    { key: 'songimg', label: 'Cover Art' },
    { key: 'songname', label: 'Song Name' },
    { key: 'artistname', label: 'Artist' },
]


let userid = ''
        userid = await fetch('/api/userid')
        PresenceStore.setUID(await userid.text())

let appid = ''
        appid = await fetch('/api/appid')
        PresenceStore.setAID(await appid.text())

let webSocket = new WebSocket("wss://api.lanyard.rest/socket");

function reconnectWss() {
    clearInterval(PresenceStore.heartbeat_timer)
    webSocket = new WebSocket("wss://api.lanyard.rest/socket");
}

webSocket.onclose = (event) => {
  reconnectWss()
}

webSocket.onmessage = async (event) => {
    const data = JSON.parse(event.data);
    if (data.op === 1) {
        let ht_int = data["d"]["heartbeat_interval"];
        let htid = setInterval(() => {
           try {
            webSocket.send(
                JSON.stringify({
                    op: 3,
                })
            );
            console.log("Heartbeat sent");
           } catch {
             reconnectWss()
           }
        }, ht_int - 100);
        PresenceStore.setHeartbeatTimer(htid)
        console.log("Connected to Lanyard API")
        webSocket.send(
                JSON.stringify({
                    op: 2,
                    d: {
                        subscribe_to_id: PresenceStore.user_id,
                    }
                })
        )
    }
    if (data.op === 0) {
        let pre = data.d
        let pre2 = pre["activities"]
        let real = {}

        let trip = false

        for(let search in pre2){
            if(!trip) {
            if(pre2[search].application_id === PresenceStore.app_id){
                real = pre2[search]
                trip = true
            }
        }
        }

        try {
        let songimg = real["assets"]["large_image"]
        if(songimg.substr(0,3) == "mp:") {
            let whole = songimg.length
            songimg = songimg.substr(3, whole)
            songimg = "https://media.discordapp.net/" + songimg
        } else {
            songimg = "https://cdn.discordapp.com/app-assets/" + PresenceStore.app_id + "/" + songimg + ".png"
        }
        let songname = real["state"]
        let devicename = real["details"]
        PresenceStore.setPresence(songimg, songname, devicename);
        console.log("Presence Updated");
        let quickc = await fetch('/api/prevsong')
        let hist = await quickc.json()
        hist.pop()
        hist.pop()
        PresenceStore.setHistory(hist)
        
        } catch (error) {
            console.log(error);
        }
}
}
</script>

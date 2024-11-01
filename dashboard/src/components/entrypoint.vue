<template>
    <BContainer fluid class="bv-example-row">
        <BRow>
            <BCol>
    <BCard
  :title="PresenceStore.songname"
  :img-src="PresenceStore.songimg"
  :img-alt="PresenceStore.songname"
  style="max-width: 20rem; position: center; background-color: black; color: white;"
>
  <BCardText>
    {{  PresenceStore.devicename }}
  </BCardText>
</BCard>
</BCol>
<BCol>
    <h1 style="font-style: bold; color: white; font-size: 20px;">Previous songs (up to 4)</h1>
    <BTable show-empty :items="PresenceStore.play_history" style="" :fields="songs_field" :table-class="'table-dark .th-lg'" responsive>
        <template #cell(songimg)="row">
            <img :src="row.value" style="width: 70px; height: 70px;">
        </template>
        <template #cell(songname)="row">
            {{row.value}} 
        </template>
        <template #cell(artistname)="row">
            {{row.value}}
        </template>
        <template #cell(devicename)="row">
             {{row.value}}
        </template>
        <template v-slot:empty>
            <h1 style="font-style: bold; color: white;">No songs played yet!</h1>
        </template>
        
    </BTable>
</BCol>
</BRow>
</BContainer>
</template>

<script setup>
import { usePresenceStore } from '/src/stores/PresenceStore.ts';
const PresenceStore = usePresenceStore();

const webSocket = new WebSocket("wss://api.lanyard.rest/socket");

const songs_field = [
    { key: 'songimg', label: 'Cover Art' },
    { key: 'songname', label: 'Song Name' },
    { key: 'artistname', label: 'Artist' },
    { key: 'devicename', label: 'Device' },
]

let play_history = await fetch('/api/prevsong')
PresenceStore.setHistory(await play_history.json())



webSocket.onmessage = async (event) => {
    const data = JSON.parse(event.data);
    if (data.op === 1) {
        let ht_int = data["d"]["heartbeat_interval"];
        setInterval(() => {
            webSocket.send(
                JSON.stringify({
                    op: 3,
                })
            );
            console.log("Heartbeat sent");
        }, ht_int - 100);
        console.log("Connected to Lanyard API");
        let userid = ''
        userid = await fetch('/api/userid')
        userid = await userid.text()
        webSocket.send(
                JSON.stringify({
                    op: 2,
                    d: {
                        subscribe_to_id: userid,
                    }
                })
        )
    }
    if (data.op === 0) {
        let pre = data.d
        let pre2 = pre["activities"]
        let real = {}

        let appid = ''
        appid = await fetch('/api/appid')
        appid = await appid.text()

        let trip = false

        for(let search in pre2){
            if(!trip) {
            if(pre2[search].application_id === appid){
                real = pre2[search]
            }
            trip = true
        }
        }

        try {
        let songimg = real["assets"]["large_image"]
        if(songimg.substr(0,3) == "mp:") {
            let whole = songimg.length
            songimg = songimg.substr(3, whole)
            songimg = "https://media.discordapp.net/" + songimg
        } else {
            songimg = "https://cdn.discordapp.com/app-assets/" + appid + "/" + songimg + ".png"
        }
        let songname = real["state"]
        let devicename = real["details"]
        PresenceStore.setPresence(songimg, devicename, songname);
        console.log("Presence Updated");
        let quickc = await fetch('/api/prevsong')
        PresenceStore.setHistory(await quickc.json())
        
        } catch (error) {
            console.log(error);
        }
}
}
</script>
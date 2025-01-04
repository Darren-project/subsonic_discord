
import { defineStore } from 'pinia'
export const usePresenceStore = defineStore('Presence', {
    state: () => ({ songimg: 0, songname: '', devicename: '', history: [], uid: "", aid: "", heartbeat_timer_id: 0 }),
    getters: {
      img: (state) => state.songimg,
      name: (state) => state.songname,
      device: (state) => state.devicename,
      play_history: (state) => state.history,
      user_id: (state) => state.uid,
      app_id: (state) => state.aid,
      heartbeat_timer: (state) => state.heartbeat_timer_id
    },
    actions: {
        setPresence(songimg: number, songname: string, devicename: string) {
            this.songimg = songimg
            this.songname = songname
            this.devicename = devicename
        },
        setHistory(history: Object) {
            for(let item in history) {
                 let real = history[item]
                 if (real["artistname"].length > 15) {
                    real["artistname"] = real["artistname"].substr(0, 15) + " ..."
                 }
            }
            this.history = history
        },
        setUID(uid: String) {
            this.uid = uid
        },
        setAID(aid: String) {
            this.aid = aid
        },
        setHeartbeatTimer(ht: Number) {
          this.heartbeat_timer_id  = ht
        }
    },
  })

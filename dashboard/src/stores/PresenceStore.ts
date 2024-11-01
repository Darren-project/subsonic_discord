
import { defineStore } from 'pinia'
export const usePresenceStore = defineStore('Presence', {
    state: () => ({ songimg: 0, songname: '', devicename: '', history: [] }),
    getters: {
      img: (state) => state.songimg,
      name: (state) => state.songname,
      device: (state) => state.devicename,
      play_history: (state) => state.history
    },
    actions: {
        setPresence(songimg: number, songname: string, devicename: string) {
            this.songimg = songimg
            this.songname = songname
            this.devicename = devicename
        },
        setHistory(history: any) {
            this.history = history
        }
    },
  })
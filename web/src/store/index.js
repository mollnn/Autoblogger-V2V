import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    index:0,
    vlink:"http://clips.vorwaerts-gmbh.de/big_buck_bunny.mp4",
    objlist : [],
    posterlist:[],
    videolist:[],
    value3:'',
    value4:'',
    isloading: true,
  },
  getters:{

  },
  mutations: {
  },
  actions: {
  },
  modules: {
  }
})
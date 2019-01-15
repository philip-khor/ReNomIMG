<template>
  <component-frame :width-weight="6" :height-weight="4">
    <template slot="header-slot">
      Train Progress
    </template>
    <div id="component-progress-model-num">
      <div id="model-bar-legend">
        <div id="total-num">
          Total Models : {{ getFilteredModelList.length }}
        </div>
        <div id="legend">
          <div id="legend-item" v-for="alg in getAlgorithList()">
            <div id="legend-box" :class="getColorClass(alg.id)">
            </div>
            <div id="legend-title">
              {{alg.title}}
            </div>
          </div>
        </div>
      </div>
      <div id="model-bar" v-if="this.getFilteredModelList.length != 0"
        @mouseenter="onHovering=true" @mouseleave="onHovering=false">
        <section v-for="model in reduceModelList(this.getFilteredModelList)" :style="getStyle(model)">
          <transition name="fade">
            <div v-if="onHovering">
                {{ model[2] }}
            </div>
          </transition>
        </section>
      </div>
      <div id="model-bar" v-else>
        <section id="green" style="width: 100%">No Model</section>
      </div>
      <div id="component-progress" class="scrollbar-container">
        <div id="progress-title">
          Running Progress
        </div>
        <div id="progress-bars">
          <progress-bar :isTitle="true" v-if="getRunningModelList.length > 0"/>
          <progress-bar v-for="item in getRunningModelList" :model="item"/>
        </div>
      </div>
    </div>
  </component-frame>
</template>

<script>

import { mapGetters } from 'vuex'
import { RUNNING_STATE, ALGORITHM, TASK_ID } from '@/const.js'
import ComponentFrame from '@/components/common/component_frame.vue'
import ProgressBar from '@/components/page/train_page/progress_bar.vue'

export default {
  name: 'ComponentProgress',
  components: {
    'component-frame': ComponentFrame,
    'progress-bar': ProgressBar
  },
  data: function () {
    return {
      onHovering: false
    }
  },
  computed: {
    ...mapGetters([
      'getRunningModelList',
      'getFilteredModelList',
      'getAlgorithmTitleFromId',
      'getAlgorithmColor',
      'getCurrentTask',
    ]),
  },
  created: function () {
    window.addEventListener('resize', this.draw, false)
  },
  methods: {
    reduceModelList: function (model_list) {
      model_list = Object.entries(model_list.reduce(
        function (algs, model) {
          const id = model.algorithm_id
          if (id in algs) {
            algs[id] += 1
          } else {
            algs[id] = 1
          }
          return algs
        }, {})).map(d => [d[0], parseFloat(d[1]) / parseFloat(model_list.length), d[1]])
      return model_list
    },
    getStyle: function (model_info) {
      return {
        'width': model_info[1] * 100 + '%',
        'background-color': this.getAlgorithmColor(model_info[0])
      }
    },
    getAlgorithList: function () {
      const task = this.getCurrentTask
      let arr
      if (task === TASK_ID.CLASSIFICATION) {
        arr = Object.values(ALGORITHM.CLASSIFICATION)
      } else if (task === TASK_ID.DETECTION) {
        arr = Object.values(ALGORITHM.DETECTION)
      } else if (task === TASK_ID.SEGMENTATION) {
        arr = Object.values(ALGORITHM.SEGMENTATION)
      }
      return arr.map(d => { return {title: d.title, key: d.key, id: d.id} })
    },
    getColorClass: function (alg_id) {
      const id = alg_id % 10
      return 'color-' + id
    }
  }
}
</script>

<style lang='scss' scoped>
#component-progress-model-num {
  width: 100%;
  height: 100%;
  display: flex;
  flex-wrap: wrap;
  padding-left: $total-model-padding-left-right;
  padding-right: $total-model-padding-left-right;
  #model-bar-legend {
    width: 100%;
    height: 30%;
    #total-num {
      width: 100%;    
      height: 80%;
      display: flex;
      align-items: flex-end;
      padding-bottom: $total-model-title-padding-bottom;
      color: $component-font-color-title;
    }
    #legend {
      width: 100%;
      height: 20%;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: flex-end;
      #legend-item {
        height: 100%;
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        margin-left: $total-model-legend-item-margin-left;
        #legend-box {
          width: $total-model-legend-box-width;
          height: $total-model-legend-box-width;
        }
        #legend-title {
          font-size: $component-font-size-small;
          margin-left: $total-model-legend-box-margin-left;
        }
      }
    }
  }
  #model-bar {
  	width: 100%;
  	height: 7%;
    display: flex;
  	overflow: hidden;
    section {
      height: 100%;
    	min-width: 10%;
      line-height: 30px;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-wrap: wrap;
      color: white;
      #alg-title {
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        height: 55%;
      }
      #alg-num {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 45%;
        width: 100%;
      }
    }
    section:last-of-type {
      flex: auto;
    }
  }
  #component-progress {
    width: 100%;
    height: calc(63% - #{$progress-bar-area-margin-top});
    overflow: auto;
    line-height: auto;
    margin-top: $progress-bar-area-margin-top;
    #progress-title {
      width: 100%;
      margin-bottom: $total-model-title-padding-bottom;
      color: $component-font-color-title;
      #progress-bars {
        width: 100%;
      }
    }
  }
  #green {
    background: #65d260;
  }
}
</style>
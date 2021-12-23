<template>
    <form class="container card position-absolute top-0" style="width:18rem; left:3rem" novalidate>
        <div class="fs-5">Select Algorithm<fas class="iconAlgos" icon="robot"/></div>
        <!-- LOAD IF SORTING PROJECT -->
        <div v-if="url === 'sorting'" class="btn-group is-invalid" role="group" aria-label="Basic radio toggle button group">
            <input v-model="settings.algorithm.name" type="radio" class="btn-check form-check-input" name="algoGroup" value="selectionSort" id="selectionSort">
            <label class="btn btn-outline-primary" for="selectionSort">Selectionsort</label>

            <input v-model="settings.algorithm.name" type="radio" class="btn-check form-check-input" name="algoGroup" value="quickSort" id="quickSort">
            <label class="btn btn-outline-primary" for="quickSort">Quicksort</label>
        </div>
        <div v-if="v$.settings.algorithm.name.$invalid && v$.settings.$dirty && url === 'sorting'" class="invalid-feedback">You must select an algorithm!</div>
        <!-- LOAD IF PATHING PROJECT -->
        <div v-if="url === 'pathfinding'" class="btn-group is-invalid" role="group" aria-label="Basic radio toggle button group">
            <input v-model="settings.algorithm.name" type="radio" class="btn-check form-check-input" name="algoGroup" value="Dijkstra" id="Dijkstra">
            <label class="btn btn-outline-primary" for="Dijkstra">Dijkstra</label>

            <input v-model="settings.algorithm.name" type="radio" class="btn-check form-check-input" name="algoGroup" value="aStar" id="aStar">
            <label class="btn btn-outline-primary" for="aStar">A-Star</label>
        </div>
        <div v-if="v$.settings.algorithm.name.$invalid && v$.settings.$dirty && url === 'pathfinding'" class="invalid-feedback">You must select an algorithm!</div>
        <br>
        <div class="fs-5">Select Speed<fas class="iconSpeed" icon="tachometer-alt"/></div>
        <div class="btn-group" role="group" aria-label="Basic radio toggle button group">
            <input v-model="settings.speed" type="radio" class="btn-check form-check-input" name="speedGroup" value="1.0" id="speedOption1">
            <label class="btn btn-outline-primary" for="speedOption1">1.0 x</label>

            <input v-model="settings.speed" type="radio" class="btn-check form-check-input" name="speedGroup" value="0.66" id="speedOption2">
            <label class="btn btn-outline-primary" for="speedOption2">0.6 x</label>

            <input v-model="settings.speed" type="radio" class="btn-check form-check-input" name="speedGroup" value="0.33" id="speedOption3">
            <label class="btn btn-outline-primary" for="speedOption3">0.3 x</label>
        </div>
        <br>

        <div class="fs-5">Select Cells</div>
        <div class="btn-group" role="group" aria-label="Basic radio toggle button group">
            <input type="radio" class="btn-check form-check-input" name="cursorGroup" value="start" id="cursorOption1">
            <label class="btn btn-outline-primary" for="cursorOption1">start</label>

            <input type="radio" class="btn-check form-check-input" name="cursorGroup" value="target" id="cursorOption2">
            <label class="btn btn-outline-primary" for="cursorOption2">target</label>

            <input type="radio" class="btn-check form-check-input" name="cursorGroup" value="bomb" id="cursorOption3">
            <label class="btn btn-outline-primary" for="cursorOption3">obstacle</label>
        </div>

        <div v-if="v$.settings.speed.$invalid && v$.settings.$dirty" class="invalid-feedback">You must select a speed level!</div>
        <br>
        <button @click.prevent="reset" type="submit" class="btn btn-outline-danger">Reset <fas icon="power-off"/></button>
        <br>
        <button @click.prevent="start" type="submit" class="btn btn-outline-success">Start <fas icon="play"/></button>
        <br>
        <div class="d-flex align-items-center">
            <div>Runtime: {{ timer.value }}</div>
            <div v-if="timer.instance" class="spinner-border spinner-border-sm ms-auto" role="status" aria-hidden="true"></div>
        </div>
        <br>
    </form>
    <Sorting v-if="url === 'sorting'" ref="sorting"/>
    <Pathfinding v-else-if="url === 'pathfinding'" ref="pathfinding"/>

</template>

<script>
import useVuelidate from "@vuelidate/core"
import { required } from "@vuelidate/validators"

export default {
    data() {
        return {
            v$: useVuelidate(),
            url: window.location.href.substr(window.location.href.lastIndexOf("/") + 1), // get last part of url to load different elements.,
            settings: {
                algorithm: {
                    name: "",
                    running: false
                },
                speed: ""
            },
            timer: {
                instance: null,
                value: "0.000"
            }
        }
    },
    validations() {
        return {
            settings: {
                algorithm: {
                    name: { required }
                },
                speed: {
                    required
                }
            }
        }
    },
    methods: {
        start: async function() {

            this.v$.$validate()

            if (!this.v$.$error) {
                clearInterval(this.timer.instance)
                this.timer.instance = null
                this.startTimer()

                switch(this.url) {
                    case "sorting":

                        if (this.$refs.sorting.playfield.running || this.$refs.sorting.playfield.isSorted) {
                            this.$refs.sorting.createPlayfield()
                        }

                        switch(this.settings.algorithm.name) {

                            case "selectionSort":
                                await this.$refs.sorting.startSelectionSort(this.settings.speed)
                                break

                            case "quickSort":
                                await this.$refs.sorting.startQuickSort(this.settings.speed)
                                break
                        }
                        break

                    case "pathfinding":
                        this.$refs.pathfinding.hi()
                        break
                
                    default:
                        throw "url path is doomed, please reload."
                }
            }
        },
        reset: function() {

            var radioButtons = document.getElementsByTagName("input")

            for (var button of radioButtons) {
                button.checked = false
            }

            this.settings.algorithm.name = ""
            this.settings.algorithm.running = false
            this.settings.speed = ""
            clearInterval(this.timer.instance)
            this.timer.instance = null
            this.timer.value = "0.000"

            switch(this.url) {
                case "sorting":
                    this.$refs.sorting.createPlayfield()
                    break
                
                case "pathfinding":
                    this.$refs.pathfinding.createPlayfield()
            }
        },
        startTimer: function() {

            var startTime = (new Date()).getTime()
            var passedTime;
            this.settings.algorithm.running = true

            this.timer.instance = setInterval(() => {

                if (!this.$refs.sorting && !this.$refs.pathfinding) {
                    clearInterval(this.timer.instance)
                    this.timer.instance = null
                    return
                }

                switch(this.url) {
                    
                    case "sorting":

                        if (this.settings.algorithm.running && !this.$refs.sorting.playfield.isSorted) {
                            passedTime = ((new Date()).getTime() - startTime)/1000
                            this.timer.value = ((Math.round(passedTime * 100) / 100).toFixed(3)).toString()
                        
                        } else {
                            clearInterval(this.timer.instance)
                            this.timer.instance = null
                        }
                        break;

                    case "pathfinding":

                        if (this.settings.algorithm.running) {
                            passedTime = ((new Date()).getTime() - startTime)/1000
                            this.timer.value = ((Math.round(passedTime * 100) / 100).toFixed(3)).toString()
                        
                        } else {
                            clearInterval(this.timer.instance)
                            this.timer.instance = null
                        }
                }
            }, 10)
        }
    }
}
</script>

<style scoped>

.iconAlgos {
    margin-left: 45px;
}

.iconSpeed {
    margin-left: 94px;
}

</style>

<template>
    <div style="position:absolute; left:21rem" :key="renderKey">
        <div ref="playfield" v-for="i in playfield.rowCount" :key="i">
            <div v-for="j in playfield.cellCount" :key="j" @mouseup="set($event)"
                :class="[           
                    'border-end',
                    'border-bottom',
                    { 'border-top': i === 1 },
                    { 'border-start': j === 1 },
                    'cell'
                ]"
                :id="[(i-1) * playfield.cellCount + j]"
                :style="{ 
                    position: 'fixed', 
                    left: `${21.5 + (j-1) * 2}rem`,
                    top: `${0.5 + (i-1) * 2}rem`,
                    minWidth: '2rem',
                    minHeight: '2rem',
                    }"
                >
                <component 
                :class="['draggable']"
                @mousedown="get($event)"
                v-if="(i-1) * playfield.cellCount + j === startCellId"
                :is="'fas'" 
                :icon="'arrow-down'"
                :style="{
                    minWidth: '1.95rem',
                    minHeight: '1.7rem',
                    position: 'relative',
                    top: '0.1rem'
                }"
                >
                </component>
                <component 
                :class="['draggable']"
                @mousedown="get($event)"
                v-if="(i-1) * playfield.cellCount + j === targetCellId"
                :is="'fas'" 
                :icon="'bullseye'"
                :style="{
                    minWidth: '1.95rem',
                    minHeight: '1.7rem',
                    position: 'relative',
                    top: '0.1rem'
                }"
                >
                </component>
            </div>
        </div>
    </div>
</template>

<script>
import { useWindowSize } from "vue-window-size"

export default {
    data() {
        var { width, height } = useWindowSize();
        return {
            window: {
                width: width,
                height: height
            },
            playfield: {
                rowCount: null,
                cellCount: null,
                running: false,
                timeout: null,
                pathFound: false,
                solvingSpeed: 0
            },
            renderKey: 0,
            startCellId: null,
            targetCellId: null,
            lastSelected: "ARROW"
        }
    },
    mounted() {
        this.calculatePlayfieldSize()
        window.addEventListener("resize", () => {

            clearTimeout(this.playfield.timeout)
            this.playfield.timeout = setTimeout(() => {
                this.calculatePlayfieldSize()
            }, 150)
        })
    },
    methods: {
        get: function(event) {

            var x = event.x; var y = event.y
            var elementsAtCursor = document.elementsFromPoint(x, y)
            
            for (var element of elementsAtCursor) {
                
                if (element.classList.contains("fa-arrow-down")) {
                    this.lastSelected = "ARROW"
                } 
                else if (element.classList.contains("fa-bullseye")) {
                    this.lastSelected = "BULLSEYE"
                }
            }
        },
        set: function(event) {

            var x = event.x; var y = event.y
            var elementsAtCursor = document.elementsFromPoint(x, y)
            var body = document.getElementsByTagName("body")[0]

            for (var element of elementsAtCursor) {
                
                if (element.classList.contains("cell")) {
                    var cell = element
                }
            }

            switch(this.lastSelected) {
                case "ARROW": {
                    this.startCellId = parseInt(cell.id)
                    body.style.cursor = "url(https://chuckie-droid.de/public/images/start.png), pointer"
                    break
                }

                case "BULLSEYE": {
                    this.targetCellId = parseInt(cell.id)
                    body.style.cursor = "url(https://chuckie-droid.de/public/images/goal.png), pointer"
                    break
                }
            }
        },
        calculatePlayfieldSize: function() {
            this.playfield.rowCount = Math.min(Math.floor(this.window.height / 16 / 2), 40)
            this.playfield.cellCount = Math.floor((this.window.width - 350) / 16 / 2)
            this.startCellId = (Math.ceil(this.playfield.rowCount / 2) - 1) * (this.playfield.cellCount) + Math.floor(this.playfield.cellCount / 4)
            this.targetCellId = (Math.ceil(this.playfield.rowCount / 2) - 1) * (this.playfield.cellCount) + Math.ceil((this.playfield.cellCount / 4) * 3) + 1
            this.renderKey += 1
        },
        sleep: function(seconds) {

            return new Promise((resolve, reject) => {
                var promise = setTimeout(() => {
                    resolve("Success")
                }, seconds * 1000)

                if (!promise) {
                    reject("Something weird happend.")
                }
            });
        },
        colorize: function(element, newColor) {

            // newColor parameter is not actually a color, but a bootstrap class
            // classname definitions: dark = grey; primary = blue; warning = yellow; danger = red; success = green
            var currentColor = element.classList[1].split("-")[3]
            element.classList.replace(`list-group-item-${currentColor}`, `list-group-item-${newColor}`)
        },
        startDijkstra: function() {



        },
        startAStar: function() {
        }
    }
}
</script>


<style scoped>

</style>

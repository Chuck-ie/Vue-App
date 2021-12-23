<template>
    <div style="position:absolute; left:21rem">
        <div ref="playfield" v-for="(rowItem, rowId) in playfield.rowCount" :key="rowId">
            <div v-for="(cellItem, cellId) in playfield.cellCount" :key="cellId" style="animation-name: fadeIn; animation-duration: 4s;"
                :class="[
                    'row',
                    rowId,
                    'border-end',
                    'border-bottom',
                    { 'border-top': rowId === 0 },
                    { 'border-start': cellId === 0 }
                ]"
                :id="[(rowId + 1) * cellId]"
                :style="{ 
                    position: 'fixed', 
                    left: `${22.4 + cellId * 2}rem`,
                    top: `${0.5 + rowId * 2}rem`,
                    minWidth: '2rem',
                    minHeight: '2rem',
                    }">
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
            targetCursor: "url(https://chuckie-droid.de/public/images/square-green.png), pointer",
        }
    },
    mounted() {
        this.setRowsAndCells()
        window.addEventListener("resize", () => {

            clearTimeout(this.playfield.timeout)
            this.playfield.timeout = setTimeout(() => {
                this.setRowsAndCells()
            }, 150)
        })
    },
    methods: {
        setRowsAndCells: function() {
            this.playfield.rowCount = [...Array(Math.min(Math.floor(this.window.height / 16 / 2), 40)).keys()]
            this.playfield.cellCount = [...Array(Math.floor((this.window.width - 350) / 16 / 2)).keys()]
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

        }
    }
}
</script>


<style scoped>

</style>

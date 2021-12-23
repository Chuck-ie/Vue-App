<template>
    <div style="position:absolute; left:21rem" :key="renderKey">
        <div ref="playfield" v-for="i in playfield.rowCount" :key="i">
            <div v-for="j in playfield.cellCount" :key="j"
                :class="[
                    'cell',
                    i-1,
                    'border-end',
                    'border-bottom',
                    { 'border-top': i === 1 },
                    { 'border-start': j === 1 }
                ]"
                :id="[(i) * (j-1)]"
                :style="{ 
                    position: 'fixed', 
                    left: `${21.5 + (j-1) * 2}rem`,
                    top: `${0.5 + (i-1) * 2}rem`,
                    minWidth: '2rem',
                    minHeight: '2rem',
                    }">
                    <fas v-if="i === Math.floor(playfield.rowCount / 2) && j === Math.floor(playfield.cellCount / 3)" icon="star" 
                        :style="{
                            marginLeft: '0.25rem',
                            marginTop: '0.3rem',
                            fontSize: '1.3rem'
                        }"/>
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
            targetCursor: "url(https://chuckie-droid.de/public/images/square-green.png), pointer",
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
        calculatePlayfieldSize: function() {
            this.playfield.rowCount = Math.min(Math.floor(this.window.height / 16 / 2), 40)
            this.playfield.cellCount = Math.floor((this.window.width - 350) / 16 / 2)
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

@keyframes fadeIn {
    from {
        min-width: 0rem;
        min-height: 0rem;
    };
    to {
        min-width: 2rem;
        min-height: 2rem;
    }
}

.cell {
    animation: fadeIn 1s;
}

</style>

<template>
    <div style="position:absolute; left:21rem">
        <div id="playfield">
            
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
                running: false,
                timeout: null,
                isSorted: false
            }
        }
    },
    mounted() {
        this.onResize()
        window.addEventListener("resize", () => {
            clearTimeout(this.playfield.timeout)
            this.onResize()
        })
    },
    methods: {
        onResize: function() {

            if (!this.playfield.running) {
                this.playfield.timeout = setTimeout(() => {
                    this.createPlayfield()
                }, 100)
            }
        },
        createPlayfield: function() {

            var arrayLength = Math.floor((this.window.width * 0.7) / 49)
            var arrayHeight = Math.floor(this.window.height * 0.6 / arrayLength)

            var playfield = document.getElementById("playfield")
            playfield.innerHTML = ""
            var allElements = []
            
            for (var i = 0; i < arrayLength; i++) {
                var newElement = document.createElement("DIV")
                newElement.id = `${i}`
                newElement.classList.add("list-group-item", "list-group-item-dark")
                newElement.style.position = "fixed"
                newElement.style.minWidth = `${1.8}rem`
                newElement.style.minHeight = `${arrayHeight * i + arrayHeight}px`
                allElements.push(newElement)
            }
            allElements.sort(() => Math.random() - 0.5)
            
            for (var j = 0; j < allElements.length; j++) {
                allElements[j].style.left = `${24 + j * 2.6}rem` 
                playfield.appendChild(allElements[j])
            }
        },
        sleep: async function(seconds) {

            return new Promise((resolve, reject) => {
                var promise = setTimeout(() => {
                    resolve("Success")
                }, seconds * 1000)

                if (!promise) {
                    reject("Something weird happend.")
                }
            });
        },
        colorize: async function(element, newColor) {

            // newColor parameter is not actually a color, but a bootstrap class
            // classname definitions: dark = grey; primary = blue; warning = yellow; danger = red; success = green
            var currentColor = element.classList[1].split("-")[3]
            element.classList.replace(`list-group-item-${currentColor}`, `list-group-item-${newColor}`)
        },
        selectionSort: async function(speed) {

            var solvingSpeed = 0.05 / parseFloat(speed)
            this.playfield.running = true

            var allElements = Array.from(document.getElementById("playfield").childNodes)
            
            for (var selectedElement of allElements) {
                
                var bestElement = selectedElement
                var slicedArray = allElements.slice(allElements.indexOf(selectedElement) + 1)
                this.colorize(selectedElement, "primary")

                for (var compareElement of slicedArray) {

                    await this.sleep(solvingSpeed)
                    this.colorize(compareElement, "warning")

                    await this.sleep(solvingSpeed)
                    if (parseInt(compareElement.id) < parseInt(bestElement.id)) {

                        if (bestElement !== selectedElement) {
                            this.colorize(compareElement, "success")
                            this.colorize(bestElement, "danger")
                        } else {
                            this.colorize(compareElement, "success")
                        }
                        bestElement = compareElement

                    } else {
                        this.colorize(compareElement, "danger")
                    }
                }
                await this.sleep(solvingSpeed)
                
                if (bestElement !== selectedElement) {
                    [selectedElement.id, bestElement.id] = [bestElement.id, selectedElement.id];
                    [selectedElement.style.minHeight, bestElement.style.minHeight] = [bestElement.style.minHeight, selectedElement.style.minHeight]
                    this.colorize(selectedElement, "success")
                    this.colorize(bestElement, "primary")

                } else {
                    this.colorize(selectedElement, "success")
                }
                
                await this.sleep(solvingSpeed)
                for (var element of slicedArray) {
                    this.colorize(element, "dark")
                }
            }

            return true
        },
        quickSort: async function() {

            console.log("CALLED QUICKSORT");

        }
    }
}


</script>

<style scoped>

h3 {
    text-align: center;
}

</style>

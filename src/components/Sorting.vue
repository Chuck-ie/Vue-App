<template>
    <div style="position:absolute; left:21rem">
        <div ref="playfield">
            
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
                isSorted: false,
                solvingSpeed: 0
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

            // Calculate the amount and hight of sorting elements, the formula works as the following:
            // this.window.width - 450 is the free space availabe (- lefthand menu); / 16 is to get the available rem (css property); / 2.6 because each element take 2.6 rem in width
            var arrayLength = Math.floor((this.window.width - 450) / 16 / 2.6)
            var arrayHeight = Math.floor((this.window.height - 450) / arrayLength)

            var playfield = this.$refs.playfield
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

            this.playfield.isSorted = false
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
        calculateDelay: function(x, y) {
            
            var averageDelay = 20/(x ** 2 + x)
            this.playfield.solvingSpeed = averageDelay / parseFloat(y)
            console.log(this.playfield.solvingSpeed)
        },
        colorize: function(element, newColor) {

            // newColor parameter is not actually a color, but a bootstrap class
            // classname definitions: dark = grey; primary = blue; warning = yellow; danger = red; success = green
            var currentColor = element.classList[1].split("-")[3]
            element.classList.replace(`list-group-item-${currentColor}`, `list-group-item-${newColor}`)
        },
        swapElements: function(element1, element2) {
            
            [element1.id, element2.id] = [element2.id, element1.id];
            [element1.style.minHeight, element2.style.minHeight] = [element2.style.minHeight, element1.style.minHeight]
        },
        startSelectionSort: async function(userMultiplier) {

            var allElements = Array.from(this.$refs.playfield.childNodes)
            this.calculateDelay(parseInt(allElements.length), userMultiplier)
            this.playfield.running = true
            
            for (var selectedElement of allElements) {
                
                var bestElement = selectedElement
                var slicedArray = allElements.slice(allElements.indexOf(selectedElement) + 1)
                this.colorize(selectedElement, "primary")

                for (var compareElement of slicedArray) {

                    await this.sleep(this.playfield.solvingSpeed)
                    this.colorize(compareElement, "warning")

                    await this.sleep(this.playfield.solvingSpeed)
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
                await this.sleep(this.playfield.solvingSpeed)
                
                if (bestElement !== selectedElement) {
                    this.swapElements(selectedElement, bestElement)
                    this.colorize(selectedElement, "success")
                    this.colorize(bestElement, "primary")

                } else {
                    this.colorize(selectedElement, "success")
                }
                
                await this.sleep(this.playfield.solvingSpeed)
                for (var element of slicedArray) {
                    this.colorize(element, "dark")
                }
            }

            if (document.body.contains(allElements[0])) {
                this.playfield.running = false
                this.playfield.isSorted = true
                return
            }
        },
        startQuickSort: async function(userMultiplier) {

            var allElements = Array.from(this.$refs.playfield.childNodes)
            this.playfield.running = true

            this.calculateDelay(parseInt(allElements.length), userMultiplier)
            await this.quickSort(allElements, 0, allElements.length-1)
            
            if (document.body.contains(allElements[0])) {
                this.playfield.running = false
                this.playfield.isSorted = true
                return
            }
        },
        quickSort: async function(array, low, high) {
            
            if (low < high) {

                var split = await this.quickSortParter(array, low, high)
                await this.quickSort(array, low, split - 1)
                await this.quickSort(array, split + 1, high)

            } else if (low === high) {
                this.colorize(array[low], "success")
                this.sleep(this.playfield.solvingSpeed)
            }
        },
        quickSortParter: async function(array, low, high) {

            let pivot = high
            let i = low
            let j = high-1

            this.colorize(array[pivot], "primary")
            this.colorize(array[i], "warning")
            this.colorize(array[j], "danger")
            await this.sleep(this.playfield.solvingSpeed)

            while (i < j) {

                while (i < high && parseInt(array[i].id) < parseInt(array[pivot].id)) {
                    i++
                    this.colorize(array[i - 1], "dark")
                    await this.sleep(this.playfield.solvingSpeed)
                    this.colorize(array[i], "warning")
                    await this.sleep(this.playfield.solvingSpeed)
                }

                while (j > low && parseInt(array[j].id) > parseInt(array[pivot].id)) {
                    j--
                    this.colorize(array[j + 1], "dark")
                    await this.sleep(this.playfield.solvingSpeed)
                    this.colorize(array[j], "danger")
                    await this.sleep(this.playfield.solvingSpeed)
                }

                if (i < j) {
                    this.swapElements(array[i], array[j])
                }
            }

            if (parseInt(array[i].id) > parseInt(array[pivot].id)) {
                this.swapElements(array[i], array[high])
            }

            this.colorize(array[i], "success")
            await this.sleep(this.playfield.solvingSpeed)

            var unsortedElements = array.filter(element => {
                return element.classList[1] !== "list-group-item-success"
            })

            for (var element of unsortedElements) {
                this.colorize(element, "dark")
            }

            return i
        }
    }
}


</script>

<style scoped>

</style>
